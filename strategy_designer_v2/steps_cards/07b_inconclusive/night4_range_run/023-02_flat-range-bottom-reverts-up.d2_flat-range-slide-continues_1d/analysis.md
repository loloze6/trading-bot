---
line: 7.b inconclusive
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5450 USD
---
## Findings
- **F1:** The test's main measure is essentially zero, not merely short of the bar. On 1085 mean_reversion grid bars, the slope of the next-5-day excess return on the forecast is -1.06e-05, with a t of -0.02. More data cannot move a result with no side, so the tested idea unchanged on more data is not called for.
- **F2:** The effect is not graded with the depth of the fall, so the slope finds nothing. Forecast buckets over 5 days, from deepest to shallowest:
- **F3:** The idea's situation carries a level, not a gradient.
- **F4:** The effect is mixed across coins and years.
- **F5:** The horizon does not rescue the tested direction.
- **F6:** Recomputed from prices, flat coins below their range's middle show only weak continuation over 5 days: the slope of excess return on the 10-day return is +0.036 with a t of 1.12 (820 bars). By ratio band:
- **F7:** The clear graded effect is in trending coins below the middle of their 30-day range, and it is reversion.
- **F8:** The idea's size cannot carry a short book.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back` (from F7, F5, F2): In a coin whose 30-day net move has been large relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 10 days, the more it rises over the next 5 days.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues` (from F2, F3): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
