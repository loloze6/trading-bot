---
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum_1d
idea tested: N2-04_slow-and-fast-momentum
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3158 USD
---
## Findings
- **F1:** Inside the trend regime (forecast > 0), a down day bigger than half the coin's 20-day daily standard deviation was followed by a next-day mean return of +0.61%. This is averaged across coins per day, then tested over 516 independent days: t = 2.95. That is about twice the next-day return after an ordinary active day (+0.30%, t = 2.11, 1052 days) or an up day (+0.28%, t = 1.80, 808 days).
- **F2:** The bounce after a down day shows up in all 6 coins and in 7 of 8 years. In every coin, the next-day mean after a down day (+0.27% to +0.83%) is above the mean after other days (−0.14% to +0.10%). The only year where it is not higher is 2024 (+0.08% vs +0.30%). Outside the trend regime the bounce is weaker: +0.32%, t = 1.98, over 1000 days.
- **F3:** Measured per bar rather than per day, the same reversal holds. Moves between −1.5 and −0.5 standard deviations were followed by +0.47% the next day (t = 5.05, 2977 coin-days, not independent across coins). Moves between +0.5 and +2.5 standard deviations were followed by −0.04% and +0.18%, neither different from 0.
- **F4:** The 20-day trend edge itself is weak, which agrees with the verdict. Active 20-bar blocks earned an excess of +2.1% (t = 0.93, 262 blocks). Blocks where both the 60-day and 20-day returns were positive earned +3.3% (t = 1.50, 141 blocks).
- **F5:** The book's profit comes from the few trades that last. The 1019 trades held 3 days or less (40% of all trades) lost about −3.6% each. The 787 trades held more than 10 days averaged +10.5% (10–30 days) and +87.8% (over 30 days). The median trade is negative in every coin.
- **F6:** The next-day return following a weekday-4 bar was +0.37% when averaged across coins per day (t = 2.31, 345 days). Weekday-3 and weekday-4 bars together beat the other weekdays in 5 of 6 coins and 6 of 8 years. This is the strongest of 7 weekdays tested, so it is weaker evidence than F1.

## Ideas
- `N2-04_slow-and-fast-momentum.g1_buy-dips-inside-uptrends` (from F1, F2, F3, F4): In a coin whose 20-day and 60-day returns are both positive, a daily close that falls by more than half its recent daily standard deviation is followed by an above-average return over the next day.
- `N2-04_slow-and-fast-momentum.g2_one-day-rebound-after-drops` (from F2, F3): In any regime, a coin's large down day is followed by a next-day return above the coin's average, while a large up day is not.
- `N2-04_slow-and-fast-momentum.g3_late-week-daily-drift` (from F6): A coin's return over the day after a weekday-4 bar is higher than its return after the other weekdays' bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
