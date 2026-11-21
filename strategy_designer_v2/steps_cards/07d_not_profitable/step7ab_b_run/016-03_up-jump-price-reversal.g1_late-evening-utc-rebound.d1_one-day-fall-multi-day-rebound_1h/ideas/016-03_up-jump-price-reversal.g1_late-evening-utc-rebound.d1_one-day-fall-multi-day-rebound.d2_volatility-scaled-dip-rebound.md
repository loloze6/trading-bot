---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its last 24 hours relative to its typical hourly moves of the last 30 days, the more it rises over the next 3 days, only while its price is above its average price of the last 30 days.
Consequence: A trader sizes the rebound bet by how unusual the one-day fall is for that coin, which concentrates the position in the cases whose move is many times a round trip.
Why:
- F4: The rebound sits in the deepest falls and is not graded across the rest. On the 2,054 grid cases with a positive forecast, the 72-hour excess return by forecast quartile is -0.03 %, -0.27 %, -0.69 % (t -2.1), then +1.22 % (t 3.5) in the deepest quartile only.
- F5: Measured against the coin's own hourly volatility over the last 30 days, the 24-hour fall separates the cases more sharply. The deepest quartile is followed by +1.93 % over 72 hours (t 5.2, 514 cases); the other three quartiles give -0.27 %, +0.32 % and +0.04 %.
- F6: The deepest falls rebound most when the coin is above its 30-day average.
- F7: As tested, the idea's unusual move is +0.06 % per case, 0.3 times the 0.19 % round-trip cost. In the deepest quartile above the 30-day average, the total move is +2.83 % per case. That is about 15 times the cost, and still several times the cost once the coin's normal drift of about 0.4 % over 72 hours is removed.
- F8: The book's 30-day context matters for the forecast itself. The forecast is standardised over its last 60 hours, so it grades a fall against the last 2.5 days, not against the coin's usual volatility. This is why its middle quartiles carry no rebound (F4), while the volatility-scaled fall does (F5).
