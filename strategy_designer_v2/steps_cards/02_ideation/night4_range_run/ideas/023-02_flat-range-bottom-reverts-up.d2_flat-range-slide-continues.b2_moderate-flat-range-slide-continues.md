---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
line: 7.b inconclusive
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves.
Consequence: A flat coin sliding moderately below the middle of its range is a short to take, while its most extreme slides are left alone.
Why:
- F2: The effect is not graded with the depth of the fall, so the slope finds nothing. Forecast buckets over 5 days, from deepest to shallowest:
- F3: The idea's situation carries a level, not a gradient.
