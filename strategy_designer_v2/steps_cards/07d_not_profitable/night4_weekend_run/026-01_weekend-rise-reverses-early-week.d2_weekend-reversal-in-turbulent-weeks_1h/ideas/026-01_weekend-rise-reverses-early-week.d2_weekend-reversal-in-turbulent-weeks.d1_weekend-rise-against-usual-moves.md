---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, and the larger the weekend gain against the coin's usual two-day move over the last 30 days, the larger the fall.
Consequence: A trader would size the Monday fade by how unusual the weekend's rise is for that coin's recent two-day moves, putting more of the book on the rare large weekend rises, where the fall pays the most against the fixed fee per trade.
Why:
- F5: The size of the forecast does not grade the fall. Across the quartiles of the forecast's size, the 48-bar coin return after the signal runs −0.30 %, −0.97 %, +0.69 %, −1.78 %, not a steady rise in the fall. The step-5 check of the larger half minus the smaller half is −0.08 %. The forecast standardises the weekend's 48-bar gain over only 60 hourly bars, so it compares the weekend mostly with itself.
- F6: The effect exists and is large per case: an unusual fall of +0.84 % over 48 bars (strength 0.118, t 2.80, 557 cases), against a 0.19 % cost per trade. But it is earned against the coin's normal drift (−0.27 % in the short's direction), and the book is short only, with a mean position of −0.39 of the book at entry.
- F1: The book loses because fees take more than the trades gain: summed over all coins and windows, the gain before costs is +0.295 while fees are 0.396, so the book ends at −0.101. The fees fall almost entirely at entry and exit, 0.199 on Sunday's entry bar and 0.179 on Tuesday's exit bars, against less than 0.02 on all other days.
