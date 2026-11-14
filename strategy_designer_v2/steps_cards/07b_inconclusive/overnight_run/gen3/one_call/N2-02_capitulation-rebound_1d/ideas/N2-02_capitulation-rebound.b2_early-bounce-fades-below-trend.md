---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close is far below its 200-day average in a high-volatility stretch but it has risen over the last three days, it falls back below its usual drift over the next ten days.
Consequence: Refuse long entries on deep-discount coins whose short bounce has already begun, because that bounce tends to fade.
Why:
- F3: The same split holds in the deepest fifth of in-regime distance below the 200-day SMA, and it shows up in both directions. A negative 3-day return gives +0.028 excess (t 1.32, 76 cases). A positive 3-day return, meaning the bounce has already started, gives −0.034 (35% positive, t −2.38, 83 cases).
- F2: When the coin was still falling into the signal, the rebound is concentrated there. Top-forecast bars with a negative 3-day return average +0.043 excess (median +0.006, 55% positive, t 1.27, 42 cases). Those with a positive 3-day return average −0.014 (37% positive, t −0.51, 27 cases). The 5-day split gives the same picture: +0.036 (t 1.26, 50 cases) against −0.019 (19 cases).
