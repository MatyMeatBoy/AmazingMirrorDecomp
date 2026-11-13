"""Count main-source functions separately from European binary coverage."""
from collections import Counter
from html import escape
from pathlib import Path
import json
import re
import render
from metadata_build import function_kinds, validate_manifest
from report import summarize as source_report

SDK_SOURCES = {
    'src/agb_sram.c', 'src/m4a.c', 'src/multi_sio.c',
    'src/multi_boot.c', 'src/sio32_multi_load.c',
    'asm/libagbsyscall.s', 'asm/m4a_asm.s', 'asm/multi_sio_asm.s',
}
DOMAINS = {'game':'Juego y motor', 'sdk':'SDK / bibliotecas', 'startup':'Arranque', 'all':'Total'}
STATES = ('verified_c','c_pending_eu','drafts','pending_asm','original_asm')


def summarize(source, european, root):
    records=[]; lookup={}; raw_kinds={}
    for module in source['modules']:
        path=module['source']
        domain='sdk' if path in SDK_SOURCES else 'startup' if path=='asm/crt0.s' else 'game'
        for cell in module['cells']:
            if not cell['function']:continue
            state={'c':'c_pending_eu','asm':'pending_asm','original_asm':'original_asm'}[cell['kind']]
            if state=='pending_asm' and path.endswith('.c'):
                if path not in raw_kinds:
                    text=(Path(root)/path).read_text(errors='replace')
                    raw_kinds[path]=function_kinds(re.sub(r'\bNAKED\b','naked',text))
                if any(raw_kinds[path].get(n)=='c' for n in cell['aliases']):state='drafts'
            record={'source':path,'name':cell['name'],'aliases':cell['aliases'],
                    'domain':domain,'state':state,'existing_name':cell['named'],
                    'source_object_bytes':cell['size']}
            index=len(records);records.append(record)
            for alias in cell['aliases']:
                key=(path,alias)
                if key in lookup:raise ValueError('Duplicate function alias in source inventory')
                lookup[key]=index
    verified=set()
    if european['rom_match_verified']:
        for span in european['c_spans']:
            key=(span['source'],span['name'])
            if key not in lookup:raise ValueError('Verified EU function absent from source inventory')
            index=lookup[key];record=records[index]
            if record['state']!='c_pending_eu' or index in verified:
                raise ValueError('EU proof must identify one source C function once')
            verified.add(index);record['state']='verified_c'
            record['eu_start']=span.get('start');record['eu_bytes']=span['bytes']
    result={'available':True,'scope':'Main-source inventory; not the complete European ROM function total.',
            'excluded':['Compiler archives (libc/libgcc)','Auxiliary multiboot programs'],
            'draft_scope':'Readable alternate C definitions; compilation and matching are separate checks.',
            'naming_scope':'Existing descriptive identifiers; semantic correctness not independently audited.',
            'sdk_sources':sorted(SDK_SOURCES),'functions':records}
    return recount(result)


def recount(result):
    records=result['functions']
    for domain in DOMAINS:
        subset=[r for r in records if domain=='all' or r['domain']==domain]
        counts=Counter(r['state'] for r in subset)
        row={state:counts[state] for state in STATES}
        row.update(total=len(subset),existing_names=sum(r['existing_name'] for r in subset))
        row['unnamed']=row['total']-row['existing_names']
        assert row['total']==sum(row[s] for s in STATES)
        result[domain]=row
    assert result['all']['total']==sum(result[d]['total'] for d in ('game','sdk','startup'))
    return result


def load(root,european):
    try:
        manifest=json.loads((Path(root)/'build/metadata/manifest.json').read_text())
        validate_manifest(manifest,root)
    except (OSError,ValueError,KeyError) as exc:
        return {'available':False,'issue':'Current compiled source inventory unavailable: '+str(exc)}
    primary=dict(european,c_spans=[s for s in european['c_spans'] if not s.get('library_member')])
    result=summarize(source_report(manifest),primary,root)
    from draft_inventory import compile_source, recover
    import subprocess
    proofs={};issues=[]
    for record in result['functions']:
        if record['state']!='drafts':continue
        source=record['source']
        if source not in proofs:
            try:proofs[source]=compile_source(root,source,True)
            except (OSError,ValueError,subprocess.SubprocessError) as exc:
                proofs[source]={'c_functions':[]};issues.append(source+': '+str(exc))
        if not any(n in proofs[source]['c_functions'] for n in record['aliases']):record['state']='pending_asm'
        else:record['draft_compilation']=proofs[source]
    recovered,recovery_issues=recover(root);issues+=recovery_issues
    for draft in recovered:
        matches=[r for r in result['functions'] if r['source']==draft['owner'] and draft['symbol'] in r['aliases']]
        if len(matches)==1 and matches[0]['state']=='pending_asm':
            matches[0].update(state='drafts',draft_source=draft['source'],draft_evidence=draft['evidence'],draft_compilation=draft['compilation'])
    result['draft_issues']=issues
    from extra_inventory import load as extra_inventory,apply_european
    result['additional_inventory']=apply_european(extra_inventory(root),european)
    recount(result)
    extra=result['additional_inventory']
    result['known_source_function_instances']=result['all']['total']+(extra['totals']['functions'] if extra.get('available') else 0)
    return result


def markdown(inventory):
    if not inventory.get('available'):return 'Inventario de funciones no disponible; regenerar los objetos de metadatos.\n'
    lines=['## Funciones por categoría','',
           '| Categoría | Total | C EU verificado | C pendiente EU | Borrador C | ASM pendiente | ASM conservado |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for domain,label in DOMAINS.items():
        row=inventory[domain]
        lines.append('| '+label+' | '+' | '.join(f'{row[k]:,}' for k in ('total',*STATES))+' |')
    lines += ['','| Nombrado | Total | Nombre existente | Sin nombre descriptivo |','|---|---:|---:|---:|']
    for domain,label in DOMAINS.items():
        row=inventory[domain]
        lines.append('| '+label+' | '+' | '.join(f'{row[k]:,}' for k in ('total','existing_names','unnamed'))+' |')
    lines += ['','Inventario de fuentes principales: excluye archivos de biblioteca del compilador (libc/libgcc) y programas multiboot auxiliares. No es el total definitivo de funciones de la ROM europea.',
              'Borrador C significa definición alternativa legible; no recibe crédito C verificado. Los nombres existentes no equivalen a nombres auditados.',
              'SDK agrupa SRAM, m4a, MultiSio, MultiBoot, Sio32MultiLoad y wrappers BIOS. Los adaptadores específicos del juego permanecen en juego/motor. Arranque contiene crt0.',
              'Inventario completo: [functions.json](functions.json).','']
    extra=inventory.get('additional_inventory',{})
    if extra.get('available'):
        lines += ['## Bibliotecas del compilador y auxiliares','',
                  f"**Total contabilizado: {inventory['known_source_function_instances']:,} funciones**, incluidas las copias de biblioteca de cada programa. No es un total europeo verificado.",'',
                  '| Programa | Funciones | C disponible | C EU verificado | ASM |','|---|---:|---:|---:|---:|']
        for row in extra['groups']:
            lines.append(f"| {row['program']} | {row['functions']:,} | {row['c_available']:,} | {row.get('verified_c',0):,} | {row['assembly']:,} |")
        lines += ['','Solo las instancias del programa principal con prueba regional reciben crédito C EU; las copias auxiliares no heredan esa prueba. Los aliases comparten una función. La entrada manual __start del cargador se cuenta una vez; no se cuentan etiquetas internas.','']
        names=inventory['all']['existing_names']+extra['totals']['existing_names']
        lines += [f"Nombre existente en todo el inventario: **{names:,}**; sin nombre descriptivo: **{inventory['known_source_function_instances']-names:,}**. Las propuestas externas sin revisar no se cuentan como nombres confirmados.",'']
    return '\n'.join(lines)


def svg(inventory):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="670" viewBox="0 0 1000 670" role="img" aria-labelledby="title" font-family="Segoe UI,Helvetica,Arial,sans-serif"><title id="title">Funciones: juego, SDK y arranque</title><rect width="1000" height="670" fill="{render.BG}"/><g fill="{render.FG}">']
    def text(x,y,value,size=13):parts.append(f'<text x="{x}" y="{y}" font-size="{size}">{escape(str(value))}</text>')
    text(16,30,'AmazingMirrorDecomp | Funciones por categoría',20)
    if not inventory.get('available'):
        text(16,70,'Inventario no disponible: regenerar metadatos.')
        return '\n'.join(parts+['</g></svg>'])
    total=inventory['all']
    text(16,60,f"TOTAL CONTABILIZADO: {inventory.get('known_source_function_instances',total['total']):,} funciones",23)
    text(16,85,f"Programa principal: {total['total']:,}. El total definitivo de toda la ROM europea sigue sin medir.")
    xs=[16,230,325,465,595,720,850]
    for x,label in zip(xs,['Categoría','Total','C EU verificado','C pendiente EU','Borrador C','ASM pendiente','ASM conservado']):text(x,121,label,12)
    for i,(domain,label) in enumerate(DOMAINS.items()):
        row=inventory[domain];y=151+31*i
        for x,value in zip(xs,[label,*[f'{row[k]:,}' for k in ('total',*STATES)]]):text(x,y,value,14)
    text(16,285,'Nombres existentes / sin nombre descriptivo',16)
    for i,domain in enumerate(('game','sdk','startup','all')):
        row=inventory[domain]
        text(16+(i%2)*490,313+(i//2)*27,f"{DOMAINS[domain]}: {row['existing_names']:,} / {row['unnamed']:,}")
    extra=inventory.get('additional_inventory',{})
    text(16,375,'Bibliotecas del compilador y programas auxiliares (contados aparte del principal)',16)
    if extra.get('available'):
        for x,label in zip([16,590,690,790,900],['Programa','Funciones','C disponible','C EU verificado','ASM']):text(x,405,label,12)
        for i,row in enumerate(extra['groups']):
            for x,value in zip([16,590,690,790,900],[row['program'],row['functions'],row['c_available'],row.get('verified_c',0),row['assembly']]):text(x,432+26*i,f'{value:,}' if isinstance(value,int) else value,12)
        names=total['existing_names']+extra['totals']['existing_names']
        text(16,590,f"Todos los programas: {names:,} nombres existentes / {inventory['known_source_function_instances']-names:,} sin nombre descriptivo.",13)
    else:text(16,410,'Inventario adicional no disponible; total mostrado parcial.',12)
    text(16,610,'Las copias de biblioteca en distintos programas se cuentan por separado. Aliases no se duplican.',12)
    text(16,633,'C disponible / borradores sin crédito EU. Nombres existentes pendientes de auditoría semántica.',12)
    text(16,655,'Fuentes sin inventariar o funciones regionales aún no delimitadas no reciben un total inventado.',12)
    return '\n'.join(parts+['</g></svg>'])


def treemap(inventory):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="680" viewBox="0 0 1000 680" role="img" aria-labelledby="title" font-family="Segoe UI,Helvetica,Arial,sans-serif"><title id="title">Inventario de funciones y borradores</title><rect width="1000" height="680" fill="{render.BG}"/><g fill="{render.FG}">']
    lines=['AmazingMirrorDecomp | Inventario de funciones',
           'Área = bytes del objeto fuente; no representa posiciones ni huecos regionales europeos.',
           'Verde: C verificado EU | Amarillo: C disponible pendiente EU / borrador | Gris: ASM']
    for i,line in enumerate(lines):parts.append(f'<text x="14" y="{28+22*i}" font-size="{17 if i==0 else 12}">{escape(line)}</text>')
    if inventory.get('available'):
        colors={'verified_c':render.GREEN,'c_pending_eu':'#e4bd4c','drafts':'#e4bd4c','pending_asm':render.GREY,'original_asm':render.GREY}
        items=[(r['source_object_bytes'],r) for r in inventory['functions']]
        for record,x,y,w,h in render.squarify(items,8,87,984,506):
            tip=f"{DOMAINS[record['domain']]} :: {record['source']} :: {record['name']} | {record['state']} | {record['source_object_bytes']} source-object bytes"
            parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(0,w-.5):.2f}" height="{max(0,h-.5):.2f}" fill="{colors[record["state"]]}"><title>{escape(tip)}</title></rect>')
    parts += ['<text x="14" y="623" font-size="12">Amarillo no suma al porcentaje C verificado. Nombres existentes no equivalen a nombres auditados.</text>',
              '<text x="14" y="648" font-size="12">Inventario principal: bibliotecas del compilador y programas auxiliares se contabilizan aparte.</text>']
    return '\n'.join(parts+['</g></svg>'])
