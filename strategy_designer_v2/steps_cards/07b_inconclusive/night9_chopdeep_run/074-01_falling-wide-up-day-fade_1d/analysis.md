---
line: 7.b inconclusive
backtest: 074-01_falling-wide-up-day-fade_1d
idea tested: 074-01_falling-wide-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2199 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar. Step 5's mean next-day move in the short direction is +0.48 % with a day-clustered t of 1.28 over 258 case-days, and its size is +0.56 %, strength 0.125 of a usual move, t 1.43 over 234 days. The shortfall is a weak t, not a wrong sign.
- **F2:** In folds B and C, the falling-market up days with a range above the 20-day mean are followed by a next-day fall that is clear on its own. The mean is +1.12 % below drift in the short direction (t 2.05, 289 cases on 122 days). The forecast <= -2 cases show the same at +1.32 % (t 1.98, 155 cases, 74 days).
- **F3:** The grading the idea states is in the raw width, not in the step 5 forecast. The slope of the next-day short-direction move on the range multiple is +0.0188 per unit of multiple (t 2.88, n 289), and by width bucket the means are as follows.
- **F4:** The effect lives where the brief says it does and is mirrored in rising markets. In rising markets the next day after a wide up day is stronger, not weaker, at −0.67 % (multiple 1.0–1.3, t −1.43) and −2.63 % (1.7–2.2, t −2.14). In choppy markets it is mixed.
- **F5:** The effect is spread across coins but uneven, so with six coins it stays close to the bar. All six coins are on the predicted side: BTC +1.78 % (t 2.02), ETH +1.45 % (t 2.14), LTC +1.63 % (t 2.31), ZEC +1.16 % (t 1.43), XMR +0.73 % (t 1.03) and XRP +0.33 % (t 0.35). Each coin has only 30 to 56 case-days.
- **F6:** Across periods the sign holds in most years but not all, which dilutes the t.
- **F7:** The move is a one-day effect, as the brief claims. On non-overlapping grids it is +1.12 % over 1 day (t 2.05) against +0.50 % over 2 days (t 0.58), and the 3-day and 5-day readings rest on only 48 and 21 days. More data at the plan's own horizon is the cleaner answer.

## Ideas
- `074-01.b1_falling-wide-up-fade-more-coins` (from F1, F2, F3, F5, F7): In a falling market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day, and the wider that range is against the 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
