---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.g2_wide-day-after-long-climb_1d
idea tested: 031-02.b1.b1.b1.g2_wide-day-after-long-climb
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4620 USD
---
## Findings
- **F1:** On coins with a positive 20-day return, the excess 3-day return grows with the log of the day's range over its 20-day mean range (slope 0.0153, t 2.70 with cases of one day taken together, 4936 cases on 688 days), while on coins with a zero or negative 20-day return the same slope is flat (−0.0010, t −0.17, 5088 cases on 702 days).
- **F2:** Across all bars, the excess 3-day return rises with the range ratio above 1.25: +0.09 % at 1.25–1.5 (887 cases), +0.54 % at 1.5–2 (845), +0.87 % at 2–3 (483) and +4.90 % above 3 (t 1.97, 164 cases on 85 days), against −0.58 % at 1.0–1.25 (1444 cases).
- **F3:** On wide days the gain sits in the top fifth of 20-day returns (+3.31 % excess over 3 days, t 3.31, 521 cases on 232 days); the other four fifths range from −0.98 % to +0.88 % with every |t| under 1.3, and a straight slope on the vol-scaled 20-day return gives only t 1.51 (1492 cases), and t 1.14 without 2020 and 2021.
- **F4:** The brief's flat-close reversal is not in the bars: after a 20-day rise, wide days with a flat body (|close−open| at most 0.2 of the range) are followed by +1.19 % (t 0.84, 119 cases), and wide days with a strong body (over 0.5 of the range) by +2.38 % (t 2.71, 559 cases).
- **F5:** The book's gain is concentrated on a few days: its best 30 of 2898 days sum to 163.5 % of the 177.5 % summed daily return, and its worst 10 days to −56.3 %.
- **F6:** Trades entered on the lowest quarter of forecasts earn +1.99 % net, held 7.4 days with 60 % winners, against +2.53 % net held 3.6 days with 53 % winners in the top half.
- **F7:** Wide days after a 20-day rise are followed by a positive excess in 6 of 8 years, negative in 2018 (−2.86 %, 26 cases) and 2022 (−2.15 %, 72 cases), and in 17 of 19 coins.
- **F8:** No other angle stands out against the number looked at: by weekday the largest |t| is 1.60 (n about 1400 each); on non-wide bars the 20-day return has no effect (t 0.11, 8532 cases); wide days in the top volatility quartile give +2.70 % (t 1.84); close location within wide-day cells reaches t 2.68 only once in 12 cells (52 cases).

## Ideas
- `031-02.b1.b1.b1.g2.g1_wide-range-extends-climb` (from F1, F2, F3, F4, F7): While a coin's 20-day return is positive, the wider its daily range compared with its average daily range over the past 20 days, the larger its rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
