---
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1735 USD
---
## Findings
- **F1:** The effect is small and not graded. In my recomputation (154 non-overlapping new-low cases on BTC and ETH, median 30-day fall 16.8%), the mean excess 10-day return by quintile of the fall runs -0.005, -0.023, -0.029, -0.039 and -0.003 from the mildest to the deepest. The mildest fifth falls least of all, not most, and the Spearman correlation of the fall with the 10-day excess return is only -0.016.
- **F2:** The two coins point opposite ways. On BTC, mild minus deep is -0.029 vs +0.003 (t -1.09, 47/32 cases), as the idea predicts. On ETH it is +0.001 vs -0.040 (t +1.02, 30/45 cases), the opposite. Pooled, the two cancel to step 5's t of -0.81.
- **F3:** The years flip sign as well, with groups of only 1 to 27 cases. Mild minus deep is t -2.74 in 2021 and -1.77 in 2018, but +2.35 in 2025 and +1.57 in 2020. In 2023 there were 15 mild cases against 1 deep. The mild/deep split therefore largely tracks the period.
- **F4:** Other horizons do not show the effect either. Mild minus deep is t -0.94 at 3 days, -0.36 at 5 days, +0.21 at 10 days and -0.84 at 20 days (-0.047 vs -0.020, 72/70 cases). No horizon comes near the bar.
- **F5:** Splitting by the 60-day trend does not isolate it. Mild minus deep is t -0.05 when the 60-day return is positive (18/6 cases) and +0.18 when it is negative (59/71 cases).
- **F6:** What does show is a general tendency to keep falling, across all new lows. All 154 cases average -0.020 in 10-day excess return (sd 0.149, t -1.64). Step 5's mild group averages -0.027, so its result sits on the predicted side, but this sample of two coins is too small to separate a gradient from noise.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.b1_shallow-new-lows-more-coins` (from F2, F3, F6): When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
