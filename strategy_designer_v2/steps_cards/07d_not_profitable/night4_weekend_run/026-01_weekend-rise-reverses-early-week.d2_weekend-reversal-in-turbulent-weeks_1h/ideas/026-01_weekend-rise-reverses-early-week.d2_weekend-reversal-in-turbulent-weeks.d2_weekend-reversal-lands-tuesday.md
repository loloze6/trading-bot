---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, with the larger part of the fall coming on Tuesday, the second day, and the larger the weekend gain, the larger Tuesday's fall.
Consequence: A trader would hold the fade through Tuesday and judge its result on the second day, not on Monday's move.
Why:
- F4: The reversal is almost all on Tuesday. The book was short on a similar share of bars both days (27.7 % Monday, 26.9 % Tuesday), but Tuesday's summed gain is +0.741 against Monday's +0.081.
- F2: The Monday–Tuesday hold itself pays: its gain before costs sums to +0.822 (Monday +0.081, Tuesday +0.741). Per case it is +0.122 % of the book over the 48 bars, with t 0.84 over 563 cases. Each case's entry and exit fees are about 0.072 % of the book. So the hold nets roughly +0.05 % per case before what happens after it.
