---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4201 USD
---
## Findings
- **F1:** Over 24 hours, a coin's past 24-hour move is partly reversed when its last 24 hours were volatile, and the reversal grows with that volatility. In the top quintile of past-24-hour hourly volatility, the slope of the next 24-hour standardised return on the past one is -0.125 (t -9.18, 3422 non-overlapping cases), with an unusual move against the past move of 0.56 % per case (strength 0.12). The next quintile down gives a slope of -0.036 (t -1.90), and the three lower quintiles give slopes between +0.010 and +0.058.
- **F2:** Inside that top volatility quintile, the reversal grows with the size of the past move. The unusual move against it is -0.13 % (t -0.64), 0.42 % (t 2.05) and 1.40 % (t 5.66) for the small, middle and large terciles of the absolute past move (about 1140 cases each). The large tercile is about 7 times the 0.19 % cost of a trade.
- **F3:** The high-volatility 24-hour reversal holds on every coin, with slopes from -0.072 (XRP, t -2.77) to -0.156 (XMR, t -5.81), and in 6 of 8 years with t at or beyond -2.5. It weakens in 2022 (t -1.16) and in 2024 (t -0.13).
- **F4:** The reversal is specific to the 24-hour horizon. In the top volatility quintile, the slope is -0.001 (t -0.11) over 12 hours and -0.031 (t -1.60) over 48 hours. Volatility relative to the past 7 days grades it less than the absolute level does: slope -0.106 (t -8.70) in the top relative-volatility quintile against -0.089 (t -3.36) in the bottom.
- **F5:** The tested weekend effect is not there. The weekend 48-hour move against the next 48 hours has a slope of -0.022 (t -0.82, n 2387), and the midweek move gives +0.015 (t 0.77, n 2399). Against the idea, the heaviest-volume weekend tercile shows continuation (-0.87 % against the move, t -2.72), while the thinnest shows 0.41 % reversal (t 1.72).
- **F6:** The hours starting 20:00 and 21:00 UTC rise on average, by 0.055 % (t 6.75) and 0.044 % (t 5.66) over about 17,400 hours each, the strongest of the 24 hours. The two-hour return from 19:00 to 21:00 is 0.13 % (t 4.55) in the top volatility tercile against 0.026 % (t 2.51) in the bottom one. It is positive for every coin and in 6 of 8 years, but stays below the 0.19 % cost of a trade.
- **F7:** The book's worst 1 % of days lose 7.5 % on average while the coins rise 1.06 % on those days. Its losses come from leaning against weekend moves that went on rising, as F5 shows.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.g1_volatile-day-moves-reverse` (from F1, F2, F3, F4): A coin's 24-hour return is partly reversed over the next 24 hours, and the reversed share grows with the size of that return and with the coin's hourly volatility over the past 24 hours.
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.g2_evening-utc-hours-rise` (from F6): A coin tends to rise during the hours from 20:00 to 22:00 UTC, and the rise grows with the coin's hourly volatility over the past 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
