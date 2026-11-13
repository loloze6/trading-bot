---
idea: N3-04_dip-in-uptrend
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: 20-day and 60-day returns both positive, and the daily close falls by more than half its recent daily standard deviation -> adapted: the uptrend is a regime rule; the fall is graded as the 1-day drop divided by the mean absolute daily return of the past 60 days, with a soft graded dead zone in place of the 0.5 threshold.
- Comparison: an above-average return, judged against the coin's average return -> kept: next-day return is judged against holding the coin, its mean return over all windows.
- Outcome: the return over the next day is higher, on the long side -> kept: the 1-bar return after a long position is measured.
- Verdict transfer: yes: the regime is the idea's uptrend, and the graded drop keeps its direction and size relative to recent daily dispersion.
Forecast: The regime detector computes the 20-day and 60-day price change (PriceEvolutionComponent, periods 20 and 60). When both are above 0 the bar is "trending"; on every other bar the forecast is 0 (flat). In "trending" the component is the 1-day return (PriceEvolutionComponent, period 1), processed in four steps: - It is standardised against its own past 60 values (window 60, min_periods 20). The result is 10 times the return divided by the recent mean absolute daily return. - It is negated, so a down day is positive. - It is clipped at 0, so up days give no position. - It is passed through signed_power with exponent 2 and pivot 10, a soft dead zone. A drop of about half a standard deviation (≈0.6 of the mean absolute move) gives about +3.6. A typical-size drop gives +10. A drop twice the typical size reaches the +20 cap. Tiny drops give almost 0. The forecast is never negative.
Config: N3-04_dip-in-uptrend_1d_oos_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar with forecast > 0, take the coin's next-bar return minus that coin's mean daily return over all 24 windows together (the holding mean). Average these excess returns over all coins and windows, with each bar counted once, and compute the t-statistic of the mean.
- Supporting check: Regress the same next-bar excess return on the forecast size over the forecast > 0 bars. A positive slope means larger drops are followed by larger excess gains.
- Confirm: The mean excess next-bar return is positive with t ≥ 2.0.
- Reject: The mean excess next-bar return is negative with t ≤ -2.0.
- Inconclusive: Any t between -2.0 and 2.0 is inconclusive, including a mean near zero. The test needs at least 200 bars with forecast > 0 pooled across coins and windows; fewer is inconclusive.
