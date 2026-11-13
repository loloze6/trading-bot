---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC together as a cross-coin average
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close is far below its 200-day average in a high-volatility stretch and it fell over the last three days, it outperforms the average of the other coins over the next ten days.
Consequence: Hold the deep-discount coin against the rest of the market rather than outright, to remove the market's swing that hides the rebound.
Why:
- F4: The market's own moves drown the effect. Top-forecast 10-bar returns correlate 0.80 with the cross-coin mean return over the same 10 bars. Subtracting that mean cuts the standard deviation from 0.19 to 0.12 and raises the t from 0.90 to 1.40 (mean +0.021, 64 cases).
- F2: When the coin was still falling into the signal, the rebound is concentrated there. Top-forecast bars with a negative 3-day return average +0.043 excess (median +0.006, 55% positive, t 1.27, 42 cases). Those with a positive 3-day return average −0.014 (37% positive, t −0.51, 27 cases). The 5-day split gives the same picture: +0.036 (t 1.26, 50 cases) against −0.019 (19 cases).
