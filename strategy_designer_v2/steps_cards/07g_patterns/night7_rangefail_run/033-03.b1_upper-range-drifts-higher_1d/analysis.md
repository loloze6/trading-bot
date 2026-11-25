---
line: 7.g patterns
backtest: 033-03.b1_upper-range-drifts-higher_1d
idea tested: 033-03.b1_upper-range-drifts-higher
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3916 USD
---
## Findings
- **F1:** The tested range-position slope lives in calm markets. Over the 10-day grid of folds B and C, the slope of the 10-day excess return on the close's 20-day range position is 0.105 (t 5.17, 390 cases) when the coin's 30-day swing is at or below its median, against 0.021 (t 0.68, 312 cases) when it is above. With each coin's own past-year volatility rank and the cases of one day clustered, it is 0.141 (t 2.34, 126 cases on 32 days) when calm and −0.010 (t −0.08) when agitated.
- **F2:** The effect grows as the market gets calmer. In the lowest quartile of the coin's own volatility rank the slope is 0.341 (t 3.47, 50 cases, 18 days). The next three quartiles give 0.013 (t 0.21), 0.053 (t 1.38) and −0.087 (t −0.56). In calm markets the top quartile of range position is followed by +13.9 % excess over 10 days (32 cases), against +1.5 % for the bottom quartile.
- **F3:** Over all profiles the gain sits at the top of the range. The top fifth of range position is followed by +4.41 % excess over 10 days (t 2.65, 141 cases), the bottom two fifths by −1.86 % (t −1.41) and −2.72 % (t −2.08). The pooled slope stays weak (verdict t 1.53; size +0.59 %, t 1.02 over 832 days).
- **F4:** By the 60-day trend, the slope is 0.140 in rising markets (t 2.88, 158 cases), 0.167 in choppy ones (t 2.34, 63 cases) and only 0.037 in falling ones (t 1.01, 193 cases).
- **F5:** The book earns on its long side and loses on its short side. Its 1,211 long trades average +7.67 % net (median +0.25 %); its 1,324 short trades average −0.96 % (median −2.80 %).
- **F6:** The effect is not steady across coins or windows. In calm markets the slope is positive on ETH, LTC, XMR, XRP and ZEC (t 1.20 to 2.52) but negative on BTC (−0.071, t −1.04). By window over all profiles, only w16 is strongly positive (t 5.46) and w14 is negative (t −2.07).

## Ideas
- `033-03.b1.g1_calm-range-position-drift` (from F1, F2, F3, F6): In a calm market, the higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 10 days, and the calmer the market, the steeper this rise.
- `033-03.b1.g2_rising-market-range-drift` (from F4, F3, F5): In a rising market, the higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
