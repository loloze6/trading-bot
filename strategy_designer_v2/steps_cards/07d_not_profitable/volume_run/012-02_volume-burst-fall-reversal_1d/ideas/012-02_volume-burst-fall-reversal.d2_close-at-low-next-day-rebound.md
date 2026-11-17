---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the closer the bar closes to its own low, the larger the price rise over the next 1 day.
Consequence: A sharp fall that closes at its low is a better next-day buy than one with a long lower wick; the long wick comes before further decline.
Why:
- F4: The wick works against the brief: falls that close nearest their low (bottom third of close-in-range, n 148) gain +1.64% over 1 day (t 3.46), while falls with the longest lower wick lose −0.41% over 1 day and −2.85% over 10 days (t −2.71).
- F2: After the 444 thinned sharp-fall bars, the excess return is +0.42% over 1 day (t 1.53) but turns to −0.42% over 3 days (t −1.13) and −1.05% over 5 days (t −2.14), so the rebound lasts one day and is then given back with more.
