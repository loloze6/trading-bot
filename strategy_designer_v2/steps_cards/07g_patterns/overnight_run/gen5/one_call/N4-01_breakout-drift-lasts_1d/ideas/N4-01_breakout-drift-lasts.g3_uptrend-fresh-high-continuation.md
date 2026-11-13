---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.g patterns
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, a close at the exact 20-day closing high, made while price is above its 50-day average, is followed by a larger rise over the next ten days than closes elsewhere in the 20-day range.
Consequence: A trader can take breakout longs only on fresh highs within an established uptrend, and hold them past short pullbacks instead of exiting within days.
Why:
- F5: The 10-day drift after a high is concentrated at the exact 20-day closing high. Non-overlapping 10-day returns from closes at the top of the range average +5.3% (t 3.25, n 179); every lower fifth of the range gives +0.2% to +1.3% (t below 1.9). Among new highs, those above their 50-day average give +6.1% (t 2.90, n 113, hit 58%); those below it give +3.7% (t 1.24, n 57, hit 42%).
- F6: The book's losing trades are the short ones. Trades of 15 days or less lose on average: -9.2%, -4.7%, -4.5% and -3.4% by duration band, with win rates of 2–32% over 1563 trades. Trades longer than 15 days earn +11.9% (median +3.1%, win rate 55%, n 1705). The book is profitable only because some trades keep running long after the high.
