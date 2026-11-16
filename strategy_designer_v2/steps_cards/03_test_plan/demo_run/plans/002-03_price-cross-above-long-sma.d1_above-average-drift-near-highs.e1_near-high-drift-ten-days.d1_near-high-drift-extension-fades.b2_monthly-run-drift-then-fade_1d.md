---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the close is above its 200-day average, and the coin has a 30-day return of some size -> adapted: the 200-day condition becomes a regime, and the 30-day return is held as a graded value.
- Comparison: larger 30-day returns versus smaller ones, with the trend reversed at the very largest -> adapted: the "very largest" threshold becomes a graded hump that turns down at about 1.4 times the usual size.
- Outcome: the rise over the next 10 days grows with the 30-day return, but shrinks at its extremes -> kept: measured on 10-bar forward returns against the coin's average.
- Verdict transfer: yes: the forecast's shape is the idea's shape, and both the rising part and the falling part are measured directly.
Forecast: The forecast is active only while the close is above its 200-day SMA (regime `trending`); otherwise it is flat. - Inside that regime, s is the 30-day percent return, standardised against its own past 60 values. - The forecast is (6·s − 10·sign(s)·(|s|/10)³) / 5, a weighted mean with weights 6 and −1. - It grows with s up to s ≈ 14, where it peaks at about 11. - Above s ≈ 14 it falls again, to about 8 at the cap of 20. This is the trim at extreme runs. - It is negative when the 30-day return is negative and 0 when that return is 0. - Its size changes smoothly with s, with no jumps.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: - Sample: grid bars 0, 10, 20, … of each window where the regime is `trending`. - Measure: the OLS slope, with its t, of the coin's 10-bar excess forward return on the bar's forecast. - Excess return: close[t+10]/close[t] − 1, minus that coin's mean 10-bar return over all windows. - Pool all coins.
- Supporting check: - Use the same cases, with s = `run.post_pipeline_value`. - Compute the mean excess return of cases with s ≥ 14 minus that of cases with 8 ≤ s < 14, using Welch's t.
- Confirm: The idea is confirmed when both of these hold: - the main slope has t ≥ 2; - the supporting check is negative with t ≤ −2.
- Reject: The idea is rejected when either of these holds: - the main slope has t ≤ −2; - the supporting check is positive with t ≥ +2 (extreme runs are followed by larger rises).
- Inconclusive: Every other result is inconclusive, including any t between −2 and 2. - The main measure needs at least 100 non-overlapping cases. - The check needs at least 20 cases in each tier; with fewer, the check is inconclusive.
