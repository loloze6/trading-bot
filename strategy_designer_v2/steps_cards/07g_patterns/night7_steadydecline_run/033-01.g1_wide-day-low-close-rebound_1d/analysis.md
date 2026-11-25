---
line: 7.g patterns
backtest: 033-01.g1_wide-day-low-close-rebound_1d
idea tested: 033-01.g1_wide-day-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4530 USD
---
## Findings
- **F1:** The rebound after a close near the day's low lasts one day and is then given back. The forecast's day-clustered slope on the next day's excess return is positive (t 3.38). On the following day it is negative (t -2.66). Over the two days together it is t 0.81, about nothing. In the bottom close-location fifth, day 1 is +0.52 % (t 3.82) and day 2 is -0.53 % (t -4.10, 1,720 cases).
- **F2:** The effect needs a wide day. The close-location slope is t -0.15 in the narrowest third of days, against t 2.86 and t 2.88 in the middle and widest thirds. Low-half closes on the widest third of days are followed by +0.93 % the next day (t 5.36, 1,268 cases), against +0.36 % in the middle third and -0.28 % in the narrowest.
- **F3:** The pattern is almost all on the low-close side. The slope is t 2.70 on bars with the close in the lower half (3,669 bars, 950 days) and t 0.55 in the upper half. The book's position gain sums to 3.02 on long bars against 0.44 on short bars, for similar counts (4,288 against 4,258).
- **F4:** By profile, the effect sits in agitated, non-rising markets. The slope is t 2.45 in falling agitated (651 bars, 201 days) and t 2.03 in choppy agitated (145 bars). It is t -0.03 in falling calm, t -0.77 in rising agitated and t 0.91 in rising calm. With a 30-day swing rank, agitated gives t 2.86 against calm t 1.00. But on the low-close side alone the agitation split is not clear (agitated t 0.28 against calm t 1.11, on fewer bars), so the profile result is suggestive, not firm.
- **F5:** The day-2 giveback is graded and shows on both sides. On upper-half closes, the slope of the second day's return on the forecast is t -2.22 (4,316 bars, 1,042 days): the nearer the close to the high, the larger the second-day rise. The most near-high fifth of the forecast gains +0.45 % on day 2 (day-clustered t 2.09). The top close-location fifth gains +0.37 % (t 2.79).
- **F6:** The next-day rebound is spread across coins and years, but unevenly. In the top forecast fifth, day-clustered t is 3.16 for XMR, 2.41 for ZEC, 2.10 for ETH and 0.75 for BTC. By year, t is 2.65 in 2020 and 0.57 to 1.48 in 2018, 2019 and 2021. This adds to the 0.25 %-per-case size, which is only 1.3 times the 0.19 % cost of a trade.

## Ideas
- `033-01.g1.g1_falling-agitated-low-close-rebound` (from F4, F2, F3, F1): In a falling, agitated market, the wider a coin's day is against its usual daily range and the nearer its close sits to that day's low, the larger its rise over the next day.
- `033-01.g1.g2_second-day-reversal-after-extreme-close` (from F5, F1): The wider a coin's day is against its usual daily range and the nearer its close sits to that day's high, the larger its rise from the close one day later to the close two days later.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
