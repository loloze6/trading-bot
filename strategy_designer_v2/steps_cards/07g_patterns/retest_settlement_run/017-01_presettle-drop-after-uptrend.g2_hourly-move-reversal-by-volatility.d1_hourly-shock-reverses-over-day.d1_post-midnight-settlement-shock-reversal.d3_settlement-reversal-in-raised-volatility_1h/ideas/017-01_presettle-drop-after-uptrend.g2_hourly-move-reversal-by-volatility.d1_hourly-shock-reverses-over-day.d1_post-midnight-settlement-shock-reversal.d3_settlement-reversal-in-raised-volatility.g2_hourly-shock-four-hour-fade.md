---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return relative to its 24-hour volatility, the more its return over the next 4 hours runs the opposite way, and more so the higher the coin's 24-hour volatility stands.
Consequence: A trader would fade sharp single-hour moves over a few hours, weighting the fade toward the coin's most volatile stretches.
Why:
- F3: A coin's 1-hour return in 24h-volatility units reverses over the next 4 hours at many hours of the day, not only after settlement. Hour 11 gives −10.8 bp per unit (t −5.8), hour 18 −7.6 (t −5.0), hour 23 −6.3 (t −4.0) and hour 5 −6.7 (t −3.9). Pooled over hours 5, 11, 18 and 23 the slope is negative in every year (t below −2.5 in 6 of 8 years, about 8600 cases a year).
- F4: That 4-hour reversal, on the non-overlapping 4-hour grid, scales with how volatile and thin the coin is. ZEC gives −7.7 bp per unit (t −4.0), XRP −5.6 (t −3.4), XMR −5.2 (t −3.4) and LTC −3.2 (t −2.1), against BTC −0.9 (t −0.8) and ETH −0.1 (t −0.1), about 17000 cases each.
