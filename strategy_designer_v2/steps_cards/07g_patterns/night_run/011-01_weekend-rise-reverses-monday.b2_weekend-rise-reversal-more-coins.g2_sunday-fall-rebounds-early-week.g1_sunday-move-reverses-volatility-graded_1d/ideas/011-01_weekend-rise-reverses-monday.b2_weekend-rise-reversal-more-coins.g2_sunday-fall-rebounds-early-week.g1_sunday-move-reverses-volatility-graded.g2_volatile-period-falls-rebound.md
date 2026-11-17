---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high, a fall measured in units of that volatility is followed by a rebound over the next day. The rebound is larger the deeper the fall.
Consequence: A trader can buy sharp vol-scaled falls in volatile periods at the close, with confidence growing with the size of the fall, and need not short sharp rises as hard.
Why:
- F1: Daily moves reverse only when the coin's own 20-day volatility is high, and the effect is graded. In the top volatility tercile, the excess next-day return taken against the sign of the day's vol-scaled move averages +0.46% (t 6.43, n 10814), and the slope of next-day excess return on the move is −0.0058 (t −7.8). In the bottom tercile the same fade averages −0.10% (t −2.65). The high-volatility reversal also holds on non-overlapping grids: +0.49% over 2 days (t 3.21, n 5333) and +0.75% over 3 days (t 3.53, n 3592).
- F4: The high-volatility reversal is lopsided toward falls. On non-Sunday high-volatility bars, the bottom quintile of vol-scaled moves (mean z −1.24) is followed by a +1.18% excess next-day return. The top quintile (mean z +1.46) is followed by only −0.27%. On Sundays, the top quintile is followed by −0.45% and the bottom by +0.61%.
