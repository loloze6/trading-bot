---
line: 7.g patterns
backtest: 032-02.b1.e2_tight-range-breakouts-continue_1d
idea tested: 032-02.b1.e2_tight-range-breakouts-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3706 USD
---
## Findings
- **F1:** A coin's own 20-day return predicts its next 10-day move beyond its normal drift. Over non-overlapping 10-day cases (702 cases, folds B and C), the rank correlation is 0.125 (t 3.33). It rises to 0.138 (t 3.69) when the 20-day return is divided by the 20-day volatility. The sign-weighted unusual move is +2.04 % per case (day-clustered t 1.97).
- **F2:** The 20-day momentum effect points the same way in all six coins, with per-coin rank correlations from 0.080 (XMR) to 0.151 (ETH), 117 cases each. It also points the same way in 3 of 4 years (0.147 in 2019, 0.076 in 2020, 0.118 in 2021), but reverses in 2018 (−0.182).
- **F3:** The momentum effect is concentrated in trendless coins. With the 60-day efficiency ratio at or below 0.15, the rank correlation between the 20-day return and the 10-day unusual move is 0.187 (225 cases). Between 0.15 and 0.30 it is 0.236 (158 cases). Above 0.30 it is −0.028 (31 cases).
- **F4:** Grouped by 20-day return quintile, the 10-day unusual move climbs from −0.74 % and −3.83 % (t −3.08) in the lower two quintiles to +2.56 % and +2.97 % (t 1.83 and 1.81) in the top two. That pattern runs against the brief's fade-the-break premise and is consistent with the tested idea's continuation.
- **F5:** Coins returned more on Fridays and Saturdays (UTC) than on other days. The mean is +0.58 % on Saturday (t 4.24) and +0.54 % on Friday (t 3.75). Fridays and Saturdays together beat the other days with Welch t 4.83 (2,473 against 6,216 coin-days). This holds in all six coins and in 2018–2020, but not in 2021 (0.39 % against 0.42 %). It is a calendar effect with no grading, so I propose no idea from it.
- **F6:** The book's gain rests on very few days. Its 10 best days sum to 0.283, equal to its whole summed daily return over folds B and C (0.283), and its 10 worst sum to −0.205. Its daily returns correlate 0.51 with holding the coins.
- **F7:** The 60-day breakouts that the tested idea trades are rare on a 10-day grid: only 11 upside-break cases in folds B and C. Among them, the overshoot past the high ranks +0.38 with the move that follows, and the range width ranks −0.57. These are too few to count as a finding beyond the tested idea.

## Ideas
- `032-02.b1.e2.g1_choppy-coin-twenty-day-momentum` (from F1, F2, F3, F4): In a coin whose past 60 days have been trendless, the larger its 20-day return relative to its own daily volatility over those 20 days, the further the coin moves the same way over the next 10 days, beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
