---
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4471 USD
---
## Findings
- **F1:** The failing Calmar of 0.61 comes from one fall: the book dropped 18.5 % over 132 days from a peak in w11 to a trough in w12, both in 2021. 2021 is the book's worst year (summed daily return −0.111), and in that year the cases lost on both sides (de-drifted 48-hour return in the forecast's direction −0.66 % on shorts and −0.83 % on longs).
- **F2:** The coin's 7-day return at the Sunday 23:00 close sorts the cases. When it points the same way as Saturday's move, the cases earn +0.98 % on shorts (t 2.91, 368 cases) and +0.84 % on longs (t 2.85, 488 cases). When it points the other way, they earn +0.19 % (t 0.37, 248 cases) and +0.10 % (t 0.32, 315 cases).
- **F3:** The 7-day condition alone is not the effect. Following the 7-day return on the 48-hour grid without the Saturday signal earns +0.19 % (t 2.46, 7869 cases), about a fifth of what it earns together with the signal. It belongs to the idea's own theory: Saturday's thin-market move continues when it extends the week's move rather than going against it.
- **F4:** Rebuilt with the same costs, the full book has a Calmar of 0.57 and a deepest fall of −19.6 %. Dropping the cases whose 7-day return disagrees raises its Calmar to 0.77 and cuts its deepest fall to −12.5 %, with a Sharpe of 1.04 against 1.06.
- **F5:** By side, long trades summed +927 % (1161 trades) and short trades −320 % (781 trades). A long-only rebuild reaches a Calmar of 0.79 with a deepest fall of −11.4 % (Sharpe 1.02), and the deepest fall stays in w12.
- **F6:** The long side is not just the coin's drift. Being long on every calm Sunday regardless of Saturday's sign earns +0.02 % (t 0.13, 1424 cases), while calm up-Saturday cases earn +0.55 % (t 2.51, 803 cases).
- **F7:** The book's losses are concentrated. The worst 5 % of trades sum to −1418 % against a total of +607 %, the 5 % worst adverse excursion inside the hold is −9.8 %, and trade gain is not graded by |forecast| quintile (+0.45, +0.33, +0.01, +0.40, +0.38 % per trade).
- **F8:** Cost is not the obstacle: the total move per case (+0.65 %) is 3.4 times the 0.19 % cost of a trade, so the failure is in the depth of the falls, not in the gain covering the fee.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend` (from F1, F2, F3, F4, F7): A coin's 24-hour return over Saturday is followed over the next two days, Monday and Tuesday, by a move in the same direction that grows with the size of Saturday's move, while the coin's 30-day volatility of hourly returns is low against its own past year. The continuation is larger the more the coin's 7-day return points the same way as Saturday's move.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d2_calm-up-saturday-continues-higher` (from F5, F6, F1, F8): A coin's rise over Saturday's 24 hours is followed over the next two days, Monday and Tuesday, by a further rise that grows with the size of Saturday's rise, while the coin's 30-day volatility of hourly returns is low against its own past year, and the calmer the coin, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
