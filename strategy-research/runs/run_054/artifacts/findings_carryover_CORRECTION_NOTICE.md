# CORRECTION NOTICE — findings_carryover.yaml, 2026-07-10

This carryover file was generated under `run_054`'s **original kill verdict**
(`median_sharpe -1.78 (BTCUSDT) / -1.54 (ETHUSDT)`, a LIFO-fragment-basis bug),
which was overturned by the metric-basis correction — see
`strategy-research/incident_20260710/INCIDENT.md`. Corrected bar-level medians:
**+0.5791 (BTCUSDT) / +0.0318 (ETHUSDT)**; corrected verdict: **refine**.

The following fields in `findings_carryover.yaml` are superseded and must not
be treated as current:
- `what_failed` (all three entries, including the -1.78/-1.54 kill threshold
  and the misapplied IC upper-bound criterion)
- `next_altitude: "pivot"`
- `regime_gate_rationale` (proposes gating on the unvalidated 1h
  `regime_detector_report.yaml` detector — a different, non-conforming
  mechanism from the operator's ER-gate brief)

**Do not consume this file for any future run.**

The original `findings_carryover.yaml` is preserved unedited alongside this
notice, as historical record.
