---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3039 USD
---
## Findings
- **F1:** The effect is near zero at every horizon: when the close sits below its SMA200, the coin's 10-bar excess fall beyond holding averages +0.0020 (t 0.44, 931 non-overlapping blocks), against +0.0011 at 5 bars (t 0.47, n 1905), -0.0001 at 20 bars (t -0.01, n 448) and -0.0010 at 40 bars (t -0.05, n 207), so moving the horizon does not reveal it.
- **F2:** The effect flips sign by year, so the pooled mean cancels: the 10-bar excess fall is positive in the bear years 2018 (+0.0365, t 2.18, n 133), 2019 (+0.0165, t 1.85, n 140) and 2022 (+0.0232, t 2.48, n 195), and negative in the bull years 2020 (-0.0257, t -1.72, n 87), 2021 (-0.0683, t -2.78, n 68) and 2024 (-0.0157, t -1.59, n 109).
- **F3:** The forecast's grading does not work: the deepest quarter of below-average closes gives an excess fall of -0.0058 (t -0.58, n 233) and the shallowest quarter gives +0.0078 (t 0.95, n 233), and the step-5 slope of excess return on allocation is negative (-0.0126).
- **F4:** Being below the average carries no information on its own: flat blocks above the SMA200 show a 10-bar excess return of +0.0028 (t 0.42, n 726), about the same size as the short side's +0.0020, and no coin is significant (t from -0.35 for XRP to 0.57 for XMR).
- **F5:** The market's own rise sinks the book. The gross short gain before the mean is removed is -0.0054 per 10-bar block (t -2.53, n 931) and stays negative at every horizon (t -2.1 to -2.6), while the excess part is about zero (F1). The book's Sharpe of -0.43 comes from shorting coins that drift up, not from bad timing.
- **F6:** Middling cases are the only ones with a hint of an effect: blocks with mid recent volatility give +0.0132 (t 1.74, n 265) against -0.0040 (t -0.44) for high volatility, and blocks with a mid 20-bar past move give +0.0110 (t 1.47), still short of t 2.

## Ideas
- `002-04_price-cross-below-long-sma.b1_below-average-short-in-downtrends` (from F2, F4, F5): While a coin's close is below its 200-day moving average, the price keeps falling beyond its usual drift over the following days, only while that long average is itself falling, and the faster the average falls the further the price drops.
- `002-04_price-cross-below-long-sma.b2_dip-below-rising-average-rebounds` (from F2, F5): While a coin's close is below its 200-day moving average and its long average is rising, the price rises beyond its usual drift over the following days, and the further the average has risen the larger that rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
