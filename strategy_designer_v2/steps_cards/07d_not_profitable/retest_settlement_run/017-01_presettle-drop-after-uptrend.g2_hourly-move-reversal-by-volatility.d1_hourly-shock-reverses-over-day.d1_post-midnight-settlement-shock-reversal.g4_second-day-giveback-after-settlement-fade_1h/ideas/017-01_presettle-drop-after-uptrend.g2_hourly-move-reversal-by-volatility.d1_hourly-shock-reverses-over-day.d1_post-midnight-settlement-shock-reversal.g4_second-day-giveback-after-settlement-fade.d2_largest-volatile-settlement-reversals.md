---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While the coin's 20-day volatility is high, the larger the coin's 24-hour return after the first post-00:00-settlement hour runs against that hour's move, measured in units of that 20-day volatility, the larger the percentage return over the following 24 hours back toward that hour's direction.
Consequence: A trader would put most of the risk on the largest reversals in volatile markets, where one case's move is several times the cost of a trade, rather than spreading it evenly or shrinking it as volatility rises.
Why:
- F1: The idea's give-back sits almost entirely in volatile markets: on the active bars, the mean unusual 24-hour move is +0.65 % (t 5.3, n 2923) in the top tercile of the coin's 20-day volatility, against +0.07 % (t 1.1, n 2827) and +0.06 % (t 0.8, n 2839) in the lower two. Ranked by 20-day volatility over 90-day volatility instead, the top tercile gives +0.63 % (t 6.1, n 2523) and the lower two +0.08 % and +0.11 %. So only the volatile cases exceed the 0.19 % cost of a trade, by about 3.3 times; the rest are below it.
- F3: Inside the volatile tercile the effect stays graded by the size of the 24-hour reversal against 20-day volatility: by quintile it is −0.06 %, +0.42 %, +0.59 %, +0.59 % and +1.75 % (top quintile t 5.6, n 557). Both sides hold there (short +0.73 %, t 4.3; long +0.56 %, t 3.2).
- F4: The book is sized against where the effect lives: the vol-target sizing holds a mean allocation of 0.70 on low-volatility cases, 0.48 on middle ones and 0.31 on high-volatility cases. It turns over 0.44 of a coin's value per coin-day, about 4.2 bp a day in costs at 0.095 % per side. That cost is larger than the book's 2.2 bp mean daily return on days in a position, which fails its 5 bp rule.
- F6: The move peaks at 24 hours (+0.25 %, t 4.7) against +0.12 % at 12 hours and +0.19 % at 48 hours; in the top two reversal quintiles it is +0.48 % (t 5.2) at 24 hours and +0.28 % at 48 hours. The 24-hour horizon is right, and a longer holding would not raise the move per case.
