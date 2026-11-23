---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs in the opposite direction.
Consequence: A trader would fade, not follow, an outsized hourly move in an already agitated market, holding it for a day.
Why:
- F1: Across all regimes, a large hourly move reverses over the next 24 hours, and the reversal grows with the move's size. The pooled slope of the unusual 24-hour return on the hour's return in 24-hour volatility units is negative (t -4.18, 17102 non-overlapping cases). By quartile of |z| (mean |z| 0.15, 0.46, 0.86, 1.81), the reversal strength rises 0.015, 0.027, 0.036, 0.059, with t 0.93, 1.65, 2.67, 3.77. The top quartile's unusual move is 0.30 % per case, against a 0.19 % trade cost.
- F2: The 24-hour reversal sits in the regime the tested idea excluded and is absent where the idea looked. In the highest quintile of the 24h/720h volatility ratio the slope t is -3.02 (2604 cases); in the lowest it is +0.62 (2558 cases). With the ratio at or above its 60th percentile, t is -2.60 (5171 cases); below it, t is -0.24 (7755 cases). This is why the quiet-market continuation idea was rejected (t -2.30).
- F3: The 24-hour reversal is fading over time. The all-regime slope t by year is -0.77, -3.04, -0.77, -3.23, -3.60, -1.98, -0.15, +1.85 for 2018–2025. In the high-ratio subset only 2018 (t -2.49) and 2019 (t -2.88) pass 2. ZEC (t -2.34) and XRP (t -1.67) carry most of it, and BTC and ETH show none (t -0.12, +0.10).
