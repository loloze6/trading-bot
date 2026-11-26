---
line: 7.g patterns
backtest: 058-02_choppy-agitated-weekly-fall-continues_1d
idea tested: 058-02_choppy-agitated-weekly-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3555 USD
---
## Findings
- **F1:** The tested fall-continuation is not in these folds. In the choppy agitated profile, which held only 4.8 % of the coins' bars, coins fell on the 7-day grid after weeks of either sign. After a falling week the unusual 7-day move was -10.7 % (18 cases, 12 days, clustered t -1.87). After a rising week it was -4.9 % (12 cases, 9 days, t -2.68). Split by 7-day scaled return, there is no grading: the lowest quintile gave -13.3 % and the top quintile -7.7 %.
- **F2:** The in-profile decline does not hold up as a separate effect. The grid's pooled -8.4 % per 7 days (30 cases, 20 days, t -2.30) comes from very few cases. Read over every in-profile bar, the 7-day move is positive in w11, w12, w13 and w14 (+11.1 %, +6.5 %, +0.1 %, +5.9 %) and negative in w15 to w18. It shows windows that happened to be falling, not a property of the profile.
- **F3:** In choppy markets outside the agitated profile (60-day return between -10 % and +10 %, calm swing), a week with a large rise against the usual swing kept rising over the next 7 days. The top quartile of the 7-day scaled return was followed by an unusual move of +11.5 % (18 cases, 9 days, clustered t 3.34). The three lower quartiles gave +0.0 %, -1.5 % and -4.0 %, all with |t| ≤ 1.3.
- **F4:** The same lean shows weakly across all bars outside the profile, but the grading is faint. The top two quintiles of the 7-day scaled return were followed by +2.4 % unusual 7-day moves (t 1.98 and 1.70, about 160 cases each). The bottom two gave -0.6 % (t -0.5). The rank correlation is only 0.035 over 795 grid cases.
- **F5:** No other angle stood out beyond what chance allows across the many angles looked at. The 1-day scaled return spread over the next 3 days stayed within |t| 1.8. Close location gave |t| < 0.3. The day's range was not monotone in its quintiles (t +2.3, -3.4, -0.9, -0.6, +2.0). Weekdays gave next-day t from -2.8 on Wednesday to +2.8 on Thursday and Friday.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-02.g1_choppy-calm-rally-continues` (from F3, F4): In a choppy, calm market, a coin whose 7-day return is a rise keeps rising over the next 7 days, and the larger that 7-day rise is against the coin's usual daily swing over the past 30 days, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
