---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 20 days, and the lower its 20-day realised volatility at the cross, the larger the rise.
Consequence: A trader would favour calm upward cloud breakouts held for about three weeks, rather than violent ones or a longer hold whose gain fades.
Why:
- F2: The grading the idea states, calmer crosses rising more, does appear in the plain 20-day volatility, but the test's forecast does not carry it. The Spearman correlation of the 20-day volatility at the cross with the 40-day drift-adjusted return is −0.27 (p 0.005, 151 cases), while that of the forecast is only +0.04 to +0.13 (p 0.63). The forecast compares today's volatility with its own 365-day mean, which is why step 5's calm-minus-violent split came out at −0.169, on the wrong side.
- F3: Within each coin, the gradient runs the predicted way but is too weak to show clearly. Ranked within each coin, the calm, middle and violent thirds of crosses end at +0.39, +0.24 and −0.14 of a usual 40-day move, with 56 %, 50 % and 29 % of cases above the drift. Calm minus violent is +0.21, but its Welch t is only 0.82 (53 against 53 cases). The pattern is also not shared by every coin: it holds in BTC, ETH, LTC and XRP, while XMR and ZEC run the other way.
- F4: The effect is strongest at a shorter horizon than the plan's 40 days. The mean drift-adjusted return after the cross is +1.9 % over 10 days (t 1.51, 190 cases), +5.8 % over 20 days (t 2.32, 181 cases), +8.7 % over 40 days (t 1.81, 151 cases) and +7.6 % over 60 days (t 0.82, 103 cases). Its t peaks at 20 days.
- F1: The rise after an upward cloud cross comes from a few large cases, not from a typical one. Over 151 cross bars with 40 days left, the mean drift-adjusted 40-day return is +8.7 % (t 1.81), but the median is −2.1 % and only 48 % end above the drift. The 5 largest cases make up 141 % of the summed standardised return, and without them the mean is −0.066 of a usual move. This is why step 5's weighted mean only just reaches t 2.04.
