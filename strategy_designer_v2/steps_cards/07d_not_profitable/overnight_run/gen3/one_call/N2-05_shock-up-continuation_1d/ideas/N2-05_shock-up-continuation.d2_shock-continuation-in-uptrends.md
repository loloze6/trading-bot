---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.d not profitable
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's outsized up day is followed by further gains over the next days when the coin closes above its 50-day average and is up over the prior 20 days.
Consequence: A trader should take the long after a big up day only when the coin is already in an uptrend, and refuse it when the coin sits below its 50-day average or is down over 20 days.
Why:
- F4: The continuation exists only when the coin is already in an uptrend. Shocks with the close above its 50-bar mean give +2.06% over 5 bars (t 2.87, n 314), against −0.03% below it (t −0.04, n 196). Shocks after a positive 20-bar return give +1.87% (t 3.01, n 452), against +0.68% (t 1.18, n 424) after a negative one.
- F5: The book's losses sit in the downtrend state. Bars below the 50-bar mean (12,258) net −0.000294 per bar, against +0.000137 on bars above it (5,122). Bars with a negative 20-bar return net −0.000309, against +0.000034 with a positive one.
- F6: The losing years are falling-market years where shocks reversed. In 2022 the 5-bar return after shocks was −2.56% (t −1.98, n 97) and the book's gross was −0.000135 per bar. 2018 gave −0.17% (n 98). The rising years 2021 and 2024 gave +4.11% (t 2.65, n 106) and +3.89% (t 3.23, n 104).
