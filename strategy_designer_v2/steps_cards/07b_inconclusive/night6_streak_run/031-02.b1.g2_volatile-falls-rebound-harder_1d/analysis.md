---
line: 7.b inconclusive
backtest: 031-02.b1.g2_volatile-falls-rebound-harder_1d
idea tested: 031-02.b1.g2_volatile-falls-rebound-harder
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3473 USD
---
## Findings
- **F1:** The tested measure lands on the predicted side but short of the bar: slope t 1.47 on 8,650 grid points over 1,509 days; the unusual move is only +0.09 % per case (t 0.53, 1,681 days), a strength of 0.014, while one trade costs 0.19 %.
- **F2:** The volatility half of the idea points the wrong way. Among 2-day falls, those in each coin's low-volatility half earn a mean excess of +0.19 % with a fall-size t of 1.98. Those in the high-volatility half earn -0.07 % with t 1.05. Step 5's own high-minus-low difference is also negative, -0.08 %.
- **F3:** The fall measured in units of the coin's 60-day volatility predicts the rebound better than the fall times volatility. On fall days over 2 days, its t is 2.01 against 0.93 for fall × volatility. On all grid points its t is 1.68 against 0.91.
- **F4:** The rebound grows steadily with the volatility-scaled fall. By quintile of fall/volatility on 2-day fall cases (about 560 each), the mean excess return is -0.36 %, -0.54 %, -0.03 %, +0.51 % and +0.71 %. The top quintile's unusual move is about 3.7 times the 0.19 % cost of a trade, and the top quartile's strength is 0.083.
- **F5:** The effect is mixed across coins. With the volatility-scaled fall over 2 days, XMR shows t 2.17, XRP 2.11, LTC 1.57 and ZEC 1.43, against BTC -0.14 and ETH 0.11. Every year from 2019 to 2025 has a positive t (0.07 to 1.50); 2018 alone is at -0.10.
- **F6:** The rebound shows most at the shortest horizon. On all grid points, the raw fall has a t of 2.79 over 1 day (11,620 points, 1,938 days), 1.38 over 2 days and 1.87 over 3 days. By 5 days it has faded: on fall days its t is 0.37 there.
- **F7:** Up days do not mirror this: a rise scaled by volatility gives a t of 0.59 on the next 2 days' excess return, so the effect is on the falling side only.

## Ideas
- `031-02.b1.g2.b1_volatile-falls-more-coins` (from F1): The larger a coin's percentage fall on its latest day, the more it rises over the next 2 days, and this rebound is larger the higher the coin's volatility over the past 60 days.
- `031-02.b1.g2.b2_unusually-large-falls-rebound` (from F2, F3, F4, F5, F7): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 2 days.
- `031-02.b1.g2.b3_next-day-rebound-after-falls` (from F3, F6): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
