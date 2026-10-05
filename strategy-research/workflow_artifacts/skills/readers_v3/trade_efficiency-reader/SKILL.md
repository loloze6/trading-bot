---
name: trade_efficiency-reader
description: E-068 slice 5 reader v3 (trade_efficiency). Reads artifacts/reports/trade_efficiency.yaml, explains the measured result and proposes side findings (claim blocks) and at most one patch, as one v3 reading. Never judges the claim.
---

# Trade Efficiency Reader (v3)

Follow READING_CONTRACT.md (your first input) for the exact output shape and rules. Write
`rubric_version: trade_efficiency-reading-v1` and `reading_id: trade_efficiency-<run_id>`.

## Your focus

Your report, `artifacts/reports/trade_efficiency.yaml`, measures execution quality: entry and
exit efficiency, holding time, boundary re-crossing, signal flips and the fee-reduction
metrics, per window and per variant. Every graded variant has its own `variants.<vid>.slices`;
a pattern on `base` that does not hold on the other variants is coin- or design-specific, so
say which variants show it.

- Explain how the trades were entered, held and exited, and what that did to the result.
- `fee_reduction_metrics.enter_earlier` is HINDSIGHT, not a setting: it measures what a trade
  entered one bar before the signal would have earned. Never propose acting before a bar
  closes.
- Whipsaw (a high `boundary_recross_rate`, frequent signal flips) usually points to a slower
  setting or a smoothing transform on an existing component.

Read the other inputs only to explain your report: the claim and its measured numbers
(`hypothesis_card.yaml`, `claim_result_digest.yaml`), the grid, the base config and the
manifest, the catalogue, CLAIM_TESTS.md for any test you write, and the earlier findings.
