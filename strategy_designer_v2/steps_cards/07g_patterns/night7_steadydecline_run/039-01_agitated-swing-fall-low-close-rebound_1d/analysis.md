---
line: 7.g patterns
backtest: 039-01_agitated-swing-fall-low-close-rebound_1d
idea tested: 039-01_agitated-swing-fall-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4209 USD
---
## Findings
- **F1:** In agitated bars the next-day rise after a down day is concentrated in the largest falls against the coin's 30-day swing. Falls beyond 2 usual swings were followed by +4.75 % above the coin's mean (53 cases, t 4.37). With the cases of one day taken together, falls of 2 to 2.5 swings gave +3.22 % (17 days, t 2.61) and falls beyond 2.5 gave +6.12 % (13 days, t 1.55). Falls of 1 to 2 swings gave only +0.94 % to +1.20 % (t 1.1 to 1.5), and falls under 1 swing gave −0.04 % to +0.63 % (t under 1.7).
- **F2:** In the agitated product quintiles (fall × closeness to the low), quintiles 1 to 4 were followed by a flat +0.30 % to +0.53 % next day (t 0.8 to 1.3). The top quintile gave +1.55 % (289 cases, t 3.95), so the grading is steep at the top rather than linear.
- **F3:** The close location adds only on large falls. In agitated bars, falls beyond 1.5 swings closing near the low gave +2.83 % next day (115 cases, 57 days, t_day 2.38). The same falls closing mid or high gave +1.26 % (23 cases, t_day 1.18). Small falls (under 1 swing) gave +0.40 % closing near the low and +0.36 % closing mid or high (t_day 0.92 and 0.78).
- **F4:** Falls beyond 1.5 swings in agitated bars were followed by a similar rise in every year:
- **F5:** The rebound after the strongest cases lasts beyond one day. In the agitated top product quintile, the 2-day return on a non-overlapping grid was +2.46 % above the coin's 2-day mean (148 cases, t 3.25), against +1.55 % over one day. The 3-day return was +1.79 % (81 cases, t 1.65).
- **F6:** The effect is absent in calm bars. Calm down days showed no gradient by fall size, with the cases of one day taken together:
- **F7:** The book's result rests on a few days.

## Ideas
- `039-01.g1_extreme-agitated-fall-rebound` (from F1, F2, F3, F4, F7): In an agitated market, the larger a one-day fall measured in the coin's 30-day standard deviation of daily returns, the larger the rise over the next day. The rise grows faster than the fall, so most of it follows the falls that lie furthest beyond the usual swing and close near the day's low.
- `039-01.g2_agitated-low-close-two-day-rebound` (from F5, F2, F6): In an agitated market, the larger a one-day fall against the coin's 30-day standard deviation of daily returns and the nearer its close to the day's low, the larger the rise over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
