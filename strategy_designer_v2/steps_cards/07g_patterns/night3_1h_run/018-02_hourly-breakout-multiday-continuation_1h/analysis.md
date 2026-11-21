---
line: 7.g patterns
backtest: 018-02_hourly-breakout-multiday-continuation_1h
idea tested: 018-02_hourly-breakout-multiday-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3961 USD
---
## Findings
- **F1:** The move after an hourly close first breaks above its 20-day high keeps growing well past the tested 5 days: on the first break per 120-hour cell, the unusual move is +0.41 % over 1 day (t 1.61, 663 cases), +1.63 % over 5 days (t 3.19, 663), +3.13 % over 10 days (t 3.60, 629) and +4.09 % over 20 days (t 3.07, 572). The 10-day move is about twice the 5-day one, with the highest t, which fits findings F9 and F10.
- **F2:** The book's gain comes from the trades that outlast the horizon. Trades held over 10 days earn a mean +20.7 % before fees (167 trades), and those over 20 days earn +60.0 % (19). Trades closed within 5.5 days lose a mean −2.0 % (687), and those held 5.5 to 10 days earn +2.6 % (334).
- **F3:** Over 5 days, the move grows with the size of the break up to a point, then levels off. On all first breaks (1,940 events), it is +0.77 % for breaks of 0 to 0.1 usual daily moves (t 1.52), +1.76 % for 0.1 to 0.3 (t 3.71), +3.13 % for 0.3 to 0.6 (t 4.01) and +2.59 % above 0.6 (t 3.11). Over 20 days the quartiles rise steadily, from +2.1 % to +6.4 %, but the rank correlation is weak (Spearman 0.04, 572 cases).
- **F4:** Acting at the hour of the break catches a small part of the move that a trader acting at the daily close misses. From the break hour to that day's close, the coin rises +0.41 % (t 2.27, 663 cases, a mean of 12 hours to the close). The 5-day unusual move is +1.63 % when entering at the hour and +1.31 % when entering at the following daily close.
- **F5:** Other features of the break do not grade the move once their rank correlation is checked. Spearman correlations with the 5-day move are 0.009 for the breakout hour's volume, −0.019 for the width of the 20-day range, 0.001 for the prior 30-day return and 0.018 for the breakout hour's own return. Each has one weak quartile (for example, a 30-day return in the lowest quartile gives +0.16 % against +1.5 % to +2.8 % for the others), but none of these stands out among the many angles looked at.
- **F6:** The move is not tied to a time of day or a weekday. Every 4-hour UTC block gives a positive 5-day move, from +0.93 % to +2.87 %, and Sunday is the weakest weekday (+0.62 %, t 0.95, 224) without differing clearly from the others. The 1-day return and the distance to the 20-day low give no monotonic pattern on the 5-day grid.

## Ideas
- `018-02_hourly-breakout-multiday-continuation.g1_hourly-breakout-ten-day-continuation` (from F1, F2, F3): When a coin's hourly close first rises above its highest price of the prior 20 days, the price keeps rising over the next 10 days by more than the coin's usual 10-day return. The further that close sits above the 20-day high, in multiples of its 30-day average absolute daily return, the larger the rise.
- `018-02_hourly-breakout-multiday-continuation.g2_hourly-breakout-twenty-day-continuation` (from F1, F2): When a coin's hourly close first rises above its highest price of the prior 20 days, the price keeps rising over the next 20 days by more than the coin's usual 20-day return. The further that close sits above the 20-day high, in multiples of its 30-day average absolute daily return, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
