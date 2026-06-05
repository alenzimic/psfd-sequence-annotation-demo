#!/usr/bin/env python3
"""Build a small browser-side PSFD protein sequence index.

This experimental repository is static-only, so the sequence search must run in
the browser. The index links UniProt FASTA records back to PSFD gene/protein
entities already present in data/global_path_index.json.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GLOBAL_INDEX = ROOT / "data" / "global_path_index.json"
OUT = ROOT / "data" / "sequence_index.json"


def fetch_fasta(accession: str) -> tuple[str, str]:
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
    request = urllib.request.Request(url, headers={"User-Agent": "psfd-sequence-annotation-demo/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "", ""
        raise
    header = ""
    sequence_parts: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            header = line[1:]
        else:
            sequence_parts.append(line)
    return header, "".join(sequence_parts)


def accession_rows(global_index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_accession: dict[str, dict[str, Any]] = {}
    for entity in global_index.get("entities", []):
        profile = entity.get("gene_protein_normalization") or {}
        for fasta in profile.get("fasta_accessions", []):
            accession = str(fasta.get("accession") or "").strip()
            if not accession:
                continue
            row = by_accession.setdefault(
                accession,
                {
                    "accession": accession,
                    "entities": [],
                    "source": "UniProt",
                },
            )
            row["entities"].append(
                {
                    "id": entity.get("id", ""),
                    "label": entity.get("label", ""),
                    "type": entity.get("type", ""),
                    "pmcid": entity.get("pmcid", ""),
                    "ontology_id": entity.get("ontology_id", ""),
                    "ontology_ids": entity.get("ontology_ids", []),
                    "selected_label": entity.get("selected_label", ""),
                    "paper_title": entity.get("paper_title", ""),
                    "accession_kind": fasta.get("kind", ""),
                    "entry": fasta.get("entry", ""),
                    "protein_name": fasta.get("protein_name", ""),
                    "organism": fasta.get("organism", ""),
                }
            )
    return by_accession


def main() -> None:
    global_index = json.loads(GLOBAL_INDEX.read_text(encoding="utf-8"))
    rows = accession_rows(global_index)
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for index, accession in enumerate(sorted(rows), start=1):
        try:
            header, sequence = fetch_fasta(accession)
        except Exception:
            failures.append(accession)
            continue
        if not sequence:
            failures.append(accession)
            continue
        records.append(
            {
                **rows[accession],
                "header": header,
                "sequence": sequence,
                "length": len(sequence),
            }
        )
        if index % 10 == 0:
            time.sleep(0.2)

    payload = {
        "source": "UniProt FASTA records linked from PSFD gene/protein normalization.",
        "record_count": len(records),
        "failed_accessions": failures,
        "records": records,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(records)} sequence records to {OUT}")
    if failures:
        print(f"Missing {len(failures)} accessions: {', '.join(failures[:20])}")


if __name__ == "__main__":
    main()
