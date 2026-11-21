---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its last 24 hours, the more it rises over the next 3 days, only while its price is above its average price of the last 30 days.
Consequence: A trader buys one-day falls in coins that sit above their 30-day average and refuses them below it, where the long falls that sink the book happen.
Why:
- F1: The Calmar failure comes from the days the coin closed below its 30-day average price. On those 6,743 coin-days the book's position averaged 0.87 and its gain averaged only 0.031 % a day. On the 6,430 coin-days above that average the position averaged 0.81 and the gain averaged 0.207 % a day. These are hourly gains before costs, with the coin's state read at the first bar of each day.
- F2: Rebuilt from those daily gains before costs, the book over all days falls 81 % at its deepest and has a Calmar of 0.34. Kept only on days above the 30-day average, its deepest fall shrinks to 34 %, its yearly return rises from 27.6 % to 37.2 %, its Calmar reaches 1.11 and its Sharpe 1.13. Kept only below it, Calmar is -0.06 and Sharpe 0.13.
- F3: The recorded book's deepest fall is 66 % and lasts across many windows: inside the chain it is between 50 % and 64 % in 12 of the 24 windows. Its worst 3 % of days hold 2.9 times the book's whole net gain in losses. The falls are long declines the book stays long through, not one window's accident.
- F6: The deepest falls rebound most when the coin is above its 30-day average.
