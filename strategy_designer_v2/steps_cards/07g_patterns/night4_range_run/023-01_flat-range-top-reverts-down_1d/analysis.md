---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down_1d
idea tested: 023-01_flat-range-top-reverts-down
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5079 USD
---
## Findings
- **F1:** Saturday is the one day that stands out across all seven weekdays: the coins' daily return from Friday's close to Saturday's close, averaged over the six coins each day, is +0.454 % with t 3.04 on 414 days (no other weekday reaches t 2 on that coin-averaged series), and against all other days the Welch t is 4.26.
- **F2:** The Saturday rise holds coin by coin and year by year: its mean is positive in all six coins (ETH 0.40 % t 2.40, LTC 0.57 % t 2.92, XMR 0.45 % t 2.57, XRP 0.57 % t 2.15, ZEC 0.58 % t 2.30, BTC 0.16 % t 1.40; 414 days each), and positive in 7 of 8 years, with t above 2.7 in 2019, 2020, 2024 and 2025, near 0 in 2022 (0.07 %) and 2023 (−0.001 %).
- **F3:** The Saturday rise is larger in the more volatile half of each coin's 20-day volatility (0.45 % t 2.74 and 0.47 % t 1.74 in the top two quartiles, 0.29 % and 0.23 % in the bottom two, about 522 days each), so the grading is loose and not monotone; the 20-day window includes Saturday's own bar, so this ordering is weak evidence.
- **F4:** The tested reversion is absent in flat coins: on 5-day grid cases with the 30-day net move at most 0.33 of the range, the range position's Spearman correlation with the next 5 days' unusual move is −0.035 (p 0.30, n 917), and its quintiles show no ordering (strengths 0.007, −0.061, 0.012, 0.077, −0.095, none with |t| above 1.6); the book earned 7.5e-05 a day with Sharpe 0.16 against holding's higher Sharpe.
- **F5:** Continuation at the top of the range in trending coins does not survive a robustness check: the top range-position quintile has strength +0.174 (t 2.64, n 329) and the overall Spearman is 0.048 (p 0.054, n 1638), but by coin only ETH is significant (0.134, p 0.022), and by year the sign flips (2020 +0.120, 2022 −0.153 p 0.034, 2025 −0.132), so I do not count it as a finding to build on.

## Ideas
- `023-01_flat-range-top-reverts-down.g1_saturday-drift-scaled-by-volatility` (from F1, F2, F3): A coin rises from Friday's daily close to Saturday's daily close, and the rise is larger the higher the coin's 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
