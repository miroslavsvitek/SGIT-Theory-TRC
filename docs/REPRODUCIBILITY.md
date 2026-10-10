# Reproducibility scope — SGIT the accompanying SGIT manuscript

**Included:** full manuscript in PDF and LaTeX; reference mathematical code; versioned constants from manuscript; executable internal consistency tests; author-supplied historical JSON evidence and frozen protocol records for selected controls; file checksums.

**Source of the frozen sensor geometry and original visual pipeline:** https://github.com/miroslavsvitek/SGIT-Hodge-Curl-Conscious-Visual-Detection (tree commit `f0ffc52cf0003bdba2e90ca53712375beda6709d`). Its `supplementary/S1`–`S7` objects provide the coordinates, edges, triangles, and frozen eigenbases. Its `frozen_analysis/discovery` and `frozen_analysis/replication` directories contain the original visual scripts and configurations. These are linked rather than silently replaced or regenerated.

**Not verified here:** raw-to-result EEG reproduction across every cohort in the the accompanying SGIT manuscript article, the independent derivation and training provenance of uS3, or new calculation of all paper p-values. These need the original EEG records and exact dataset-specific pipelines. Frozen result JSON is a record of reported outputs, not independent replication.

**Clinical/interpretive scope:** pair-preserving TRC examines an explicitly defined third-moment statistic; it does not prove universal causal irreducibility. No-report SWS primary p≈0.0107 is positive, while its content-specific control p≈0.073 is inconclusive. Historical negative/unevaluable controls are retained and labeled accordingly.

The companion package is publishable as a transparent versioned software-plus-manuscript artifact without implying that it contains licensed/raw participant EEG or a full re-execution of all published claims. Do not claim otherwise in the Data and Code Availability statement.
