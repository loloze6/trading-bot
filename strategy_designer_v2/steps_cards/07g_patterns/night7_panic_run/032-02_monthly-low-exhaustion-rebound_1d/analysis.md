---
line: 7.g patterns
backtest: 032-02_monthly-low-exhaustion-rebound_1d
idea tested: 032-02_monthly-low-exhaustion-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3952 USD
---
## Findings
- **F1:** In the falling-agitated profile, a close below the prior 30-day closing low is followed by a 3-day move of +5.47 % (t 3.77, 32 grid cases), against +0.44 % on the profile's other days (t 0.86, 386 cases); the effect sits entirely in the late windows (w13–w18: unusual move +5.27 %, t 2.41 with the cases of one day together, 30 cases on 13 days; the early windows hold only 2 cases).
- **F2:** Outside the profile, the same fresh 30-day low is followed by −0.90 % over 3 days (t −0.81, 86 cases), and its deepest tercile by −3.71 % (t −1.61), so the rebound after a monthly low is specific to the falling-agitated profile.
- **F3:** Inside the falling-agitated profile, the 3-day move falls as the day's own move (in units of its 30-day swing) rises, by quintile from the largest fall to the largest rise: +3.71 % (t 3.37, 82 cases), +0.01 %, +2.14 % (t 2.52), −0.49 %, −1.83 % (t −1.03); on profile days that are not a new low, the top quartile of the day's move is followed by an unusual move of −3.41 % (t −2.37, 86 cases on 42 days); outside the profile the same quintiles are flat (+0.67 % to +0.11 %, all t under 1.4).
- **F4:** Across all bars, the coin's 5-day return in units of its 30-day swing grades the next 3 days' unusual move monotonically by quintile (−0.76 %, −0.43 %, −0.10 %, +0.27 %, +1.27 %; top quintile t 1.83, 164 days); outside the profile its top quintile is +1.54 % (t 2.27, 150 days); the correlation is positive on all six coins (0.02 to 0.12); within the profile the pattern is absent (top quintile −0.96 %, t −0.38); the 10-day version is the same and slightly weaker (top quintile +1.11 %, t 1.48).
- **F5:** The tested idea's size is not the book's problem: the total move per case, +2.59 %, is 13.4 times the 0.19 % cost of a trade. The book fails because it is in a position on only 13 % of the coins' days (Sharpe 0.35, 0.22 below holding; Calmar 0.147). Its trades earn more when the entry forecast is low and the hold is long (forecast terciles: +7.5 % and +9.2 % net, held 589 and 265 hours) than when the forecast is high (+3.8 %, 121 hours).
- **F6:** Weekday is not a finding given the many angles looked at: Thursday and Friday carry +0.41 % and +0.38 % one-day unusual moves (t 1.34 and 1.52), and the combined Thursday–Friday edge holds a t of 1.97 in the early windows but 0.94 in the late ones.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-02.g1_agitated-fall-one-day-reversal` (from F3, F1, F2): In a falling, agitated market, the larger a coin's one-day fall relative to its usual daily swing over the past 30 days, the larger its rebound over the next 3 days, and the larger its one-day rise, the larger its fall over the next 3 days.
- `032-02.g2_swing-scaled-weekly-momentum` (from F4): The larger a coin's 5-day return relative to its usual daily swing over the past 30 days, the more the coin moves in that same direction over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
