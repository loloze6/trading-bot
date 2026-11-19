---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the two hours from 21:00 to 23:00 UTC that follow, and the more so the higher the coin's own volatility over the past 20 days.
Consequence: A trader would put the evening rebound trade where the coin is turbulent and refuse it in calm markets, where the rise does not cover the cost.
Why:
- F1: Fees, not the forecast, sink the book: the summed position gain before fees is 5.29 against 9.49 in fees; trades last a median 2 hours with a mean gross gain of 0.01–0.31% per trade against a mean commission of 0.27–0.54%, so four of six coins lose net (XRP −0.089%, XMR −0.061%, LTC −0.035% per trade).
- F3: The rebound sits in high-volatility states, where the sizing holds the least: among positive-forecast cases, the high-volatility tercile earns 0.23% over 2 hours and 0.38% over 24 hours, against 0.062% and 0.054% in the low-volatility tercile, while the mean position is 0.29 against 0.65 (n ≈ 2,688 each).
