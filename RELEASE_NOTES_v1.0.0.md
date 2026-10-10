# SGIT–TRC v1.0.0 — initial citable software release

## Scope
Manuscript-independent research software accompanying work on Spatiotemporal Geometry Integration Theory and Temporal Relational Closure.

Included:
- Reference Python implementation for oriented EEG relations, Hodge operators and projections, third-order cross-moments, tensor symmetry energies, and pair-preserving null analyses.
- Frozen configuration and protocol records.
- Selected historical JSON results and verification utilities.
- Unit tests and provenance documentation.

## Verification status
The mathematical unit-test suite has passed in the development environment (5 tests). This is **not** independent reproduction of all reported EEG contrasts or p-values. No raw third-party EEG datasets are distributed here. Users must consult the provenance and data availability documents.

## Citation
After publishing a GitHub Release tagged `v1.0.0`, cite that exact tag and commit. An archival DOI must be obtained from Zenodo separately; do not cite an unassigned DOI.

## Release procedure
1. Review current source and historical result files for public redistribution and sensitive data.
2. Open https://github.com/miroslavsvitek/SGIT-Theory-TRC/releases/new .
3. Choose **Create new tag** `v1.0.0` from branch `main`, set title `SGIT–TRC v1.0.0`, and paste this release note.
4. Publish the release.
5. In Zenodo, authorize GitHub and enable archiving for `miroslavsvitek/SGIT-Theory-TRC`. Verify that the new release is archived; if Zenodo was connected only after publication, follow Zenodo's instructions to archive the existing release or publish a subsequent release.
6. Record the DOI actually issued by Zenodo in the manuscript's Data and Code Availability section.
