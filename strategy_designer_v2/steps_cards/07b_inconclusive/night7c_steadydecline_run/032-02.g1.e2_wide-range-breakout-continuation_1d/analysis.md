---
line: 7.b inconclusive
backtest: 032-02.g1.e2_wide-range-breakout-continuation_1d
idea tested: 032-02.g1.e2_wide-range-breakout-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3363 USD
---
## Findings
- **F1:** The tested measure was positive but short of the bar (mean excess 5-day return +0.82 %, t 1.86, 855 grid cases), and its size is clearer once same-day cases are taken together (unusual move +1.02 %, t 2.33 over 734 days), so the result lies on the predicted side; the six coins tested are the only coins the test used, and 13 more coins have data in folds A and D and in part of B and C.
- **F2:** The rise sits almost entirely in closes at the 28-day highest close. On uptrend, wide-range 5-day grid cases in folds B and C, closes within 0.5 % of the high were followed by +4.87 % (t 2.89, 99 cases). The other distance bins were +0.82 % (0.5–2 %, 27 cases), −0.66 % (2–5 %, 72), +0.33 % (5–10 %, 79) and −3.48 % (>10 %, 51, t −1.75).
- **F3:** Inside the regime the grading itself is strong (slope of 5-day excess return on proximity +0.072, t 3.99, 328 cases). The plan's mean is diluted because its standardised forecast stays positive on many closes far from the high: its lowest forecast tercile was −2.21 % (t −1.94, 149 cases) against +2.79 % (t 2.12) for the highest.
- **F4:** The closes at the high hold over a longer horizon: on uptrend, wide-range days they were followed by +10.19 % over 10 days (t 2.85, 52 cases), while all active cases together gave only +1.29 % over 10 days (t 1.08, 232 cases).
- **F5:** The wide range acts as a condition, not as a grade. Uptrend closes at the high on narrow-range days were followed by +0.59 % over 5 days (t 0.30, 24 cases), against +4.87 % on wide-range days. Within uptrend closes at the high, the range terciles gave about the same rise (+3.89 %, +4.37 %, +3.83 %).
- **F6:** The effect is mixed across periods and coins. Active 5-day cases were negative in 2018 (−3.72 %, t −1.94, 59 cases) and 2019 (−1.44 %, 93 cases), and positive in 2020 (+2.36 %, t 2.59, 161 cases) and 2021 (+1.36 %, 134 cases). At the high, four coins were positive and LTC (−0.40 %) and ZEC (−0.30 %) were flat; at the high the rise was +7.49 % in 2021 (t 2.01) against −0.90 % in 2019.

## Ideas
- `032-02.g1.e2.b1_wide-range-breakout-more-coins` (from F1, F6): In a coin whose close is above its close of 28 days ago, a close near its 28-day highest close on a day whose high-low range is wide compared with its ranges of the last 28 days is followed by a rise over the next 5 days, larger the nearer the close is to that high.
- `032-02.g1.e2.b2_wide-range-close-beyond-high` (from F2, F3, F5): In a coin whose close is above its close of 28 days ago, a close above its highest close of the previous 28 days, on a day whose high-low range is wide compared with its ranges of the last 28 days, is followed by a rise over the next 5 days, larger the further the close stands above that previous high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
