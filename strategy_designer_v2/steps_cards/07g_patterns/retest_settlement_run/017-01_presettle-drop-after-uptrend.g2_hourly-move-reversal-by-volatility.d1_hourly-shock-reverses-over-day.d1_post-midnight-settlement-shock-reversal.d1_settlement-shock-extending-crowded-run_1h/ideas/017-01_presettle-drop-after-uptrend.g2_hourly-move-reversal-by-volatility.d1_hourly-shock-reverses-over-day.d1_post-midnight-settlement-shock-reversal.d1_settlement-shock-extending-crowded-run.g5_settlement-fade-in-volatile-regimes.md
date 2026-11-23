---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When the coin's first hour after the 00:00 UTC settlement runs the same way as its previous 23 hours, the over-24-hours reversal of that hour grows with the hour's return relative to its 24-hour volatility, and it grows more steeply the higher the coin's 24-hour volatility is relative to its last 30 days.
Consequence: A trader would size the post-settlement fade up when the market is in a raised-volatility stretch and keep it small in calm ones.
Why:
- F2: On the 00:00 UTC bar, the tested idea's gain sits almost entirely in high relative volatility. In the aligned cases, the top third of volatility gives slope 55.2 bp, t 5.5, sign mean +0.77 %, t 6.3, on 2,012 cases. The bottom third gives slope 11.8 bp, t 1.4, sign mean +0.16 %. Fading the full 24-hour return at 00:00 shows the same split: top third t 5.0, sign mean +0.39 %; bottom third t 0.4, sign mean −0.01 %.
- F5: The tested aligned post-settlement fade holds in every year, with t from 1.6 to 3.7 from 2018 to 2025, and in every coin, with t from 1.5 for BTC to 3.7 for LTC and XMR. The weakest coin is BTC: slope 11.8 bp, sign mean +0.24 %. The broader unconditioned 00:00 fade of the 24-hour return has faded away: t 4.6 in 2018, −0.4 in 2024 and −1.5 in 2025.
- F6: The book's worst days come with the coin's largest moves. The bottom decile of book days averages −2.99 % on days when the coin moved 6.3 % in absolute terms. The middle deciles see coin moves of 1.9–3.4 %. Losses concentrate on days of outsized moves, not at random.
