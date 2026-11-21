---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound, only while its hourly volatility over the past 3 days is high against its hourly volatility over the past 30 days, with the rebound larger the higher that ratio.
Consequence: Size the rebound purchase up when a drop came with a burst of volatility (forced flow), and refuse quiet declines that tend to keep drifting down.
Why:
- F5: The rebound is carried by agitated markets. Active cases where the 3-day hourly volatility was high against the 30-day volatility returned +0.0086 over the next 3 days (t 2.58, n 679). The calm third returned -0.0019 (n 678).
- F4: Only the strongest forecasts pay. Active cases in the forecast's top third had a mean excess 3-day return of +0.0047 (t 1.71, n 921). The low third had -0.0035 (t -1.30, n 921) and the middle third -0.0057 (t -2.09, n 920), yet the book holds a position on all of them.
- F1: The book barely earns while simply holding the coins earns far more. Its mean daily return is 5.6e-05 against roughly 0.0007–0.0016 a day for holding each coin. Its chained yearly return is -0.7%, with a deepest fall of -49%. Its 3761 trades average -1.35% before fees and -1.45% after, with a 48.8% win rate.
