---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.d not profitable
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days, only while its 20-day return is already positive; the larger the rise, the heavier its volume and the higher that 20-day return, the larger the further gain.
Consequence: A heavy-volume surge inside an established 20-day advance is a reason to stay long for days, and the same surge after a weak month is a reason to refuse the trade.
Why:
- F4: The continuation after strong signals depends on the coin's prior 20-day return. For the top third of 20-day return, the 5-day excess is +0.025 (days 2 to 5: +0.022). For the bottom third it is +0.0018 (days 2 to 5: +0.0041). Each group has 530 cases.
- F5: The volume part of the forecast adds little among strong signals. The Spearman correlation between relative volume and the 5-day excess is 0.018, and between the scaled rise and the 5-day excess it is 0.017. The 5-day excess is +0.009 for the low-volume third and +0.017 for the high-volume third.
- F2: After days with forecast >= 5, the coin's daily excess return over its own mean is small on the first day (+0.0012, t 0.92, n 1979, position held 0.90) and is concentrated on the second day (+0.0052, t 4.41, position held 0.22) and the fourth day (+0.0027, t 2.24, position held 0.16). The book has mostly left before the gain it forecasts arrives.
