---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 28-day rise or fall, the further its price continues the same way over the next 10 days, and more so the closer its close sits to its highest close of the last 60 days. The strength of the situation is the size of the 28-day return itself, not how it compares with the coin's own recent 28-day returns.
Consequence: A trader would size a 10-day momentum bet by the plain size of the 28-day move scaled by nearness to the 60-day high, and would not rescale it against the coin's last two months of signals, which removed the effect here.
Why:
- F1: The idea as worded is present, but the test's forecast hid it. The raw situation (the 28-day return times nearness to the 60-day high, as recorded on the bars) predicts the 10-day excess return with slope t +3.42 on 1,259 non-overlapping cases. The forecast after standardising against its own past 60 values reaches only t +0.56 on the same cases (+1.09 on all 1,691), and it correlates only 0.33 with the raw value.
- F2: The effect is graded in the raw value. By raw quintile, the mean 10-day excess return runs -0.58 %, -1.28 %, -0.64 %, +1.19 %, +1.59 % (252 cases each). By forecast quintile it shows no order: +0.37 %, -1.33 %, -0.26 %, +0.91 %, +0.59 %.
- F3: Nearness to the high is what carries the momentum. With the 28-day return alone and the near-high product in one regression, the product keeps t +2.10 and the 28-day return falls to t +0.98 (1,259 cases). Split at the median distance from the 60-day high, the 28-day return's slope is t +2.39 near the high (630 cases) and t -0.18 far from it (629 cases).
- F5: The plan's horizon is the right one. At 20 days the raw product's t of +2.22 falls to +0.95 once its extremes are clipped (539 cases), and the forecast's t is 0.00 (827 cases). At 10 days the clipped product keeps t +2.49.
