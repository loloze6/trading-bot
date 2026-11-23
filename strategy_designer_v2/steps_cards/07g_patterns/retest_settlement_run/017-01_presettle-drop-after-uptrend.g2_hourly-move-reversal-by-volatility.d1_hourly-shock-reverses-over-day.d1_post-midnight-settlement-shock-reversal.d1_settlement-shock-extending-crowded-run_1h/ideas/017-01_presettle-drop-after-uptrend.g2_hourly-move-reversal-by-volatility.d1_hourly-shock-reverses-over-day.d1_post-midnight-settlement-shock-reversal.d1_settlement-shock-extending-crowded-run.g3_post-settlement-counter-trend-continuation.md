---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's return over the 1 to 3 hours after the 00:00 UTC settlement runs against its return over the previous 23 hours, the coin's return over the next 24 hours runs in the direction of that post-settlement move, and the larger that move relative to the coin's 24-hour hourly volatility, the larger it is.
Consequence: A trader would follow an early-morning UTC move that breaks against the previous day's run, sized by the move, rather than fade it.
Why:
- F3: In the hours just after the 00:00 UTC settlement, an hour that moves against the coin's previous 23-hour return is followed by a 24-hour return in that hour's own direction, not a fade. Fading it gives sign means of −0.21 %, −0.25 % and −0.29 % at 01:00, 02:00 and 03:00, with t −4.2, −4.8 and −5.7, on about 8,900 cases each. The same opposed hours at 11:00–14:00 give positive fades (t +2.2 to +3.5). Counter-trend 3-hour moves ending at 03:00 also continue: slope +21 bp, t 2.7, on 5,815 cases, while those ending at 09:00, 15:00 and 21:00 show nothing (t 0.08, 0.16, −0.83).
- F4: Fading the coin's 24-hour return depends on the hour it is read at. Read at 23:00–04:00 UTC, the fade pays, with slopes +12 to +23 bp and t 2.7 to 5.0 (01:00: t 5.0, sign mean +0.17 %). Read at 12:00–15:00 UTC, it is negative, with slopes −8 to −17 bp; at 14:00 the t is −3.8 and the sign mean is −0.09 %. Volume follows the same clock: relative log volume is +0.15 at 00:00 and −0.39 at 05:00, and peaks at +0.45 at 16:00.
