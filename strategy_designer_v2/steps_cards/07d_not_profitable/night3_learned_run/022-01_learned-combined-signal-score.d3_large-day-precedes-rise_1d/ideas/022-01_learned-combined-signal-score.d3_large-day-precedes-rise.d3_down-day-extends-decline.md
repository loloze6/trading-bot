---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its last day, measured against its usual daily move, the lower its return over the next 5 days, the more so the larger its 20-day decline.
Consequence: Treat a large down day in a coin falling over 20 days as a reason to refuse a long position, or to lean short, for the next 5 days.
Why:
- F3: Mid-sized down days inside a falling 20-day trend are followed by a fall. Their excess 5-day return is -1.58 % (t -2.26, 242 cases). Large up days inside a rising 20-day trend are followed by a rise: +1.42 % (t 2.00, 301 cases), 7.5 times the 0.19 % cost of a round trip.
- F4: The deepest fall was carried by positions opened on down days. In w12 to w14, positions last raised after a down day lost a summed 0.95 of daily gain while the 20-day trend was falling (781 bars) and 0.15 while it was rising (229 bars). Positions opened on up days gained a net +0.42 over the same windows. In w14 alone, down-day positions lost 1.02 against 0.14 for up-day positions.
