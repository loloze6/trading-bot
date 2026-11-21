---
idea: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a Saturday, and the coin's return over the preceding 7 days -> kept: a weekday regime selects the coming Saturday bar, and the 7-day return is measured at Friday's close.
- Comparison: a higher 7-day rise against a lower one, with fallen coins left out -> kept: the position grows with the 7-day return and is clipped at zero.
- Outcome: the next day's return is larger, upward -> kept: the Saturday bar's return is held for 1 bar.
- Verdict transfer: yes: the test measures the idea's own day, its own lookback and its own horizon.
Forecast: The forecast is nonzero only on the bar whose coming bar is a Saturday. That is the Friday close, so the next day held is Saturday. On that bar the forecast is the coin's 7-bar percent return, standardised against its own past 60 values (target 10, cap 20). The short side is clipped off. It is positive and grows in proportion to the past week's rise. It is zero when the coin fell over the week, and zero on every other weekday.
Config: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: This uses Saturday-signal bars, the bars where the regime is mean_reversion. On each one, take the next-day return minus the coin's mean daily return over all windows, then take the forecast-weighted mean of that excess return. Test it with the t of the mean over the bars with forecast > 0.
- Supporting check: Over those same bars, the Pearson correlation between the forecast and the next-day excess return is positive.
- Confirm: The weighted mean excess return is positive with t >= 2, and the correlation is above 0.
- Reject: The weighted mean excess return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a correlation of 0 or below. At least 300 Saturday bars with forecast > 0 are needed across all coins and windows; fewer is inconclusive.
