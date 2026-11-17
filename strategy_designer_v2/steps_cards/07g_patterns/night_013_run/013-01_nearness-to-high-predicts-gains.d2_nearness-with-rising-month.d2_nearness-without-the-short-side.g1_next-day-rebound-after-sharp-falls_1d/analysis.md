---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3587 USD
---
## Findings
- **F1:** The rebound after down days lives in high volatility: on down days split by the coin's 20-day volatility rank within its own past 120 days, the slope of next-day excess return on the scaled fall is 0.0073 (t 3.45, n 1459) in the high tercile, 0.0007 (t 0.37) in the middle and −0.0011 (t −0.59) in the low; the fall × volatility-rank interaction has t 3.57, and fall alone has t −1.84.
- **F2:** The book's timing gain follows the same split: the mean daily position × excess return is 0.00153 (sum 4.52) in the high-volatility tercile, 0.00044 in the middle and −0.00063 (sum −1.87) in the low, so low-volatility days give back about 40% of what high-volatility days earn.
- **F3:** For falls beyond one usual move (z < −1), next-day excess return is 0.0121 (t 3.54, n 373) in high volatility against −0.0028 (t −1.19, n 374) in low; high-minus-low Welch t is positive in 5 of 6 coins (BTC 2.44, ZEC 2.23, ETH 1.71, XRP 1.71, LTC 1.17), and XMR is the exception at −0.48.
- **F4:** In the high-volatility tercile the reversal holds on all bars, both sides: the slope of next-day excess return on the scaled one-day return is −0.0041 (t −4.38, n 2962), against 0.0009 (t 1.14) in the low tercile; moderate up days (z 0.5 to 1) are followed by −0.0023 (t −2.43, n 1987).
- **F5:** Heavy volume strengthens the rebound: for z < −1, next-day excess return is 0.0102 (t 4.02, n 614) in the high volume-surprise tercile against 0.0018 (t 0.91) in the low; the fall × volume-z interaction is only t 2.05, so this is weak given how many angles were checked.
- **F6:** The rebound is not steady over time: for z < −1 it is 0.0150 (t 3.49) in 2020 and 0.0146 (t 3.43) in 2021, but between −0.0013 and 0.0043 (all |t| < 1.1) in 2022–2025, which fits the book's weak Calmar of 0.43.
- **F7:** A weekday pattern shows across all bars: next-day excess return is 0.0030 (t 3.76, n 2479) from Friday's bar and 0.0025 (t 2.63) from Thursday's, against −0.0024 (t −2.53) from Monday's and −0.0030 (t −2.70) from Wednesday's; Friday is positive in both halves of the sample (0.0040, 0.0021) and in all 6 coins (t 0.35 to 2.44).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g1_rebound-grows-with-volatility` (from F1, F2, F3, F6): The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day, and the rebound per unit of fall grows the higher the coin's 20-day volatility stands against its own past 120 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g2_high-volatility-one-day-reversal` (from F4, F1): When a coin's 20-day volatility is high against its own past 120 days, the larger its one-day return relative to that 20-day volatility, the lower its return over the next 1 day, on up days as well as down days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g3_heavy-volume-falls-rebound-more` (from F5, F3): The larger a coin's one-day fall relative to its 20-day volatility, the higher its return over the next 1 day, and the rebound per unit of fall grows with that day's volume relative to the coin's own 20-day volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
