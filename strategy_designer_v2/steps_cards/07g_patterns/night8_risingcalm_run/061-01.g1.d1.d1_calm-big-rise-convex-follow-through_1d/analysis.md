---
line: 7.g patterns
backtest: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d
idea tested: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5272 USD
---
## Findings
- **F1:** In calm markets (30-day swing at or below the coin's median), the 5-day excess return after a day rises as the day's move in swing units grows, in both directions. Days of +1 to +2 usual swings are followed by +2.45 % (t 2.61, 64 cases). Days above +2 swings are followed by +7.81 % (t 1.94, 23 cases). Days of −1 to −2 swings are followed by −1.70 % (t −1.65, 62 cases), and days below −2 by −2.49 % (t −1.04, 12 cases).
- **F2:** The same big days carry little follow-through in agitated markets. Days of +1 to +2 swings are followed by +1.01 % over 5 days (t 0.44, 48 cases), and days of −1 to −2 swings by −0.50 % (t −0.39, 77 cases).
- **F3:** Across all profiles, the 5-day excess return climbs steadily with the day's move, from −2.74 % below −2 swings to +5.97 % above +2 swings (t 2.21, 37 cases); the middle bins in between are −1.04 %, −0.47 %, −0.01 %, +0.30 % and +1.83 %. This is the brief's continuation, but the tested choppy-calm, long-only book measured −0.20 % per case (t −0.32, 314 cases), against a cost of 0.19 % per trade.
- **F4:** Where a day closes inside its range sorts the next day's excess return in a straight line across five bins. Days closing in the top fifth of the range are followed by −0.37 % (t −2.87, 1,789 days); the next bins are −0.21 % (t −1.73) and −0.08 %; days closing in the bottom fifth are followed by +0.63 % (t 3.93, 1,199 days). The t's here count each coin-day separately, not grouped by day.
- **F5:** The largest next-day reversal follows big down days in agitated markets: +3.61 % after days below −2 swings (t 4.57, 81 cases) and +1.12 % after days of −1 to −2 swings (t 2.84, 301 cases). The same bins in calm markets give +0.40 % (t 0.76) and +0.17 % (t 0.66). The profile map already holds this effect in about a dozen agitated, long rebound books.
- **F6:** Other angles did not stand out once the number of tests is counted:

## Ideas
- `061-01.g1.d1.d1.g1_calm-big-day-both-way-continuation` (from F1, F2, F3): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further the coin keeps moving the same way over the next 5 days, upward after up days and downward after down days.
- `061-01.g1.d1.d1.g2_high-close-next-day-fade` (from F4): The nearer a coin's daily close sits to the day's high within its high-low range, the lower its return over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
