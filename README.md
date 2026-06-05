# PSFD Sequence Annotation Demo

Experimental static GitHub Pages demo for PSFD annotation.

This repository is intentionally independent from `alenzimic.github.io` so the
stable PSFD webpage can remain available while sequence/compound relationship
features are tested here.

## Features

- Existing PSFD annotation and evidence browser copied from the stable demo.
- Browser-side approximate protein FASTA similarity search against PSFD-linked
  UniProt sequences.
- Compound-name relationship extraction from the PSFD relation graph.
- Attribute filters for genes, metabolites, pathways, tissues, species, traits,
  molecular traits, and experimental conditions.
- Tab-delimited relationship export with these columns:
  `compound_or_gene_name`, `relation`, `context`, `attribute_type`,
  `ontology_normalized_relation`.

## Scientific Note

The FASTA search is a browser-side k-mer similarity search, not BLAST or MMseqs.
It is useful for fast demo annotation of close sequence matches. Final sequence
validation should use BLAST, DIAMOND, or MMseqs against the full sequence
database.

## Updating Data

The static data files are in `data/`. To rebuild the sequence index after
refreshing `data/global_path_index.json`, run:

```bash
python scripts/build_sequence_index.py
```
