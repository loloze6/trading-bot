---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 14 days, and the larger that range multiple, the higher the return, only while its volatility over the past 7 days is high against its volatility over the past 60 days, the excess growing with that ratio.
Consequence: A trader would buy a panic only inside a turbulent week. They would stay out of sharp drops that hit a calm market, which sit inside the long declines that make the book's deepest falls.
Why:
- F1: The book is close to holding the coins, so it falls as deep as they do. It holds a long position on 98.3 % of bars, at a mean allocation of 1.07 when long. Its median trade lasts 75.5 days across 916 trades. Its daily returns correlate 0.93 with holding. Its deepest fall is -79.0 % against holding's -81.2 %, which with a yearly return of 26.1 % gives the failing Calmar of 0.33.
- F3: The two deepest falls are the long declines of holding the coins. From w12 to w16 the book fell -79.0 % over 485 days to the bottom, while holding fell -80.7 % over the same days. From w1 to w3 it fell -70.1 % while holding fell -66.9 %. The book stayed long through both.
- F5: Cases also lose where the week's volatility is low against its 60-day level. In the lowest quintile of the 7-day over 60-day volatility ratio (mean 0.55), the mean unusual move is -5.18 % (t -2.89, 87 cases). In the highest quintile (mean 1.63) it is +4.78 % (t 1.72, 87 cases), and it rises almost steadily from the lowest quintile to the highest.
- F7: The forecast's own size barely grades the outcome. The top forecast quintile earns +1.50 % (t 0.77), the middle one -1.36 %, and two of the five quintiles sit at the cap of 20.
