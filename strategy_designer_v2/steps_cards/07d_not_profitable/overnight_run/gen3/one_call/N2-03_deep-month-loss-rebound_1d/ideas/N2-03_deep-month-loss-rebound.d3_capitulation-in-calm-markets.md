---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.d not profitable
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A deep 20-day fall whose last 5 days are still down, in calm or ordinary volatility, is followed by an above-usual rise. This is a capitulation-type rebound.
Consequence: Take rebound longs on deep falls while selling is still active in calm markets, and refuse them once a bounce has started or volatility is extreme.
Why:
- F6: Among deep falls, those still falling over the last 5 days do better. Their 10-bar excess return is +1.35% (t 1.62, n=302), against -0.79% (t -0.65, n=112) when the last 5 days were already up. Deep falls in the most volatile third of bars show -0.61% (t -0.54, n=146).
- F4: Small forecasts lose and deep ones gain. Over non-overlapping 20-bar periods, forecasts between 0 and 2 are followed by -4.36% excess return (t -2.63, n=167), while forecasts of 5 or more are followed by +3.11% (t 2.06, n=216). The two lower forecast quartiles show -3.7% and -3.9% (t about -1.8 to -1.9, n=105 each).
