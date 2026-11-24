---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend_1d
idea tested: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4070 USD
---
## Findings
- **F1:** The book fails Calmar because of its short side: on Thursday-close cases the 1235 shorts lose 0.20 % per case, while the 1230 longs gain 0.87 %; rebuilt with costs, the short-only book has Sharpe -0.57 and a deepest fall of -50 %, the long-only book has Sharpe 1.30, a yearly return of +20.2 %, a deepest fall of -11.9 % and Calmar 1.69, against 0.46 for both sides together (recorded 0.478).
- **F2:** The book's deepest fall, -24.5 % over 376 days in w24 (2025), came while its coins rose 58 %. The short side lost money in 6 of 8 years (2025: -0.179 summed per coin; 2024: -0.115). In the three deepest falls the book held short on 840 coin-days and long on 767.
- **F3:** The shorts fight a weekend drift. From Thursday's close the coins' 2-day return averages +0.75 % (t 5.97, 2465 cases), and from Friday's close +0.54 % (t 4.75); every other weekday lies between -0.12 % and +0.18 %. Even the lowest forecast quintile on Thursday is followed by +0.34 % over 2 days, so a short there loses on average.
- **F4:** The grading sits in the rise side. Across the forecast quintiles on Thursday the 2-day moves are +0.34 %, +0.34 %, +0.27 %, +0.62 % and +2.17 %. Across the 14-day return quintiles they are +0.16 %, +0.31 %, -0.07 %, +0.41 % and +2.29 %, against a top quintile of only +0.43 % on other weekdays. The largest 14-day rises at Thursday's close carry the effect; the size of a 14-day fall grades nothing.
- **F5:** A 60-day rise steepens the grading but earns nothing alone.

## Ideas
- `031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend` (from F1, F2, F3, F4): After a 14-day rise, a coin's 14-day return at Thursday's close (UTC) grades its gain over the following Friday and Saturday: the larger its two-week rise, the larger its gain over those two days.
- `031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum` (from F1, F4, F5): While a coin trades above its price of 60 days earlier, the larger its 14-day rise at Thursday's close (UTC), the larger its gain over the following Friday and Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
