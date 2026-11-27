---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6666 USD
---
## Findings
- **F1:** The book is mostly a bet against the market: its daily return across coins has a correlation of -0.49 with the coins' mean daily return. On its best 2 % of days the coins fell 10.0 % on average, and on its worst 2 % they rose 7.6 %. This is why it trails holding even though the idea is real: in w11 the book averaged -0.011 % a day while the coins rose 1.93 % a day, and in w14 it made +0.31 % a day while the coins fell 0.43 % a day.
- **F2:** The tested situation shows clearly on the non-overlapping 5-day grid. High closes (close location at least 0.8) after a 5-day fall were followed by an unusual 5-day move of -3.55 % (t -3.66, 135 cases, cases not pooled by day). High closes after a 5-day rise were followed by +1.56 % (t 2.00, 375 cases).
- **F3:** The trades confirm the grading by depth. Mean net trade P&L rises steadily across quartiles of |entry forecast|: -2.34 %, -1.35 %, -0.31 %, +1.90 % (247 trades each). The average trade is still -0.52 % net, with a median of -1.34 % (988 trades).
- **F4:** Among all high-close bars, the next 5 days follow the coin's 20-day return, but only in a choppy market (60-day return between -10 % and +10 %). There the slope of the unusual 5-day move on the 20-day return is 0.309 (t 5.50 with cases of one day pooled, 44 cases on 29 days). In falling markets the slope is 0.074 (t 0.82, 86 cases) and in rising markets 0.042 (t 0.65, 118 cases). On bars without a high close it is -0.0005 (t -0.03, 1608 cases).
- **F5:** Among choppy high-close bars, those in the lowest third of 20-day return had an unusual 5-day move of -9.7 % (t -2.42, 11 cases on 11 days). The high-close cases in the lowest third of 20-day return across all trends fell 3.9 % (t -2.02, 136 cases, 44 days) and over 2 days fell 3.4 % (t -1.99).
- **F6:** Across all bars in a choppy market, the 20-day return scaled by the 20-day swing also leans toward continuation: slope 0.065 (t 2.65, 189 cases, 76 days). Its terciles go -5.9 % (t -1.87), -2.0 %, +8.7 % (t 1.33). The slope is 0.005 in falling markets (t 0.44) and 0.013 in rising ones (t 1.13). It is not stable by year: -0.030 in 2018, +0.088 in 2021.
- **F7:** I looked at weekday, the previous day's return, range expansion and relative volatility, and none shows a graded pattern that stands out once the day-pooled t is used:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d2.d2.g1_choppy-high-close-follows-month` (from F4, F5, F2): In a choppy market, when a coin's daily close sits near the top of that day's high-low range, its price moves over the next five days in the direction of its 20-day return, and the larger that 20-day return in either direction, the larger the move.
- `061-01.b1.b1.b1.d1.d2.d2.g2_choppy-month-scaled-continuation` (from F6, F4): In a choppy market, a coin's 20-day return measured against its daily swing continues over the next five days, and the larger that scaled return, the larger the move in its direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
