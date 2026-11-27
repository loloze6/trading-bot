---
line: 7.g patterns
backtest: 067-02.b2_agitated-choppy-month-fall-continues_1d
idea tested: 067-02.b2_agitated-choppy-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4382 USD
---
## Findings
- **F1:** Inside the choppy agitated profile, the visible folds hold only 36 non-overlapping 7-day cases, and all four 30-day-return quartiles are followed by negative excess 7-day returns, with mean z between -0.31 and -0.86 and t from -1.9 to -2.5. This includes the quartile with 30-day returns from -2 % to +91 %, so the fall seen in the profile does not grow with the depth of the month's fall. This matches the step 5 slope t of 1.01 on 215 cases.
- **F2:** Across all bars, the 30-day return points the following week only weakly and not in a graded way. The Spearman rho is 0.068 (p 0.033, 981 cases). The excess 7-day move is -2.5 % (t -2.58) in the second-lowest quintile and +3.1 % (t 2.68) in the second-highest, but flat in both extreme quintiles (t -0.81 and +0.80). Scaling the 30-day return by its volatility gives the same hump shape (t -1.55, -1.82, -0.79, +2.33, +1.30).
- **F3:** Closes in the top fifth of the day's range appear to be followed by a 7-day excess of +4.2 % (z 0.27, t 4.14). The close-position slope on the 7-day move, however, is t 1.84 on grid offset 0 and between -1.35 and +0.90 on the other six offsets of the same bars, so the pattern depends on the grid's placement and is not a property of the bars.
- **F4:** The close position does lean towards next-day reversal on every offset: day-clustered slope t of -2.44, -1.10, -0.48, -1.30, -1.88, -0.79 and -0.04, about 220 days each. The lowest-close quintile is followed by +1.0 % the next day (t 2.21, 292 cases). The profile map already holds this effect many times over: wide low-close rebounds, and 79 long strategies acting in every profile.
- **F5:** The widest-range fifth of days is followed by a 7-day excess of -2.9 % (t -2.81, 278 cases). The range scaled by the coin's 30-day volatility has no slope (t -0.45, 981 cases), so the raw-range effect only reflects high-volatility periods.
- **F6:** The weekday the 7-day grid starts on gives t +4.70 for Fridays and -3.13 for Sundays. A window's grid starts on the same weekday throughout, so these groups are windows under another name, not a calendar effect.
- **F7:** The book is in a position on 9 % of coin-days, with 715 active days. Its daily returns run against the coin's (correlation -0.74). Its ten best days sum to +128 % against a +22 % total. Only w16 shows a mean daily return above 0.0002 (+0.11 %), and the trades lose a median of 2.4 % to 4.7 % net in every tercile of entry forecast.

## Ideas
- No ideas: Across about fifteen angles (the 30-day, 7-day and 1-day returns, range, close position, volatility, the 60-day trend, weekday, windows, coins and the book's extreme days), no pattern held across grid offsets and windows strongly enough to count after so many looks. The one consistent effect, the next-day reversal of the close position, is already held in the profile map.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
