---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close is far below its 200-day average in a high-volatility stretch and it has still fallen over the last three days, it rises more than its usual drift over the next ten days.
Consequence: Buy capitulation only while the coin is still falling into the signal, not after it has already started to bounce.
Why:
- F2: When the coin was still falling into the signal, the rebound is concentrated there. Top-forecast bars with a negative 3-day return average +0.043 excess (median +0.006, 55% positive, t 1.27, 42 cases). Those with a positive 3-day return average −0.014 (37% positive, t −0.51, 27 cases). The 5-day split gives the same picture: +0.036 (t 1.26, 50 cases) against −0.019 (19 cases).
- F3: The same split holds in the deepest fifth of in-regime distance below the 200-day SMA, and it shows up in both directions. A negative 3-day return gives +0.028 excess (t 1.32, 76 cases). A positive 3-day return, meaning the bounce has already started, gives −0.034 (35% positive, t −2.38, 83 cases).
- F1: The pooled result rests on a few large winners. After forecast ≥ 10, the mean 10-bar excess is +0.021 (t 0.90, 69 non-overlapping cases), but the median is −0.016 and only 48% of cases are positive. Dropping the 5% largest absolute moves brings the mean to −0.0005 (t −0.03, 65 cases), and XRP alone averages +0.119 with a median of −0.019 (11 cases).
