---
line: 7.c no effect
backtest: 064-01_falling-calm-up-day-fades_1d
idea tested: 064-01_falling-calm-up-day-fades
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3174 USD
---
## Findings
- **F1:** In falling calm markets, a one-day rise is not given back: on the non-overlapping 3-day grid, up days are followed by an unusual move of +0.71 % in the long direction (day-clustered t +0.69, 72 cases, 55 days), and the slope on the scaled rise is -0.010 (t -0.62), which matches step 5's short-side t of +0.45 and its size of -0.22 % per case in the short direction.
- **F2:** The market moves the other way, and it shows at 5 days, not at the plan's 3. After an up day the 5-day unusual move is +2.40 % long (day-clustered t +1.86, 43 cases, 34 days; total +2.89 %), and the slope on the scaled rise is +0.046 (t +1.48). At 2 and 4 days the mean is near zero or negative (-0.33 %, -0.90 %).
- **F3:** The 5-day follow-through is graded at the top. Up days above the median scaled rise are followed by +4.89 % unusual (day-clustered t +2.40, 21 cases, 18 days; total +5.30 %, about 16 times the 0.33 % cost of a trade). Up days below the median give +0.02 % (t 0.02, 22 cases).
- **F4:** The 5-day follow-through is positive on every coin: BTC +1.56 % (t 0.79, 13), DOGE +6.46 % (t 1.38, 7), XMR +1.64 % (t 1.03, 23). It is not spread evenly over time. By year it is carried by 2021 (+4.91 %, t 2.15, 16 cases) and 2018 (+1.61 %, 16), while 2019 is flat (-0.10 %, 11). By window, w17 gives +10.3 % (6 cases) while w8 and w12 are near 0 (+0.10 %, +0.96 %). The effect is thin and needs the check half to confirm it.
- **F5:** A larger 3-day rise is also followed by more rise. The unusual move is +1.67 % over 5 days (t 1.42, 41 cases) and +2.96 % over 7 days (t 1.53, 29 cases). No horizon shows a giveback: the 3-day mean in the short direction is negative at every horizon from 2 to 7 days.

## Ideas
- `064-01.c1_calm-decline-big-rise-follows-through` (from F1, F2, F3, F4): In a falling, calm market, the larger a coin's one-day rise measured in units of its own 30-day standard deviation of daily returns, the larger the further rise in its close over the next 5 days.
- `064-01.c2_calm-decline-bounce-extends-week` (from F5, F1): In a falling, calm market, the larger a coin's 3-day rise measured in units of its own 30-day standard deviation of daily returns, the larger the further rise in its close over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
