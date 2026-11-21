---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d
idea tested: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3620 USD
---
## Findings
- **F1:** The book earns too little because it is rarely in and small when in: it holds a position on 24.4 % of bars at a mean size of 0.55 of the book, so its mean daily return is 0.044 % against the coins' 0.119 %, though it gains 0.19 % per bar while in.
- **F2:** The move after a break outlasts the 5-day holding. The excess return over the coin's drift from the 878 entries is +1.15 % over 5 days (t 3.3, 849 cases), +2.24 % over 10 days (t 4.0, 815), +3.76 % over 20 days (t 3.4, 775) and +8.7 % over 40 days (t 3.8, 631). The increments after day 5 stay positive: days 6–10 +1.45 % (t 3.8), days 11–20 +1.71 % (t 2.6), days 21–40 +5.6 % (t 4.5).
- **F3:** Distance above the 50-day average does not grade the move, yet it sets the size. Across distance quartiles of 1.7 %, 5.3 %, 10.2 % and 22.9 %, the 5-day return is 1.3 %, 1.9 %, 1.9 % and 1.8 %, and the 20-day return is 5.0 %, 9.2 %, 5.9 % and 4.4 %. The verdict's slope is -6.8e-5. The lowest quartile is held at a mean allocation of 0.22 against 0.61 to 0.82 for the others.
- **F4:** Breaks that come after a falling 60-day return do not continue. In the quartile with a mean 60-day return of -10.6 %, the 20-day excess return is -1.7 % (10-day +0.7 %). The three other quartiles give +5.6 % to +14.1 % (top minus bottom t 1.89, about 95 cases each).
- **F5:** The losing breaks are concentrated in falling years. The 20-day excess return is -26 % in 2018 (24 cases), -2.8 % in 2022 (68) and -1.1 % in 2023 (161), against +13.8 % in 2020 (122) and +5.5 % in 2024 (134).
- **F6:** Cost is not the cause. The total 5-day move per case is 1.61 %, against a round-trip cost of 0.19 %, and the 1119 trades average +3.17 % net after a mean of 7.3 days.

## Ideas
- `020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend.d1_resistance-break-held-longer` (from F2, F3, F6, F1): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 20 days, only while its close is above its 50-day average, and the more times the price had turned down at that level, the larger the rise.
- `020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend.d2_breaks-after-rising-quarter` (from F4, F5, F2, F3): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 20 days, only while its close is above its 50-day average and its 60-day return is positive, and the more times the price had turned down at that level, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
