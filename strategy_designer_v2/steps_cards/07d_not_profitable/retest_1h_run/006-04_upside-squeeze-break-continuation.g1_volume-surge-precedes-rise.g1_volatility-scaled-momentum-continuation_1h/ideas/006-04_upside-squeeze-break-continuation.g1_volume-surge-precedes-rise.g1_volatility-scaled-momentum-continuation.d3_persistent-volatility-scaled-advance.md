---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The longer a coin's 10-day return relative to its own 20-day volatility has stayed strong over the past 3 days, the more its price rises over the next 3 days relative to its usual 3-day return.
Consequence: A trader should size the long on how persistently strong the advance has been over several days, not on its latest hourly reading, which cuts the churn whose fees exceed the gain.
Why:
- F5: Fees ate about half of the gross gain: 0.000019 against 0.000039 per bar, over 32,526 trades (1.83 per day, median 9 hours). In the transitional forecast quintile (mean forecast 7.3), fees of 0.000088 per bar exceeded that quintile's gain of 0.000027.
- F6: Only the full-cap forecast quintile (forecast 20, position 1.00) earned clearly: 0.000185 per bar, coin r1 t 4.19. The book's mean daily return of 0.00043 was below holding's 0.00118 at a mean position of 0.27, and its timing part (0.000023 per bar) was about as large as its market part (0.000016).
