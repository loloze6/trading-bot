---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return is read at the close of the hours around and just after midnight UTC, its return over the next 24 hours runs opposite to it, and the larger that 24-hour return in units of the coin's hourly volatility, the larger the reversal.
Consequence: A trader would fade the day's run around the UTC day change, sized by its stretch, and refuse that fade when the same run is read in the European and US midday hours.
Why:
- F4: Fading the coin's 24-hour return depends on the hour it is read at. Read at 23:00–04:00 UTC, the fade pays, with slopes +12 to +23 bp and t 2.7 to 5.0 (01:00: t 5.0, sign mean +0.17 %). Read at 12:00–15:00 UTC, it is negative, with slopes −8 to −17 bp; at 14:00 the t is −3.8 and the sign mean is −0.09 %. Volume follows the same clock: relative log volume is +0.15 at 00:00 and −0.39 at 05:00, and peaks at +0.45 at 16:00.
- F5: The tested aligned post-settlement fade holds in every year, with t from 1.6 to 3.7 from 2018 to 2025, and in every coin, with t from 1.5 for BTC to 3.7 for LTC and XMR. The weakest coin is BTC: slope 11.8 bp, sign mean +0.24 %. The broader unconditioned 00:00 fade of the 24-hour return has faded away: t 4.6 in 2018, −0.4 in 2024 and −1.5 in 2025.
