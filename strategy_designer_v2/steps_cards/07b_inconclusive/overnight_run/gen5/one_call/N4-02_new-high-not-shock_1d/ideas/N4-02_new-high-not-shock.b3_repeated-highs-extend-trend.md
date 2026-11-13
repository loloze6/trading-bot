---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-02_new-high-not-shock
line: 7.b inconclusive
backtest: N4-02_new-high-not-shock_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin keeps printing new 20-day closing highs within ten days of earlier ones, its 10-day forward rise is larger than its average 10-day rise.
Consequence: A trader would add to or keep longs in coins already in an established run of new highs, rather than only buying the first break.
Why:
- F6: Holding on to breakout runs after their first day showed a mild edge on non-overlapping samples, with large outsized days doing somewhat better. On every 10th positive-forecast bar, the top half gave +3.99 pp (n=98, t=1.75) and the bottom half +1.70 pp (n=97, t=0.89).
- F2: The result is unclear because the effect is tiny next to the noise. The per-breakout standard deviation is 14–18 pp against a difference of about 1–2 pp. With roughly 380 clusters, the standard error of the gap is near 1.5 pp, so neither the reject rule (|t| ≥ 2) nor the ±1 pp equivalence test can be reached.
