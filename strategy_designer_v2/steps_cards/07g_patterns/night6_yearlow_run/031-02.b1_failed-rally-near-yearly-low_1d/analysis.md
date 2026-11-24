---
line: 7.g patterns
backtest: 031-02.b1_failed-rally-near-yearly-low_1d
idea tested: 031-02.b1_failed-rally-near-yearly-low
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5097 USD
---
## Findings
- **F1:** Inside the tested idea's regime (60-day return above 0), the 20-day excess return barely changes with nearness to the yearly low; the nearest quintile of the standardised distance (0.20 to 7.19) has −2.36 % (t −1.07, 82 cases) and the other quintiles have +1.08 % to +4.95 %, all with |t| < 1, so the idea's graded relation is not in the bars (step 5's correlation t was 0.50, n = 410).
- **F2:** The book's gain comes mostly from its long side. Long bars earn a mean of 0.053 % a bar, summing to 3.30 over 6,200 bars; short bars earn 0.018 %, summing to 0.71 over 3,916 bars. Long trades average +15.3 % but have a median of −2.6 % and win 45.5 % of the time, so a few large rallies carry the book.
- **F3:** Daily moves scaled by their prior 20-day volatility partly reverse the next day across all bars. After a z between −2 and −1, the next day's excess return is +0.456 % (t 3.12, 1,262 days); after a z between 0 and 1 it is −0.172 % (t −2.82, 5,179). The day-clustered reversal slope has t 1.83 over 2,346 days, and the effect is gone by 3 days (t 0.49, 860 days).
- **F4:** The one-day reversal sits where the 60-day return is 0 or below. There the day-clustered t is 1.74 over 1,087 days, against −0.40 over 1,092 days where it is positive. In the lowest 60-day-return quintile it is t 1.98 over 580 days, and the higher quintiles show t −0.51 to 0.60.
- **F5:** In the 60-day-down bars the next-day excess return falls step by step with the scaled move: +0.755 % after z in (−2, −1] (t 3.19, 395), +0.005 % after (−1, 0], −0.336 % after (0, 1] (t −3.03, 1,481) and −0.549 % after (1, 2] (t −2.34, 321). The two largest are 2.9 to 4.0 times the 0.19 % cost of a trade.
- **F6:** The down-60 reversal has the same sign in all six coins, with day-clustered t from 1.05 (ZEC) to 2.24 (XRP), and in both halves of the windows: t 0.67 in w1–w12 and 1.73 in w13–w24. It is a consistent but individually weak pattern, and by calendar year the pooled reversal is positive from 2018 to 2023 and slightly negative in 2024 and 2025 (t −0.65, −0.44).

## Ideas
- `031-02.b1.g1_next-day-reversal-in-downtrends` (from F3, F4, F5, F6): The larger a coin's 1-day return compared with the usual size of its daily returns over the past 20 days, the more the coin moves the opposite way over the next day, while its 60-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
