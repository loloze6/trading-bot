---
line: 7.e profitable but not proven
backtest: 031-01.b1_wide-day-extends-up-run_1d
idea tested: 031-01.b1_wide-day-extends-up-run
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4078 USD
---
## Findings
- **F1:** About 58 % of the book's mean daily return comes from the coins' own rise, not from timing: the book earns 0.0706 % a day, of which 0.0412 % is the position held times the coins' mean daily return and 0.0426 % is timing, and the timing part cannot be told from 0 (t 1.53 over 2898 book days).
- **F2:** The book's gain rests on a few days and trades: the top 1 % of book days sum to 1.94 of the 2.04 total of daily returns, leaving 0.10 for the other 99 %; the top 5 % of the 6775 trades carry 17386 of the 20042 summed net percent, and only 52 % of trades win.
- **F3:** The timing gain comes from strong-market years and one coin: it is +0.20 % a day in 2020, +0.14 % in 2021 and +0.12 % in 2024, but negative in 2018, 2019, 2022 and 2025 (−0.098 % in 2022); XRP alone gives 0.124 % of timing against 0.03–0.06 % for the other coins and −0.007 % for XMR; 9 of the 24 windows lose.
- **F4:** The idea's own grading is not monotonic: inside 5-day up-runs, the 3-day excess return by range-ratio quartile is +0.36 %, +0.24 %, −0.34 % and +0.78 % (t 2.09 only in the top quartile, 645 cases); where the close lands in the day's range changes nothing (+0.32 %, +0.28 % and +0.30 % for low, middle and high closes).
- **F5:** What predicts the 3-day move is the strength of the prior 5-day rise: by quintile of the 5-day return, the 3-day excess return climbs from −0.56 % to −0.26 %, −0.09 %, +0.07 % and +0.72 % (top quintile t 2.42, 1087 cases on a non-overlapping grid).
- **F6:** Scaled by the coin's 20-day daily volatility, the same pattern holds, and it is graded inside up-runs: the top quintile of the volatility-scaled 5-day return is followed by +0.96 % excess over 3 days (t 2.24 with same-day cases together, 943 cases on 370 days), while the four lower quintiles are between −0.16 % and −0.29 %; the slope of the 3-day excess return on this scaled return within up-runs has t 2.07 (2373 cases), against t 1.63 for the range ratio.
- **F7:** The run-strength effect is short-lived and not uniform: at 10 days the top 5-day-return quintile's excess return is +1.67 % but with t 1.50, at 5 days the up-run excess return has t 0.52, and the slope on the scaled 5-day return is positive on 5 of the 6 coins (t 1.26 to 1.62 for BTC, ETH and XRP) but negative in 2022, 2023 and 2025.

## Ideas
- `031-01.b1.e1_strong-run-continues-three-days` (from F5, F6, F7, F1): The larger a coin's rise over the past 5 days compared with its usual daily move over the past 20 days, the more the coin rises over the next 3 days.
- `031-01.b1.e2_wide-day-in-strong-run` (from F4, F6, F3): Within a coin's 5-day rise, the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days, the effect concentrated in the widest days and growing with how strong the 5-day rise was.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
