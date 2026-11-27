---
line: 7.c no effect
backtest: 032-02.b1_calm-fall-depth-more-coins_1d
idea tested: 032-02.b1_calm-fall-depth-more-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3657 USD
---
## Findings
- **F1:** In falling calm markets, a deeper fall below the 30-day closing high did not lead to a further fall. The slope of the excess return on depth runs the wrong way for the idea at every horizon: t 0.61 at 1 day (484 cases), 0.87 at 3 days (155 cases), 1.12 at 5 days (94 cases) and 1.26 at 10 days (47 cases). The verdict's size agrees: an unusual short-side move of -0.19 % per 3 days (t -0.47, 407 days), against a trade cost of 0.33 %.
- **F2:** The depth quartiles show the market rose most where the coin had fallen least. The shallowest quartile (mean depth -4.3 %) earned an excess +2.05 % over 3 days (t 2.00, 39 cases) and +2.87 % over 5 days (t 2.14, 24 cases). The deeper three quartiles, from -14 % to -33 %, sat between -1.3 % and +0.2 % with |t| ≤ 1.04, so the effect is a rebound near the high, not a continuation of deep falls.
- **F3:** Within the shallower half of depths, the effect is graded: the closer the close to its 30-day high, the larger the 5-day excess return (slope t 2.02, 47 cases). The shallowest quartile is positive in both halves of the data (w1-9: +1.6 %, t 0.74, 14 cases; w10-18: +2.3 %, t 2.27, 25 cases) and on all three coins at 3 days (BTC +1.6 %, DOGE +6.1 %, XMR +1.2 %).
- **F4:** The coin's rise above its lowest close of the past 30 days grades the next move upward in falling calm markets. The slope t is 1.32 at 1 day (484 cases), 2.01 at 3 days (155 cases) and 2.15 at 5 days (94 cases). The quartile with the largest rise (+23 % above the low) earned an excess +1.6 % over 3 days (t 1.59) and +3.2 % over 5 days (t 1.79).
- **F5:** Over 5 days, the gain per case near the high or far above the low is +2.9 % to +3.2 % excess (+3.3 % total). That is about ten times the 0.33 % trade cost, whereas the tested idea's own size was below that cost.
- **F6:** The 5-day return is not graded. Its most negative quartile (-12 %) fell a further -2.2 % over 3 days (t -1.34) and -4.8 % over 5 days (t -1.85). Its second-highest quartile (+1.7 %) rose +2.9 % (t 2.88), but its top quartile (+10.6 %) earned about 0 % (t -0.05).

## Ideas
- `032-02.b1.c1_calm-fall-rise-off-low` (from F4, F5): In a falling, calm market, the further a coin's close sits above its lowest close of the past 30 days, the more it rises over the next five days.
- `032-02.b1.c2_calm-fall-nearness-to-high` (from F2, F3, F5): In a falling, calm market, the closer a coin's close sits to its highest close of the past 30 days, the more it rises over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
