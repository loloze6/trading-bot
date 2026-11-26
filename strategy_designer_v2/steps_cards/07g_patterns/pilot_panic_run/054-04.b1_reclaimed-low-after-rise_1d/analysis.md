---
line: 7.g patterns
backtest: 054-04.b1_reclaimed-low-after-rise_1d
idea tested: 054-04.b1_reclaimed-low-after-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4165 USD
---
## Findings
- **F1:** Across all profiles in folds B and C, a day that trades below the prior 30 days' lowest low and closes back above it is followed by a 10-day move graded by the coin's 60-day return before that day. By quartile of that return, from lowest to highest, the unusual 10-day move is +4.9 % (t 0.91, 23 cases, 14 days), −2.0 % (t −0.51, 24 cases), −8.6 % (t −2.30, 24 cases, 16 days) and −12.8 % (t −3.69, 22 cases, 14 days), with strengths running from +0.30 to −0.78 of a usual move.
- **F2:** The same grading holds when the day closes below the 30-day low. By 60-day-return quartile the unusual 10-day move is −2.6 % (t −0.50), −2.2 % (t −0.47), −8.6 % (t −1.93) and −14.6 % (t −2.36, 19 cases, 12 days). Pooling both kinds of event, those after a 60-day rise above +10 % average −16.2 % (t −3.66, 14 cases, 9 days) and those in a choppy 60 days −12.9 % (t −3.21, 22 cases, 16 days), against −2.6 % (t −0.63, 76 cases) after a 60-day fall below −10 %.
- **F3:** The tested book's agitated filter keeps only a sliver of the reclaims: 39 cases in the verdict against 114 reclaims over all profiles here. In the agitated bars I could measure, the trend groups hold 1 to 11 cases each, and the falling-agitated group even moved the other way (+8.7 %, t 1.11, 11 cases). The effect is not visible as living in the agitated profile.
- **F4:** The book's problem is how rarely it trades, not cost. It held a position on 3.95 % of the coins' days, made 56 trades over folds B and C, and its trades' net results swing by window from −11.3 % to +11.0 %. Meanwhile the verdict's unusual move per case (+3.72 %) is 19 times the 0.19 % cost of a trade.
- **F5:** Among reclaims after a 60-day fall below −10 %, a close high in the day's range is followed by −9.8 % over 10 days (t −2.37, 25 cases, 15 days), against +4.6 % (t 0.87, 27 cases) after a close low in the range. This is one cut among many I looked at, so it does not stand out enough to carry an idea alone.
- **F6:** Other angles showed patterns the portfolio already holds, or nothing:

## Ideas
- `054-04.b1.g1_reclaimed-low-after-rise-any-market` (from F1, F3, F4): When a coin's day trades below its lowest price of the past 30 days but closes back above that low, the coin falls over the next 10 days, and the fall is larger the higher the coin's 60-day return before that day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `054-04.b1.g2_monthly-low-break-after-rise` (from F2, F1): When a coin closes below its lowest price of the past 30 days, it keeps falling over the next 10 days, and the fall is larger the higher the coin's 60-day return before that day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
