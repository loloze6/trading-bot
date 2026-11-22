---
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3566 USD
---
## Findings
- **F1:** The idea's move does not grow with the forecast, but the position does: by |forecast| bin (2–5, 5–10, 10–15, 15–20) the 48-hour signed move is 0.62 %, 0.86 %, 0.72 % and 0.61 % (n 313/367/243/289), while the mean |allocation| rises from 0.18 to 0.36, 0.61 and 0.96. The largest bets earn no more than the smallest and carry the risk.
- **F2:** The worst 60 cases by book gain held a mean |allocation| of 0.92, against 0.51 over all cases, and 58 % of them came after a prior 5-day move against the weekend's direction, against 51 % overall. The book's deepest falls come from full-size bets on weekends that broke from the week before.
- **F3:** The continuation lives where the weekend move extends the preceding 5 days (Monday to Friday) in the same direction: 1.22 % per case (t 3.89, n 569) against 0.33 % (t 1.24, n 593) when they disagree.
- **F4:** Ranked by that prior 5-day move in the weekend's direction (scaled by 30-day hourly volatility), the book's gain per case grows across the quintiles: 0.11 % (t 0.52), −0.14 % (t −0.58), 0.46 % (t 2.34), 0.74 % (t 3.01), 0.71 % (t 2.60).
- **F5:** Longs carry the effect and shorts barely do:
- **F6:** The book is too thin and too shallow to clear its bars:
- **F7:** Over the years the effect fades: per case it was 1.09 % (2019), 1.69 % (2020) and 1.29 % (2021), against 0.43 % (2024) and −0.03 % (2025). The windows w1, w12, w14 and w23 lost between 6 % and 10 % each.

## Ideas
- `026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.d1_weekend-extends-weekly-trend` (from F1, F2, F3, F4): When a coin's 30-day hourly volatility is low against its own last 6 months, its move from Saturday 00:00 UTC to Monday 00:00 UTC continues in the same direction over the following two days (Monday and Tuesday), only while the coin's return over the five days before Saturday was in the same direction as the weekend move. The larger that preceding five-day return in the weekend's direction, the larger the continuation.
- `026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.d2_calm-weekly-rise-continues` (from F3, F4, F5, F6): When a coin's 30-day hourly volatility is low against its own last 6 months, a rise over its 7 days to Monday 00:00 UTC continues over the following two days (Monday and Tuesday). The larger that 7-day rise against the coin's 30-day volatility, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
