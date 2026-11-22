---
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation_1h
idea tested: 028-01_volume-surge-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3547 USD
---
## Findings
- **F1:** The idea has no edge to pay for its trades: per case over 6 hours the unusual move is +0.00 % and the total move +0.04 %, against a cost of 0.11 % per trade (8827 cases); on hours sampled once per 6-hour cell, the top 1 % of up-scores is followed by an excess 6-hour return of −0.143 % (t −0.64, n 214) and the next 4 % by +0.056 % (t 0.70, n 856).
- **F2:** Volume adds nothing to up-hours: after hours rising more than 3 usual hourly moves, the excess 6-hour return is about zero at every volume ratio (ratio 2–3: +0.002 %, t 0.01, n 144; ratio above 5: −0.013 %, t −0.08, n 345); on all up-hours sampled every 6 hours, the regression slope on the score has t 0.93.
- **F3:** The book is mostly a costly part-time holding of the coin: it is long on 70 % of BTC bars and 67 % of ETH bars (mean allocation 0.37 and 0.30); it gains 0.29 and 0.40 bp per bar before fees, of which the market's own rise is 0.20 and 0.19 bp; it makes 2.88 trades a day and ends at a mean daily return of −0.016 %, with a Sharpe 0.77 below holding.
- **F4:** Large down-hours rebound instead. After hours falling more than 3 usual hourly moves, the excess 3-hour return is +0.397 % (t 3.02, n 143) at volume ratio 2–3 and +0.278 % (t 2.69, n 433) at ratio above 5, and the 24-hour excess return is +0.757 % (t 2.67). That rebound is larger than the 0.11 % cost; its 6-hour t is only 1.1–1.5. These samples take the largest-score hour of each 6-hour cell.
- **F5:** Among the top 5 % of up-scores, the hours that follow the highest quartile of the prior 24-hour return are followed by an excess 6-hour return of −0.417 % (t −2.67, n 268). Those in the second quartile are followed by +0.231 % (t 2.35, n 267). On all up-hours the prior 24-hour return's slope is negative (t −1.47).
- **F6:** On a fixed 6-hour grid, there is no steady continuation or reversal after hourly moves of any size: by size quintile every |t| is below 1.4, and by year t runs from −1.81 to 0.74 with no year significant.

## Ideas
- `028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound` (from F4, F2, F1): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next three to twenty-four hours; the larger that hour's fall relative to its typical hourly move, the larger the rebound.
- `028-01_volume-surge-up-continuation.d2_volume-surge-after-quiet-day` (from F5, F1, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next two to six hours, only while the coin's 24-hour return before that hour is modest; the larger the coin's rise over the previous 24 hours, the weaker the further rise, turning into a fall after the largest prior rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
