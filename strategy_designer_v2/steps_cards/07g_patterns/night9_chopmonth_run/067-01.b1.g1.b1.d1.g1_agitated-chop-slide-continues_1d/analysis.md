---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6091 USD
---
## Findings
- **F1:** The tested short side has a real-sized but uncertain move that the coin's drift cancels. Per case the unusual move is +1.36 % over 10 days (t 1.51, 227 days, strength 0.055), but the normal drift against the short is −1.30 %, so the total move is +0.07 %, 0.3 times the 0.22 % cost of a trade. The book's Sharpe is −0.15 and its yearly return −1.4 %.
- **F2:** The profile is very narrow. Only 4.9 % of the 10-day grid bars in folds B and C fall in the choppy agitated profile (30 of the 720 with a 30-day return), so the confirmed-looking in-profile pattern rests on almost nothing. In those cases the 30-day return's Spearman correlation with the next 10 days' excess return is 0.58, and the lowest third (30-day return −32 %) is followed by −15.6 % excess (t −4.8, n 10).
- **F3:** The same continuation holds in the wider choppy market, calm and agitated together (60-day return within ±10 %, 77 grid cases on 33 days).
- **F4:** The choppy continuation of F3 is uneven by side and by year, so it is not yet sure.
- **F5:** A day that closes in the lowest fifth of its range is followed by +0.67 % the next day (t 5.26, 1,981 days), against −0.17 % after a close in the top fifth. A large down day (lowest seventh of the swing-scaled daily return, z −1.6) is followed by +0.96 % (t 5.5). Both are low-close and fall rebounds that the map already holds many times.
- **F6:** Two other patterns reach only about t 2 and do not stand out given the many angles looked at.

## Ideas
- `067-01.b1.g1.b1.d1.g1.g1_choppy-scaled-month-continuation` (from F3, F2, F4, F1): In a choppy market, the larger a coin's 30-day return measured against its own daily swing over those 30 days, the further it moves the same way over the next 10 days, after falls and after rises alike.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
