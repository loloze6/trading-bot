---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the last 24 hours is high relative to its last 30 days, its 24-hour return reverses over the next 24 hours, and the larger that 24-hour return in units of its hourly volatility, the larger the reversal.
Consequence: A trader would fade a coin's day-long move only in a stretch of raised volatility, sized by how stretched the move is, and refuse that fade in calm stretches.
Why:
- F1: Across all hours except 00:00, fading the coin's 24-hour return (in units of its 24-hour hourly volatility) over the next 24 hours depends on the volatility regime. When the 24-hour volatility is in the top third relative to its 30-day level, the fade pays: slope +25.4 bp per unit, t 14.3, sign mean +0.26 %, t 15.1, on 98,930 overlapping bar cases. When it is in the bottom third, the sign flips: slope −16.4 bp, t −10.5, sign mean −0.10 %, t −7.7. In calm regimes the 24-hour move continues rather than reverses.
- F2: On the 00:00 UTC bar, the tested idea's gain sits almost entirely in high relative volatility. In the aligned cases, the top third of volatility gives slope 55.2 bp, t 5.5, sign mean +0.77 %, t 6.3, on 2,012 cases. The bottom third gives slope 11.8 bp, t 1.4, sign mean +0.16 %. Fading the full 24-hour return at 00:00 shows the same split: top third t 5.0, sign mean +0.39 %; bottom third t 0.4, sign mean −0.01 %.
