---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal
line: 7.g patterns
backtest: 016-08_down-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the late-UTC-evening hours, the more a coin has fallen over its past 24 hours as of the 20:00 UTC close, the more it rises over the next 2 hours.
Consequence: A trader could buy coins that are down on the day into the 21–22 UTC hours for a short rebound, and refuse to short them there.
Why:
- F1: Hourly returns are strongly positive at 21 and 22 UTC: mean 5.5e-4 (t 6.87) and 4.4e-4 (t 5.76) per bar, about 17,400 bars each. Every coin is positive over these two hours (t 3.0 to 4.6 across all six), and 7 of 8 years are positive (2022 is -2.2e-4, t -1.46). No other hour reaches t 3.9 in absolute value.
- F2: The 2-hour return from the 20 UTC close grows with the coin's prior 24-hour fall. The lowest prior-24-hour-return quintile earns 2.29e-3 (t 7.03); the fourth quintile earns 0.0 (t 0.02). Low half minus high half is 7.8e-4 (Welch t 3.64, n 17,052). The Spearman rho is negative in all six coins (-0.056 to -0.083, all p < 0.005). Outside hours 21 and 22, the same prior-20-hour quintiles show no such gradient. The effect is short-lived: at 6 hours the low-minus-high difference turns to -8.0e-4 (t -2.14).
