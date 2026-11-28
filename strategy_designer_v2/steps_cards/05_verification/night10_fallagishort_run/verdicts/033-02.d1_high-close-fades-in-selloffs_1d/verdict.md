---
plan: 033-02.d1_high-close-fades-in-selloffs_1d
idea: 033-02.d1_high-close-fades-in-selloffs
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean short-direction excess next-day return: 0.000694519; day-clustered t of weighted mean: 0.334811 (threshold: above 0 with day-clustered t >= 2 to confirm; t <= -2 to reject)
- Supporting check: top third minus bottom third by abs(forecast), short excess next-day return: 0.00348022, passed: True
- Counts: independent days with a nonzero forecast: 902, cases: 2457
- Decided by: The weighted mean's t lies between -2 and 2 (or the confirm rule is not met). No effect (common/verdicts.md): t in the idea's direction +0.335 (below 1), 2457 cases (30 needed).
- Reading: The falling agitated profile is read from the recorded regime (the detector's decision, 'unknown' = not vetoed to chop) with a close location above the low as the graded situation, the 1-bar grid is every bar, the coin's mean is over all its bars in all windows, the weighted t clusters per UTC day with a G/(G-1) correction, terciles are pooled over all cases by abs(forecast) with unweighted means, and the plan's 'fewer than 150 days' is reported as not observable.
- Size: unusual move +0.11 % (t 0.49, the cases of one day together: 545 days) per case over 1 bars, 0.019 of the coin's usual move (4.92 %); normal drift in its direction -0.06 %, total +0.05 %; 1151 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.335 (below 1), 2457 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/033-02.d1_high-close-fades-in-selloffs_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/033-02.d1_high-close-fades-in-selloffs_1d`
Measure: `measure.py`
