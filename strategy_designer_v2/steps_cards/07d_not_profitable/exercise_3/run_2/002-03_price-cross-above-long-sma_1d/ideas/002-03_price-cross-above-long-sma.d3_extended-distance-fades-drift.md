---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, except when the close is stretched very far above, where the upward drift weakens as the stretch grows.
Consequence: A trader caps exposure when price is extremely extended above the average, which shrinks the large-position falls that set the Calmar.
Why:
- F4: The book's worst 5% of held days came at large positions far above the average: mean allocation 1.76 against 0.93 over all held days, and mean distance 89% against 31%. In the 20-bar blocks the furthest-above distance quintile returned -0.020 excess (t -0.62), while the 29 to 54% quintile returned +0.038 (t 1.24).
- F6: The falls sit in a few windows. The book lost -0.33, -0.39 and -0.48 in w12, w13 and w18 against the coins' -0.15, -0.31 and -0.24, while w24 (4.37) and w11 (2.06) carry the gain. XMR's book Sharpe was -0.02 against 0.48 for holding it, with a deepest fall of -0.96.
