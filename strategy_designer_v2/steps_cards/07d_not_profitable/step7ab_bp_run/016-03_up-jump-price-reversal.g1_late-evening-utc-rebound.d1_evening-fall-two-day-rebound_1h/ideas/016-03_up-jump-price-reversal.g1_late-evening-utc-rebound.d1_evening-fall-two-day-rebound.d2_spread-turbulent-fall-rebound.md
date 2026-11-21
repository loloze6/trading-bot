---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days, only while that day's hourly volatility is high against the past 30 days, and the more so the more evenly the fall was spread across the 24 hours rather than made by its largest hour.
Consequence: On a turbulent day a fall built across many hours is the one to buy for two days, while a fall made by one violent hour gives little rebound.
Why:
- F3: Depth and turbulence together carry the idea. Deeper-than-median falls in the top turbulence tercile earn +0.95 % excess over 48 hours (t 3.42, n 800), strength 0.13, total move +1.22 %, which is 6.4 times the cost. The same deep falls in the bottom tercile lose -0.69 % (t -2.58, n 568), strength -0.10.
- F5: Within turbulent days, a fall spread across many hours rebounds more than one made by a single hour. With the largest hour's share of the day's total absolute move as the jump measure, high-turbulence low-jump falls earn +1.42 % excess (t 3.25, n 341, strength 0.21), while high-turbulence high-jump falls earn +0.08 % (t 0.28, n 600). Calm-day jump-made falls keep falling, at -0.91 % (t -2.89, n 319).
- F6: The idea's horizon is right; its move does not outlast 2 days. The fall evenings' excess is +0.22 % over 96 hours (t 0.94, n 2144) and -0.13 % over 168 hours (t -0.34, n 1158).
