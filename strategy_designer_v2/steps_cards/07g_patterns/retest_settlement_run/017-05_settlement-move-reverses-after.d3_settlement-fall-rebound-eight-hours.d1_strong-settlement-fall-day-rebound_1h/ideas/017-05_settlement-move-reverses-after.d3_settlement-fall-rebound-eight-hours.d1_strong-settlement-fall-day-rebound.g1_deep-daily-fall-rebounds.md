---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin falls sharply over 24 hours, it rises over the next 24 hours, and the larger the fall against its usual 24-hour move, the larger the rise, at any hour of the day.
Consequence: A trader buys deep one-day falls on any hour rather than only at settlement times, and expects a rebound several times larger per case than the settlement fall gave.
Why:
- F1: The large 24-hour fall is what rebounds, whatever the hour. On the non-overlapping 24-bar grid, bars in the bottom decile of the 24-hour return (scaled by the mean absolute 24-hour move of the last 720 bars) are followed by a 24-hour return of +82.6 bp above the coin's normal drift (t 5.21, 1581 cases). The next decile gives only +19.8 bp (t 1.53). The middle and top deciles give between -4 and -26 bp, so the rebound sits in the deepest falls.
- F2: That rebound is much larger than the tested idea's. For the bottom two deciles of the 24-hour move, the strength is 0.102 of the coin's usual 24-hour move, against 0.031 for the settlement-fall cases. At +43 to +83 bp per case, the unusual move alone covers the 0.19 % cost of a trade.
- F4: The rebound after large 24-hour falls holds on every coin and in every part of the period:
- F5: The rebound after a 2-hour fall is not tied to the settlement clock, which is the brief's third falsifier. The 24-hour excess after a 2-hour fall of 1.5 usual moves or more is:
