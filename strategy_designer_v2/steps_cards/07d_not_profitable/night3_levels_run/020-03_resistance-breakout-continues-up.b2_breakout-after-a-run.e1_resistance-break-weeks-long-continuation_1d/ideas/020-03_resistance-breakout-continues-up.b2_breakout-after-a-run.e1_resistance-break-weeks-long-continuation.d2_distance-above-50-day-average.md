---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close stands above its 50-day average, and the larger its 20-day return, the larger its rise over the next 20 days. The further below, the smaller the rise.
Consequence: The distance of the close from its 50-day average is a reason to hold a coin through weeks of trend and to step aside while it trades below it, which removes the long falls a nearly always-long book carries.
Why:
- F1: The book is close to holding the coins, so it carries the coins' own falls: it is in a position on 89 % of coin-days with a mean allocation of 1.04, and its daily return follows the coins' day by day (worst tenth of days −586 bps against the coins' −757, best tenth +568 against +729), which gives a deepest fall of 70.8 % against holding's 81.2 %, a yearly return of 25.0 % and a Calmar of 0.35.
- F3: Being long while the close is below its 50-day average earns nothing and carries the worst falls. On in-position days, the two lower quartiles of the close against its 50-day average earn +2.6 and −0.4 bps a day, against +17.1 and +36.7 bps in the two upper quartiles. On the 20-day grid, in-position cells that start below the average return −1.47 % (157 cells, worst −82.6 %), against +6.13 % above it (189 cells, worst −44.5 %), Welch t 3.20.
- F4: The same split holds on the coin's own past return. In-position days in the lower quartiles of the 10-day return earn +9.2 and −1.5 bps a day, against +19.4 and +36.1 bps in the upper ones. For the 20-day return the figures are +7.8 and +1.1 bps against +17.8 and +35.8 bps, and the gain per unit of risk rises from 0.002 to 0.067.
- F5: The losses are spread over many ordinary down days, not a few crashes: the 40 worst book days carry only 16 % of all the book's losing-day losses, so a fall in this book is a long stretch of being long in a falling coin.
