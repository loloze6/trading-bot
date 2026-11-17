---
line: 7.b inconclusive
backtest: 013-04_heavy-volume-below-high-breakout_1d
idea tested: 013-04_heavy-volume-below-high-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1720 USD
---
## Findings
- **F1:** The tested measure lands on the predicted side but just short of the bar: over 50 de-duplicated breakout events (25 per half), the top-forecast half beats the bottom half by +0.273 in 30-day excess return, Welch t 1.99, and the quartile means climb in order: -0.060, -0.028, +0.169, +0.283.
- **F2:** The gap rests on a few large top-half events rather than a broad shift. The top half's spread is far wider (std 0.644 vs 0.239, max +2.31), its median is only +0.047 vs -0.032, and dropping its single largest event cuts the Welch t to 1.69. A rank test shows the same weakness: Mann-Whitney p 0.23, Spearman 0.17.
- **F3:** The sign holds at every horizon, but the 30-day plan horizon is where it shows most. The top-minus-bottom difference is +0.062 at 10 days (t 0.75), +0.134 at 20 days (t 1.18), +0.273 at 30 days (t 1.99) and +0.227 at 60 days (t 1.01, only 13 top events).
- **F4:** Within coins, the top half beats the bottom half in 5 of 6 coins: BTC 0.145 vs 0.031, ETH 0.112 vs 0.090, LTC -0.056 vs -0.200, XRP 0.403 vs -0.194, ZEC 0.712 vs -0.287. The only exception is XMR, with a single top event. Each coin has only 5 to 16 events, so the test is limited by too few breakouts, and more coins would add more.

## Ideas
- `013-04_heavy-volume-below-high-breakout.b1_volume-before-breakout-more-coins` (from F1, F2, F4): When a coin closes above its prior 52-week high, the heavier its volume over the preceding 10 days, relative to its own 90-day average, the larger its return over the next 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
