---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-02_capitulation-rebound
line: 7.g patterns
backtest: N2-02_capitulation-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close falls by at least one of its own recent daily volatilities while it trades below its 200-day average, its next one to three days rise more than its usual drift. The rise is larger when recent volatility is above its usual level.
Consequence: A trader can buy a coin's single sharp down-day below the long average for a short hold, rather than wait for an extreme distance from the average.
Why:
- F1: After a daily close that fell between 1 and 2 of its own 20-day volatilities, the next day returned +0.69% on average (t 4.9, n=1386); after a fall of more than 2 volatilities it returned +0.67% (t 2.2, n=403). Over all bars the next day returned +0.13% (t 3.5, n=17022), and after rises of the same size it returned only +0.11% to +0.13% (t 0.9 and 0.5).
- F2: The next-day rebound after a fall of 1 volatility or more is concentrated in two places. Below the 200-day SMA it is +0.75% (t 5.5, n=1608), against +0.16% above it (t 0.4, n=181). In the high-volatility regime it is +1.20% (t 4.9, n=722), against +0.34% outside it (t 2.5, n=1067).
- F3: The rebound is positive in every coin: from +0.34% for BTC (t 1.4, n=292) to +1.09% for XMR (t 4.0, n=299). It is positive in 7 of 8 years, with 2024 the exception at -0.01%.
- F4: Over 3 days the rebound persists. After down days of 1 volatility or more, counted at least 3 bars apart, the mean 3-day return is +0.84% (t 3.7, n=1387), against a 3-day base of +0.39%.
- F6: The idea's own signal does not sort outcomes. The 10-bar excess return is flat across the five quintiles of distance from the 200-day SMA (all |t| < 0.7, about 160 cases each). In-regime bars with a forecast of 0 to 5 are negative: -1.6% (t -2.1, n=233).
