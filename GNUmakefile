# Europe is the primary profile. Keep the original USA Makefile intact.
REGION ?= eu
ifneq ($(REGION),eu)
ifneq ($(REGION),us)
$(error Unsupported REGION '$(REGION)'; use eu or us)
endif
endif

ifeq ($(REGION),us)
include Makefile
else ifneq ($(filter graphics/% sound/%,$(MAKECMDGOALS)),)
# Metadata generation uses the original editable-asset conversion rules.
include Makefile
else
.DEFAULT_GOAL := all
PYTHON ?= python3
JOBS ?= 4
EU_ROM ?= baserom_eu.gba
.PHONY: all rom compare compare-eu progress metadata record-eu progress-map test-progress compare-us progress-us

all rom compare progress: compare-eu

metadata:
	$(PYTHON) tools/progress/metadata_build.py --jobs $(JOBS)
	$(PYTHON) tools/progress/library_metadata.py

compare-eu: metadata
	$(PYTHON) tools/progress/eu_build.py --rom "$(EU_ROM)"
	$(PYTHON) tools/progress/eu_report.py --receipt build/eu/receipt.json

record-eu: compare-eu
	$(PYTHON) tools/progress/eu_report.py --receipt build/eu/receipt.json --record config/regions/eu_verified.json

progress-map:
	$(PYTHON) tools/progress/update_progress.py

test-progress:
	$(PYTHON) -m unittest discover -s tests -v

compare-us:
	$(MAKE) REGION=us compare

progress-us:
	$(MAKE) REGION=us compare
	perl calcrom.pl katam.map
endif
