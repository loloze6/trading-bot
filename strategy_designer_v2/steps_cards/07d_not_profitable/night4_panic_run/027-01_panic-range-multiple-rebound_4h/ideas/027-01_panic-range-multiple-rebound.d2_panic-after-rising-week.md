---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 14 days, and the larger that range multiple, the higher the return, except when the coin's 7-day return before the panic is negative, where the deeper that 7-day fall, the lower its return over the next 14 days.
Consequence: A trader would refuse panic buys that come at the end of a week-long slide, which keep falling, and keep those that interrupt a rising week.
Why:
- F1: The book is close to holding the coins, so it falls as deep as they do. It holds a long position on 98.3 % of bars, at a mean allocation of 1.07 when long. Its median trade lasts 75.5 days across 916 trades. Its daily returns correlate 0.93 with holding. Its deepest fall is -79.0 % against holding's -81.2 %, which with a yearly return of 26.1 % gives the failing Calmar of 0.33.
- F3: The two deepest falls are the long declines of holding the coins. From w12 to w16 the book fell -79.0 % over 485 days to the bottom, while holding fell -80.7 % over the same days. From w1 to w3 it fell -70.1 % while holding fell -66.9 %. The book stayed long through both.
- F4: Cases where the coin had already fallen over the prior 7 days lose. The lowest quintile of the 7-day return (mean -16.2 %) has a mean unusual 14-day move of -3.94 % (t -3.37, 201 cases), and its worst point averages -13.3 % with 25.9 % of cases falling below -20 %. The highest quintile (mean +20.9 %) earns +3.55 % (t 1.75, 201 cases).
- F6: Cases below their 30-day mean price lose. In the quintile furthest below that mean (-18.7 %), the mean unusual move is -2.23 % (t -1.73, 151 cases), against +2.81 % (t 1.66) in the quintile 6.5 % above it.
