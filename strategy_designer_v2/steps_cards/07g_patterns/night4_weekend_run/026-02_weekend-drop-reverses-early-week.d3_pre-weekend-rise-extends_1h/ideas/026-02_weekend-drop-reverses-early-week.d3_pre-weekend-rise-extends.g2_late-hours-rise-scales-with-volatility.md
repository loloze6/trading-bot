---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's hourly volatility over the past 7 days, the larger its rise over the 2 hours from 22:00 to 24:00 UTC.
Consequence: A trader can lean long into the late UTC hours mainly when the coin has been volatile, where the rise is several times larger.
Why:
- F1: The two hours from 22:00 to 24:00 UTC rise. The coin's return from the 21:00 close to the 23:00 close averages +0.099 % (t 8.8, 16200 cases, one per coin per day). It is positive in all six coins (t 2.9 to 4.6), on all seven weekdays (t 1.7 to 4.3) and in seven of eight years (2022: -0.05 %, t -1.6). The hourly z-returns of the bars closing at 22:00 and 23:00 are the largest of the day (t 6.2 and 5.3).
- F3: The late rise grows with the coin's past-week hourly volatility: +0.04 % (t 3.3) in each coin's lowest volatility tercile, +0.09 % (t 5.1) in the middle and +0.17 % (t 6.4) in the highest.
