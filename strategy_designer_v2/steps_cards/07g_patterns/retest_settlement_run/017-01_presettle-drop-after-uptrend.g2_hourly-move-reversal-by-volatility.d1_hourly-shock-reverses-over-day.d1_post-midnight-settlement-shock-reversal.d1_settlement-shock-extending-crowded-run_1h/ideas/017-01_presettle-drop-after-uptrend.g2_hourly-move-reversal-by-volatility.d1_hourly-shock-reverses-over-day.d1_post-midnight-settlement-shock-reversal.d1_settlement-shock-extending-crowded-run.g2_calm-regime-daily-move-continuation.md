---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the last 24 hours is low relative to its last 30 days, its 24-hour return continues in the same direction over the next 24 hours, and the larger that 24-hour return in units of its hourly volatility, the larger the continuation.
Consequence: A trader would follow a coin's day-long move in calm stretches, sized by the move's size relative to volatility, instead of fading it.
Why:
- F1: Across all hours except 00:00, fading the coin's 24-hour return (in units of its 24-hour hourly volatility) over the next 24 hours depends on the volatility regime. When the 24-hour volatility is in the top third relative to its 30-day level, the fade pays: slope +25.4 bp per unit, t 14.3, sign mean +0.26 %, t 15.1, on 98,930 overlapping bar cases. When it is in the bottom third, the sign flips: slope −16.4 bp, t −10.5, sign mean −0.10 %, t −7.7. In calm regimes the 24-hour move continues rather than reverses.
