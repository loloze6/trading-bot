---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while its 5-day volatility exceeds its 30-day volatility; the larger that ratio, the larger the rise.
Consequence: A trader buys fading-volume down-streaks in expanding-volatility moments, and refuses them in quiet markets, where they drift on down.
Why:
- F3: The idea's edge is negligible. Per case, the unusual move is +0.02 % over 18 bars, 0.003 of the usual 8.17 % move and 0.1 times the 0.19 % trade cost, over 4334 cases (t 0.14). So the book's falls are the market's falls, which the signal does not avoid.
- F6: Cases also split by volatility, comparing 5-day with 30-day volatility, over about 790 cases per quintile:
- F7: Among trades, the most extreme streak losses pay and the middling ones lose, over about 1260 trades per quintile:
