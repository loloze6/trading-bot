---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 2-hour return relative to its usual 2-hour move, the more its price moves the opposite way over the next 8 hours, at any time of day.
Consequence: A trader leans against a sharp 2-hour move for the next 8 hours, sized by its size, without waiting for a funding time.
Why:
- F5: The 2-hour move also reverses over the next 8 hours, graded by its size: from -1.3 bp in the smallest |2h| quintile to +6.4 bp (t 2.4) in the fourth and +15.7 bp (t 4.1, 10369 cases) in the largest. This total move is below the 0.19 % cost of a trade.
- F6: The 8h reversal of the 2h move is not tied to funding times. At the 08:00 settlement it is -2.8 bp (t -1.2), while at 04:00, a time with no funding, it is +4.5 bp (t 2.2), next to +12.2 bp at 00:00 (t 6.1) and +7.3 bp at 16:00 (t 3.3; about 17300 cases each). The idea's own measure has a strength of 0.007 and a mean of only +0.02 % per case (t 1.25).
