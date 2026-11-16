---
idea: 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the first 30 days after the 50-day SMA crosses above the 200-day SMA, fresher counting more -> adapted: a 30-bar regime on the cross's age, with the short graded by freshness.
- Comparison: the coin's usual move over 10 days -> kept.
- Outcome: the coin falls over the next 10 days, more the fresher the cross -> kept.
- Verdict transfer: yes: the test checks the same window, the same direction and the same freshness ordering against the coin's usual 10-day move.
Forecast: The detector reads how many daily bars the 50-day SMA has stayed above the 200-day SMA (MovingAverageAgeComponent, period 200, fast_period 50, max_bars 31). While that age is between 1 and 30, the bar is in the 30-day post-cross regime. Every other bar is flat. - Inside the regime, the forecast is (−10 + 0.5 × s_age) / 1.5. Here s_age is the cross age standardised over 200 bars, which grows from about 0.4 on day 1 to about 12 on day 30. The −10 is the standardised "50 above 200" side (the same age component capped at 1 bar), negated. - The forecast is always short. It is largest on the day of the cross (about −6.5) and shrinks smoothly toward about −2.7 by day 30, so the short grows with freshness. - It goes to zero when the regime ends.
Config: 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take the coin's 10-bar forward return on regime bars, sampled on the non-overlapping 10-bar grid of each window. Subtract the coin's mean 10-bar return over all windows on the same grid. Report the t of the mean of these differences, with the number of cases.
- Supporting check: On the same grid, the forward 10-bar excess return of fresh bars (age 1–15) minus stale bars (age 16–30) is negative (Welch t below 0).
- Confirm: The main-measure t is −2 or less, and the supporting difference is below zero.
- Reject: The main-measure t is +2 or more: after fresh golden crosses the coin rises more than usual.
- Inconclusive: Any main t between −2 and +2, or a confirming main t with a fresh-minus-stale difference at or above zero. A verdict needs at least 20 non-overlapping regime cases across all coins and windows; with fewer, the result is inconclusive.
