---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.b inconclusive
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC (the altcoin's bars plus BTC's bars on the same day)
bar: 1d
period: folds A, B, C, D
---
Idea: When an altcoin is up over 20 and 60 days in high volatility with an unusually large 20-day run-up, and BTC on the same daily bar is in the same strong, volatile run-up, the altcoin rises more than its usual 5-day return over the next 5 days.
Consequence: A trader would take altcoin momentum longs only when BTC is also in a strong volatile run-up, and refuse them when the altcoin's run-up is on its own.
Why:
- F3: Among altcoins, the effect appears only when BTC is itself in a strong run-up on the same bar: mean excess +2.74% (t=2.12, n=126, hit 51%) when BTC's forecast is also ≥10, against −0.50% (t=−0.47, n=180, hit 43%) when it is not. BTC's own cases give +1.63% (t=1.79, n=63, hit 54%).
- F2: The market's own move drowns the effect: the excess return of the cases correlates 0.68 with the six-coin mean 5-bar move, and that move explains 46% of their variance. Net of the market the mean is only +0.28% (t=0.54, n=369). For altcoins, the excess is +6.7% (t=6.15, n=160) when BTC's next 5 bars rise and −5.5% (t=−5.34, n=146) when they fall.
