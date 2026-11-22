---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
line: 7.b inconclusive
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the breakout day's volume was below its 20-day average, and the lower that volume against its average, the larger the fall.
Consequence: A trader would short only failed breakouts that came on thin volume, and stand aside from those that came on heavy volume, which tend to break higher again.
Why:
- F1: The tested result points the way the idea predicts but is too small for this data: over the backtest's 221 cases the short-direction unusual 5-day move is +0.69 % (t 1.06, strength 0.083), and my rebuild of the same cases gives +0.85 % (t 1.33, 220 cases). Reaching t 2 at this effect size needs about 3.6 times as many cases.
- F2: The graded check could not run, because the forecast is pinned at its limit. 209 of the 220 cases sit at exactly -20, which left 0 cases in the larger half and all 221 in the smaller. The raw thinness value itself does grade the move: Spearman rho 0.138 (p 0.041, 220 cases), and the upper half minus the lower half is +1.75 % (t 1.38, 110 vs 110).
- F3: The effect sits in the thinner failures. By tercile of raw thinness, the thinnest-volume failed breakouts move +1.76 % (t 1.60, 74 cases), the middle +1.84 % (t 1.73, 73 cases) and the least thin -1.07 % (t -0.95, 73 cases).
- F4: Across all failed breakouts, the volume condition separates the two sides. Thin-volume failures move +0.40 % in the short direction (200 cases) and heavy-volume failures -1.07 % (t -1.69, 305 cases), a thin-minus-heavy difference of +1.47 % (t 1.61). Without the volume condition, all failures together move -0.49 % (t -1.05, 505 cases).
- F5: The market's own moves drown the effect in strong-trend years, and it is uneven across coins.
