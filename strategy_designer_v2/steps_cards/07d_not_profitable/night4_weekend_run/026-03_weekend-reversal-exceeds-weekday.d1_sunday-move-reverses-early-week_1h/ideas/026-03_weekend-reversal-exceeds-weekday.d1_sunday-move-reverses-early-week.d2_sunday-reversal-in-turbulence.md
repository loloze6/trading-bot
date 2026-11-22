---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only while the coin's 30-day volatility of hourly returns is high: the higher that volatility and the larger Sunday's 24-hour return, the larger the opposite move over the next two days.
Consequence: A trader would fade Sunday's move mostly in turbulent markets, where the reversal is several times the cost of a trade, and largely skip calm weeks, where it does not cover the fee.
Why:
- F5: The effect lives in volatile markets. Ranked by the coin's 30-day hourly volatility, the bottom two quartiles gain +0.05 % (t 0.23) and +0.15 % (t 0.56), under the trade's cost. The top two gain +0.89 % (t 3.05) and +1.17 % (t 2.81), about 597 cases each.
- F6: The failures show up in the falls and the daily gain. The book's daily chain falls by up to 31.0 % (worst in w13, w12, w9), giving a Calmar of 0.12, and its mean daily return is 0.014 %. Mondays (mean +0.108 %, standard deviation 1.78 %) and Tuesdays (+0.036 %, standard deviation 1.53 %) carry all of the risk. All 40 of the book's worst days fall on Monday (23) or Tuesday (17), so the falls come from the bets themselves, half of them the dead same-direction weekends.
