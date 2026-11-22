---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: In coins whose 30-day return before the panic was negative, a 24-hour stretch with a range several times its 30-day average and a hard fall is followed by higher than usual returns over the next 1 day, rather than 14 days, and the more extreme the panic, the higher the return.
Consequence: The liquidity premium is paid within a day of the forced selling, so a long taken on the panic earns it only when held for about a day, not for weeks of the coin's later drift.
Why:
- F1: The panic premium is short-lived. Over all 1975 cases, the excess return over the coin's normal drift is +0.35 % over 6 bars (24 h, t 2.98). It is +0.02 % over 18 bars (3 days, t 0.12), then turns negative: -1.59 % over 42 bars (t -5.75) and -2.17 % over 84 bars (t -4.88). The 14-day horizon the book bets on sits where the effect has already reversed.
- F2: The book holds far past the premium. It made 3400 trades lasting 34.8 days on average, with a minimum holding of 84 bars. Its daily mean return of 0.047 % therefore mostly carries the coin's later fall, giving a deepest fall of -64.6 % on the chained book and a Calmar of 0.059.
- F4: Over all cases, panic depth barely grades the 14-day outcome (correlation of raw depth with the 84-bar excess 0.010). Over 1 day it does grade: the excess rises from +0.16 % in the bottom tercile (t 0.91) to +0.44 to +0.46 % in the upper two (strength 0.036 against 0.083 to 0.088).
- F7: On a 1-day horizon the move is large enough to cover the trade cost of 0.22 %. In the deepest-panic tercile of 60-day-negative coins, the total 1-day move is +2.01 %, 9 times the cost. Over all 60-day-negative cases it is +1.00 %.
