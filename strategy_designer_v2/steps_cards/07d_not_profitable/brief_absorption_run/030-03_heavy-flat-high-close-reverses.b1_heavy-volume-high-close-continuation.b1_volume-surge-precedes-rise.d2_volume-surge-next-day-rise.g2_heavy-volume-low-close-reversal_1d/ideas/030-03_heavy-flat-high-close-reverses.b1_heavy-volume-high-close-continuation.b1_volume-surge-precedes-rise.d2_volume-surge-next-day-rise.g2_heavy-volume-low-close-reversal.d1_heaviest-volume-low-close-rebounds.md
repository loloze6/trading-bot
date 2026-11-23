---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day whose volume is heavy against the coin's prior 20-day average, the lower the close sits within that day's high-low range, the more the coin rises over the next day, and this rise grows steeply with the volume ratio, so that the heaviest-volume days, well above their 20-day average, carry most of it.
Consequence: A trader goes long for one day mainly after the heaviest-volume closes near the low, scaled by how far volume exceeds its 20-day average, and leaves ordinary heavy days alone because their move does not cover the fee.
Why:
- F3: Inside the signals (forecast > 10), the next-day excess return rises with the day's volume against its prior 20-day mean: by volume-ratio quartile (means 0.75, 1.07, 1.48, 2.99) it is +0.14 %, +0.06 %, +0.34 % and +0.56 %, with 1254 cases each. Keeping only signals with a ratio above 1.5 lifts the book to Sharpe 0.85 and Calmar 0.672, with its deepest fall cut to −24.7 %, the best of all the variants tried.
- F2: The size of the move is the binding limit. The total move per case is +0.23 % against a 0.19 % cost per trade, 1.2 times the cost, and the unusual move of +0.11 % is 0.6 times the cost (strength 0.025). Only a stronger case of the situation can carry the fees.
- F1: The failing Calmar (0.499 against 0.75) comes from a book that sits in a position on 98 % of the coins' days and falls 43–45 % at its deepest; the 6049 bars with forecast below 2 hold only 0.037 of the book and earn about 0 (+0.0025 % a day), so the falls are made on signal days. Rebuilt at the same cost, keeping only forecast > 10 cuts the deepest fall to −37.6 % for a Calmar of 0.566, and halving every position gives a Calmar of 0.570 (fall −22.8 %, yearly +13 %); neither reaches 0.75.
