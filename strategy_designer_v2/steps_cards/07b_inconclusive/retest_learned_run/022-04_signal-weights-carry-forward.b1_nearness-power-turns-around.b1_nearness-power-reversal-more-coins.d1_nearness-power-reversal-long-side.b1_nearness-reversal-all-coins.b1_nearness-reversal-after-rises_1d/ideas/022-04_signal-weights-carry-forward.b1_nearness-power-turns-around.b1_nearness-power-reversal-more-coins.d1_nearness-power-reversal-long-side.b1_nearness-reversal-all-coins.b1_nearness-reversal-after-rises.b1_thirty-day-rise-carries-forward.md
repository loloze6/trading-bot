---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: Among coins whose 30-day return is positive, the larger the coin's 30-day return, the higher its return over the next 5 days.
Consequence: A trader should lean longer into a rising coin in proportion to how far it has risen over the past 30 days, rather than on the turn in the nearness-to-high relation.
Why:
- F4: What separates good from bad active cases is the size of the 30-day rise, not the reversal reading:
- F5: The same grading by the 30-day rise shows in trending bars where the forecast is 0:
- F2: The forecast's own grading carries almost none of that slope. Among the 1,127 active cases the rank correlation of forecast with 5-day excess return is −0.014 (p 0.64). The forecast quartiles are not monotonic (+0.46 %, +1.71 %, +0.93 %, +0.54 %). Within the trending regime the slope on the forecast is +0.000326 with t 0.89 over 2,444 cases.
- F3: The effect rests on one year. 2021 alone gives a slope t of 3.67 over 474 cases with an active mean of +5.35 %. Without 2021 the pooled slope is +0.000278 with t 0.88 over 4,401 cases, and the active mean is +0.45 % with t 1.43 over 1,021 cases. 2018, 2022, 2023 and 2025 have negative slopes, and only 10 of 16 coins have a positive slope, none with t above 1.6.
