---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day hourly volatility is low against its own last 6 months, its move from Saturday 00:00 UTC to Monday 00:00 UTC continues in the same direction over the following two days (Monday and Tuesday). The larger the weekend move, the larger the continuation.
Consequence: In calm weeks a trader would follow the weekend's direction into Monday and Tuesday rather than fade it, and would refuse the weekend fade in those weeks.
Why:
- F3: When a coin's 30-day hourly volatility is low against its own 6-month volatility, the weekend move continues over Monday and Tuesday instead of reversing. The continuation's unusual move is +0.97 % (t 2.49, 457 cases, strength 0.14) and its total move is +1.00 %, about 5 times the 0.19 % cost. In the middle and hot thirds of that ratio the continuation is −0.15 % and −0.05 % (t −0.50 and −0.16).
- F4: Inside that calm regime the continuation is strongest after weekend falls and after the largest weekend moves:
- F5: The same pattern shows on the coin's own volatility thirds. In each coin's lowest-volatility third, the slope of the next 48 hours on the standardised weekend move is +0.0101 (t 3.55, n 645) and the reversal is −0.50 % (t −2.27). In the highest third the reversal is +0.15 % (t 0.40). There, the reversal grows with the weekend move's size from −1.10 % to +1.11 % across quartiles (top-quartile strength 0.16), but after weekend rises it is only +0.50 % (t 1.00, n 332).
- F1: Weekend rises are not reversed over Monday and Tuesday. Across 1124 cases the unusual move is −0.02 % (t −0.10) and the total move is −0.29 % against a trade cost of 0.19 %. The slope of the next 48 hours on the weekend's 48-hour return is −0.036 (t −1.21, n 1932). By weekend z-quintile, the next 48 hours rise most after the largest weekend falls (+0.51 %) and after the largest weekend rises (+0.64 %), so no quintile shows a reversal.
