---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return the larger the gain, and the gain is larger the further its close sits above its lowest close of the past 52 weeks, so a coin far below its high earns little rather than falling.
Consequence: Treat distance below the high as a reason to stand aside, not to sell short. That removes short positions that cost the market's rise and earned no timing.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: the 7-day forward return minus the coin's grid mean averages +0.0069 over 1199 independent forecast > 0 cases, with t = 1.71. The supporting check passes, with the upper half minus the lower half at +0.0185.
- F2: The effect is small against the market's own noise: the active cases' excess returns have a standard deviation of 0.139, about 20 times their mean. Their median is -0.0042, only 47.1 % are positive, and winsorising at 1 % drops the t from 1.71 to 1.48.
- F4: The direction holds across coins but no coin is clear alone. Five of six coins have positive mean excess at 7 days (BTC +0.0085 t 1.30, ETH +0.0117 t 1.33, ZEC +0.0114 t 0.87, XRP +0.0092 t 0.66, LTC +0.0023 t 0.25), and XMR is flat at -0.0010 (t -0.13), each on only 175 to 215 cases.
- F5: The graded part of the idea shows, and it is concentrated in the strongest cases. The upper half of the forecast earns +0.0162 excess (t 2.54, 599 cases) against -0.0024 in the lower half (t -0.48, 600 cases). The top forecast quintile earns +0.0231 (t 1.94, 240 cases), and active minus flat bars is +0.0139 (Welch t 2.58, 1199 vs 1179 cases).
- F6: The test did not miss the effect by its horizon. On the same non-overlapping grids the active excess is +0.0058 at 14 days (t 0.61, 578 cases) and +0.0117 at 28 days (t 0.55, 281 cases), so 7 days is the clearest horizon. The shortfall is a lack of cases at a small effect size, not a misplaced measure.
