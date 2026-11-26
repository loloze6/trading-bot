---
line: 7.b inconclusive
backtest: 058-02.b1.g1_falling-market-rally-fades_1d
idea tested: 058-02.b1.g1_falling-market-rally-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4788 USD
---
## Findings
- **F1:** In folds B and C, the one-day effect sits on the idea's side but is not graded by the size of the rise. Every short case's next-day unusual move averages +0.47 % with t 1.98 (1,603 cases, 526 days), and weighted by abs(forecast) it is only +0.38 % with t 1.29. By forecast quartile it is +0.66 %, +0.75 %, -0.01 % and +0.49 %. By the rise in usual moves it is +0.67 % for 0 to 0.5, +0.35 % for 0.5 to 1, +0.52 % for 1 to 2 and +0.88 % above 2 (t 1.06, 62 cases). The correlations of the move with abs(forecast) and with the scaled rise are -0.024 and -0.005. This is why step 5's supporting check failed (-0.16 %, Welch t -0.91) and the weighted main t stayed at 1.51.
- **F2:** Inside the falling profile, what matters is the day's sign, not its size: the coin reverts over one day either way. Next-day unusual moves in the short direction are +0.57 % after up days (t 2.18, 1,391 cases, 457 days) and -0.36 % after down days (t -1.44, 1,580 cases), with -0.91 % after falls of 1 to 2 usual moves (t -1.85). All falling days together give +0.02 % (t 0.12).
- **F3:** The fade of up days lives where the coin is swinging more than its usual. Up days in a falling market are followed by an unusual fall of +1.27 % (t 3.15, 509 cases, 209 days) when the 30-day swing is above its running median. They give only +0.14 % (t 0.40, 717 cases, 286 days) when it is at or below.
- **F4:** The effect is strong in some years and absent in others, which also blurs the pooled t. Up-day fades are +1.03 % in 2018 (t 2.03) and +0.63 % in 2019 (t 2.21), but +0.10 % in 2020 and -0.10 % in 2021. The plan's short cases show the same pattern: +0.82 %, +0.57 %, -0.02 % and -0.01 %.
- **F5:** The test's one-day horizon is where the effect is. Over 2, 3 and 5 days the short cases' unusual move is +0.09 % (t 0.19), -0.17 % (t -0.26) and -0.22 % (t -0.20).
- **F6:** Per case, the idea's total move is +0.18 %, which is 0.9 times the 0.19 % cost of a trade. The book lost money: Sharpe -0.11, yearly return -1.7 %. A move this small cannot pay unless the cases are concentrated where the fade is larger, such as the agitated part in F3.

## Ideas
- `058-02.b1.g1.b1_falling-rally-fades-more-coins` (from F1, F2): In a falling market, the larger a coin's one-day rise is against its usual daily swing over the last 20 days, the larger its fall over the next day.
- `058-02.b1.g1.b2_agitated-falling-rally-fades` (from F3, F2, F5, F6): In a falling, agitated market, the larger a coin's one-day rise is against its usual daily swing over the last 20 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
