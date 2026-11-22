---
plan: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 5-day grid return on forecast: 0.000273992; OLS slope t: 0.929317 (threshold: confirm: slope > 0 with t >= 2 and check > 0; reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return before costs minus position x coin mean daily return: 0.000203165, passed: True
- Counts: grid cases with a non-zero forecast: 1176, grid cases: 1178
- Decided by: The slope's t lies between -2 and 2.
- Reading: The regression uses all grid cases (zero forecasts included) with an intercept and the ordinary OLS slope t, the coin's mean 5-day return is the mean of its grid returns over all its windows, the check's before-cost book uses the held position times the next bar's close-to-close return, averaged over coins each day, and the minimum of 200 non-zero cases is applied as 'not observable'.
- Size: unusual move +0.22 % per case over 5 bars, 0.018 of the coin's usual move (9.44 %); normal drift in its direction +0.10 %, total +0.31 %; 565 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d`
Measure: `measure.py`
