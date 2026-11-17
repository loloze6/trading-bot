---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-04_heavy-volume-drop-continues
line: 7.b inconclusive
backtest: 003-04_heavy-volume-drop-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it keeps falling over the next 5 days. The larger the fall and the heavier its volume against that average, the larger the further loss.
Consequence: A sharp drop on heavy volume reflects many traders acting on new information that is still spreading, so the decline carries on as slower traders arrive.
Why:
- F1: The test's measure is on the side the idea predicts but short of the bar: across 286 independent signal events the mean excess 5-day return is -0.0089 with t = -1.51, only 52% of events negative, and the median-split check passes at -0.0086.
- F2: The effect is graded as the idea says but carried by the strongest cases. The third with the most negative forecasts has a mean excess 5-day return of -0.0190 (t = -2.01, n = 95), the middle third -0.0114 (t = -0.95), and the weakest third +0.0034 (t = +0.37).
- F4: The effect varies a lot by period and coin, which drowns it in the pooled test:
