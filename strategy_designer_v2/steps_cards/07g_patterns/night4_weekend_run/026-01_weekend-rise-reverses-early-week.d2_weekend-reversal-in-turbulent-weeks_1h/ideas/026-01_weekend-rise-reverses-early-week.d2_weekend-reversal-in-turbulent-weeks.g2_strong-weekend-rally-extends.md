---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's weekend rise from Saturday 00:00 to Monday 00:00 UTC, measured against its 30-day hourly volatility, the larger its rise over the next two days.
Consequence: A trader would refuse to short a strong weekend rally and would lean long into Monday and Tuesday instead.
Why:
- F1: Weekend moves continue rather than reverse. On the 00:00 UTC grid, Monday's next 48-hour return rises with the weekend's 48-hour return, each standardised by the coin's 30-day hourly volatility: slope +0.119, t 3.65, 2228 cases. After a weekend rise, Monday and Tuesday returned +0.39 %; after a weekend fall, −0.26 %. The same slope at the other weekday points is between +0.006 and +0.058.
- F3: The weekend continuation is not monotone in the weekend's size. By quintile of the standardised weekend move, the next 48-hour return was +0.43 %, −0.60 %, −0.30 %, +0.39 % and +0.53 % (about 445 cases each), so it shows mainly in the top quintile of weekend rises.
