---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's close sits above the middle of its 30-day closing range, the larger its rise over the next 5 days; the flatter the 30 days were, the larger that rise, and the closer the close stands to its 90-day high, the larger that rise again.
Consequence: A close near the top of a flat month is a reason to buy for 5 days when the coin is near its 90-day high, and a weak one when the flat month sits well below that high.
Why:
- F1: The Calmar fails at 0.70 because the deepest fall is −32.8 % against a yearly return of +23.4 %; that fall took 362 days across w1–w4, while holding the coins fell −60.7 %. The next falls are −24.2 % (w21–w22, holding −39.4 %), −19.8 % (w20–w21, holding −3.8 %) and −18.9 % (w12–w13, holding −70.2 %).
- F2: Inside the six deepest falls the book stays invested on 61 % of bars (72 % elsewhere) at a mean allocation of 0.40 (0.48 elsewhere). Its active bars there lose −0.19 % per bar over 3294 bars, against +0.22 % per bar over 8584 bars outside the falls. The coin's next-day return on those bars is −0.50 %, against +0.38 % outside.
- F3: The falls are flat months sitting inside a longer decline. On active fall bars the coin's median 30-day return is +0.4 % (+9.3 % elsewhere). Its median 90-day return is −4.1 % (+15.9 % elsewhere), and its median distance below the 90-day high is −21.3 % (−10.3 % elsewhere). The 30-day flatness factor cannot see this 90-day downtrend.
- F4: Active bars within 3.4 % of the 90-day high gain +0.197 % per bar (t 2.9, 1851 bars), and only 10 % of them fall inside the book's falls. Bars 18–33 % below that high gain +0.008 % (t 0.2), and 40 % of them fall inside the book's falls. The deepest quintile, more than 33 % below, gains +0.147 % (t 3.1) but also has 42 % of its bars inside the falls.
- F5: Being below or above the 50-day mean does not separate the losses. Inside the falls, bars below it lose −0.17 % per bar (2235 bars) and bars above it lose −0.25 % per bar (1059 bars).
