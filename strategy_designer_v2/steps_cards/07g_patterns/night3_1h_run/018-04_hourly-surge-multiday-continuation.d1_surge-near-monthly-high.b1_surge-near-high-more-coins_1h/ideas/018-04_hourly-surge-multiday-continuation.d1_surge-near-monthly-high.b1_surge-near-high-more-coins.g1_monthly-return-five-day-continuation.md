---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day return at an hourly close, the more its price rises over the next 5 days beyond its usual 5-day return.
Consequence: A trader would hold a coin long for days in proportion to how strongly it has risen over the past month, and refuse longs in coins whose month has been flat or falling.
Why:
- F1: The 5-day move rises step by step with the coin's own 30-day return at an hourly close. On non-overlapping 120-hour cells, the top fifth of 30-day returns is followed by an unusual move of +1.26 % (t 2.95, 1076 cases, strength 0.107) and the fourth fifth by +0.52 % (t 1.29). The three lower fifths are followed by −0.55 %, −0.99 % and −0.67 % (t −1.57, −3.28, −2.14). The t's pool 19 coins over shared dates, so they overstate independence.
- F2: The book earns almost only while the coin's 30-day return is high. Its hourly position gain is 1.59 and 1.55 bps in the top two fifths of 30-day return, against 0.15, −0.74 and 0.25 bps in the three lower fifths (about 107,500 position-hours each).
- F6: The book is mostly the coins' own direction:
