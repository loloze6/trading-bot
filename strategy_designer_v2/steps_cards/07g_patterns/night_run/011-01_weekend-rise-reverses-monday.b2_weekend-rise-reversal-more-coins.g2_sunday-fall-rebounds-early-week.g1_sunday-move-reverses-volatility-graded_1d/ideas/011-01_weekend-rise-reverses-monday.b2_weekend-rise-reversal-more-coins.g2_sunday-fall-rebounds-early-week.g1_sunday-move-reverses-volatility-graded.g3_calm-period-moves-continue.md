---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is low, its 1-day return in units of that volatility is followed by a move the same way over the next day. The continuation is larger the larger the move.
Consequence: A trader should refuse to fade daily moves in calm periods and can lean with them instead.
Why:
- F1: Daily moves reverse only when the coin's own 20-day volatility is high, and the effect is graded. In the top volatility tercile, the excess next-day return taken against the sign of the day's vol-scaled move averages +0.46% (t 6.43, n 10814), and the slope of next-day excess return on the move is −0.0058 (t −7.8). In the bottom tercile the same fade averages −0.10% (t −2.65). The high-volatility reversal also holds on non-overlapping grids: +0.49% over 2 days (t 3.21, n 5333) and +0.75% over 3 days (t 3.53, n 3592).
- F5: In calm periods moves continue rather than reverse. In the lowest volatility tercile, the next-day fade has t −3.40, −3.95 and −3.71 on Wednesday, Thursday and Friday bars. The overall slope of next-day return on the move in that tercile is +0.0013 (t 3.6).
