---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 2 hours from 16:00 UTC follows the coin's 3-day move, and the stronger the 3-day rise, the larger the rise over those 2 hours, only while the coin's hourly volatility over the past 3 days is high, and the higher that volatility the larger the 2-hour move in the 3-day direction.
Consequence: A trader would lean with the 3-day trend in the European afternoon mainly on volatile days, when the move is large enough to pay a round trip, and stand aside on quiet days.
Why:
- F1: The book loses because each 2-hour slot pays more in fees than it earns: the mean gross gain is 0.000504 per slot (t 8.08, 17452 slots), the mean fee is 0.001017 (about 0.00107 per unit of turnover, paid on both entry and exit), so the net is -0.000513 per slot and the book's mean daily return is -0.000605, while holding the coin returned 0.001190 a day.
- F3: The gain grows with the 3-day trend's strength but never covers its fee. By third of |forecast|, the gross per slot is 0.000020, 0.000308 and 0.001185, against fees of 0.000314, 0.000952 and 0.001785. Even the strongest third nets -0.000600.
- F4: The signed move after the slot grows with the coin's recent hourly volatility while staying a constant share of it. The 2-hour return signed by the 3-day trend is 0.000331, 0.000571 and 0.001159 in the low, mid and high volatility thirds, which is 0.072, 0.073 and 0.078 of each third's hourly volatility. The volatility-targeted sizing therefore shrinks the position exactly where the move per round trip is largest against a fixed fee.
