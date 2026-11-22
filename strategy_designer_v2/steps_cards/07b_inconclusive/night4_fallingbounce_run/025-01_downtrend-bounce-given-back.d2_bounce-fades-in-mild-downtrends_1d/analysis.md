---
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
idea tested: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3546 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but too small to show: the mean unusual 5-day move after the short bets is +0.23 % (t 0.78, 1,045 cases, 6 coins), only 0.026 of the coin's usual 5-day move of 10.6 %. My recount gives the same, +0.22 % (t 0.74, 1,045 cases).
- **F2:** The idea's grading by depth holds while its mean does not. Step 5's depth slope is positive (t 2.94). By depth quartile, the deepest-fall quarter of cases gives back nothing: its unusual 5-day move is −1.18 % (t −1.58, 263 cases). The other three quarters all fade: +0.92 % (t 1.78), +0.73 % (t 1.50) and +0.41 % (t 0.79, shallowest).
- **F3:** Over 10 days the fade in the three shallower quarters is larger: +2.21 % (t 2.75, 242 cases), +0.06 % (t 0.06) and +1.76 % (t 2.14, shallowest). The deepest quarter loses −1.75 % (t −1.78, 259 cases). Over all cases, the 10-day move is +0.55 % (t 1.21) against the plan's 5-day +0.22 % (t 0.74).
- **F4:** The effect is mixed across periods and coins, and the market's own moves drown it. By year, the 5-day move is positive in 2018 (+1.23 %, t 1.30), 2019 (+0.90 %, t 1.77), 2022 (+0.83 %, t 1.35) and 2025 (+1.94 %, t 2.94). It is strongly negative in the bull years 2020 (−2.90 %, t −2.84, 92 cases) and 2021 (−2.99 %, t −2.16, 70 cases). By coin, BTC, ETH, LTC and ZEC are each about +0.6 % to +1.0 % (t 0.9 to 1.2), while XRP is −1.40 % (t −1.57) and XMR −0.08 %.
- **F5:** The size of the bounce does not grade the outcome. By forecast-size quartile, the strongest bets give +0.13 % (t 0.20), against +0.29 %, +0.78 % and −0.33 % for the other three.
- **F6:** The book cannot pay at this size. Per case the unusual move (+0.23 %) is 1.2 times the 0.19 % cost of a trade. The total move is −0.37 %, −1.9 times the cost, because shorting works against the coins' normal drift of −0.59 % in the short's direction. The book's Sharpe is −0.40.

## Ideas
- `025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins` (from F1, F2): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the shallower the coin's 90-day fall, the larger the fall that follows.
- `025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b2_mild-downtrend-bounce-fades-slowly` (from F2, F3): In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 10 days, and the shallower the coin's 90-day fall, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
