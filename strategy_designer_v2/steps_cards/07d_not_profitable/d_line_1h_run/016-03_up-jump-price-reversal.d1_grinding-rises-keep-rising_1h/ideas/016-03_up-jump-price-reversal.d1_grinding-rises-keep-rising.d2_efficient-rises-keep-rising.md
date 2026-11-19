---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day net rise is compared with the total distance its hourly prices travelled over those 3 days (an efficient, one-way path), the more the coin rises over the next 3 days.
Consequence: A trader would go long coins whose 3-day rise was made efficiently and size by that efficiency, refusing longs after choppy rises of the same size.
Why:
- F5: Much of that evenness effect is the size of the rise. Among rising cases the evenness term has t 3.12 alone but t 1.76 next to the 3-day return (t_past 1.05). Within the largest-rise tercile both evenness halves earn about +0.008, while in the smallest-rise tercile both lose (-0.0068 and -0.0029).
- F6: Path efficiency (net 3-day log move over the summed absolute hourly moves) grades the next 3 days better than the top-gain share. On all grid cases its top quintile earns +0.0074 (t 2.74) and its flat middle quintile -0.0059 (t -2.27). Among rising cases it has t 3.30 alone and 1.91 next to the rise's size.
