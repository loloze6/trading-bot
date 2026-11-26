---
line: 7.b inconclusive
backtest: 059-01.b1_calm-swing-scaled-move-continues_1d
idea tested: 059-01.b1_calm-swing-scaled-move-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3114 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but short of the bar: the slope of the 5-day excess return on the forecast is +0.00044 with a day-clustered t of 1.41, over 1829 grid cases on 483 days. The size is +0.27 % per case, 0.027 of a usual move, with t 0.91 over 916 days, so the effect is real in sign but too small for six coins to show clearly.
- **F2:** On the shown folds B and C, the calm bars carry the effect and the agitated bars do not. On calm bars the 5-day slope of the scaled move is t 2.67 (773 cases); on agitated bars it is t 0.34 (591 cases). The calm-side t is 1.92 at 2 days, 2.34 at 10 days and 1.56 at 20 days. So the full-sample t of 1.41 means folds A and D hold a weaker or noisier version, not an opposite one.
- **F3:** On calm bars at 5 days, the slope is positive on every one of the six coins. The t values run from 1.21 (LTC) to 2.60 (ETH), and none is negative. A consistent but small effect per coin is the case where more coins would sharpen the estimate.
- **F4:** Within calm bars, the effect is strongest when the coin's 60-day trend is choppy or rising and weakest when it is falling.
- **F5:** The grading holds on the up side but breaks at the extreme of the down side.
- **F6:** The book barely differs from holding the coins. Its Sharpe is 0.55, against holding's Sharpe higher by 0.016. The total move per case, 0.25 %, is only 1.3 times the 0.19 % cost of a trade. A clearer test of the idea needs more independent cases, not a different holding rule.

## Ideas
- `059-01.b1.b1_calm-scaled-move-more-coins` (from F1, F2, F3): In a calm market, the larger a coin's 20-day rise measured in units of its own daily swing over those 20 days (the 20-day return divided by the standard deviation of its daily returns over the same days), the larger its rise over the next 5 days, and the larger such a fall, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
