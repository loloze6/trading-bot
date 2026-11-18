---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 10 days.
Consequence: A new low reached after only a mild fall is a reason to refuse a rebound long, and a reason to expect continuation.
Why:
- F2: The two coins point opposite ways. On BTC, mild minus deep is -0.029 vs +0.003 (t -1.09, 47/32 cases), as the idea predicts. On ETH it is +0.001 vs -0.040 (t +1.02, 30/45 cases), the opposite. Pooled, the two cancel to step 5's t of -0.81.
- F3: The years flip sign as well, with groups of only 1 to 27 cases. Mild minus deep is t -2.74 in 2021 and -1.77 in 2018, but +2.35 in 2025 and +1.57 in 2020. In 2023 there were 15 mild cases against 1 deep. The mild/deep split therefore largely tracks the period.
- F6: What does show is a general tendency to keep falling, across all new lows. All 154 cases average -0.020 in 10-day excess return (sd 0.149, t -1.64). Step 5's mild group averages -0.027, so its result sits on the predicted side, but this sample of two coins is too small to separate a gradient from noise.
