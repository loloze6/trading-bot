---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3477 USD
---
## Findings
- **F1:** The book is close to holding the coins, so it carries the coins' own falls: it is in a position on 89 % of coin-days with a mean allocation of 1.04, and its daily return follows the coins' day by day (worst tenth of days −586 bps against the coins' −757, best tenth +568 against +729), which gives a deepest fall of 70.8 % against holding's 81.2 %, a yearly return of 25.0 % and a Calmar of 0.35.
- **F2:** The breakout itself adds almost nothing, so the falls cannot be cut by the forecast as it stands: per case, the unusual move over 20 days is +0.35 % (strength 0.004, t 0.30 over 680 cases), while the total move of +2.84 % is mostly the coins' normal drift of +2.50 %.
- **F3:** Being long while the close is below its 50-day average earns nothing and carries the worst falls. On in-position days, the two lower quartiles of the close against its 50-day average earn +2.6 and −0.4 bps a day, against +17.1 and +36.7 bps in the two upper quartiles. On the 20-day grid, in-position cells that start below the average return −1.47 % (157 cells, worst −82.6 %), against +6.13 % above it (189 cells, worst −44.5 %), Welch t 3.20.
- **F4:** The same split holds on the coin's own past return. In-position days in the lower quartiles of the 10-day return earn +9.2 and −1.5 bps a day, against +19.4 and +36.1 bps in the upper ones. For the 20-day return the figures are +7.8 and +1.1 bps against +17.8 and +35.8 bps, and the gain per unit of risk rises from 0.002 to 0.067.
- **F5:** The losses are spread over many ordinary down days, not a few crashes: the 40 worst book days carry only 16 % of all the book's losing-day losses, so a fall in this book is a long stretch of being long in a falling coin.
- **F6:** Trades are lopsided and the gain sits in a few coins: 942 long trades have a median of −1.3 % and a mean of +12.4 %, with ZEC at +47.6 % per trade and XMR at +0.04 %.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend` (from F1, F2, F3, F5): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 20 days, only while its close is above its 50-day average. The more times the level held, the further the close above it and the further the close above its 50-day average, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d2_distance-above-50-day-average` (from F1, F3, F4, F5): The further a coin's close stands above its 50-day average, and the larger its 20-day return, the larger its rise over the next 20 days. The further below, the smaller the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
