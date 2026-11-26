---
line: 7.g patterns
backtest: 031-04.a1_yearly-low-break-all-coins_1d
idea tested: 031-04.a1_yearly-low-break-all-coins
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3529 USD
---
## Findings
- **F1:** The one pattern that stands out is the day's range against the coin's recent volatility (the high-low range over the close, divided by the 20-day standard deviation of daily returns). Over the 10-day grid, its top fifth (mean 3.10) was followed by an unusual 10-day move of +1.73 % (510 cases, 137 days). Its bottom fifth (mean 0.75) was followed by -0.99 % (512 cases, 138 days). The difference of +2.72 % has a Welch t of 2.81; that t does not group cases by day, and about a dozen angles were looked at, so it is only just past chance.
- **F2:** Two other angles point the same way, toward a rebound after a wide or weak day. Closes near the day's low (bottom fifth of close location, mean 0.13) were followed by +0.49 %, and closes near the high (mean 0.92) by -1.37 % (top minus bottom -1.85 %, t -2.00). The day with the largest 1-day fall (bottom fifth of the 1-day return, mean -6.5 %) was followed by +2.68 % (t 1.96, 566 cases on 125 days).
- **F3:** The tested break below the yearly low has a large size but too few cases: +6.84 % unusual move per case over 10 days (0.42 of a usual move, t 1.84 on 16 days, 18 cases). That is about 31 times the 0.22 % cost of a trade. The deeper-break half did worse than the shallower half (-2.74 %), so the forecast's grading by depth is not supported.
- **F4:** Distance from the 30-day and 60-day lows showed no graded pattern. The bottom fifths (closest to the low) were followed by -0.05 % and +0.14 %, the middle fifths were negative (lo30 q2 -2.48 %, t -2.26), and the top fifths +2.09 % and +2.05 % (t 1.44 and 1.30). The year-by-year difference between bottom and top fifths flipped sign in 4 of 8 years.
- **F5:** No other angle stands out once days are counted as one piece of evidence:

## Ideas
- `031-04.a1.g1_wide-range-day-rebound` (from F1, F2): The wider a coin's daily high-low range compared with its own recent daily volatility, the more the coin rises over the next 10 days, most of all when that day closes near its low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
