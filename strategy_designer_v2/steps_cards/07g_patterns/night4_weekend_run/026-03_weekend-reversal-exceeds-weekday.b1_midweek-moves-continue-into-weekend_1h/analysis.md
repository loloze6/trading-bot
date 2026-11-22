---
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3795 USD
---
## Findings
- **F1:** The Friday-Saturday continuation is carried by midweek rises. After a Wednesday-Thursday rise the drift-removed 48-hour move is +0.70 % (t 3.77, 1138 cases, slope t 3.69). After a midweek fall it is only +0.09 % (t 0.50, 1254 cases, slope t -0.64). By quintile of the midweek move, the top quintile earns +1.36 % (t 4.19, 480 cases) and the bottom three are near zero (t between -0.25 and 0.52).
- **F2:** The book shows the same split. Long trades earn +0.62 % per trade after fees and short trades lose -0.94 %. Every quartile of entry forecast loses after fees (from -0.11 % to -0.30 % per trade).
- **F3:** Hours 20:00 and 21:00 UTC carry the largest hourly drift of the day across the six coins: +0.055 % (t 6.75) and +0.044 % (t 5.66), about 17,400 cases each. That 2-hour return falls as the coin's return over the prior 20 hours rises (slope -0.000701 per standard deviation, t -5.85, 15,966 cases). After the lowest-quintile 20-hour moves it is +0.17 % (t 4.39); after the middle quintile it is about 0 (t -0.08).
- **F4:** The 20:00-21:00 UTC rise is concentrated in the high-volatility tercile: +0.136 % (t 4.90) there, against +0.014 % (t 1.00) and -0.000 % (t -0.02) in the lower two. The rise is positive in 6 of 8 years (2020 t 4.29, 2021 t 4.36, 2024 t 2.84) and negative in 2018 and 2023.
- **F5:** The brief's own situation does not appear. Among 48-hour-back to 48-hour-forward fits by start weekday, only the Friday start is significant (slope 0.056, t 3.38, 2392 cases). The Monday start, which is the weekend move followed by Monday-Tuesday, has slope -0.017 (t -0.62), and no other weekday has |t| above 1.6.
- **F6:** The tested idea is unstable across coins and years. By coin, only ZEC is significant (t 3.53); the others range from t -1.70 (XMR) to t 1.24 (XRP). Yearly slope t values swing from 4.12 (2018) and 3.88 (2025) to -1.98 (2019) and -1.83 (2020).

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.g1_midweek-rises-run-into-weekend` (from F1, F2, F6): A coin's 48-hour rise over Wednesday and Thursday is followed by a further rise over the next two days, Friday and Saturday, and the larger the midweek rise, the larger the rise that follows.
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend.g2_evening-rebound-after-day-s-fall` (from F3, F4): When a coin is in a turbulent period (its 30-day hourly volatility high for it), its fall over the 20 hours up to the 19:00 UTC close is followed by a rise over the next two hours, 20:00 to 22:00 UTC. The larger that fall relative to its 30-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
