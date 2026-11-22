---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch with a wide high-low range while its volatility over the past 7 days is low against its volatility over the past 60 days, it earns less than its usual return over the next 14 days, the lower that volatility ratio, the weaker the return.
Consequence: A trader would refuse to buy, or would sell, a sharp drop that hits a calm market, since it tends to start further decline rather than a rebound.
Why:
- F4: The effect depends on the 7-day/60-day volatility ratio at the signal bar:
- F1: The book's deepest fall is −76.5 % against a yearly return of 26.8 % (Calmar 0.34). The fall ran 277 days across windows w12 to w14, while the coins fell −79.0 % together. So the book fell almost exactly as much as the coins did.
