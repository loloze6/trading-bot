---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d
idea tested: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4632 USD
---
## Findings
- **F1:** In the most volatile fifth of each coin's days, the 3-day move after a day ran against that day's direction by 0.247 of a usual 3-day move (t 4.85, 1625 cases on 319 days), roughly 2 % of a 9 % usual move and about ten times the 0.22 % cost of a trade; volatility here is the 20-day mean daily range against its own 60-day average. The effect rose steadily across volatility fifths, from -0.082 in the calmest fifth (t -1.68), through -0.039 and -0.013, to +0.023 in the fourth.
- **F2:** Inside that most volatile fifth, the move back grew with the size of the day's own move. By quartile of the day's absolute return it was 0.115 (t 1.85), 0.203 (t 3.29), 0.194 (t 3.19) and 0.396 (t 3.82). The slope of the 3-day move on the day's return was -0.168 in the most volatile third, against +0.044 and +0.037 in the other two.
- **F3:** In volatile days the move back held for both directions of the day: 0.316 after down days (t 3.91, 219 days) and 0.171 after up days (t 2.39, 202 days). It held for the older coins (0.257, t 4.43) and the others (0.236, t 3.76) alike. It was positive in every year from 2018 to 2025, with t above 2 in 2020, 2022, 2023 and 2025.
- **F4:** The tested situation pointed the wrong way. After a 5-day fall, a wide day (range at least 1.5 times its 20-day mean) closing in its top quarter was followed by a 3-day move of -0.188 of a usual move in the short direction (t -1.21, 230 cases), so the coin rose rather than fell. Consistent with this, the book's worst 5 % of active days came on days its coins rose 13.8 %, and only 40 % of its 2651 active days gained.
- **F5:** The move back appeared from the first day and was strongest at 3 days. In the two most volatile fifths it was 0.048 (t 2.25) and 0.062 (t 2.01) over 1 day, and 0.247 (t 4.85) over 3 days. Over 5 days it faded to 0.077 (t 1.49).

## Ideas
- `031-02.b1.b1.b1.d2.g1.g1_high-volatility-daily-move-reverses` (from F1, F2, F3, F5): When a coin's average daily range over the past 20 days is high against its average over the past 60 days, the coin moves back against its latest day's return over the next 3 days; the larger that day's move and the higher that volatility, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
