---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4623 USD
---
## Findings
- **F1:** The Sunday reversal is concentrated in turbulent stretches. Cases were split into thirds by the coin's 20-day volatility relative to its earlier 60-day volatility. In the wildest third, Sunday's move is undone by 1.38 % over Monday and Tuesday (t 5.77, 1148 cases). In the calmest third it is undone by 0.52 % (t 2.38, 1201 cases). The difference, wild minus calm, is 0.85 % (Welch t 2.62).
- **F2:** The effect belongs to Sunday, not to turbulence in general. In the wild third, Sunday's reversal minus the other weekdays' 2-day reversal is 1.38 % (Welch t 5.41). No other weekday's wild third reverses by more than 0.82 % (Monday, t 3.52), and Friday's wild third continues by 0.44 % (t -2.45).
- **F3:** Sunday moves that go against the coin's previous 4-day move reverse more. Over the next 2 days they reverse by 1.17 % (t 7.62, 2316 cases), against 0.53 % (t 2.98, 2013 cases) for Sunday moves that go with it. That is a gap of about 0.64 % (t about 2.7 from the two standard errors).
- **F4:** The reversal is spread over both days of the hold and grows with the move. Monday alone gives 0.48 % (t 5.51) and Tuesday alone 0.43 % (t 5.55). The size-weighted measure rises from 0.09 % in the smallest fifth of |Sunday z| to 1.55 % in the largest fifth. The 2-day Saturday+Sunday move carries no reversal (product t 1.22), so the effect belongs to Sunday's own bar.
- **F5:** The brief's volume claim is not visible. Sunday cases split by Sunday volume relative to the coin's 60-day volume reverse by 0.66 % (low third) and 0.99 % (high third). The difference, high minus low, is 0.32 % (t 1.09), in the opposite direction to the brief's.
- **F6:** Friday moves continue over the weekend. Over Saturday to Monday they continue by 0.37 % (t -3.00, 4263 cases; size-weighted t -3.58), mostly in the wild-volatility third (size-weighted t -3.42). The sign is not stable by year: Friday moves reversed in 2018–2020 (t about +2.2 to +2.3 each year) and continued in 2022–2024 (t down to -3.08).
- **F7:** The book's gain is carried by Monday. Its mean daily return is 0.196 % on Mondays, 0.033 % on Tuesdays and -0.037 % on Sundays, where the entry fees fall. Its yearly Sharpe was negative only in 2022 (-0.32) and near zero in 2023 (0.03), the same years in which Sunday's reversal was weakest (2022 t 0.58).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence` (from F1, F2, F4): A coin's Sunday close-to-close move is undone over the next 2 days (Monday and Tuesday) more strongly the higher the coin's past 20-day volatility stands relative to its usual 60-day volatility, with the larger moves reversing the most.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g2_countertrend-sunday-moves-reverse` (from F3, F4): A Sunday move that runs against the coin's previous 4-day move reverses over the next 2 days more than one that extends it, and the more strongly Sunday's move opposes the prior 4-day move, the larger the reversal.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g3_friday-move-carries-weekend` (from F6): A coin's Friday close-to-close move continues in the same direction over the next 3 days (Saturday to Monday), more so the larger the Friday move and the higher the coin's recent volatility relative to its usual level.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
