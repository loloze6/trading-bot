---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past day against its typical one-day move over the past 30 days, the more it rises over the next three days.
Consequence: A sharp one-day drop is a reason to buy for a three-day rebound rather than to sell.
Why:
- F4: A sharp one-day fall is followed by a rise. After a 1-day fall, scaled by the coin's mean absolute 1-day move over 30 days, the larger the fall, the larger the 3-day return above drift (slope 0.0058, t 3.50, 2373 cases). The lowest quintile of 1-day return ends +0.74 % above drift (t 2.57, 1116 cases). The slope is positive in five of six coins, but it holds only in w13-24 (t 3.78) and not in w1-12 (t 0.50).
- F5: Large 1-day moves are followed by gains on both sides, a U-shape. Scaled 1-day rises are followed by gains too (slope 0.0057, t 3.65, 2479 cases), and the size of the 3-day scaled move predicts the excess return (slope 0.0030, t 2.46). The middle quintiles of the 3-day scaled return lose -0.27 % to -0.50 % above drift, while the top quintile gains +0.74 % (t 2.51).
