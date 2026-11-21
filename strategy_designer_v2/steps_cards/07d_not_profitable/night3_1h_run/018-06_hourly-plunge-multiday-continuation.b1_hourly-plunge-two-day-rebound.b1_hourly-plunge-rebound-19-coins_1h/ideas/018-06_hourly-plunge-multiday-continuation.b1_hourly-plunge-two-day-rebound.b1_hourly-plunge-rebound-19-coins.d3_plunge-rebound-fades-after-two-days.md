---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The 2-day rise that follows a coin's 24-hour drop of a large multiple of its 30-day average absolute daily return is spent within those 2 days, and the larger the drop, the larger the rise inside the 2 days compared with the days after.
Consequence: A trader buying a plunge should take the two-day rebound and not stay long after it.
Why:
- F1: The book's gain is too small because it stays long for long stretches after its signal has faded. 51 % of bars carry a forecast of 0, yet the book still holds about 0.14 of its value on them; those bars lose 0.32 of the book's total gain (timing −0.24 bps per bar) and pay 28 % of its fees. Its trades last 159 hours on average against a 48-hour horizon.
- F2: The gain sits almost entirely in the strongest drops. Bars with a forecast of 8 to 20 are 2.0 % of bars but carry 65 % of the gain, with timing of +6.8 bps per bar. Bars with a forecast of 0 to 0.5 earn only +0.13 bps of timing.
- F7: The book lags holding mainly because it is barely in the market, not because its rebounds fail. Its mean allocation when long is 0.22, and its mean daily return is 0.033 % against holding's 0.139 %. It trails holding by the most in rising windows: w11 earned 0.28 against 2.29, w6 0.16 against 0.76.
