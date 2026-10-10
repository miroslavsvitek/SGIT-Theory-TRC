# SGIT–TRC: reusable computational research repository

**Spatiotemporal Geometry Integration Theory (SGIT), Temporal Relational Closure (TRC).**

This repository is intentionally **manuscript-version independent**. It contains no article PDF or TeX source. Scientific papers can cite a specific tagged release and commit hash while the methods and audit resources continue to evolve under version control.

## Scope and scientific status

- Reference Python functions for local oriented EEG relations, graph/Hodge operations, third-order moments, symmetry decomposition and pair-preserving nulls.
- Frozen parameter/configuration objects and documented links to the exact original visual-analysis repository.
- Selected historical original result JSONs and protocol locks; these are labelled as archived analyses, not a replacement for raw third-party EEG data.
- Unit tests check mathematics, **not** all published participant-level p-values. Do not interpret a PASS as full reproduction.

## Quick start (Python 3.11+)

```bash
python -m pip install -e '.[test]'
python -m pytest -q tests
python scripts/sync_frozen_visual.py --help
```

Do not overwrite the original datasets or historical archives. Consult `docs/REPRODUCIBILITY.md` and `docs/DATA_AND_CODE_AVAILABILITY.md` for provenance and limitations.

## Foundation and frozen provenance

Original canonical visual analysis: https://github.com/miroslavsvitek/SGIT-Hodge-Curl-Conscious-Visual-Detection

Reference tree: `f0ffc52cf0003bdba2e90ca53712375beda6709d`.

The repository release tag and DOI must be assigned when the GitHub/Zenodo release is actually published; none is invented here.

## Relationship to manuscripts

This is an independently maintained software and evidence companion. **No manuscript files are included**. When a paper is submitted, cite the release tag or commit actually used in its analyses.
