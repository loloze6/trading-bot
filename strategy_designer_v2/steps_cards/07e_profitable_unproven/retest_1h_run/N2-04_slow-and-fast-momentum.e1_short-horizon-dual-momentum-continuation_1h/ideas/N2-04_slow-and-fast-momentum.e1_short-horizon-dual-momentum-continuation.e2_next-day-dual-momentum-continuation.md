---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 60-day and 20-day returns are both positive, its return over the next 1 day exceeds its average daily return, and more so the larger both returns are relative to their usual size.
Consequence: A trader expecting trend continuation should expect it at a horizon of about a day, re-checked daily, rather than over several days.
Why:
- F4: At a shorter horizon the plain in-situation continuation already passes. The 1-day excess return at forecast > 0 grid bars is +0.0016 (t 2.22, 5648 cases), and the forecast > 0 minus forecast ≤ 0 difference is t 2.78. At 3 days the same excess is t 1.66, at 7 days t 1.81 and at 20 days t 1.15.
- F3: The top-third effect is carried as much by the fast 20-day return as by the slow 60-day one. The top third of the standardised 20-day return gives a 3-day excess of +0.0125 (t 2.78, 620 cases) and a 1-day excess of +0.0044 (t 3.23, 1883 cases). The top third of the standardised 60-day return gives +0.0101 (t 2.31) and +0.0034 (t 2.57).
