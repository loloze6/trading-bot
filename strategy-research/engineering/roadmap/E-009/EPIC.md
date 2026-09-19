# E-009 — Pipeline harmonization

**Moved to Linear.** This epic's status, findings, and decisions now live there:
https://linear.app/culito/project/e-009-pipeline-harmonization-stage-configsskill-map-sample-split-70b5b6fe6df3

This file is kept only as a pointer so existing cross-links (`../E-009/EPIC.md`) keep resolving — it is not updated any more.

---

## Closed 2026-09-09

- **S1 (skill_map merge):** done — commit `4250d833` on branch `fix/e009-s1-skill-map-merge`.
- **S2 (`sample_split` override/narrowing merge onto `baseline_v1.json`):** retracted 2026-09-09. `sample_split` as a term matches nothing real anywhere in the codebase — zero hits outside unrelated `venv/`-bundled sklearn test files. The real, more substantial mechanism the story was gesturing at — `strategy-research/protocols/*.json` walk-forward specs resolved by `_resolve_protocol_path()`, and the documented-but-unwired `validation_protocol.yaml` `sample_split_design` field (declared in docs, produced by nothing, read by nothing) — is now tracked separately as **E-049 · Protocol construction — sample_split_design & variant audit**.
- Epic closed in Linear with nothing legitimately left open under this epic's own name.
