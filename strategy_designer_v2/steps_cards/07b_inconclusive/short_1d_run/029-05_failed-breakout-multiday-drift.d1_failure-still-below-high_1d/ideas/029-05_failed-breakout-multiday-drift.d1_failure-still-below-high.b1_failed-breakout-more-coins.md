---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.b inconclusive
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The further that day-2 close sits below the old high, the larger the fall from day 2 to day 10.
Consequence: A trader would short a failed breakout only once price has stayed below the old high for two days, sized by the current distance below it, and would refuse the short when price is already back above.
Why:
- F1: Step 5's main measure is on the side the idea predicts but below the bar: the mean unusual 8-day move in the short direction is +0.84 % per case (t 1.44, 436 cases, strength 0.048), and my own case reading gives +1.05 % (t 1.89, 486 cases), also short of t 2.
- F5: The effect is mixed across coins at 8 days: XRP +2.71 % (t 2.04, 61 cases), ZEC +3.23 % (t 1.76, 75) and BTC +1.54 % (t 1.69, 92), while LTC is -0.94 % (t -0.57, 83) and XMR -0.19 % (t -0.19, 94). Six coins leave each with under 100 cases.
