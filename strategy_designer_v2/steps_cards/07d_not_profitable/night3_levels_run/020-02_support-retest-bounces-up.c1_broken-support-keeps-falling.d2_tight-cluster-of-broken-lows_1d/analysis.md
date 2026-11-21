---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3553 USD
---
## Findings
- **F1:** The book lost because it was short against rising coins. Its mean position was -0.48 and it was short 75 % of bars. Holding short against the coins' own rise cost -0.057 % per bar, while its timing earned +0.030 %, for a net of -0.028 % per bar. That net was negative in 5 of 8 years and on all 6 coins.
- **F2:** Even where the short signal was strongest, the coin barely fell, so a short on this idea cannot cover the 0.19 % cost of a trade.
- **F3:** The forecast does rank what follows, but on the long side. Bars with no past-90-day swing low above the close rose most, +1.37 % over 5 days (+0.79 % above the coin's drift, 1060 cases). From there the rise shrinks steadily as the short grows: +0.81 %, +0.10 %, -0.20 %.
- **F4:** Once the standardisation is removed, the raw count-times-nearness measure grades the move only weakly. Its slope on the 5-day excess return has t -1.14 (2359 cases). Its quartiles give +1.13 %, -0.32 %, +0.24 % and -0.10 % raw.
- **F5:** Among bars with a past low above the close, the coin's past 60-day return shapes the 5-day move:
- **F6:** Holding longer does not rescue the short. In the largest third of short sizes, the excess return deepens with the horizon: -0.80 % at 5 days, -1.59 % at 10 days, -2.05 % at 20 days. The raw return stays near zero, though: -0.20 %, -0.40 % and +0.48 %. The coin's drift eats the effect at every horizon.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows.d1_close-above-all-past-lows` (from F1, F3, F2): When a coin's daily close sits above every price where it turned up in the past 90 days, it tends to rise over the next 5 days. The farther the close sits above the highest of those past turning-up lows, the larger the rise.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows.d2_broken-support-mild-decline` (from F5, F2, F4): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, only while its 60-day decline is still mild. The more such past turning-up lows lie within a few percent above the close, the nearer the closest of them, and the smaller the coin's 60-day loss, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
