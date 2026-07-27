# CORRECTION NOTICE — research_brief.yaml, 2026-07-16

`research_brief.yaml` (the machine-materialized artifact `_materialize_run`
wrote for run_058 from `briefs/H-041-C-v2.md`) gained a `constraints` field
it did not carry at materialization time:

```yaml
constraints:
- One variant only — fully pre-registered closure run; expand exactly the registered
  mechanism; no additional variants.
```

**Why:** the operator's own H-041-C-v2 registration ratification
(2026-07-15) omitted an explicit variant-count constraint. This was
identified as an omission at the operator's ratification, not an error
introduced by materialization or by any pipeline stage — the run_058
resume ruling of 2026-07-16 adds it retroactively, both to the source
brief (`briefs/H-041-C-v2.md`, commit `996f432`) and to this
already-materialized copy, so the constraint is present before
`innovation_expansion` is re-attempted.

**No other field in this file was touched.** The original,
pre-correction `research_brief.yaml` is not separately preserved as a
distinct artifact — this file was edited in place, per the operator's own
explicit authorization for this exact edit (this is a hand-edit of a
normally machine-authored artifact, done under direct operator
instruction, not agent-initiated).
