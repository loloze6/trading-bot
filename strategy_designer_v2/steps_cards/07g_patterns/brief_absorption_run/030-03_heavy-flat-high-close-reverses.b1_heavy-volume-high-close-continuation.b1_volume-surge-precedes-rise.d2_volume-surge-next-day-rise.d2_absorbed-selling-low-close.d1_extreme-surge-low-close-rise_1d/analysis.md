---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4220 USD
---
## Findings
- **F1:** The next day reverses the day's return measured against its own 20-day volatility, and this grows with the coin's volatility. The slope of the next-day excess return on that scaled return goes from +0.0012 (t 2.1, 3197 cases) in the calmest fifth of 20-day volatility to −0.0090 (t −7.3, 3197 cases) in the most volatile fifth. In a regression on all days, the interaction with the high-volatility fifth is −0.0087 (t −3.4).
- **F2:** The high-volatility reversal holds in all six coins: slopes −0.0058 to −0.0159, with t from −1.6 (XRP, ZEC) to −5.5 (XMR), about 530 cases each. It also holds in every year from 2018 to 2024 (t −3.4, −1.0, −5.0, −4.1, −2.9, −3.1, −0.8). Only 2025 has the opposite sign (+0.0037, t 0.6, 208 cases).
- **F3:** The reversal outlasts the next day. In the high-volatility fifth, days in the lowest fifth of scaled return gain +1.16 % over 2 days (t 1.8, 302 cases) and +2.27 % over 3 days (t 2.3, 169 cases) beyond drift. Days in the highest fifth lose −1.03 % (t −2.1, 322 cases) and −1.41 % (t −1.8, 181 cases).
- **F4:** In the most volatile fifth, the tested idea's low-close effect vanishes once the day's scaled return is in the regression: the close-location slope is +0.00015 (t 0.08) against −0.0090 (t −3.7) for the scaled return. Within that regime, the edge from the low close is largely the reversal of a down day.
- **F5:** Volume surge carries its own next-day rise, separate from the close location and the day's return. The log surge coefficient is +0.0018 (t 4.0) on all days and +0.0045 (t 3.4) in the most volatile fifth. The top surge fifth gains +0.39 % beyond drift (t 3.8, 3198 cases), while the other four fifths sit between −0.13 % and 0.00 %.
- **F6:** The book makes its worst 2 % of days on falls of the coins themselves: −6.4 % for the book against −9.6 % for the coins. It is in a position on 98 % of coin-days, so little of the ordinary-day exposure is removed. This is the exposure behind its Calmar of 0.51.
- **F7:** Weekday effects are not stable and are not a finding. The pooled values are Thursday +0.25 % (t 2.6), Friday +0.31 % (t 3.8) and Wednesday −0.30 % (t −2.7). The year-by-year signs flip for most weekdays (Wednesday ranges from −1.56 % to +0.25 %).

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.g1_turbulent-day-volatility-scaled-reversal` (from F1, F2, F3, F4): The larger a coin's one-day return relative to its own 20-day volatility, the more the coin moves the opposite way over the next three days. The reversal is stronger the higher the coin's 20-day volatility.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.g2_turbulent-volume-surge-rise` (from F5, F1): The heavier a coin's volume on a day relative to its prior 20-day average, the more the coin rises over the next day, and more so the higher the coin's 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
