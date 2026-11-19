---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
line: 7.b inconclusive
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, most strongly while its 60-day return is positive.
Consequence: Treat extreme overbought RSI on these coins as a reason to stay long or add, not to short, and refuse RSI-based shorts in uptrends.
Why:
- F1: The main measure is clearly on the side the idea predicts: the pooled slope of the 240-bar excess return on the forecast is 0.00280 with t 4.74 over 1,674 grid cases. The same positive slope holds at 24, 120, 480 and 720 bars (t 2.54, 3.72, 3.96 and 4.22), so the horizon is not the issue.
- F2: The effect is graded. Among the 821 positive-forecast cases, the mean 240-bar excess return rises steadily across forecast quartiles, from -0.0101 to 0.0026, 0.0131 and 0.0391 (about 205 cases each). The positive-only slope is 0.0036 (t 3.59).
- F3: The result is unclear only because the regime split is too weak to separate. On all grid bars the slope is 0.00336 (t 3.83, n 841) in `trending` and 0.00143 (t 1.56, n 833) in `unknown`. On positive-forecast bars it is 0.0039 (t 2.95, n 574) against 0.0024 (t 1.75, n 247). The difference therefore leans the predicted way, but its Welch t is only 1.53, with just 247 positive cases in `unknown`.
- F4: The effect is mixed across coins and periods, which lowers its power on six coins. Per-coin slopes run from 0.0004–0.0005 (t 0.37–0.42) for XMR and LTC up to 0.0060 (t 3.30) for XRP. By year, 2023 runs strongly the other way (slope -0.0043, t -3.89) and 2018 and 2022 are negative, against t 2.6–3.8 in 2019, 2020 and 2025.
