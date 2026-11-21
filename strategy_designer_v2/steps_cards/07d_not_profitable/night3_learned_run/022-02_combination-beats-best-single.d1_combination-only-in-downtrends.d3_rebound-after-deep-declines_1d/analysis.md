---
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3553 USD
---
## Findings
- **F1:** Inside the tested situation (90-day return below 0), the rebound exists only in the deepest declines. Below 60 % under the 90-day high, the 5-day excess return is +5.0 % (t 2.59, 67 cases, strength 0.44). From 46 to 60 % below it is +0.8 % (t 1.00, 208 cases). At every shallower depth, from 46 % below up to the high, it is negative, about -0.6 % to -1.0 % (for example t -2.02 on 425 cases from 20 to 35 % below). The relation is not linear, which is why the pooled linear slope has a t of only 0.79.
- **F2:** The book holds about the same position at every depth, so it carries the losing middle depths at full size. Its mean allocation is 0.46 below 60 %, 0.51 from 46 to 60 %, and 0.58 to 0.63 from 46 % below up to the high, because vol-target sizing undoes the depth gradient. Summed per-bar gains are +2.29 and +1.42 in the two deepest bins and -0.37, -0.07 and -0.09 from 35 % below up to the high.
- **F3:** The gain is lost to holding mostly because the book is out when the coin's 90-day return is positive. Those bars earn +0.10 % excess per 5 days on 1767 grid cases, against -0.10 % on 1652 cases in the tested regime. Near the 90-day high (within 10 %) they earn +1.05 % excess (t 2.56, 775 cases; total move +1.63 %, about 8.6 times the 0.19 % cost). The book gives up this continuation and trails the coin's mean daily return in 21 of 24 windows.
- **F4:** The deep rebound outlasts the 5-day horizon. Below 60 % under the high, the 10-day forward return is +10.8 %, against +5.6 % over 5 days. From 46 to 60 % below it is +2.3 %, against +1.4 %.
- **F5:** The deep-decline rebound is spread over coins but not over every year. Below 46 % under the high, every coin's mean 5-day excess is positive (+0.7 % to +4.4 %), and 73 % of coin-windows are positive. Yet 2018 holds 130 of its 275 cases with a mean of -0.15 %, while 2020 to 2022 carry it (+9.5 %, +3.4 %, +2.2 %).
- **F6:** The tested idea's size at the tested depths is below the cost. Its unusual move is -0.44 % per case (strength -0.050), and its total move of +0.13 % is 0.7 times the 0.19 % round trip. Only the deepest cases (F1) have a move many times the cost.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.d1_convex-rebound-deepest-declines` (from F1, F2, F4, F5, F6): While a coin's 90-day return is negative, the further it stands below its 90-day high, the higher its return over the next 10 days, the rise growing faster than the depth itself, so that most of the rebound comes from the deepest declines.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.d2_uptrend-nearness-to-highs` (from F3, F6): While a coin's 90-day return is positive, the closer its close stands to its 90-day high, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
