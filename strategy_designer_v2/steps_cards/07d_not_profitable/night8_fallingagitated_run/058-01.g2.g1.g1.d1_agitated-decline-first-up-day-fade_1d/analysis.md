---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade_1d
idea tested: 058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6305 USD
---
## Findings
- **F1:** The check failed on Calmar (0.56 against 0.75). In folds B and C the book's deepest fall is -5.99 %, and almost all of it comes from one day in w14: the book lost 5.92 % while the coins rose 11.0 %. On that day five coins (BTC, ETH, LTC, XMR, ZEC) were short at allocations of -0.58 to -0.69, and each rose 10.2 % to 12.1 % the next day. The 15 worst book days carry 70 % of all losing days' losses, and on every one of them except one the coins rose (+1.1 % to +12.5 %).
- **F2:** The sizing grows much faster than the effect. In the strongest quarter of forecasts the mean allocation is -0.54 against -0.10 in the weakest, 5.4 times larger, but the next-day short gain is only 2.05 % against 0.74 %, 2.8 times larger. Across range quartiles the gain rises less than in proportion to the range: 0.30 %, 1.46 %, 1.24 % and 2.14 % for ranges of about 0.5, 0.9, 1.3 and 2.5 usual swings.
- **F3:** Sizing changes alone repair the falls, because the effect itself is broad. Rebuilding the book on folds B and C (pnl per day divided by 6):
- **F4:** Inside the signal, the gain is largest when the up day closes well below its high. Ordered by the upper wick's share of the range, the four quartiles gain 0.76 % (t 1.3), 1.22 %, 1.21 % and 1.83 % (t 3.3), about 94 cases each. The close's place in the range shows the same in reverse: 1.83 % in the lowest quarter against 0.76 % in the highest. The day that caused the worst loss closed high in its range, at 0.75 to 0.89 of it.
- **F5:** Days whose close-to-close rise is above 0.88 of the 30-day swing are the weakest part of the signal. They gain 0.68 % (t 1.17, 72 cases), against 2.23 % (t 4.7) for rises of 0.49 to 0.88. Leaving them out shrinks the deepest fall from -5.9 % to -2.5 % and gives a Calmar of 1.55, with a yearly +3.9 %.
- **F6:** The repair conditions are not effects of their own:
- **F7:** A recent fall strengthens the signal but does not fix the falls. Signal cases whose 5-day return is below zero gain 1.74 % (t 3.7, 166) against 0.67 % (t 1.8, 122) for the rest. Kept alone, they lower the rebuilt Calmar to 0.80, because the worst day (5-day returns of -0.34 to -2.6 swings) stays in.
- **F8:** The horizon fits and costs are not the problem:

## Ideas
- `058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade` (from F1, F4, F6, F8): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The further that day's close sits below its high, measured against the standard deviation of its daily returns over the past 30 days, the larger that next-day fall.
- `058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave` (from F1, F2, F3, F8): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The wider that day's low-to-high range against the standard deviation of its daily returns over the past 30 days, the larger the fall, though growing less than in proportion to the range.
- `058-01.g2.g1.g1.d1.d3_wide-range-small-gain-fade` (from F1, F5, F6, F8): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The wider that day's range against the standard deviation of its daily returns over the past 30 days, and the smaller its close-to-close rise against that same swing, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
