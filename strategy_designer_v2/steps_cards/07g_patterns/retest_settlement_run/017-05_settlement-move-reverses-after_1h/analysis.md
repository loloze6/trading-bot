---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
idea tested: 017-05_settlement-move-reverses-after
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4183 USD
---
## Findings
- **F1:** The 2-hour reversal is not tied to funding settlement. Measured on every bar, the drift-removed contrarian 2-hour return after a 2-hour move is +0.062 % (t 4.9) for bars closing at 00:00 UTC, +0.009 % (t 0.8) at 08:00 and +0.042 % (t 3.4) at 16:00. Non-settlement closes are as large or larger: +0.082 % (t 6.6) at 12:00, +0.072 % (t 6.5) at 21:00 and +0.071 % (t 6.2) at 01:00. This is the brief's third way of being wrong.
- **F2:** After a large one-day move, the coin gives part of it back over the next day. On a non-overlapping 24-hour grid, the top quintile of |24h return| is followed by a drift-removed contrarian 24-hour return of +0.710 % (t 5.8, 3190 cases), and the total move including drift is +0.704 %. That is about 3.7 times the 0.19 % cost of a trade, against 0.05 % per case for the tested idea.
- **F3:** The one-day reversal is graded and concentrated in the largest moves. By quintile of the 24-hour move scaled by 30-day volatility, the contrarian return rises from −0.118 % (t −1.4) through +0.017 %, +0.287 % (t 3.2) and +0.508 % (t 4.8). Regressing the next-day return on the past-day return gives a negative slope in all 6 coins (−0.068 to −0.126, p ≤ 0.0004).
- **F4:** The one-day reversal grows with the volatility regime. Among large moves, it is +0.043 % (t 0.4) in the lowest quartile of last-day volatility over 30-day volatility and +0.938 % (t 5.5) in the highest. By tercile of 30-day volatility, it is −0.079 % (t −0.7) in the lowest and +1.531 % (t 6.0, 969 cases) in the highest.
- **F5:** The one-day reversal is broad but has faded recently. It is positive in 18 of 24 windows and in all 6 coins (+0.28 % to +0.57 % for the top two quintiles), and it holds after falls (+0.482 %, t 4.3) and after rises (+0.295 %, t 3.0). It is near zero in 2024 (−0.016 %) and 2025 (+0.004 %), against +0.49 % to +0.67 % in 2018, 2019 and 2021–2023.
- **F6:** The 2-hour reversal is strongest at the US open. For bars closing at 12:00–14:00 UTC, the top quintile of |2h move| is followed by a contrarian 2-hour return of +0.271 % (t 7.2, 3915 cases), against +0.061 % (t 5.9) at the other hours. Within those hours it grows from −0.009 % in the second quintile to +0.090 % (t 3.6) in the fourth and +0.271 % in the fifth.
- **F7:** The book lost money before fees, so cost was not its only problem. Its 65,566 trades, with a median hold of 120 minutes, average −0.078 % gross and −0.178 % net. Every coin's book loses between −0.14 % and −0.33 % a day while the coins gain +0.07 % to +0.16 % a day.
- **F8:** Large 2-hour and 8-hour moves also reverse over the following day, by more than a trade costs. The top decile of |2h move| is followed by +0.526 % (t 3.3) over the next 24 hours, and the top decile of |8h move| by +0.643 % (t 3.8).

## Ideas
- `017-05_settlement-move-reverses-after.g1_one-day-large-move-reversal` (from F2, F3, F5): The larger a coin's 24-hour return against its usual daily move over the past 30 days, the more of it the coin gives back over the next 24 hours.
- `017-05_settlement-move-reverses-after.g2_reversal-in-volatility-bursts` (from F4, F3): When a coin's volatility over the past day is high against its volatility over the past 30 days, its 24-hour return is given back over the next 24 hours, more so the larger that return is.
- `017-05_settlement-move-reverses-after.g3_us-open-move-reversal` (from F6, F1): The larger a coin's 2-hour return into the US market open, read at a bar closing between 12:00 and 14:00 UTC, the more of it the coin gives back over the next 2 hours.
- `017-05_settlement-move-reverses-after.g4_intraday-move-reverses-next-day` (from F8, F3): The larger a coin's 8-hour return against its usual 8-hour move over the past 30 days, the more of it the coin gives back over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
