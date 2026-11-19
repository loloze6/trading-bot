---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the absolute share of its 3-day summed absolute hourly moves that pointed up, the more it rises over the following 3 days. This share is taken on its own fixed scale, not relative to its recent values.
Consequence: A climb made of mostly same-direction hours is a reason to stay long for 3 days, and a choppy climb is a reason to step aside, whatever the climb's recent history of smoothness.
Why:
- F1: Among 3-day climbs, the raw 72-hour efficiency ratio (the share of summed absolute hourly moves that points up) predicts the next 3 days, while the recorded forecast does not. Pooled over 2865 non-overlapping up cases, the per-coin z-scored slope has t 3.43 for the raw ratio and t 1.41 for the recorded forecast, which is the same ratio standardised against its own past 72 values (correlation 0.72 with the raw ratio). The standardisation is where the idea's signal was lost.
- F2: The raw-ratio effect is graded and not a proxy for the size of the climb. The 72-hour forward excess return rises steadily across efficiency quintiles: -0.0044, -0.0025, +0.0013, +0.0033, +0.0113 (top quintile t 2.78, about 574 cases each). In a joint regression with the 3-day return, the ratio keeps t 2.48 while the 3-day return drops to t -0.31.
- F3: The F1 slope is positive in all 6 coins (t from 0.40 for XMR to 2.46 for ZEC) and in both halves of the windows (w1–w12 t 1.46, w13–w24 t 3.20).
