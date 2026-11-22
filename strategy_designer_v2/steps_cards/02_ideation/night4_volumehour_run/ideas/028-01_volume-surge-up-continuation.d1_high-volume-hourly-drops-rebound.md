---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next three to twenty-four hours; the larger that hour's fall relative to its typical hourly move, the larger the rebound.
Consequence: A trader would buy into a sharp high-volume hourly drop instead of chasing a sharp high-volume rise, because only the drop is followed by a move larger than the cost of a trade.
Why:
- F4: Large down-hours rebound instead. After hours falling more than 3 usual hourly moves, the excess 3-hour return is +0.397 % (t 3.02, n 143) at volume ratio 2–3 and +0.278 % (t 2.69, n 433) at ratio above 5, and the 24-hour excess return is +0.757 % (t 2.67). That rebound is larger than the 0.11 % cost; its 6-hour t is only 1.1–1.5. These samples take the largest-score hour of each 6-hour cell.
- F2: Volume adds nothing to up-hours: after hours rising more than 3 usual hourly moves, the excess 6-hour return is about zero at every volume ratio (ratio 2–3: +0.002 %, t 0.01, n 144; ratio above 5: −0.013 %, t −0.08, n 345); on all up-hours sampled every 6 hours, the regression slope on the score has t 0.93.
- F1: The idea has no edge to pay for its trades: per case over 6 hours the unusual move is +0.00 % and the total move +0.04 %, against a cost of 0.11 % per trade (8827 cases); on hours sampled once per 6-hour cell, the top 1 % of up-scores is followed by an excess 6-hour return of −0.143 % (t −0.64, n 214) and the next 4 % by +0.056 % (t 0.70, n 856).
