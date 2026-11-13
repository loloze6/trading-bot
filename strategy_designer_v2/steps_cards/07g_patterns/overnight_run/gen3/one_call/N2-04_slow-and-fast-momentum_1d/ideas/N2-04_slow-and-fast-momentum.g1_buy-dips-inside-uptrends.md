---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day and 60-day returns are both positive, a daily close that falls by more than half its recent daily standard deviation is followed by an above-average return over the next day.
Consequence: A trend follower should add to, or enter, its long on a down day inside an uptrend rather than on an up day.
Why:
- F1: Inside the trend regime (forecast > 0), a down day bigger than half the coin's 20-day daily standard deviation was followed by a next-day mean return of +0.61%. This is averaged across coins per day, then tested over 516 independent days: t = 2.95. That is about twice the next-day return after an ordinary active day (+0.30%, t = 2.11, 1052 days) or an up day (+0.28%, t = 1.80, 808 days).
- F2: The bounce after a down day shows up in all 6 coins and in 7 of 8 years. In every coin, the next-day mean after a down day (+0.27% to +0.83%) is above the mean after other days (−0.14% to +0.10%). The only year where it is not higher is 2024 (+0.08% vs +0.30%). Outside the trend regime the bounce is weaker: +0.32%, t = 1.98, over 1000 days.
- F3: Measured per bar rather than per day, the same reversal holds. Moves between −1.5 and −0.5 standard deviations were followed by +0.47% the next day (t = 5.05, 2977 coin-days, not independent across coins). Moves between +0.5 and +2.5 standard deviations were followed by −0.04% and +0.18%, neither different from 0.
- F4: The 20-day trend edge itself is weak, which agrees with the verdict. Active 20-bar blocks earned an excess of +2.1% (t = 0.93, 262 blocks). Blocks where both the 60-day and 20-day returns were positive earned +3.3% (t = 1.50, 141 blocks).
