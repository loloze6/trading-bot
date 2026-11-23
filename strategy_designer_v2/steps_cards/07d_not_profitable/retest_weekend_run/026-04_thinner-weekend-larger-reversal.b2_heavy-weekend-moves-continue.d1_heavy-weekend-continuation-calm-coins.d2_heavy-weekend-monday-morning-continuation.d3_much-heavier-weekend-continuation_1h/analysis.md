---
line: 7.d confirmed, not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7019 USD
---
## Findings
- **F1:** The continuation lives only in the heaviest-volume weekends. Ranking Sunday 23:00 cases by the weekend-to-weekday volume ratio, the top decile's signed 12-hour excess return is +0.93 % (t 3.03, 229 cases) and the ninth decile's is +0.45 % (t 1.67, 228 cases), while deciles 0–7 lie between −0.20 % and +0.17 % with every |t| below 0.9; across all Sundays the signed 12-hour continuation is only +0.09 % (t 1.22, 2286 cases).
- **F2:** The heavy-volume condition is not an effect of its own. On the 23:00 bars of Monday to Friday, the same top fifth of volume ratio gives signed 12-hour excess returns of −0.16 % to +0.27 % (all |t| ≤ 1.46, about 458 cases each) and −0.31 % on Saturday (t −2.01), against +0.93 % / +0.45 % on Sunday; heavy volume needs the weekend situation the theory gives it, the thin weekend.
- **F3:** The book loses its gain in positions it keeps long after Monday morning. The quarter of trades with the smallest entry |forecast| (mean 3.1) is held 230 hours on average and nets −0.21 % per trade (171 trades), while the two largest quarters are held about 8 hours and net +0.38 % and +0.37 %; this lingering exposure, about 10–18 % of cases still held 12 to 48 hours later, dilutes the mean daily return on days in a position to 0.047 %, under the 0.05 % rule.
- **F4:** Within the heaviest-volume fifth, weekend falls carry the effect. Falls continue by +1.19 % over the next 12 hours (t 3.42, 185 cases) and rises by only +0.34 % (t 1.40, 272 cases), yet the book holds rises with slightly more size (mean |allocation| 0.39 against 0.32).
- **F5:** Within the heaviest-volume fifth, the largest move tercile continues by +1.13 % over 12 hours (t 2.91, 153 cases) against +0.43 % and +0.49 % (t ≈ 1.4) for the smaller two, so the move's size grades the effect only at its top.
- **F6:** The effect extends over Monday and Tuesday. In the heaviest-volume fifth of Sundays, the signed excess return is +0.76 % over 24 hours (t 1.77) and +1.56 % over 48 hours (t 2.66, 229 cases in the top decile), so a longer holding roughly doubles the move against the same 0.19 % cost.
- **F7:** The book's falls are concentrated in the Monday trade. 32 of the 40 worst coin-days fall on Monday (sum −115.7 %), mostly XMR and ZEC (11 each). Monday carries the whole gain (sum of daily returns +1.42), Tuesday to Sunday together sum −0.27, and the maximum drawdown reaches 6.4 % against a yearly return of +2.3 % (Calmar 0.36). The heavy-volume effect is uneven by year: 12-hour excess of +3.16 % in 2022, −0.38 % in 2018 and −0.26 % in 2023.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.d1_heavy-weekend-falls-continue` (from F1, F2, F4, F5): A coin's Saturday-Sunday fall made on weekend volume heavier than its mean over the preceding five weekdays continues downward over the first 12 hours of Monday, more steeply the heavier the weekend volume is relative to the coin's own past weekends and the larger the fall.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.d2_heavy-weekend-two-day-continuation` (from F1, F2, F6, F7): A coin's Saturday-Sunday move made on weekend volume a multiple of its mean over the preceding five weekdays continues in the same direction over the next 48 hours, through Monday and Tuesday, more strongly the heavier the weekend volume relative to the coin's past weekends.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.d3_heavy-weekend-monday-only-continuation` (from F1, F3, F5, F7): A coin's Saturday-Sunday move made on weekend volume a multiple of its mean over the preceding five weekdays continues in the same direction over the first 12 hours of Monday only as far as the weekend volume ranks high among the coin's own past weekends, the continuation fading entirely by Monday afternoon.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
