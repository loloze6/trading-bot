---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day whose volume is heavy against the coin's prior 20-day average, the lower the close sits within that day's high-low range, the more the coin rises over the next day, while the coin's 20-day volatility is high against its own past 120 days, and the higher that volatility, the larger the rise.
Consequence: A trader takes the one-day long after a heavy-volume low close when the coin is in a volatile spell, and holds less or nothing on such days when the coin is calm.
Why:
- F7: By the coin's 20-day volatility quartile, signals earn +0.66 % excess next day in the highest quartile (1614 cases), against −0.08 % to +0.03 % in the three others. The highest quartile without the signal earns −0.16 % (2011 cases), so high volatility alone is not the effect. Keeping only signals with volatility above its 120-day median cuts the deepest fall to −15.3 %, but the Calmar is 0.44 because the book trades much less.
- F2: The size of the move is the binding limit. The total move per case is +0.23 % against a 0.19 % cost per trade, 1.2 times the cost, and the unusual move of +0.11 % is 0.6 times the cost (strength 0.025). Only a stronger case of the situation can carry the fees.
- F1: The failing Calmar (0.499 against 0.75) comes from a book that sits in a position on 98 % of the coins' days and falls 43–45 % at its deepest; the 6049 bars with forecast below 2 hold only 0.037 of the book and earn about 0 (+0.0025 % a day), so the falls are made on signal days. Rebuilt at the same cost, keeping only forecast > 10 cuts the deepest fall to −37.6 % for a Calmar of 0.566, and halving every position gives a Calmar of 0.570 (fall −22.8 %, yearly +13 %); neither reaches 0.75.
