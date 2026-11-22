---
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size_4h
idea tested: 024-02_fading-volume-downrun-rebound-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4096 USD
---
## Findings
- **F1:** The tested idea has no size. Over 4537 cases its mean 18-bar unusual move is +0.00 % (t 0.002). Bars with the strongest forecast (15 to 20, 401 grid cases) show a strength of only +0.097 (t 1.89). Bars with forecasts from 0 to 15 are all slightly negative: −0.114, −0.066 and −0.032 over 48, 94 and 101 cases.
- **F2:** Large rises tend to continue rather than give back. The top quintile of the 3-day return in usual 4h moves (mean +9.3 usual moves) has a next-3-day strength of +0.104 (t 3.03, 1032 cases). The bottom quintile, the large falls the tested idea bets on, shows only +0.023 (t 0.72). The top quintile of the 7-day return has +0.098 (t 2.77, 1032 cases).
- **F3:** That continuation depends on high volume. Take the top tercile of the 3-day return and split it by 3-day volume against the 30-day volume. With the highest volume its strength is +0.134 (t 3.12, 738 cases); with the lowest volume it is −0.029 (t −0.65, 433 cases). This contradicts the brief's claim that fading-volume runs give back more.
- **F4:** The continuation is not steady across coins, years or the full range of returns. In the top 3-day-return tercile, strength is positive in 5 of 6 coins but no coin reaches t 2 (t −0.20 to 1.70). It is negative in 2018, 2019, 2022 and 2025 (−0.062, −0.050, −0.093, −0.016) and positive in 2020, 2021, 2023 and 2024 (+0.221, +0.165, +0.061, +0.129). The per-coin rank correlation between the 3-day return and the following strength lies between −0.045 and +0.031.
- **F5:** A wide last bar is followed by higher 3-day returns, in a graded way. By quintile of the last 4h bar's range relative to its 180-bar mean, the next-18-bar strength is −0.062, −0.070, +0.006, +0.023 and +0.087 (t −2.24, −2.52, 0.21, 0.73, 2.33; about 1030 cases each). By quintile of last-bar volume relative to its 7-day mean, the top quintile has +0.105 (t 2.99, 1086 cases) and the other four quintiles are all negative.
- **F6:** The 4h bar starting at 20:00 UTC rises more than any other bar of the day. Its pooled mean is +9.1 bp (t 5.78, 16066 bars), against −4.1 bp for the 00:00 bar (t −2.55). In return scaled by the usual move, the 20:00 bar is positive in all 6 coins (t 1.26 to 3.26) and in 7 of 8 years (t −0.69 to 4.27).
- **F7:** Most of the book's result comes from holding the coins, not from timing. The book's daily returns correlate 0.86 with the coins' returns. On the book's worst 2 % of days the coins fell 10.8 %, and on its best 2 % they rose 9.5 %. Its yearly mean daily return follows the coins' sign every year, for example −21.3 bp against −34.9 bp in 2018 and +33.1 bp against +42.3 bp in 2020.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.g1_high-volume-rise-continues` (from F2, F3, F4): The larger a coin's 3-day rise relative to its typical 4-hour move over the past 30 days, and the higher its volume over those 3 days relative to its 30-day volume, the more the coin keeps rising over the next 3 days.
- `024-02_fading-volume-downrun-rebound-size.g2_wide-heavy-bar-precedes-rise` (from F5): The wider a coin's last 4-hour bar relative to its average 4-hour range over the past 30 days, and the higher that bar's volume relative to its 7-day average, the more the coin rises over the next 3 days.
- `024-02_fading-volume-downrun-rebound-size.g3_late-evening-utc-lift` (from F6): A coin rises over the 4 hours starting at 20:00 UTC, by an amount that grows with its typical 4-hour move over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
