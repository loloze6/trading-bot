---
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
idea tested: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3521 USD
---
## Findings
- **F1:** The book fails on mean daily return (0.000288 against 0.0005) because it is invested only one day a week, not because trades cost too much. It holds a position on 6.1 % of bars, at a mean allocation of 0.58, and earns 0.25 % per active bar. Each case's total move (+0.90 %) is 4.7 times the 0.19 % cost of a trade.
- **F2:** The 7-day continuation exists on Saturday only. The correlation of the 7-day return with the next day's excess return is 0.185 on Saturdays (rising minus falling weeks, Welch t 4.68, 1172 rising cases). On every other day the correlation lies between -0.07 and +0.07, so stretching this same signal to more days adds no gain.
- **F3:** Sunday shows the opposite effect, a reversal. The next-day excess return correlates -0.093 with the 7-day return and -0.102 with the 1-day return. Rising weeks minus falling weeks give Welch t -2.49. The quintile with the lowest combined momentum earns +0.69 % on Sunday (t 2.98, 378 cases), and the other quintiles are flat to negative.
- **F4:** Wednesday also shows a reversal of the 3-day return: correlation -0.113 with the next day's excess return, over 1859 cases.
- **F5:** The Saturday effect is graded. Next-day excess returns by 7-day-return quintile run -0.19 %, -0.04 %, +0.22 %, +0.60 %, +0.99 %. It does not grow when held longer: the top quintile is +0.88 % after 2 days and +0.42 % after 3, so it gives back part of the gain on Sunday.
- **F6:** Combining lookbacks does not beat the best single one on Saturday. The correlation with the next day's excess return is 0.163 for the combination, against 0.187 for the 7-day return, 0.132 for the 28-day return and 0.091 for the 3-day return.
- **F7:** Adding the short side on Saturday would add little. The lowest 7-day quintile earns only -0.19 % the next day, and the lowest combined quintile -0.29 % (t -1.34).
- **F8:** Within Saturdays after a rising week, the move does not rise steadily with volatility. The next-day excess return is +0.80 %, +0.32 % and +1.10 % from the lowest to the highest volatility tercile, with correlations of 0.29, 0.15 and 0.32.

## Ideas
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.d1_weekend-continuation-then-reversal` (from F1, F2, F3, F5): On a Saturday, a coin's return over the next day is larger the higher its return over the preceding 7 days, and on a Sunday, a coin's return over the next day is larger the lower its return over the preceding 7 days.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.d2_sunday-reversal-of-weak-weeks` (from F3, F5): On a Sunday, a coin's return over the next day is larger the lower its return over the preceding 7 days.
- `022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week.d3_midweek-short-term-reversal` (from F4, F1): On a Wednesday, a coin's return over the next day is larger the lower its return over the preceding 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
