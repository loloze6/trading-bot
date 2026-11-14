---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A new 20-day closing high made while the close is still below the coin's 50-day average is followed by returns below the coin's average over the next days.
Consequence: Treat highs made under a falling or overhead 50-day average as failed rallies and refuse them, cutting the many short losing trades.
Why:
- F6: Entries made with the close below the 50-day average lose. These trades average -5.7% (median -7.4%, 27.5% winners, n 305), against +3.0% to +6.4% for the other quintiles.
- F5: The book's gain comes from a few long trades, and the many short ones lose (trades summed per trade, not book days). Of 3269 long trades, the median net return is -2.5% and 41% win. The 722 trades of 7 days or less average -4.85%, and those of 7 to 19 days average about -3.5%. The 620 trades longer than 29 days average +32.7%.
- F4: Held days with a falling 50-day average carry almost none of the book's gain. These 3695 held coin-days have a mean next-day book return of 0.0001 and contribute 0.08 of summed per-coin book return. The 5456 held days with a rising 50-day average have a mean of 0.0042 and contribute 3.84. This split is pooled coin-days, not the book's daily mean over coins.
