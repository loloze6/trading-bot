# Claim kind `execution_behaviour` (E-077, orchestrator.folds.enabled only)

This page is shown to no prompt yet. It is the text the analyst's guide (E-077 PR-5) will
add to CLAIM_TESTS.md's "claim kind" table once that guide exists. Until then CLAIM_TESTS.md,
the card schema's kind enum and `claim_card.check_claim` (called without `folds=True`) know
only the original kinds, so a run with `orchestrator.folds.enabled` off sees exactly what it
saw before.

| Claim `kind` | What the claim needs |
|---|---|
| `execution_behaviour` | a claim about the strategy itself (E-077). Today a bar test on its own `bars.csv` (`event` or `regime` + `fwd_return` + `complement` + `mean_diff`), or `tests: none` with `missing_block` for what only the trades show (a trade-level test family is a later PR) |

The kind is a finding only, never a block (absent from `claim_card.KIND_BLOCK`). It is accepted
by `check_claim(claim, folds=True)` only; the callers that run under the folds flag pass it
(`fold_confirm`, `explore_confirm.finding_route` / `finding_spec_hashes`, the step 1a card
checks in `run_phase1_research.py`).
