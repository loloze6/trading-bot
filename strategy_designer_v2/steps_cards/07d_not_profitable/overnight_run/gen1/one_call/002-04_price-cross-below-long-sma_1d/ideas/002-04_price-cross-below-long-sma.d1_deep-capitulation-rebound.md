---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has fallen more than half below its recent multi-week high and sits deep under its 200-day average, price tends to rise over the following two weeks rather than keep falling.
Consequence: A trader would refuse new shorts after deep capitulation drops and could lean long there instead.
Why:
- F2: A larger forecast loses more, the opposite of the theory. In the deepest forecast quintile (mean forecast -16.6, allocation -1.66) the coin then rose +0.29% per day and +2.67% over 10 bars, giving a gross of -0.0055 per bar. The middle quintiles sit near zero (-0.0001 to +0.0001).
- F3: The deepest falls rebound. When the close was more than 50% below its 60-day high, the coin's 10-bar excess return was +4.6% (t 1.99, up 57.8% of the time, n 512). Shorts there lost most.
- F7: The book was short in rising, falling-momentum states that rebounded. Active bars after a 20-day fall lost -0.0032 and -0.0031 gross in the mid and volatile terciles. Active bars after a 20-day rise in calm conditions earned +0.0002.
