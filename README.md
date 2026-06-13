# PSFD Sequence Annotation Demo

Experimental static GitHub Pages demo for PSFD annotation.

This repository is intentionally independent from `alenzimic.github.io` so the
stable PSFD webpage can remain available while sequence/compound relationship
features are tested here.

## Features

- Existing PSFD annotation and evidence browser copied from the stable demo.
- Browser-side approximate protein FASTA similarity search against PSFD-linked
  UniProt sequences. The static sequence index is built from normalized
  gene/protein ontology IDs/accessions in PSFD.
- FASTA demo buttons include an exact PSFD sequence match and a non-identical
  HSP70-like query derived from a PSFD-linked sequence to demonstrate homolog
  matching behavior for novel sequences.
- Compound-name relationship extraction from the PSFD relation graph. Only
  triples where the submitted compound is entity 1 or entity 2 are exported.
- Attribute filters for genes, metabolites, pathways, tissues, species, traits,
  molecular traits, and experimental conditions.
- Tab-delimited relationship export with these columns:
  `compound_or_gene_name`, `relation`, `context`,
  `event_taxon_tissue_context`, `entity_linked_taxon_tissue_context`,
  `overlap_taxon_tissue_context`, `attribute_type`,
  `ontology_normalized_relation`.

## Scientific Note

The FASTA search is a browser-side k-mer similarity search, not BLAST or MMseqs.
It is useful for fast demo annotation of close sequence matches. Final sequence
validation should use BLAST, DIAMOND, or MMseqs against the full sequence
database.

PSFD inter-event links are displayed in evidence tiers. **Supported** links are
strict evidence-supported relations. **Hypothesis** links are plausible
evidence-linked relations retained for recall-preserving discovery; they are not
error rows or failed manual review. Rejected dependency candidates are hidden by
default and are mainly useful for audits or model-training negatives.

## Updating Data

The static data files are committed in `data/`, so the demo works immediately
after cloning. To refresh them, point the builder at a local checkout of the
main PSFD pipeline that contains `output/` and `data/`.

```bash
git clone https://github.com/alenzimic/psfd-sequence-annotation-demo.git
cd psfd-sequence-annotation-demo

# Option 1: configure once for the shell.
export PSFD_SOURCE_ROOT=/path/to/1_PSFD
python scripts/build_demo_data.py

# Option 2: pass the source root per run.
python scripts/build_demo_data.py --source-root /path/to/1_PSFD

python scripts/build_sequence_index.py
```

If this repository is cloned next to the PSFD pipeline checkout, the builder
also auto-detects a sibling `../1_PSFD` directory.

`build_demo_data.py` rewrites `data/manifest.json`, `data/global_path_index.json`,
and `data/papers/*.json`. `build_sequence_index.py` rebuilds the browser-side
UniProt FASTA index from the refreshed `data/global_path_index.json`.

After rebuilding, validate and publish with:

```bash
node --check assets/app.js
python -m py_compile scripts/build_demo_data.py scripts/build_sequence_index.py
python - <<'PY'
import json
from pathlib import Path
for path in Path("data").glob("**/*.json"):
    json.loads(path.read_text(encoding="utf-8"))
print("JSON bundle is valid")
PY
git status --short
```
