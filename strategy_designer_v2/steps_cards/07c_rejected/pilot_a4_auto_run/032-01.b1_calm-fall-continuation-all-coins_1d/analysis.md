---
line: 7.c no effect
backtest: 032-01.b1_calm-fall-continuation-all-coins_1d
idea tested: 032-01.b1_calm-fall-continuation-all-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3602 USD
---
## Findings
- **F1:** The tested grading is absent and its sign is wrong. Inside falling calm (477 one-day cases on BTC, XMR and DOGE), the slope of next-day excess return on the 30-day return is +0.0098 (t +0.69). By 30-day-return quintile the next-day excess runs +0.32 %, -0.54 %, -0.68 %, +0.19 %, +0.47 %, from the deepest fall (-31 %) to the shallowest, with no monotone continuation. Step 5's full test gave a slope t of -0.03 on 2502 cases.
- **F2:** Instead, the market continues the last few days' move over the next 3 to 10 days. Inside falling calm, the slope of 5-day excess return on the 3-day return is +0.39 (t +3.59, 113 cases). On the 7-day return it is +0.18 (t +2.39, 108 cases), and on the 14-day return +0.16 (t +2.32, 104 cases). At 10 days, the slope on the 14-day return has t +2.69 (50 cases). The 30-day return carries none of it (t +0.86 at 5 days, +0.92 at 10 days).
- **F3:** The short side the brief imagined exists only for the most recent fall, which a long-only book cannot take. Coins in the bottom quartile of 7-day return (mean -16 %) had a 5-day excess of -4.2 %, against +1.8 % for the top quartile (mean +11 %), over 24 cases each. At 3 days the same quartiles give -1.1 % and +0.8 %.
- **F4:** Distance above the 30-day low grades the next days the same way. Its slope on excess return has t +2.10 at 3 days (155 cases), +2.21 at 5 days (94 cases) and +2.19 at 10 days (47 cases). The 3-day quartiles run -0.15 %, -2.2 %, +1.1 %, +1.6 %, from closest to the low (+0.5 %) to furthest (+23 %).
- **F5:** The recent-move continuation belongs to the falling calm profile. Outside the profile, the 5-day slope on the 7-day return is +0.016 (t +0.48, 568 cases).
- **F6:** Inside the profile the continuation points the same way on every coin. The correlation of the 7-day return with the 5-day excess is +0.25 on BTC, +0.26 on XMR and +0.14 on DOGE. By year it is +0.29 in 2018, -0.02 in 2019 and +0.22 in 2021. These t-statistics are not clustered by day and rest on 94 to 113 cases.
- **F7:** In falling calm the coins did not keep falling on average. The mean total next-day return in the profile is +0.10 %, and the 10-day excess return is +0.64 % (47 cases). The book's -0.22 % per case is -0.7 times the 0.33 % cost of a trade. A longer horizon is needed for the move to cover that cost.

## Ideas
- `032-01.b1.c1_calm-decline-bounce-follow-through` (from F2, F3, F5, F6, F7): In a falling, calm market, the more a coin has risen over the past 3 days, the more it rises over the next 5 days.
- `032-01.b1.c2_lift-off-monthly-low` (from F4, F1, F7): In a falling, calm market, the further a coin's close sits above its lowest close of the past 30 days, the more it rises over the next 5 days.
- `032-01.b1.c3_two-week-recovery-continues` (from F2, F5, F7): In a falling, calm market, the more a coin has risen over the past 14 days, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
