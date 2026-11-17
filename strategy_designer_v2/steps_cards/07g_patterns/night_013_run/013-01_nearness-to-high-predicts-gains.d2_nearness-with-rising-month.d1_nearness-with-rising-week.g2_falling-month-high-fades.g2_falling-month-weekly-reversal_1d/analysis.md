---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3670 USD
---
## Findings
- **F1:** When a coin's 30-day return was zero or positive, a larger 7-day return came before a larger excess return over the next 7 days (slope 0.142, t 4.35, 894 non-overlapping grid cases). The effect was much stronger in windows w13–w24 (t 4.35, n 399) than in w1–w12 (t 1.12, n 495). It was strongest in XRP (t 2.51) and ZEC (t 2.72), and not stable by year: 2023 went the other way (t −2.54) while 2025 was strongest (t 5.00).
- **F2:** A higher ratio of 7-day to 60-day average volume came before a higher 7-day excess return (slope 0.021, t 3.60, 1723 grid cases), and the top within-coin quintile averaged +1.88% (t 2.11). The effect sat in windows w13–w24 (t 3.66) rather than w1–w12 (t 0.64), and in XRP (t 2.31) and ZEC (t 2.66).
- **F3:** A one-day move scaled by 20-day volatility came before an opposite next-day excess return (slope −0.0018, t −3.62 in w1–w12; −0.0015, t −2.52 in w13–w24; about 7250 days each). The lowest quintile, the sharpest falls, was followed by +0.40% (t 4.16, n 2900). The effect was strongest in XMR (t −4.67) and ETH (t −2.44).
- **F4:** In the calmer half of bars (20-day volatility below its median), being closer to the 30-day high came before a higher 7-day excess return (slope 0.156, t 3.40, n 874). The same relation was absent in the volatile half (t 0.04). It held in BTC (t 2.46), ETH (t 2.23) and XRP (t 2.40), and was stronger in w13–w24 (t 3.24) than in w1–w12 (t 1.36).
- **F5:** The tested relation in falling months was only weakly in the idea's direction (7-day return slope −0.057, t −1.49, n 829). The book lost money on average in every coin (for example ETH −0.031% a day against the coin's +0.137%), with a book-to-coin daily correlation of 0.32.
- **F6:** Weekday means were not consistent between the two halves of the windows (Friday t 3.60 then 1.85; Monday t −0.26 then −3.25), so no weekday pattern is counted.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.g1_rising-month-weekly-continuation` (from F1, F5): While a coin's 30-day return is positive, the larger its 7-day return, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.g2_volume-surge-precedes-gains` (from F2): The higher a coin's average daily volume over the last 7 days relative to its last 60 days, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.g3_one-day-shock-reversal` (from F3): The larger a coin's one-day fall relative to its 20-day daily volatility, the higher its return over the next day.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal.g4_calm-market-nearness-to-high` (from F4): While a coin's 20-day volatility is low, the closer its close is to its 30-day high, the higher its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
