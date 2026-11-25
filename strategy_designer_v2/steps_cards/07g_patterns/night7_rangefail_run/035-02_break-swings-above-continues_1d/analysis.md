---
line: 7.g patterns
backtest: 035-02_break-swings-above-continues_1d
idea tested: 035-02_break-swings-above-continues
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3988 USD
---
## Findings
- **F1:** Below the 20-day high, the 5-day excess return over the coin's mean follows no clean grade by distance in daily swings. It is −1.17 % (t −1.81, 730 cases, 201 days) at 3 to 6 swings below, +1.34 % (t 1.56, 528 cases) at 1 to 3 below, +1.58 % (t 1.09, 126 cases) at 0 to 1 below, and −0.46 % (t −0.28, 469 cases) at 6 to 10 below. No band below the high reaches |t| 2.
- **F2:** Above the high, the breakout cases carry the confirmed effect, but each band is thin. The mean excess is +3.66 % (t 1.90, 51 cases) at 0 to 1 swings above, +17.96 % (t 1.10, 26 cases) at 1 to 2, and +9.91 % (t 1.22, 16 cases) at more than 2; all breakouts together give +8.74 % (t 1.75, 93 cases, 49 days) on folds B and C.
- **F3:** The raw next-day return looks strong on Thursdays and Fridays (t 4.04 and 5.00), but this is the coins' rise in these years. Measured as the excess over each coin's mean with the cases of one day together, no weekday passes |t| 1.47, and the sign of each weekday changes from year to year (Wednesday t −3.16 in 2019, +0.74 in 2021).
- **F4:** A large last-day move without a breakout predicts little. Up days of 1.5 to 3 swings give +2.16 % (t 1.39, 96 cases), down days beyond −1.5 swings give +1.39 % (t 0.86, 223 cases), and the 30-day-to-60-day volatility ratio quartiles range from −1.31 % to +1.65 %, all with |t| under 1.
- **F5:** Distance from the 20-day low in swings rises from −1.88 % (t −1.73, 1 to 3 swings above the low) to +2.28 % (t 1.41, more than 10 swings above). This is the same information as the distance from the high, read from the other side, and it is not significant.
- **F6:** A few large moves carry the book. Its 30 best days sum to +1.65, against a total of +1.42 over 1,449 days, and its 30 worst days to −1.23. Trades longer than 7 days, 126 of 636, carry 3,751 of the 5,380 summed net percent, while the median trade is +1.37 % with a 59 % win rate.
- **F7:** Inside breakouts, the 60-day trend groups are tiny: falling 5 cases, choppy 9, rising 43 (+5.65 %, t 1.41). They cannot show the effect is limited to, or absent from, any profile.

## Ideas
- No ideas: I looked at about 60 groupings: distance from the high and from the low, the last day's move, the volatility ratio, trend crossed with breakout, year, weekday, prior 5-day return, and trade duration, entry forecast and coin. No pattern outside the tested breakout effect reaches a day-clustered |t| of 2 in a graded way, so none stands out from chance across that many looks.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
