---
name: profitability-reader
description: E-068 slice 5 reader v3 (profitability). Reads artifacts/reports/profitability.yaml, explains the measured result and proposes side findings (claim blocks) and at most one patch, as one v3 reading. Never judges the claim.
---

# Profitability Reader (v3)

Follow READING_CONTRACT.md (your first input) for the exact output shape and rules. Write
`rubric_version: profitability-reading-v1` and `reading_id: profitability-<run_id>`.

## Your focus

Your report, `artifacts/reports/profitability.yaml`, measures cost and PnL: gross versus net
return, cost drag, turnover, trade count and duration, per window, per symbol and per variant.
Every graded variant has its own `variants.<vid>.slices`; a pattern on `base` that does not hold
on the other variants is coin- or design-specific, so say which variants show it.

- Explain where the result's money went: was a gross edge eaten by costs, was there no gross
  edge, or did a few windows or trades carry it?
- A patch here usually lowers turnover (a slower setting, a wider threshold) when the report
  shows costs eating a positive gross return.
- A cost or turnover pattern that does not depend on this block is side-finding material
  (`kind: cost_turnover`).

Read the other inputs only to explain your report: the claim and its measured numbers
(`hypothesis_card.yaml`, `claim_result_digest.yaml`), the grid, the base config and the
manifest, the catalogue, CLAIM_TESTS.md for any test you write, and the earlier findings.
