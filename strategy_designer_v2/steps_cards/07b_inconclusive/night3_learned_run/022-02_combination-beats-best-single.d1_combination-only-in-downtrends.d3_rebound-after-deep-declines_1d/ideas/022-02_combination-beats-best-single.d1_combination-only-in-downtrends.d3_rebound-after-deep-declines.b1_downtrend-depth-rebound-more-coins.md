---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is negative, the further it stands below its 90-day high, the higher its return over the next 5 days.
Consequence: A trader refuses shorts on coins already deep below their 90-day high and leans toward a rebound there.
Why:
- F2: Recomputed from the closes, raw depth below the 90-day high while the 90-day return is negative predicts the excess return clearly: slope 0.149, t 4.79 over 414 cases at 5 days, and slope 0.298, t 5.14 over 191 cases at 10 days.
- F3: The raw-depth effect is broad, not confined to one coin or period. At 5 days the slope is positive on all 6 coins (t 3.00 XRP, 2.42 ZEC, 2.33 ETH, 2.17 LTC, 1.71 BTC, 0.83 XMR), and at 10 days 5 of 6 coins reach t ≥ 2.10. It is also positive in 6 of 8 years: t 2.87 in 2018, 2.75 in 2022, 2.54 in 2021 and 2.10 in 2020, with only 2019 (t -0.85) and 2024 (t -0.11) flat or negative.
- F5: The rebound belongs to downtrends. With the 90-day return at or above 0, raw depth has no positive slope: t -1.10 at 5 days in the recomputed sample, and t -3.35 over 1,313 cases outside the regime in the recorded sample. Within downtrends the slope is steepest in the most negative third of 90-day returns (0.30, t 2.80).
