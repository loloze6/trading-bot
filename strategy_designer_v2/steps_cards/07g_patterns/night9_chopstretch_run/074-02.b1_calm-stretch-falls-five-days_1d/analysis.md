---
line: 7.g patterns
backtest: 074-02.b1_calm-stretch-falls-five-days_1d
idea tested: 074-02.b1_calm-stretch-falls-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6073 USD
---
## Findings
- **F1:** In calm markets the signed stretch from the 20-day average carries forward over 5 days. On the 5-day grid (773 cases, 196 days) the day-clustered slope t is 3.17. The bottom stretch quintile's unusual move is −3.54 % (t −4.20, 148 cases) and the top quintile's is +2.99 % (t 3.29, 172 cases). Over 10 days the slope t is 2.64 (379 cases, 95 days).
- **F2:** That calm effect is a split between the below and above sides, not a gradient inside the below side. On below-average cases alone the raw slope t is 0.56 (376 cases, 129 days) and the forecast-depth slope t is −1.38. This is why the tested idea came out inconclusive (verdict slope t −0.85) while its mean unusual move stayed positive (+0.72 %, t 1.80).
- **F3:** The calm stretch effect is not steady across windows. The 5-day Spearman correlation is positive in 7 of 12 windows (from −0.131 to +0.340). The per-window correlation inside each trend is positive in only 45 % (choppy), 55 % (rising) and 36 % (falling) of windows.
- **F4:** In agitated markets the brief's rebound after a stretch below the average is absent at 5 days in folds B and C. The agitated quintile means run from −1.10 % to +2.14 % with no order (all |t| < 1.9). The below-side slope is −0.0115 with clustered t −1.05 (331 cases, 112 days). The 10-day agitated quintiles are also unordered (−2.12 % to +2.94 %, all |t| < 1.4).
- **F5:** In agitated markets the next day reverses the day's move. The slope of the next-day unusual return on the day's return in 20-day swing units has clustered t −2.22 (2,946 cases, 866 days). The slope on the close's place in the day's range has t −2.77. This repeats the agitated low-close and fall-rebound ideas the map already holds in every agitated profile.
- **F6:** In falling agitated markets two patterns stand out. A down day is followed by a next-day unusual rise of +1.40 % (t 2.42, 377 cases) with graded slope t −2.23, which repeats 047-01 and 051-01. An up day is followed by −1.05 % (t −2.08, 361 cases, negative in every window), but that fade is not graded (slope t −0.68) and is gone by 2 days (−0.09 %, t −0.08).
- **F7:** The weekday means of the next-day unusual return have the largest |t| at Wednesday (−0.50 %, t −2.78), Thursday (+0.41 %, t 2.80) and Friday (+0.38 %, t 2.74). These t's count coins of the same day as separate cases, and they are three of seven groups searched.

## Ideas
- No ideas: The one strong pattern, calm stretch continuation (F1), is not graded on the side the idea tested (F2), is unsteady across windows (F3) and repeats the calm nearness-to-high and range-edge continuation books the map already holds. The brief's agitated rebound is not in the data at 5 or 10 days (F4). The agitated and falling-agitated reversals repeat held ideas or are not graded (F5, F6). The weekday pattern does not stand out once same-day cases and the many angles searched are allowed for (F7).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
