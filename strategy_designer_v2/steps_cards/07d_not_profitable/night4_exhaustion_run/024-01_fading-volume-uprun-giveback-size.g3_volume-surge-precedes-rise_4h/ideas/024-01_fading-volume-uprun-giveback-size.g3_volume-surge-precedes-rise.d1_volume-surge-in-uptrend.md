---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days, only while its 30-day return is positive. The higher the volume against that average and the stronger the coin's 30-day rise against its usual move, the larger the rise.
Consequence: A volume surge is a reason to lean long for three days in a coin that has been rising for a month, and a reason to stay out of one that has been falling.
Why:
- F1: The book fails on its falls: chained in window order, its daily returns fall 61.2 % at the deepest point against a yearly return of 34.4 % (Calmar 0.56). The deepest in-window falls come in w16 (-55.3 %, worst day -38.1 %), w2 (-51.0 %) and w14 (-50.5 %), windows where holding the coins lost 44 % in w2, lost 49 % in w14 and gained 36 % in w16.
- F2: The book falls with the market because it is a long-only book that stays mostly invested. On its worst 5 % of days (145 days) it lost 7.1 % on average while holding the coins lost 8.6 %. Its mean position is 0.62 to 0.80 of the book in every 30-day trend quintile.
- F3: The position's bar gains follow the coin's trailing 30-day trend, standardised by its usual move. In the most negative trend quintile the mean gain is -0.015 % per bar, summing to -2.30, with the worst bar at -41 %. In the most positive quintile it is +0.045 % per bar, summing to +7.16, with the worst bar at -18 %.
- F4: The surge cases are graded by the same 30-day trend. The excess 3-day return is -0.03 % (t -0.08, 658 cases) in the most negative trend quintile, rising to +0.47 % (t 1.50) and then +0.82 % (t 2.02, 658 cases) in the most positive. In the losing windows w2, w14 and w16, cases in a downtrend (trend z -1.22) lost 1.95 % excess (t -1.91, 131 cases), with a 10th-percentile 3-day return of -15.5 %.
