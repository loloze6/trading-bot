---
line: 7.g patterns
backtest: 032-01.b1_flat-range-upside-breaks-continue_1d
idea tested: 032-01.b1_flat-range-upside-breaks-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4252 USD
---
## Findings
- **F1:** In flat coins (60-day efficiency ratio below 0.3), the coin's 20-day return divided by its 20-day volatility ranks its next unusual move. Spearman is 0.168 over 5 days (704 non-overlapping cases, p 7e-6), 0.231 over 10 days (311 cases, p 4e-5) and 0.274 over 20 days (115 cases, p 0.003). The trending cases show no such link (11 cases, −0.49, p 0.13).
- **F2:** Sorting the flat-coin cases into quintiles of that 20-day z-score, the mean unusual 10-day move rises from −2.6 % and −5.8 % in the two lowest quintiles to +2.3 % and +8.2 % in the two highest (about 62 cases each). The rank link is positive in all six coins, from 0.03 for BTC to 0.41 for ETH, and in 2019–2021 (0.10 to 0.24), but negative in 2018 (−0.17, 70 cases).
- **F3:** Where the close sits in its prior 60-day high–low range also ranks the next unusual move in flat coins. Spearman is 0.143 over 5 days (704 cases, p 1.4e-4), 0.174 over 10 days (311 cases, p 0.002) and 0.273 over 20 days (115 cases, p 0.003). The tested breakouts above the 60-day high in flat coins gained an unusual +9.9 % over 20 days (37 cases, t 2.09, 73 % positive), against −5.7 % in trending coins (9 cases).
- **F4:** A coin's one-day return ranks the next day's return negatively, with a Spearman of −0.105 over all bars (p 1e-22). The link is stronger after Thursdays (−0.136, 1,242 cases, p 1e-6). The longer link runs the other way: in flat coins, the one-day move scaled by volatility ranks the next 5 days positively (0.127, 704 cases, p 0.0007).
- **F5:** Fridays and Saturdays earn more than the other weekdays. Mean daily returns are +0.54 % on Friday (t 3.75) and +0.58 % on Saturday (t 4.24), against −0.35 % on Thursday (t −1.94). The gap is positive in all six coins and in 2018–2020, but absent in 2021 (−0.02 %). This is not graded, so it yields no idea here.
- **F6:** The book's daily return is near zero in every window, from −0.021 % to +0.066 % a day. Its trades gain more as the entry forecast rises: a mean net gain of 3.1 %, 6.9 % and 8.2 % across forecast terciles, 47 trades each. By coin, the mean net trade ranges from −6.1 % for LTC to +17.4 % for XRP.

## Ideas
- `032-01.b1.g1_flat-coin-twenty-day-momentum` (from F1, F2): In a coin whose price has gone nowhere over the past 60 days, the larger its 20-day return relative to its own daily volatility, the larger its move in the same direction over the next 10 days: strong 20-day gains are followed by further rises and strong 20-day losses by further falls.
- `032-01.b1.g2_range-position-predicts-drift` (from F3, F1): In a coin whose price has gone nowhere over the past 60 days, the higher its close sits within its prior 60-day high–low range, the larger its rise over the next 20 days.
- `032-01.b1.g3_one-day-move-reverses-next-day` (from F4): The larger a coin's one-day return, the more of it the coin gives back over the next day, in either direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
