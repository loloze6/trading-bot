---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3475 USD
---
## Findings
- **F1:** Across all coins, a coin's return on the day after its weakest days is far above every other day: the bottom fifth of previous-day returns is followed by a mean next-day return of +0.57 % (t 5.84, n 3450), against +0.11 % (t 1.38), −0.05 %, +0.01 % and −0.08 % (t −0.81) for the other four fifths, so the rebound grows with the size of the prior day's fall, and the top fifth shows no continuation.
- **F2:** On the non-overlapping 10-day grid, the coin's own 10-day return carries forward: the top third of past 10-day returns is followed by +2.05 % excess 10-day return, against −0.63 % for the bottom third (Welch t 2.57, n 516 per third); the 20-day return (t 2.00) and the close's position inside its prior 20-day range (+1.56 % vs −0.75 %, t 2.23) point the same way.
- **F3:** Grid bars that close above the prior 20-day high are followed by a mean excess 10-day return of +6.44 % (n 86, std 0.249, t ≈ 2.4), against −0.30 % on the other 1317 grid bars, yet the tested width forecast does not grade this (slope t 0.39 on 404 cases), so the gain comes from the break, not from the prior range.
- **F4:** Compression does not precede larger moves: the 10-over-30-day range ratio leaves the absolute 10-day move flat (10.2 % bottom third vs 10.7 % top, t 0.52), and so does the realised-volatility ratio (t 0.23), while plain 30-day volatility predicts it (9.3 % vs 12.6 %, t 4.14); this is ordinary volatility clustering, against the brief.
- **F5:** The coin's daily return depends on the weekday: Saturday averages +0.45 % (t 5.53, n 2484), Friday +0.33 % (t 3.51) and Wednesday +0.28 % (t 2.51), against −0.12 % on Tuesday and −0.18 % on Thursday. This is pooled across six correlated coins, and it is a calendar condition with no grade, so I keep it as context only.
- **F6:** The book is invested on only 9.4 % of days, and its top 1 % of days sum to +9.88 against a total of +1.79, so a few breakout days carry the whole result; trades held 1.5–3.5 days gain +5.7 % on average (n 212), while one-day trades lose −2.3 % (n 520).

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound` (from F1): The larger a coin's fall over the last 1 day, the higher its return over the next 1 day.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation` (from F2, F3, F6): The higher a coin's 10-day return, and the closer its close sits to the top of its prior 20-day range, the further its price rises over the next 10 days.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation` (from F3, F4, F6): The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
