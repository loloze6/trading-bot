---
brief: 010_rsi-midline-regime-direction
source-idea: 010-08_rsi-below-streak-reversal
line: 7.d not profitable
backtest: 010-08_rsi-below-streak-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days, with the rise coming mainly from runs lasting several weeks and growing with the run's length beyond that.
Consequence: A trader would ignore short dips of RSI below 50 and would weight the reversal bet toward runs that have lasted for weeks.
Why:
- F1: The book loses because its long bars come when the coin does worse than usual: the book's mean gain per bar is -0.000046, made of +0.000296 from the coin's own rise and -0.000345 from timing. On long bars the next-day return is 0.000004 for BTC against a coin mean of 0.001183, and -0.000491 for ETH against 0.001368.
- F4: The forecast's information sits in the longest runs. Long bars with runs of 40–60 days earn a mean next-day return of +0.002006 (gain +0.001277, n=225). Runs of 0–5 days earn -0.001161 (n=321) and runs of 5–10 days earn -0.001074 (n=512); none of these bins reaches |t| 0.7.
- F6: The losses are concentrated in a few heavy bars. The 40 worst long bars average a gain of -0.0894 and sum to 24 times the book's net total. On them the position averaged 1.10, the run averaged 35 days (19.5 on all long bars) and the 7-day return averaged -0.073 (-0.049 on all long bars).
