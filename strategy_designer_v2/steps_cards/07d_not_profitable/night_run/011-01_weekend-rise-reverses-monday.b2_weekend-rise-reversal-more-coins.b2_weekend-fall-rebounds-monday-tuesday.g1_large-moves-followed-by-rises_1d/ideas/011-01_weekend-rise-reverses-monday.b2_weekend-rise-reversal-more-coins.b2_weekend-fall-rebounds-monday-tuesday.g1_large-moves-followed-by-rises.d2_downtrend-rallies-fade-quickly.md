---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise relative to its own 60-day volatility, the more that coin falls over the next 2 days, and the more negative its 30-day return, the larger that fall.
Consequence: A sharp up day in a coin that has been falling for a month is a reason to refuse a long, or to lean short, for the next two days.
Why:
- F1: The book's Calmar is 0.38 (yearly 15.4 %, deepest fall -40.3 %), and that fall runs 294 days from w1 to w3, while holding the coins fell -69.6 % over the same days. In w1–w3 the long positions taken after up days in down and up trends summed to -0.55 and -0.37, against +1.15 after down days in down trends.
- F4: A large up day (|z| > 1) is followed by a negative excess 2-day return when the coin is in its down tercile against the 50-day average (-0.00797, t -2.27, n 426), and by a positive one in its up tercile (+0.01060, t 3.64, n 1060). By the 30-day return quintile, the excess after large up days grades monotonically from -0.00926 (t -1.78) in the lowest quintile to +0.01318 (t 3.14) in the highest.
