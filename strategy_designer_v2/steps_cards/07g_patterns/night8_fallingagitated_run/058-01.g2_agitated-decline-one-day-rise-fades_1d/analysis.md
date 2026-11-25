---
line: 7.g patterns
backtest: 058-01.g2_agitated-decline-one-day-rise-fades_1d
idea tested: 058-01.g2_agitated-decline-one-day-rise-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6001 USD
---
## Findings
- **F1:** In the falling agitated profile, an up day is followed the next day by an unusual move of -1.00 % (raw -0.84 %, t -2.26 with one day's cases taken together, 500 cases on 195 days). The fade is negative on all 6 coins (-0.41 % to -1.47 %), in 9 of 10 windows and in all 4 years. Outside the profile, up days are followed by only -0.15 % (t -0.91, 2,706 cases), so the give-back lives in this profile.
- **F2:** The give-back is a one-day effect, which the tested 3-day horizon misses. The idea's 3-bar unusual move is +0.33 % (t 0.73, 694 cases), and in-profile up days measured over 2 days give -0.30 % (t -0.32, 280 cases). The book's short positions, held 3 days, earn -0.30 % on their next day (t -0.82, 771 cases), and its Sharpe is -0.16.
- **F3:** Inside the profile, the next-day fade does not grow with the size of the up day. The slope of the next-day unusual move on the up day's return in 30-day standard deviations is +0.0015 (t 0.24, 500 cases), and the quartiles give -1.02 %, -0.65 %, -1.67 % and -0.65 %. The step-5 larger-minus-smaller check was also negative, -0.19 %. The brief's grading by rise size is not in the data.
- **F4:** Among in-profile up days, the upper wick does grade the next-day fall. The wick is the distance from the close to the day's high in 30-day standard deviations, and the slope is -0.0247 per standard deviation (t -2.43 day-clustered, 500 cases, 195 days). It is the only one of the six up-day gradings tried that stands out. The others were the day's size, the prior 5-day move, the 20-day return, the swing ratio and the close location, all with |t| under 1.
- **F5:** The size of the next-day fade is large against the cost of a trade. The raw next-day fall of 0.84 % per up day, which is the total move in the short direction, is about 4.4 times the 0.19 % cost of a trade. The idea's tested 3-day total move was -0.3 times that cost.
- **F6:** Over all in-profile days, the next-day unusual move falls with the day's scaled return: slope -0.0141 per standard deviation (t -3.14 day-clustered, 1,022 cases, 343 days). Much of this comes from down days rebounding, +1.23 % (t 2.66, 522 cases), and from low closes rebounding, +2.16 % for closes in the bottom fifth of the range (t 4.94, 243 cases). That long side is already held: the falling agitated long cell has 12 strategies.
- **F7:** Weekday patterns appeared in the 1-day returns. In-profile Tuesdays gave +1.42 % (t 3.32, 188 cases). Out-of-profile Thursdays and Fridays gave +0.75 % (t 4.86) and +0.60 % (t 4.14), about 1,000 cases each. Given the many angles looked at, and with a late-week gain already held (045-01, rising market), these are not proposed.

## Ideas
- `058-01.g2.g1_agitated-decline-upper-wick-fade` (from F1, F2, F4, F5): In a falling, agitated market, a coin's up day is followed by a fall over the next day, and the further the day closed below its high, measured against the standard deviation of its daily returns over the past 30 days, the larger that next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
