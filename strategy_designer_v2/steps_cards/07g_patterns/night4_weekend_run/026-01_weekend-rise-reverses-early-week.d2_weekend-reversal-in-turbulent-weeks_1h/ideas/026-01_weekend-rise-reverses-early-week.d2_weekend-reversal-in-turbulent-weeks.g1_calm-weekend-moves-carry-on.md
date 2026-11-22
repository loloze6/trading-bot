---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's move from Saturday 00:00 to Monday 00:00 UTC carries on in the same direction over the next two days (Monday and Tuesday) while the coin's 30-day hourly volatility is low against its own last 6 months. The larger the weekend move, measured against that volatility, the larger the move that follows in its direction.
Consequence: A trader would follow, not fade, a weekend move in calm weeks, and refuse a weekend fade there.
Why:
- F1: Weekend moves continue rather than reverse. On the 00:00 UTC grid, Monday's next 48-hour return rises with the weekend's 48-hour return, each standardised by the coin's 30-day hourly volatility: slope +0.119, t 3.65, 2228 cases. After a weekend rise, Monday and Tuesday returned +0.39 %; after a weekend fall, −0.26 %. The same slope at the other weekday points is between +0.006 and +0.058.
- F2: The continuation sits in calm weeks. In the lowest tercile of each coin's 30-day hourly volatility, a weekend rise was followed by +0.84 % over Monday and Tuesday (t 2.93, 426 cases) and a weekend fall by −0.70 % (t −2.14, 317 cases), with a slope of +0.34. In the highest tercile, a weekend rise was followed by only −0.27 % (t −0.59, 385 cases) and the slope was +0.125, still not a reversal. This fits step 5's failed size check: the larger half minus the smaller half was −0.0008.
- F3: The weekend continuation is not monotone in the weekend's size. By quintile of the standardised weekend move, the next 48-hour return was +0.43 %, −0.60 %, −0.30 %, +0.39 % and +0.53 % (about 445 cases each), so it shows mainly in the top quintile of weekend rises.
- F4: The continuation is strongest in XRP and BTC. Their Monday slopes were +0.285 (t 3.47, 381 cases) and +0.202 (t 2.05, 380 cases), against 0.004 to 0.144 for XMR, LTC, ZEC and ETH.
