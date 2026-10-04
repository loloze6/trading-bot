# Claim-test review: offline measurement (run1)

Model `claude-haiku-4-5`, closed-book (the pipeline's own options). Verdict: **FAIL** (4/6 calls met their expectation). Total cost $0.2908.

| case | call | expectation | result | why | cost (USD) | input | output | cache read | cache write |
|---|---|---|---|---|---|---|---|---|---|
| A | 1 | units_flagged | pass | horizon_units_ok false on ['vol_managed_continuation'] | 0.0535 | 10 | 8152 | 0 | 5471 |
| A | 2 | units_flagged | pass | horizon_units_ok false on ['vol_managed_continuation'] | 0.0399 | 10 | 6697 | 5471 | 0 |
| B | 1 | units_not_flagged | pass | every horizon_units_ok true | 0.0688 | 10 | 11171 | 0 | 5567 |
| B | 2 | units_not_flagged | pass | every horizon_units_ok true | 0.0400 | 10 | 6703 | 5567 | 0 |
| C | 1 | level_not_move_flagged | FAIL | not flagged: ['high_close_shock_reversion', 'low_close_shock_reversion'] | 0.0566 | 10 | 8656 | 0 | 5750 |
| C | 2 | level_not_move_flagged | FAIL | not flagged: ['high_close_shock_reversion', 'low_close_shock_reversion'] | 0.0321 | 10 | 5069 | 5750 | 0 |
