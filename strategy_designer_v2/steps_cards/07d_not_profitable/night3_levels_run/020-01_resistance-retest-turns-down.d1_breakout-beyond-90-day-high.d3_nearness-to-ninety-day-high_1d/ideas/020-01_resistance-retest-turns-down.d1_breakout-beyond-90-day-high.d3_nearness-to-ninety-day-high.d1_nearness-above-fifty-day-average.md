---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close stands to its highest close of the previous 90 days, the more it rises over the next 20 days, only while its daily close stands above its 50-day average close.
Consequence: A trader should lean long on closes near the 90-day high while the coin is above its 50-day average, and stay out of longs once the close drops beneath that average.
Why:
- F1: The book earns a mean 0.000278 a day against 0.00118 for holding the coins, and its gain comes from its longs alone: long bars sum +5.75 (+0.000617 a bar), short bars sum −0.76 (−0.000109 a bar), and 524 short trades lose a mean 5.1 % after fees, with 34 % winners.
- F4: Longs pay only while the close is above its 50-day average. There they earn +0.000909 a bar on 4266 bars, with the coin returning +0.0018 a day. Below that average they lose −0.000049 a bar on 1709 bars, with the coin returning −0.0014 a day.
- F5: The book's falls are falls the coin shares while the book is long. On its 30 worst days the book lost a mean 3.5 % while the coins fell 9.5 %, and the coins were down on 100 % of them. The deepest fall is 18 %, against a yearly return that gives a Calmar of 0.53.
