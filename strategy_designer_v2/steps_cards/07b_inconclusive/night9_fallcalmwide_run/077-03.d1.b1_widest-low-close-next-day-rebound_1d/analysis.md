---
line: 7.b inconclusive
backtest: 077-03.d1.b1_widest-low-close-next-day-rebound_1d
idea tested: 077-03.d1.b1_widest-low-close-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3891 USD
---
## Findings
- **F1:** The tested result is on the side the idea predicts but far short of the bar: +0.44 % mean excess next-day return, t 0.77, on 96 cases over 78 days. The test already used every fold and all 19 coins on 1d bars, so no more data is available. In folds B and C alone the 23 long cases average +2.5 % (t 2.42), so folds A and D must carry little or a negative effect.
- **F2:** Inside the choppy agitated profile (244 bar-cases on 174 days, folds B and C), the signed score rises with the next-day excess return (Spearman rho 0.21, p 0.0009). The score is the day's width against its 30-day swing times how far the close sits from mid-range, positive for low closes. The effect is graded across the whole range: about −6.4 % (4 cases), −3.9 % (27), −1.4 % (68), −1.5 % (79), +1.0 % (38), +0.2 % (18) and +4.6 % (10), from the widest high closes to the widest low closes.
- **F3:** The high-close side is the clear one. Wide days closing near their high (score ≤ −1) are followed by a −3.9 % next-day excess return (t −2.19 over 22 days). That is −3.2 % below the profile's own mean (Welch t −1.96 against mid-range days, 31 cases). It is negative in every year: 2018 −1.9 %, 2019 −2.1 %, 2020 −10.4 %, 2021 −4.0 %.
- **F4:** The tested low-close side is weak and uneven. Wide low closes (score ≥ 1) average +2.7 % above mid-range days (Welch t 1.83, 28 cases). Moderate ones (score 1 to 2) give only +0.15 % (t 0.13, 17 days), and only the widest (score > 2) reach +4.6 % (t 1.55, 7 days). By year: 2018 −1.3 %, 2019 +3.0 %, 2020 +2.8 %, 2021 +0.05 %.
- **F5:** The profile's own next days lean down: all in-profile bars average −1.06 % excess (t −1.17, 174 days). That works against the long side and with the short side. Only 37 in-profile bars in folds B and C close in the lower fifth, which leaves the long-only test few cases.
- **F6:** Wide low closes do rebound strongly outside the profile: +1.67 % next-day excess, t 5.14, over 295 cases, mainly in rising and falling 60-day trends (t 2.42 and 1.69). They do not rebound in choppy calm markets (−0.4 %, 17 days). That result lies in other profiles than the brief's, so it is off this theme.

## Ideas
- `077-03.d1.b1.b1_wide-high-close-next-day-fall` (from F2, F3, F5): In a choppy, agitated market, a day that closes near its high on a range wide against the coin's 30-day swing is followed by a fall over the next day. The fall is larger the wider the day against that swing and the nearer the close sits to the high.
- `077-03.d1.b1.b2_wide-close-two-sided-reversal` (from F2, F3, F4): In a choppy, agitated market, where a coin closes within a day's range that is wide against its 30-day swing points the opposite way over the next day. A close near the high is followed by a fall and a close near the low by a rise, both larger the wider the day and the further the close sits from the middle of the range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
