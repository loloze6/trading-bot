---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the coin's 24-hour return after the first hour following the 00:00 UTC settlement runs against that hour's move, the more its return over the following 24 hours runs back toward that hour's direction. This holds only while the coin's 20-day volatility is high against its 90-day volatility, and the give-back grows with that ratio.
Consequence: A trader would take the second-day give-back only when the coin's recent volatility is raised against its longer-run level, and would stand aside in calm markets where the move does not cover the cost.
Why:
- F1: The idea's give-back sits almost entirely in volatile markets: on the active bars, the mean unusual 24-hour move is +0.65 % (t 5.3, n 2923) in the top tercile of the coin's 20-day volatility, against +0.07 % (t 1.1, n 2827) and +0.06 % (t 0.8, n 2839) in the lower two. Ranked by 20-day volatility over 90-day volatility instead, the top tercile gives +0.63 % (t 6.1, n 2523) and the lower two +0.08 % and +0.11 %. So only the volatile cases exceed the 0.19 % cost of a trade, by about 3.3 times; the rest are below it.
- F2: Volatility is not an effect of its own: at the same 00:00 UTC bars, when the 24-hour move and the post-settlement hour agree (no signal), the top relative-volatility tercile earns +0.007 % (t 0.06, n 2176) and the top absolute-volatility tercile +0.08 % (t 0.6, n 2536). A volatile market belongs to the brief's theory, because crowding, and the funding paid for it, is largest after strong moves.
- F4: The book is sized against where the effect lives: the vol-target sizing holds a mean allocation of 0.70 on low-volatility cases, 0.48 on middle ones and 0.31 on high-volatility cases. It turns over 0.44 of a coin's value per coin-day, about 4.2 bp a day in costs at 0.095 % per side. That cost is larger than the book's 2.2 bp mean daily return on days in a position, which fails its 5 bp rule.
