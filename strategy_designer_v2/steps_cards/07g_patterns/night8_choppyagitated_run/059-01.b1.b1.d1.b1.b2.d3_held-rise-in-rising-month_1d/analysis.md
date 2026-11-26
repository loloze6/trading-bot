---
line: 7.g patterns
backtest: 059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d
idea tested: 059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4153 USD
---
## Findings
- **F1:** No pattern stood out once cases on the same day were counted together. The strongest one, the lowest fifth of the 30-day-to-90-day swing ratio, was followed by a +6.6 % excess 7-day return (t 2.30). That rests on 65 cases but only 21 days, and half the cases (33) sit in window w18, with another 6 in w16. The higher fifths were all flat or negative (-3.4 % to +2.6 %, t -1.6 to 0.9).
- **F2:** The same ratio over shorter spans shows nothing graded. On 14 against 60 days, the lowest fifth gives -0.4 % (t -0.17, 42 days) and the Spearman correlation with the excess return is -0.045. On 7 against 30 days, the lowest fifth gives -1.6 % (t -1.0, 64 days). So F1 is not a robust "quiet coin rises" effect.
- **F3:** The weekday effect disappears when cases are clustered by day. Grid bars on Fridays looked like +4.9 % over 7 days (t 4.6, 255 cases), but the grid has few distinct start days. The next-day excess return by weekday is between -0.44 % and +0.37 %, with every t_day between -1.1 and 1.44 over about 206 days each. Friday's next-day excess changes sign across years (2018 +0.21 %, 2021 -0.12 %).
- **F4:** Inside the profile, the tested idea's own conditions carry the rise, and that is not new. The top fifth of the scaled weekly rise was followed by +5.5 % excess (t 2.4, 32 cases), and a close in the top fifth of the week's range by +7.0 % (t 2.5, 30 cases). Both are counted without day clustering, consistent with the step-5 size of +1.30 % (t 1.41, 231 days).
- **F5:** The book's gain rests on one window, and one coin loses. Window w18 carries +585 of the +837 summed trade-percent points (31 trades, mean +18.9 %). Windows w7, w9 and w14 lose (means -7.1 %, -5.9 % and -4.7 %). XMR is the only losing coin (22 trades, mean -2.9 %), against XRP's +11.8 % over 21 trades. This explains the Calmar failure more than any untested pattern does.
- **F6:** Outside the profile, follow-through after a strong week is weak and not reliable. The top fifth of the scaled 7-day rise gave +1.5 % excess (t 1.04, 148 cases), and the lowest fifth gave -3.0 % (t -2.7). The 30-day return fifths are not monotone (-0.8 %, -2.6 %, -1.0 %, +2.9 %, +0.5 %).

## Ideas
- No ideas: Across the angles examined, nothing stands out from chance once cases on the same day are clustered and the number of angles is weighed. The strongest candidate, a low 30-to-90-day swing ratio, reaches only t 2.30 on 21 days, mostly from one window, and fails on the 14/60 and 7/30 spans. The angles examined were the forecast, week-range position, 30-day return, three volatility ratios, the last day's return, weekday, year, window, coin and trades.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
