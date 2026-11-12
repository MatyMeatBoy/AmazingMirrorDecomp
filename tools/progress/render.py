"""SVG layout adapted from MatyMeatBoy/SS2Decomp and SS1Decomp.
Original renderer: emmkay440 and contributors. SS2 revision
698bbe6af4968fa6b9eefb01bcf0ae16639da681, tools/scripts/progress.py.
AmazingMirrorDecomp adaptation: MatyMeatBoy.
"""
from html import escape
BG='#0d1117'
FG='#e6edf3'
GREEN='#238636'
MINT='#39c5aa'
GREY='#484f58'


def treemap(report, names=False):
    title = 'AmazingMirrorDecomp | '+('existing function names' if names else 'compiled C source inventory')
    summary = report['totals']
    detail = f"{summary['named_functions']}/{summary['functions']} existing names" if names else f"{summary['c_percent']:.3f}% C in measured text"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="680" viewBox="0 0 1000 680" role="img" aria-labelledby="title desc" font-family="Segoe UI,Helvetica,Arial,sans-serif">',
             f'<title id="title">{escape(title)}</title>',
             '<desc id="desc">Byte-weighted unlinked main-object text. Original assembly and unattributed text are separate. No ROM match established.</desc>',
             f'<rect width="1000" height="680" fill="{BG}"/>',
             f'<text x="14" y="26" fill="{FG}" font-size="18">{escape(title)}</text>',
             f'<text x="14" y="49" fill="{FG}" font-size="13">{detail} | ROM match: not verified</text>',
             f'<text x="14" y="69" fill="{FG}" font-size="11">Scope: unlinked main .text objects; archives, multiboot, non-text and cartridge header excluded.</text>']
    for module, x, y, w, h in squarify([(m['bytes'],m) for m in report['modules']], 8, 84, 984, 514):
        parts.append(f'<g><title>{escape(module["source"])}: {module["bytes"]:,} measured bytes</title>')
        for cell, cx, cy, cw, ch in squarify([(c['size'],c) for c in module['cells']],x+1,y+1,max(0,w-2),max(0,h-2)):
            kind = cell['kind']
            color = (GREEN if cell['named'] and cell['function'] else GREY) if names else {'c':GREEN,'original_asm':MINT}.get(kind,GREY)
            tip = f"{module['source']} :: {cell['name']} | {cell['size']} bytes | {kind} | object offset 0x{cell['offset']:X}"
            parts.append(f'<rect x="{cx:.2f}" y="{cy:.2f}" width="{max(0,cw-.5):.2f}" height="{max(0,ch-.5):.2f}" fill="{color}"><title>{escape(tip)}</title></rect>')
            if cw>100 and ch>23:
                label = cell['name'][:max(4,int((cw-8)/5.6))]
                parts.append(f'<text x="{cx+4:.2f}" y="{cy+14:.2f}" fill="{FG}" font-size="10" pointer-events="none">{escape(label)}</text>')
        parts.append('</g>')
    legend = [(GREEN,'Existing name'),(GREY,'Unknown / unmeasured')] if names else [(GREEN,'Compiled C'),(MINT,'Original assembly'),(GREY,'Pending ASM / unattributed')]
    x=14
    for color,label in legend:
        parts.extend([f'<rect x="{x}" y="620" width="12" height="12" fill="{color}"/>',f'<text x="{x+18}" y="631" fill="{FG}" font-size="12">{label}</text>'])
        x += len(label)*7+48
    parts.append(f'<text x="14" y="658" fill="{FG}" font-size="11">Area includes attributed pools/alignment. This is not a whole-game matching percentage. Data recovery not measured.</text></svg>')
    return '\n'.join(parts)


def data_svg():
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="130" role="img" aria-label="Data recovery not measured"><rect width="1000" height="130" fill="{BG}"/><text x="16" y="32" fill="{FG}" font-family="sans-serif" font-size="18">AmazingMirrorDecomp | data recovery: not measured</text><text x="16" y="66" fill="{FG}" font-family="sans-serif" font-size="13">Source assets and raw ranges require a separate format and boundary audit.</text><text x="16" y="96" fill="{FG}" font-family="sans-serif" font-size="13">No automatic credit for preserved bytes, INCBIN counts or native ports.</text></svg>'
def squarify(items, x, y, w, h):
    """items: list of (weight, obj). Returns list of (obj, x, y, w, h)."""
    items = [(v, o) for v, o in items if v > 0]
    items.sort(key=lambda t: -t[0])
    total = sum(v for v, _ in items)
    if total <= 0 or w <= 0 or h <= 0:
        return []
    scale = w * h / total
    rects = []
    rest = [(v * scale, o) for v, o in items]

    def worst(row, side):
        s = sum(r for r, _ in row)
        if s == 0:
            return float("inf")
        mx = max(r for r, _ in row)
        mn = min(r for r, _ in row)
        return max(side * side * mx / (s * s), (s * s) / (side * side * mn))

    while rest:
        side = min(w, h)
        row = [rest[0]]
        i = 1
        while i < len(rest) and worst(row + [rest[i]], side) <= worst(row, side):
            row.append(rest[i])
            i += 1
        rest = rest[i:]
        s = sum(r for r, _ in row)
        if w >= h:
            cw = s / h
            cy = y
            for r, o in row:
                ch = r / cw
                rects.append((o, x, cy, cw, ch))
                cy += ch
            x += cw
            w -= cw
        else:
            rh = s / w
            cx = x
            for r, o in row:
                cwid = r / rh
                rects.append((o, cx, y, cwid, rh))
                cx += cwid
            y += rh
            h -= rh
    return rects


def badge_svg(label, value, color):
    def tw(s):
        return int(len(s) * 6.6 + 12)
    lw, vw = tw(label), tw(value)
    w = lw + vw
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="20" role="img" aria-label="%s: %s">'
            '<linearGradient id="s" x2="0" y2="100%%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
            '<stop offset="1" stop-opacity=".1"/></linearGradient>'
            '<clipPath id="r"><rect width="%d" height="20" rx="3" fill="#fff"/></clipPath>'
            '<g clip-path="url(#r)"><rect width="%d" height="20" fill="#555"/>'
            '<rect x="%d" width="%d" height="20" fill="%s"/><rect width="%d" height="20" fill="url(#s)"/></g>'
            '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" '
            'font-size="11"><text x="%.1f" y="15" fill="#010101" fill-opacity=".3">%s</text>'
            '<text x="%.1f" y="14">%s</text><text x="%.1f" y="15" fill="#010101" fill-opacity=".3">%s</text>'
            '<text x="%.1f" y="14">%s</text></g></svg>') % (
        w, escape(label), escape(value), w, lw, lw, vw, color, w,
        lw / 2, escape(label), lw / 2, escape(label), lw + vw / 2, escape(value), lw + vw / 2, escape(value))


