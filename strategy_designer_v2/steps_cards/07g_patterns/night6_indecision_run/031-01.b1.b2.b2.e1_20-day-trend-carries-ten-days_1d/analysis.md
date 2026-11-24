---
line: 7.g patterns
backtest: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d
idea tested: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3941 USD
---
## Findings
- **F1:** The tested idea has no unusual move. Over 10 days the scaled 20-day return's quintiles 0 to 3 all end slightly below the coin's drift (mean excess −0.31 %, −0.68 %, −0.60 %, −0.23 %, t between −0.86 and −0.25, about 280 grid cases each). Only the top quintile ends above it (+2.38 %, t 1.94, 281 cases, not clustered by day), so the slope's t of 2.55 rests on one quintile.
- **F2:** The book's gain comes from the market's own rise, carried by long holdings. Trades held over 23 days average +36.8 % net (768 trades), while trades held 12 days or less average −1.4 % and −3.6 % (843 and 766 trades). LTC's book earned −0.0014 % a day while LTC itself rose 0.067 % a day.
- **F3:** After a day whose volatility-scaled return is in the lowest fifth (mean z −1.36), the next day ends +0.39 % above the coin's drift (t 2.14 with each day's cases taken together, 2900 cases on 974 days). The middle fifths range from +0.02 % to −0.20 % (t from −1.65 to 0.16). The effect is gone by 3 days: +0.25 % excess, t 0.48 on 330 days.
- **F4:** A vol-scaled 3-day return shows weak continuation over 3 and 5 days: slopes +0.0028 (t 2.31, 4715 cases) and +0.0044 (t 2.23, 2843 cases), not clustered by day. The top fifth shows +0.57 % and +0.78 % excess, with day-clustered t of 1.36 and 1.13. Per coin the t runs from −0.64 (LTC) to 2.02 (XRP).
- **F5:** The brief's own situation does not show a move back. Run-signed 10-day excess after flat-bodied days is −0.47 % for narrow range (t −0.59, 219 cases), +3.15 % for mid range (t 2.22, 165 cases) and +1.25 % for wide range (t 0.91, 75 cases). Its sign is continuation, not reversal, and it is not graded by width.
- **F6:** Next-day returns by weekday are highest after Thursday and Friday bars: +0.37 % (t 3.89) and +0.42 % (t 5.23) over about 2480 coin-days each. These t's count the six coins' same-day returns as independent, so they are overstated, and the pattern is a calendar condition rather than a graded situation.

## Ideas
- No ideas: I looked at more than 25 angles: the forecast's quintiles, 5-, 20- and 60-day returns, volatility level and ratio, range width, body, close location, the brief's wide-flat days, years, weekdays, 1- to 5-day reversal and continuation, per-coin and per-trend splits, and trades by length and entry forecast. No pattern stands out enough to count. The best one, the one-day rebound after a large volatility-scaled fall (F3, +0.39 % against a 0.19 % trade cost), has a day-clustered t of only 2.14 and fades within three days. The others are under t 2 once same-day cases are taken together, or are calendar effects with overstated t's.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
