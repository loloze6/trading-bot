---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The coin's return over the next two hours rises with how far its 24-hour volume-weighted fall reaches beyond its usual 24-hour move. Here the fall is each hour's return over the past 24 hours in 30-day standard deviations, weighted by that hour's volume against its 30-day average and summed.
Consequence: A day of heavy-volume selling, rather than a single hour, is a reason to buy for a rebound that has room to cover its cost.
Why:
- F1: The 24-hour move reverses over the next 24 hours, graded. On a non-overlapping 24-hour grid, the coin's next-24-hour unusual move falls with its past 24-hour return (scaled by its 30-day hourly volatility × √24). The bottom quintile is followed by +31.6 bp for BTC (t 1.77, 516 cases) and +45.9 bp for ETH (t 1.89, 551 cases). The top quintile is followed by −20.7 bp for BTC (t −1.39) and −16.4 bp for ETH (t −0.91). The correlation is negative in 6 of 8 years (−0.03 to −0.11) and near zero in 2022 (+0.01) and 2024 (+0.02). This is about 0.06 on about 5,300 cases, an estimated t of about −4 that I did not compute directly. The move per case is several times the 0.11 % cost of a trade.
- F4: The tested rebound is graded across falls of at least 1.5 usual moves. Ranked by fall × volume ratio, the 2-hour unusual moves by quintile are −1.2, +7.8, +4.8, +17.0 (t 2.01) and +27.0 bp (t 2.72), each on about 594 cases. But the extreme cases (fall beyond 2.5 usual moves on more than 4× volume) earn their gain in 2020 (+95.6 bp, t 2.59) and 2021 (+122.5 bp, t 1.83). They are negative in 2023 to 2025 (−1.1, −3.1, −13.8 bp).
