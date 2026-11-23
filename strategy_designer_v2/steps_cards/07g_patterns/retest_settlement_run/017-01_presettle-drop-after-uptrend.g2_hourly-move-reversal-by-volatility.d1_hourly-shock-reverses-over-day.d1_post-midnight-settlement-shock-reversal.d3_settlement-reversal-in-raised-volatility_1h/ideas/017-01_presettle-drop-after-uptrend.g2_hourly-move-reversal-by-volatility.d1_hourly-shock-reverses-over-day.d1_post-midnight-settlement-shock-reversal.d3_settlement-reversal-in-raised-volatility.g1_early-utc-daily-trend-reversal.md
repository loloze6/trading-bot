---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its 24-hour volatility at the close of the early UTC hours (00:00 to 05:00), the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade the previous day's run when reading it in the hours just after the midnight settlement, sized by the run's size in volatility units, and refuse to fade it later in the day.
Why:
- F1: Apart from the tested 00:00 UTC hour itself (24-hour slope on the hour's volatility-scaled return −26.1 bp per unit, t −7.8, 17086 cases), the coin's prior 24-hour return in 24h-volatility units reverses over the next 24 hours when read at the close of the early-UTC hours. The slope is −21.1 bp at hour 0 (t −5.2), −21.7 at hour 1 (t −5.3), −19.2 at hour 2 (t −4.7), −18.2 at 3 (t −4.4), −18.0 at 4 (t −4.3) and −15.3 at 5 (t −3.6), about 17000 cases each. It fades to −3.1 (t −0.7) by hour 7 and turns positive at hours 12–15 (hour 14: +16.7, t +4.1).
- F2: At hour 0 the prior trend adds to the settlement-hour return rather than repeating it. In a joint fit, the hour's return keeps −26.2 bp (t −7.8) and the 23-hour trend before it adds −13.4 bp (t −3.2). That trend slope is negative in 2018–2023 (−47 to −15 bp) but near zero in 2024 (+2.0, t 0.2) and reversed in 2025 (+34.1, t +3.0), so it is not stable over time.
