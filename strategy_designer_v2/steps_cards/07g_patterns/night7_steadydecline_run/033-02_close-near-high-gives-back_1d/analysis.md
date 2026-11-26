---
line: 7.g patterns
backtest: 033-02_close-near-high-gives-back_1d
idea tested: 033-02_close-near-high-gives-back
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4075 USD
---
## Findings
- **F1:** The pattern lives at the low end of the range, not the high end the tested idea shorts: next-day return minus the coin's mean is +0.58 % (t 1.98, 487 days) after closes in the lowest fifth of the range but only -0.34 % (t -1.66, 675 days) after closes in the top fifth, and the close-near-high pressure (location × relative width) has a slope of -0.0028 (t -1.21, 7968 cases) against +0.0109 (t 3.69, 7968 cases) for the close-near-low pressure ((1 − location) × the day's width over its 20-day mean width).
- **F2:** The close-near-low pressure carries a move larger than a trade's cost: its top fifth is followed by a raw next-day return of +1.11 % (t 3.76, 1596 cases on 500 days), which is 5.8 times the 0.19 % cost; the unusual move is +0.97 % (t 3.30), while the four lower fifths all sit between -0.08 % and -0.13 % raw.
- **F3:** The effect needs a wide day: in the widest third of days relative to their 20-day width, the slope of next-day return on close location is -0.0237 (t -3.51, 2668 cases), and closes in the lowest fifth gain +1.43 % (t 3.24, 217 days); in the narrowest third the slope is -0.00003 (t -0.01, 2655 cases).
- **F4:** The effect needs a swinging coin: the close-near-low pressure slope is +0.0202 (t 4.92, 3953 cases) in the coin's higher half of 20-day volatility against +0.0034 (t 1.29, 3943 cases) in its lower half, and the close-location slope is -0.0261 (t -3.21) in the top volatility third against +0.0009 (t 0.17) in the bottom third.
- **F5:** The pressure is a down-day effect: on down days the close-near-low pressure slope is +0.0123 (t 3.45, 3927 cases), while on up days the close-near-high pressure slope is -0.0013 (t -0.51, 4041 cases).
- **F6:** The close-near-low pressure holds in every coin and every year: the slope is positive on all six coins (t from 1.97 for BTC to 3.45 for ZEC) and in all four years (t 1.23 in 2019 to 5.34 in 2020).
- **F7:** The rebound lasts about two days and is gone by three: on non-overlapping 2-day returns the close-near-low pressure slope is +0.0113 (t 2.87, 3966 cases) and the close-location slope is -0.0128 (t -1.75), while on 3-day returns the close-location slope is +0.0051 (t 0.49).
- **F8:** The tested book is a near-permanent short of the market rather than a timing book: its mean position is -0.43, its daily returns correlate -0.86 with holding the coins, and its gain before costs is -1.08 bp per bar; it lost 16.7 bp a day in 2020 while the coins rose 42.3 bp a day, and earned 15.1 bp a day in 2018 while the coins fell 34.9 bp.

## Ideas
- `033-02.g1_wide-low-close-rebounds` (from F1, F2, F3, F5, F6, F7): The nearer a coin's daily close sits to that day's low, and the wider that day's high-low range is against the coin's average range over the past 20 days, the larger the coin's rise over the next day.
- `033-02.g2_agitated-wide-low-close` (from F3, F4, F2): In an agitated market, the nearer a coin's daily close sits to that day's low, and the wider that day's range is against its average range over the past 20 days, the larger the coin's rise over the next day.
- `033-02.g3_low-close-two-day-rebound` (from F5, F7, F2): The nearer a coin's daily close sits to the day's low on a down day, and the wider that day's range is against its average range over the past 20 days, the larger the coin's rise over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
