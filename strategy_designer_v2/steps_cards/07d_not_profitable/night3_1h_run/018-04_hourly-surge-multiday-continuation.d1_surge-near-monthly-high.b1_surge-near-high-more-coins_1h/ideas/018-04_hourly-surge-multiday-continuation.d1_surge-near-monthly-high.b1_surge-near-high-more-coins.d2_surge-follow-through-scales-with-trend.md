---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: After an hourly upside surge in a coin, the rise over the next 5 days is larger the larger the coin's 30-day return at that hour.
Consequence: A trader would size surge trades by the coin's 30-day return and stand aside from surges after a month of decline.
Why:
- F3: The trades' net result rises steadily with the coin's 30-day return at entry. Over 8,376 trades the mean net result by quintile was:
- F5: Surge size is not graded in the trades. Mean net was +5.33 % for the smallest surges (0.17 to 1.24 usual daily moves), +0.63 % for the middle quintile (1.62 to 2.05) and +5.52 % for the largest (above 2.71). The surge's size adds no ordering of its own; the ordering comes from the coin's trend and its nearness to the high.
- F6: The idea is large enough to pay its costs. The total move is +1.18 % per case over 5 days, 5.3 times the 0.22 % cost of a trade, and the unusual move is +0.35 %, 1.6 times the cost. Trades held 426 hours on average, with a mean net result of +3.29 %, a median of −1.97 % and a 41 % win rate. The failure is the depth of the falls, not the cost of trading.
