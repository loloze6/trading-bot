---
plan: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 5-day grid return on forecast: 0.000597066; OLS slope t: 3.37568 (threshold: confirm: slope > 0 with t >= 2 and check > 0; reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return before costs minus position x coin mean daily return: 0.000712042, passed: True
- Counts: grid cases with a non-zero forecast: 7173, grid cases: 7175
- Decided by: The slope is positive with t >= 2 and the book's timing gain before costs is above 0.
- Reading: The regression uses all grid cases (zero forecasts included) with an intercept and the ordinary OLS slope t, the coin's mean 5-day return is the mean of its grid returns over all its windows, the check's before-cost book uses the held position times the next bar's close-to-close return, averaged over coins each day, and the minimum of 200 non-zero cases is applied as 'not observable'.
- Size: unusual move +1.05 % per case over 5 bars, 0.083 of the coin's usual move (12.45 %); normal drift in its direction +0.19 %, total +1.24 %; 3142 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d`
Measure: `measure.py`
