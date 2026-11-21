---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
line: 7.b inconclusive
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 26 days is larger the farther its daily close stands above the top of its Ichimoku cloud, and smaller the farther it stands below it. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.
Consequence: A trader would lean long in proportion to how far a coin trades above its cloud, and lean away from coins trading below it.
Why:
- F1: The tested slope points the way the idea predicts but falls short of the bar: t 1.52 on 576 non-overlapping 26-day cases. Its size is tiny, an unusual move of +0.22 % per case and a strength of 0.001 of the coin's usual 25.48 % move, far below the 0.05 of real ideas so far (findings F10).
- F2: The effect comes from which side of the cloud top the close is on, not from how far it is. Closes above the top were followed by +3.7 % excess over 26 days (227 cases); closes below by -2.4 % (349 cases); Welch t about 2.1 from those means and spreads. Within each side the slope on distance is flat or reversed: t -0.01 above, t -1.16 below.
- F5: The effect differs in sign across coins and years. By coin, BTC t 2.01 and ZEC t 1.80, against XRP -0.98 and XMR -0.57. By year, 2019 t 1.81 and 2025 t 2.35, against 2020 t -2.39, 2021 t -2.10 and 2023 t -1.97. Each group has 96 or 72 cases, too few to settle any of them.
