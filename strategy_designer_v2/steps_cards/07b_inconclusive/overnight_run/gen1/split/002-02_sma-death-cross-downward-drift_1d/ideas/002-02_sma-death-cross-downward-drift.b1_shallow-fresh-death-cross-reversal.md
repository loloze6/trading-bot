---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first weeks after a coin's 50-day average crosses below its 200-day average, while the short average is still only just under the long one, the coin's price over the next 10 days rises more than its usual 10-day move.
Consequence: A trader should refuse to short a fresh, shallow death cross, because that is where moves tend to reverse against the short.
Why:
- F4: Ranked by the raw SMA spread, the shallowest quartile (short average only just below the long one) loses: −0.025 (t −2.53, hit 0.45, n 206). The deepest quartile gains +0.0087 (t 0.76, hit 0.55). The middle quartiles are mixed (q2 −0.004, q3 +0.012).
- F6: Freshly crossed bars lose and older crosses gain slightly. Bars 0–20 after the cross give −0.022 (t −1.63, hit 0.46, n 227), 21–60 bars give +0.0037 (t 0.49) and 61–150 bars give +0.0094 (t 0.86). Against the market, every age bucket is about 0 (|t| < 0.09).
- F5: The |forecast| terciles are not monotone: low −0.0053 (t −0.60), mid +0.0057 (t 0.67), high +0.0018 (t 0.21). The supporting check's top-minus-bottom pass (0.0071) therefore rests on the bottom tercile's loss, not on a strong top tercile.
