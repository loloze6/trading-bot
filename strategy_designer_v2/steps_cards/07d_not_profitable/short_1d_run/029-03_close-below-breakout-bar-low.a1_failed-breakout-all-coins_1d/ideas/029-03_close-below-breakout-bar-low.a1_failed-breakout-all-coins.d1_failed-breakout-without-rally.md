---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, only while its 20-day return before that close is small; the smaller that 20-day return, the larger the fall.
Consequence: Short failed breakouts that come without a prior rally, and refuse the short when the breakout capped a strong 20-day rise.
Why:
- F2: Recomputed from prices on every failure bar (one per 5-day grid cell), closes under the breakout day's low within 3 days give 294 cases. Their mean short-signed unusual 5-day move is −0.92 % (t −1.32) and the total is −1.74 %, so the coin rises after them. Step 5's +1.33 % on 113 cases comes only from the bars where its bet rule fired.
- F4: The coin's own 20-day return at the failure splits the result.
- F5: The losses gather in the strong-rally years.
- F6: Depth under the breakout low does not grade the move.
