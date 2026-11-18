---
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a coin's high-volatility day, by its 20-day volatility -> kept: a regime where the 20-day volatility is at or above its 60-day mean.
- Comparison: that day's return relative to its 20-day volatility -> kept: the one-day return divided by the 20-day standard deviation of daily returns.
- Outcome: the next 1 day's return runs against the day just closed, larger after larger scaled moves -> kept: the position is recomputed each bar, so the lean lasts one daily bar.
- Verdict transfer: yes: every part is measured as stated, and the "above its 60-day mean" cut for "high" is a conventional setting.
Forecast: Two cases set the forecast, both on daily bars. - On a high-volatility day (the 20-day volatility of daily returns is at or above its own 60-day mean), the forecast leans against that day's move. It is today's return divided by the 20-day standard deviation of daily returns, standardised against its own past 60 values (about ±10 for a typical move, capped at ±20) and sign-flipped. - It is short after an up day and long after a down day. - Its size grows in proportion to how many usual moves the day covered. - It is zero only on a flat day. - On every other day the regime is null, so the forecast is 0. - The forecast is recomputed at every close, so a lean lasts exactly one bar.
Config: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-bar excess return on the forecast, using only high-volatility bars where regime = trending and the forecast is not zero. - The next-bar excess return is close[t+1]/close[t] − 1 minus that coin's mean daily return over all its windows, kept inside each window. - The slope is fitted by pooled OLS on forecast/10 across all coins and windows. - Its t-statistic is reported with the number of bars; with a 1-bar horizon every bar is an independent case.
- Supporting check: At least 2 of the 3 coins have a per-coin slope with the same sign as the pooled slope.
- Confirm: The pooled slope is positive with t ≥ 2, and at least 2 of the 3 coins have positive slopes.
- Reject: The pooled slope is negative with t ≤ −2, and at least 2 of the 3 coins have negative slopes. This means the next day continues the scaled move rather than reversing it.
- Inconclusive: These results neither confirm nor reject: - a pooled t between −2 and 2; - a |t| ≥ 2 when the coins do not agree as required. The test needs at least 300 pooled high-volatility bars, with at least 60 per coin; below that, the result is inconclusive.
