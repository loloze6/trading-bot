---
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
idea tested: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4542 USD
---
## Findings
- **F1:** The day after a coin's daily move, its next-day return runs against that move, with a regression slope t of −3.62 in BTCUSD and −3.98 in ETHUSD (2,873 daily cases each); the lowest prior-day quintile is followed by +0.44% and the highest by −0.06% to −0.14% (Welch t 2.27 and 1.91).
- **F2:** This next-day reversal is concentrated in the highest 20-day-volatility tercile, with a slope of −0.0070 per standardised prior move (t −5.82, n 1,612); the middle tercile shows none (t −0.06) and the lowest tercile leans to slight continuation (+0.0015, t 2.15).
- **F3:** The reversal slope is negative in every year from 2018 to 2025, and is strongest in 2020 (t −5.19, n 720) and 2021 (t −2.13).
- **F4:** The book's gain comes almost entirely from days held long, which average +0.26% a day over 2,920 days against +0.003% over 2,864 days held short; short trades net only +0.27% (BTC) and +0.88% (ETH) per trade against +4.5% and +5.2% for long trades.
- **F5:** The tested 7-day continuation is weak beside the 1-day reversal. The forecast quintiles rise monotonically in 7-day excess return, from −1.33% to +1.54%, but no quintile reaches |t| 2, and the sign-weighted excess falls to +0.2% in 2023 and −0.35% in 2024 (about 102 cases each).

## Ideas
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.g1_high-volatility-next-day-reversal` (from F1, F2, F3): When a coin's daily volatility is high, the larger its one-day return measured in units of its own 20-day daily volatility, the more its return over the next 1 day runs in the opposite direction.
- `010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week.g2_volatility-scaled-daily-reversal` (from F2, F1): The higher a coin's own 20-day daily volatility, the more strongly its return over the next 1 day runs opposite to its return over the past 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
