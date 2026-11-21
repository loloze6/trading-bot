---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3585 USD
---
## Findings
- **F1:** The test's forecast measures something other than what the idea states: it standardises the depth over 90 days, so it reads depth relative to the coin's recent depth rather than depth itself. On the same 1,651 grid cases the standardised forecast gives a slope t of only 0.87 at 5 days and 0.61 at 10 days. The recorded raw percent distance below the 90-day high gives a slope of -0.000429 per point at t -2.84 at 5 days and t -2.24 at 10 days (814 cases); since that distance is negative, deeper cases are followed by higher returns.
- **F2:** Recomputed from the closes, raw depth below the 90-day high while the 90-day return is negative predicts the excess return clearly: slope 0.149, t 4.79 over 414 cases at 5 days, and slope 0.298, t 5.14 over 191 cases at 10 days.
- **F3:** The raw-depth effect is broad, not confined to one coin or period. At 5 days the slope is positive on all 6 coins (t 3.00 XRP, 2.42 ZEC, 2.33 ETH, 2.17 LTC, 1.71 BTC, 0.83 XMR), and at 10 days 5 of 6 coins reach t ≥ 2.10. It is also positive in 6 of 8 years: t 2.87 in 2018, 2.75 in 2022, 2.54 in 2021 and 2.10 in 2020, with only 2019 (t -0.85) and 2024 (t -0.11) flat or negative.
- **F4:** The effect is graded and large at the deep end, with the deepest cases far above the cost of a trade.
- **F5:** The rebound belongs to downtrends. With the 90-day return at or above 0, raw depth has no positive slope: t -1.10 at 5 days in the recomputed sample, and t -3.35 over 1,313 cases outside the regime in the recorded sample. Within downtrends the slope is steepest in the most negative third of 90-day returns (0.30, t 2.80).
- **F6:** The test's own size is small and negative (unusual move -0.44 %, total +0.13 %, which is 0.7 times the 0.19 % cost). That is because the standardised forecast spreads its cases evenly over shallow and deep positions, and the shallow positions keep falling (F4).

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.b1_downtrend-depth-rebound-more-coins` (from F2, F3, F5): While a coin's 90-day return is negative, the further it stands below its 90-day high, the higher its return over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.b2_raw-depth-rebound-ten-days` (from F1, F2, F3, F4, F5): While a coin's 90-day return is negative, the larger the percentage by which its close stands below its highest close of the last 90 days, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
