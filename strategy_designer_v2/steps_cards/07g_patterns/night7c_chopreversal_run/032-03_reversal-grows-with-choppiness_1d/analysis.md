---
line: 7.g patterns
backtest: 032-03_reversal-grows-with-choppiness_1d
idea tested: 032-03_reversal-grows-with-choppiness
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3898 USD
---
## Findings
- **F1:** Large down days are followed by a next-day rebound, and only when volatility has risen. Pooled over 7,249 days, the slope of the next-day excess return (scaled by the 30-day daily standard deviation) on the size of a down day (also scaled) is -0.107 (t -2.02, day-clustered). The slope is -0.268 (t -3.44, 1,457 days) when 30-day volatility is in the upper third against 90-day volatility, -0.098 (t -1.17) in the middle third and +0.148 (t 1.45) in the lower third.
- **F2:** That next-day rebound after down days points the same way across all windows and coins. The slope is negative in all 12 windows (w10 -0.48 with t -4.26, w18 -0.29 with t -1.68) and in all 6 coins (XMR -0.18 with t -3.38, ZEC -0.10 with t -1.75, XRP -0.12 with t -1.77, BTC -0.04 with t -0.62).
- **F3:** The largest down days give the clearest rebound. In the bottom quintile of the day's move scaled by 30-day swings, the next-day excess return is +0.73 % (t 2.50, 1,450 cases over 431 days). The second quintile gives +0.04 % (t 0.14) and the top quintile -0.14 % (t -0.59).
- **F4:** Over the week, the tested reversal points the wrong way: the past 7-day move tends to continue, mostly when volatility is calm.
- **F5:** The book loses most where its positions are largest. When the absolute position is in the largest third, the book's mean daily return is -0.29 %, against +0.04 % and +0.01 % in the middle and smallest thirds. This matches the contrarian bet being wrong when it is sized biggest.
- **F6:** The weekday effects do not stand out once same-day cases are taken together. The next-day excess is +0.47 % after Thursday closes (t 1.50) and +0.39 % after Friday closes (t 1.55). The Thursday and Friday pooled excess changes sign across windows (w18 -0.76 %, w11 +1.96 %), so it gives no idea.

## Ideas
- `032-03.g1_next-day-rebound-after-shocks` (from F1, F2, F3): After a down day, a coin's next-day return is higher the larger that day's fall is against its usual daily swing over the past 30 days. This rebound is strongest when its 30-day volatility is high compared with its 90-day volatility.
- `032-03.g2_calm-regime-weekly-continuation` (from F4, F5): When a coin's 30-day volatility is low compared with its 90-day volatility, its 7-day move scaled by its usual daily swing over the past 30 days is followed by a move the same way over the next 7 days. The larger the scaled move, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
