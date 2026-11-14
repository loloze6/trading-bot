---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In any regime, a coin's large down day is followed by a next-day return above the coin's average, while a large up day is not.
Consequence: A trader should avoid selling, or opening shorts, right after a sharp down day, since the next day tends to bounce.
Why:
- F2: The bounce after a down day shows up in all 6 coins and in 7 of 8 years. In every coin, the next-day mean after a down day (+0.27% to +0.83%) is above the mean after other days (−0.14% to +0.10%). The only year where it is not higher is 2024 (+0.08% vs +0.30%). Outside the trend regime the bounce is weaker: +0.32%, t = 1.98, over 1000 days.
- F3: Measured per bar rather than per day, the same reversal holds. Moves between −1.5 and −0.5 standard deviations were followed by +0.47% the next day (t = 5.05, 2977 coin-days, not independent across coins). Moves between +0.5 and +2.5 standard deviations were followed by −0.04% and +0.18%, neither different from 0.
