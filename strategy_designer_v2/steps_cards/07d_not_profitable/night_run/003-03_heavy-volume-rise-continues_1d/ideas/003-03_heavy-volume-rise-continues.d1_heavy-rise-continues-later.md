---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.d not profitable
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days, with most of the further gain arriving from the second to the fifth day rather than on the first; the larger the rise and the heavier its volume against that average, the larger the further gain.
Consequence: The continuation is captured by holding through the following several days, not by being long only on the night after the rise.
Why:
- F1: The book is only in the trade on the signal day itself. It holds a mean position of 0.43 on the bar the forecast is positive and about 0.017 on every bar after it, so the book's mean daily return is 4.9e-05 against roughly 0.0012 for holding the coins, and it trails holding in 15 of 24 windows.
- F2: After days with forecast >= 5, the coin's daily excess return over its own mean is small on the first day (+0.0012, t 0.92, n 1979, position held 0.90) and is concentrated on the second day (+0.0052, t 4.41, position held 0.22) and the fourth day (+0.0027, t 2.24, position held 0.16). The book has mostly left before the gain it forecasts arrives.
- F3: Because of this one-day holding, the book's gain is about the size of its fees. The mean gain before fees is 0.000242 per bar and the mean fee is 0.000188 per bar, while the trades themselves show only a mean net of +1.32 % over 3.3 days with 49 % winners.
