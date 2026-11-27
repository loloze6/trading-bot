---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade_1d
idea tested: 061-01.b1.b1.b1.d2.d1_quiet-high-close-ten-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4798 USD
---
## Findings
- **F1:** Over the next 2 days, a down day's rebound grows with the day's volume against its 20-day average. Across the volume quintiles from the quietest to the heaviest, the mean unusual move is −0.78 %, −0.16 %, +0.13 %, +0.47 % and +1.74 %. For the heaviest quintile the strength is 0.21, with t 2.02 on 384 cases pooled over 152 days, and that move is positive in each of 2018, 2019, 2020 and 2021 (+0.67 %, +1.94 %, +1.79 %, +2.34 %).
- **F2:** The heavy-volume down-day rebound does not come from the tested profile. Outside choppy agitated it is +1.75 % over 2 days (t 2.11, 366 cases, 148 days); inside, it rests on only 18 cases. It also fades with horizon: +0.20 % over 5 days (t 0.12) and +1.94 % over 10 days (t 0.51). It is a 2-day effect.
- **F3:** Heavy volume on up days carries no 2-day move. The top volume quintile of up days gives +0.27 % (t 0.52, 438 cases, 212 days). The volume gradient lives on the down side only.
- **F4:** Inside choppy agitated, the tested situation points the idea's way in folds B and C, but on few cases. Closes in the top fifth of the range are followed by a 10-day unusual move of −15.2 % (t −3.82, 10 cases). Up days with a gain of 0 to 1 usual daily move are followed by −9.7 % (t −4.34, 12 cases).
- **F5:** The book's gain rests on a few large trades. Its 87 trades have a mean of +1.65 % but a median of −0.88 % after fees, a spread from −43.6 % to +36.6 %, and an upper quartile of +8.9 %. The window sums range from −2.6 % (w12) to +6.1 % (w16), consistent with the failed Calmar of 0.22.
- **F6:** The weekday pattern is mostly market-wide and is not a finding. Two-day returns from Sunday closes average −1.15 % (unpooled t −3.41, 713 cases), but pooled by day the t is only −1.41 over 111 days. Only LTC (t −2.31) and XMR (t −2.14) reach 2 on their own.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d2.d1.g1_heavy-volume-down-day-rebound` (from F1, F2, F3): After a down day on heavy trading volume, a coin rebounds over the next two days, and the heavier that day's volume against its usual volume of the past 20 days, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
