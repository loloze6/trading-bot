---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, a rebound that has faded by 3 days.
Consequence: Holding the rebound for one day only, rather than three, keeps the part of the move that pays and avoids the decline that follows.
Why:
- F2: After the 444 thinned sharp-fall bars, the excess return is +0.42% over 1 day (t 1.53) but turns to −0.42% over 3 days (t −1.13) and −1.05% over 5 days (t −2.14), so the rebound lasts one day and is then given back with more.
- F3: Volume ratio grades the next-day move: the top third by volume ratio gains +1.14% over 1 day (t 1.74, n 148) against −0.04% for the bottom third, but the same top third loses −1.78% over 5 days (t −1.94).
- F1: The book earns 0.0082% a day against 0.118% for holding the coins, because it is invested on only 5.4% of coin-days; its 474 trades last 1.07 days on average and earn 0.55% each before fees (0.45% after, 56% winners), which is too small and too rare to lift the mean daily return.
