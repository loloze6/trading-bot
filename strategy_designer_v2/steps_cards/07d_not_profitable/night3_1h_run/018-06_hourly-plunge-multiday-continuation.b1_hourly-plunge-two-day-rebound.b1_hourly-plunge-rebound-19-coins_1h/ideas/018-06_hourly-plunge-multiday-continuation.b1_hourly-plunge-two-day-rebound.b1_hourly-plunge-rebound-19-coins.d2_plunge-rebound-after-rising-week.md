---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the 24-hour drop in those multiples, the larger the rise, only while the coin's 7-day return is positive, and the higher that 7-day return, the larger the rise.
Consequence: A short plunge inside a week-long rise is a buy for two days, and a plunge that extends a weekly fall is not.
Why:
- F2: The gain sits almost entirely in the strongest drops. Bars with a forecast of 8 to 20 are 2.0 % of bars but carry 65 % of the gain, with timing of +6.8 bps per bar. Bars with a forecast of 0 to 0.5 earn only +0.13 bps of timing.
- F5: The 7-day return grades the rebound the same way. Entries in the top 7-day quintile rise +2.54 % over 48 hours (t 3.6) and the fourth quintile +1.45 % (t 3.0). The middle quintile rises only +0.004 %.
- F6: The book's deepest fall is 39 %, running over 305 days from window 1 to window 3, all falling-market windows (holding's summed daily returns −0.33, −0.41, −0.21). In window 2 alone the book lost −0.24 of summed daily return, while it bought drops that kept falling.
