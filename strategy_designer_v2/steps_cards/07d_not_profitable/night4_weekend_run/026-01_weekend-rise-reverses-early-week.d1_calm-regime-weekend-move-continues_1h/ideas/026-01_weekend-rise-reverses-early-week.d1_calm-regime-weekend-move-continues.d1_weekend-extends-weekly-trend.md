---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day hourly volatility is low against its own last 6 months, its move from Saturday 00:00 UTC to Monday 00:00 UTC continues in the same direction over the following two days (Monday and Tuesday), only while the coin's return over the five days before Saturday was in the same direction as the weekend move. The larger that preceding five-day return in the weekend's direction, the larger the continuation.
Consequence: In calm weeks a trader would follow the weekend's direction into Monday and Tuesday only when the week before had already moved that way, and would stay out when the weekend broke from it.
Why:
- F1: The idea's move does not grow with the forecast, but the position does: by |forecast| bin (2–5, 5–10, 10–15, 15–20) the 48-hour signed move is 0.62 %, 0.86 %, 0.72 % and 0.61 % (n 313/367/243/289), while the mean |allocation| rises from 0.18 to 0.36, 0.61 and 0.96. The largest bets earn no more than the smallest and carry the risk.
- F2: The worst 60 cases by book gain held a mean |allocation| of 0.92, against 0.51 over all cases, and 58 % of them came after a prior 5-day move against the weekend's direction, against 51 % overall. The book's deepest falls come from full-size bets on weekends that broke from the week before.
- F3: The continuation lives where the weekend move extends the preceding 5 days (Monday to Friday) in the same direction: 1.22 % per case (t 3.89, n 569) against 0.33 % (t 1.24, n 593) when they disagree.
- F4: Ranked by that prior 5-day move in the weekend's direction (scaled by 30-day hourly volatility), the book's gain per case grows across the quintiles: 0.11 % (t 0.52), −0.14 % (t −0.58), 0.46 % (t 2.34), 0.74 % (t 3.01), 0.71 % (t 2.60).
