---
line: 7.g patterns
backtest: 031-03.b1_deep-yearly-low-break-rebounds_1d
idea tested: 031-03.b1_deep-yearly-low-break-rebounds
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4193 USD
---
## Findings
- **F1:** The tested situation is too rare to judge. The book held a position on only 2 % of coin-days (325 active coin-days, only 4 of 6 coins). It made 25 trades in total, 15 of them on ZEC. Its 5 best days carry 75 % of its total daily gain (282 active book days). So its +0.7 % yearly return rests on a handful of breaks, matching the verdict's 12 case days.
- **F2:** On the 10-day non-overlapping grid, the top fifth of closes nearest their 30-day high showed the clearest pattern. They had a mean unusual move of +3.21 % (strength 0.19, day-clustered t 1.89 over 92 days), against about -0.6 % to -1.2 % in the other four fifths. Top minus bottom was +3.8 % with Welch t 2.43. Top beat the rest in all 6 coins, but in only 5 of 8 years: 2022 and 2023 went the other way, and 2018 had a single case. With the 60-day high, the same reading weakens to +2.5 % (t 1.47, 65 days).
- **F3:** Other 10-day grid features show no graded effect. The prior 10-day return gives top-bottom +2.1 % (t 1.57). The prior 20-day return gives +2.7 % (t 1.79). Distance above the 30-day low gives +2.2 % (t 1.51). The 20-day volatility gives +0.9 % (t 0.64). The volatility ratio gives +1.8 % (t 1.35). The day's return gives -1.0 % (t -0.75). The day's range gives +1.0 % (t 0.73). Every Spearman correlation with strength is at or below 0.05 in absolute value, with p ≥ 0.06.
- **F4:** Saturdays' daily coin return beats the coin's mean by +0.31 % (day-clustered t 2.15, 414 days). It is positive in all 6 coins (t from 0.35 on BTC to 2.58 on LTC), and above the other weekdays in 6 of 8 years. It does not grade with Friday's return: Saturday's excess runs from +0.03 % to +0.47 % across Friday's return quintiles, with no order.
- **F5:** The day after a coin's bottom-fifth daily return (mean -5.9 %), its excess return is +0.44 %. Every other quintile sits between -0.18 % and -0.04 %, so any next-day rebound shows only after the largest falls and is not graded.

## Ideas
- No ideas: I looked at about 15 angles: eight 10-day grid features, two lookbacks of distance to the recent high, weekday by year and by coin, next-day reversal, and the book's concentration. Given that many, nothing stands out beyond chance: the strongest graded pattern (F2) reaches a Welch t of 2.43 and a clustered t of 1.89 and fails in 2 of 8 years, and the only pattern with a clustered t above 2 (F4, Saturday) is a calendar effect with no graded situation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
