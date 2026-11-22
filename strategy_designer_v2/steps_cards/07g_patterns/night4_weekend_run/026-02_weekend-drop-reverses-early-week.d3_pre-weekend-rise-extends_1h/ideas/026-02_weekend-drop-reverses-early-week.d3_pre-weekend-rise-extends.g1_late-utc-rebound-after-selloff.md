---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the 8 hours before 22:00 UTC, it rises over the next 2 hours, and the larger that 8-hour fall measured against the coin's recent hourly volatility, the larger the rise.
Consequence: A trader can buy a coin that sold off through the European and US afternoon into the 22:00 UTC rebound, and should avoid shorting it into those hours.
Why:
- F1: The two hours from 22:00 to 24:00 UTC rise. The coin's return from the 21:00 close to the 23:00 close averages +0.099 % (t 8.8, 16200 cases, one per coin per day). It is positive in all six coins (t 2.9 to 4.6), on all seven weekdays (t 1.7 to 4.3) and in seven of eight years (2022: -0.05 %, t -1.6). The hourly z-returns of the bars closing at 22:00 and 23:00 are the largest of the day (t 6.2 and 5.3).
- F2: That late rise grows with the size of the coin's fall over the 8 hours before 21:00, measured in hourly-volatility units. It is +0.23 % in the lowest quintile (mean -4.1 vol units) against +0.04 % in the highest (+4.2 units), and the slope of the vol-scaled 2-hour return on the 8-hour move has t -5.7 (16200 cases).
