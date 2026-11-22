---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days.
Consequence: A trader would follow a coin's 30-day trend over the next 5 days, not fade it.
Why:
- F1: The test's result points the way the idea predicts but falls short of the bar. On 1,476 independent 5-day cases the correlation is +0.034 with t 1.29. The mean move in the forecast's direction is +0.52 % (strength 0.045, t 1.66), close to the 0.05 strength real ideas usually show. A true effect of that size needs far more cases than six coins provide to reach t 2.
- F2: The effect is spread thinly across coins rather than carried by one. Five of six coins have a positive correlation: BTC +0.036, ETH +0.077, LTC +0.016, XRP +0.036, ZEC +0.063. XMR alone is negative at −0.051. No coin reaches t 2 (largest t 1.28, ETH, on 275 cases), so each coin's sample is too small on its own.
- F6: The plan's 5-day horizon is roughly where the effect peaks, so a different horizon would not give a clearer answer.
- F7: The move per case is large enough to pay for trading. The total move of +0.73 % per case is 3.8 times the 0.19 % cost of a trade. The question left open is whether the effect is real, not whether it could pay.
