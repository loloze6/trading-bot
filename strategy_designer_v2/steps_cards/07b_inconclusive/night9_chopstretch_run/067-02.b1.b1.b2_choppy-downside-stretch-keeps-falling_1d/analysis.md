---
line: 7.b inconclusive
backtest: 067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling_1d
idea tested: 067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2028 USD
---
## Findings
- **F1:** In folds B and C, the tested measure points the way the idea predicts. Short-direction unusual 5-day moves in choppy, below-average cases average +2.68 % (t 2.16, 145 cases on 91 days), and the full-data verdict is +1.03 % with t 1.70 on 405 cases. The effect is on the idea's side but short of the bar.
- **F2:** The effect is present on every one of the six coins and only its strength varies. The 5-day short-direction unusual move is positive on all six: BTC +3.19 % (t 1.84), ETH +2.22 % (t 1.25), LTC +1.70 % (t 0.70), XMR +3.28 % (t 1.70), XRP +3.52 % (t 1.91) and ZEC +1.02 % (t 0.45). Each coin has only 16 to 34 cases, so it is a thin-sample problem, not a coin-specific effect.
- **F3:** The effect is drowned by large window-to-window swings. Window means run from −8.17 % (w11, t −3.60, 6 cases) to +31.13 % (w16, t 5.14, 5 cases), and by year from +5.29 % in 2018 (t 3.09, 41 cases) to −0.56 % in 2021 (t −0.23, 28 cases). Each window and year has only 4 to 41 cases, so a few market episodes decide the sign.
- **F4:** The plan's 5-day horizon is where the effect shows. The short-direction unusual move is +0.33 % at 1 day (t 1.11), +0.75 % at 3 days (t 1.01), +2.68 % at 5 days (t 2.16) and +3.32 % at 10 days (t 1.35), then −1.59 % at 20 days (t −0.34, 35 cases).
- **F5:** The grading is weak and not monotonic, but leans the idea's way. The deepest forecast tercile averages +4.79 % (t 1.65, 48 cases), the middle +1.00 % (t 0.60) and the shallowest +2.26 % (t 1.96). The Spearman correlation of the raw stretch with the 5-day unusual move in choppy bars is 0.12 (p 0.052).
- **F6:** The carry is found only below the average and only in choppy markets. Above the average in choppy markets, the long-direction unusual 5-day move is +0.003 % (t 0.00, 121 cases). Below the average outside choppy markets, the short-direction move is only +1.03 % (t 1.14, 625 cases) against +2.68 % inside them.
- **F7:** The book cannot pay as it stands. The unusual move is +0.60 % per case, 3.1 times the 0.19 % cost of a trade. But the coin's normal drift in the short direction is −0.57 %, so the total move is only +0.03 %, 0.1 times the cost. The question here is whether the idea is real, and only more cases answer it.

## Ideas
- `067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins` (from F1, F2, F3): In a choppy market, the further a coin's close stands below its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
