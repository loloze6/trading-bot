---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high, and minus its 30-day volatility. Each signal is weighted equally in the direction its effect is known for, instead of by how well it predicted that coin's own 5-day returns over the past 365 days.
Consequence: The weak effects should be combined with fixed, known directions, because weights learned from the past year point the wrong way in the year that follows.
Why:
- F1: The result is on the side the idea predicts but too small for this grid to show: the mean product is +0.0065 (t 1.21, 3419 cases), and the forecast's top fifth is followed by +0.62 % above drift over 5 days against −0.10 % for its bottom fifth, with the quintiles in between not ordered (−0.61 %, +0.23 %, −0.14 %).
- F2: The t depends on which day the 5-day grid starts: moving the grid's start by 1 to 4 days gives t 2.37, 2.63, 3.15 and 1.43 (3307 to 3407 cases), so the plan's grid (phase 0, t 1.21) is the weakest of the five, not a typical reading.
- F5: The effect is uneven across coins and periods: at 5 days ETH has t 2.48 and XMR −1.18, the year 2020 has t 3.25 and 2023 has −3.30, and at 10 days windows w13–w24 give t 3.67 while w1–w12 give 0.03.
- F6: Size against cost: the unusual move is +0.96 % per case over 5 days, a strength of 0.082 and 5.0 times the 0.19 % round trip. Over 10 days it is +0.83 % in the signal's direction, against a usual move of 15.9 %. The book's Sharpe is 0.94, 0.38 above holding, and it fails only on mean daily return (0.00029) and Calmar (0.75).
