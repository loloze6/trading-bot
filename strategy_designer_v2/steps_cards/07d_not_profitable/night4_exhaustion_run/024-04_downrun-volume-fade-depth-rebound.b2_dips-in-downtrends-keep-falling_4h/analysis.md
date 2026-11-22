---
line: 7.d not profitable
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3583 USD
---
## Findings
- **F1:** The book loses because it is short a coin that rises on average: its mean daily return of -0.000227 splits into -0.000694 from the market's own rise and +0.000467 from timing, and it is short on 63 % of coin-days with a mean position of -0.94.
- **F2:** Per case, the move the bet captures does not cover a trade: the unusual move is +0.20 % (strength 0.025, t 1.53, 3417 cases) against a cost of 0.19 %. After the normal drift of -0.41 % on the short side, the total move is -0.21 %. The 3486 short trades lose -1.91 % gross and -2.01 % net, with 30 % winners.
- **F3:** The idea's grading by the 30-day return runs the wrong way at the deep end. Cases with a 30-day return below -25 % have strength -0.107 (t -2.01, 496 cases, -0.82 % unusual move). That is a rebound against the short. Cases between -25 % and -2.4 % have strength +0.07 to +0.10 (t 1.76 to 2.44).
- **F4:** On the non-overlapping 18-bar grid of all bars, a 30-day return below -25 % is followed by a mean 3-day rise of +1.07 % (t 2.53, 511 cases). A 30-day return between -25 % and -15 % is followed by -0.76 % (t -2.17, 466 cases).
- **F5:** The forecast's size carries no information. The strongest forecast bucket (-20 to -14.3, 2048 cases) has strength 0.014 (t 0.65). The largest streak losses (2.4 to 26 usual moves) have strength 0.007 (t 0.18). The cube transform therefore puts most of the book's size where there is no edge.
- **F6:** The book keeps its shorts well past the 3-day horizon, with a mean trade length of 327 hours.
- **F7:** The losses are spread across years and coins rather than resting on one period. Mean book daily return is negative in 2019–2021 and 2023–2024 (for example -0.0020 in 2023). The strength by coin ranges from -0.031 (XMR) to +0.062 (BTC).

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.d1_deep-monthly-fall-rebounds` (from F3, F4, F1, F2): After a fall over the past 30 days that is large against the coin's usual 30-day move, the coin rises over the next three days. The deeper the 30-day fall against that usual move, the larger the rise.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.d2_dips-keep-falling-moderate-downtrends` (from F3, F4, F5, F6): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin keeps falling over the next three days. This holds only while the coin's 30-day return is negative and its 30-day fall is small against its usual 30-day move. Within that, the closer the 30-day fall comes to the coin's usual 30-day move, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
