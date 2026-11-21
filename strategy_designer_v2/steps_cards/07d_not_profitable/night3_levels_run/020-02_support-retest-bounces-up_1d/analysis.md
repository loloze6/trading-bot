---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up_1d
idea tested: 020-02_support-retest-bounces-up
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4992 USD
---
## Findings
- **F1:** The tested situation carries no rise. On the 5-day grid, the 734 active cases had a mean excess return of -0.60 % (t -1.86) and a total move of -0.02 %, against +0.16 % (t 0.73) for the 2,685 inactive cases. The verdict's total move of +0.02 % per case is 0.1 times the 0.19 % cost of a round trip, so no change of holding or sizing can make this book pay.
- **F2:** The book's yearly return is -6.2 % on its chained daily returns, with a deepest fall of 61 %, which gives the failing Calmar of -0.10.
- **F3:** The loss is not tied to one period, so leaving one window out fails as well. Active cases lost in 5 of 8 years: 2018 -3.0 % (t -2.41, 86 cases), 2019 -2.1 % (t -2.19), 2021 -2.4 % (t -1.91) and 2022 -1.6 % (t -1.71). Only 2020 gained, +2.5 % (t 3.03, 80 cases).
- **F4:** The grading runs the wrong way. The top quarter of the forecast (the most past turns near the close) had the worst excess, -1.23 % (t -1.81, 184 cases), against -0.30 % to -0.54 % in the other quarters. The Spearman correlation between forecast and excess return was -0.017.
- **F5:** The only active cases that rose sat inside a strong 90-day rise. In the top quarter of the 90-day return (mean +54 %), the excess was +1.29 % and the total move +1.88 % (39 cases, t 0.69). In the bottom quarter (mean -39 %), the excess was -1.94 % (t -1.11). The Spearman correlation between 90-day return and excess across active cases was +0.15.
- **F6:** The same split shows against the 50-day average and the 90-day range. Active cases in the top quarter of the close against its 50-day average (mean +4.5 %) had an excess of -0.01 %, while the second quarter (-7.1 %) had -1.11 % (t -1.93). In the 90-day range, the top fifth had +0.32 % and the middle fifth -1.83 % (t -2.54, 123 cases).
- **F7:** A close below the prior 60-day low was followed by no clear continuation: -0.64 % excess (t -0.48), but on only 56 cases.

## Ideas
- `020-02_support-retest-bounces-up.d1_support-bounce-in-uptrends` (from F1, F3, F4, F5, F6): When a coin's price falls back to a price where it turned up several times in the past 90 days, it tends to rise over the next 5 days, and the more times it turned up there before, the larger the rise, only while its 90-day return is positive, and the larger that 90-day return, the larger the rise.
- `020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend` (from F1, F3, F5, F6): When a coin's price falls back to a price where it turned up several times in the past 90 days while its 90-day return is negative, it tends to fall further over the next 5 days, and the deeper that 90-day fall, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
