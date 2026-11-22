---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 14 days, and the larger that range multiple, the higher the return, the excess growing with how far that multiple stands above the multiples the coin showed over the past year.
Consequence: A trader would treat only the rare, extreme panics as a buy, rather than the ordinary drops a short history makes look large, and so would be out of the market most of the time instead of holding the coin.
Why:
- F1: The book is close to holding the coins, so it falls as deep as they do. It holds a long position on 98.3 % of bars, at a mean allocation of 1.07 when long. Its median trade lasts 75.5 days across 916 trades. Its daily returns correlate 0.93 with holding. Its deepest fall is -79.0 % against holding's -81.2 %, which with a yearly return of 26.1 % gives the failing Calmar of 0.33.
- F2: The panic signal is not rare. Its forecast rises by at least 2 points in 1144 of the roughly 1250 grid cells of 84 bars, about 91 %. On those cases the mean unusual move is -0.13 % (t -0.21), so the book's gain is mostly the coins' drift.
- F7: The forecast's own size barely grades the outcome. The top forecast quintile earns +1.50 % (t 0.77), the middle one -1.36 %, and two of the five quintiles sit at the cap of 20.
