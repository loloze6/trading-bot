---
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4048 USD
---
## Findings
- **F1:** The Calmar of 0.51 fails because one fall is far deeper than the rest: the chain of daily returns falls 51.6 % over 888 days (w1 to w11, book −50.7 % while the coins fell −59.6 %), against a yearly return of 26.3 %; the next deepest falls are −33.0 % (w12–w16), −19.1 % (w19–w21) and −18.5 % (w21–w23).
- **F2:** The short side earns nothing and deepens the falls. Over 4698 short bars the position's gain is a mean of −0.013 % (t −0.45, sum −0.61), against +0.18 % (t 5.08, sum +15.2) over 8325 long bars. In the deepest fall, shorts lost −2.67 against −0.67 for longs, and every coin's short side lost (LTC −0.74, XRP −0.64, ZEC −0.57).
- **F3:** The shorts lose most after the largest monthly falls. The short bars in the lowest 30-day-return quintile (mean −36 %) average −0.12 % per bar (sum −0.94), against +0.02 % to +0.06 % in the middle quintiles. A coin far below its high after a big monthly drop did not keep falling.
- **F4:** The long gain is hump-shaped in the 30-day return. Long bars in the 30-day-return quintiles at +14 % and +27 % earn +0.29 % and +0.45 % per bar. The top quintile, at +63 %, earns only +0.06 % per bar with the widest spread (std 3.98 %).
- **F5:** The book's worst bars are longs taken after an extended rally at the high. The worst 5 % of active bars include 512 longs summing −32.2, with a mean 30-day return of +36 %, a mean distance of only 4.2 % below the 60-day high, and a mean 5-day return of +11 %. These are the bars the forecast sizes largest (mean |allocation| 1.12 in the nearest-to-high quintile).
- **F6:** Longs inside the deep falls (the book more than 10 % below its peak) earn +0.12 % per bar over 5638 bars, against +0.31 % outside them. Inside those falls their mean 30-day return is lower (+14 % vs +31 %) and they stand further from the high (12.3 % vs 8.4 %). The longs taken in the falls ride weaker, older rallies.
- **F7:** The losses are not a problem of size against cost. Per case the total move is +1.13 % and the unusual move +0.95 % (strength 0.087), 5.8 and 4.9 times the 0.19 % cost of a trade. The failure is the depth of the falls, carried by the shorts and by over-extended longs.

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.d1_momentum-near-high-long-side` (from F1, F2, F3, F7): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days, only while the 30-day return is positive.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.d2_momentum-fades-when-overextended` (from F1, F4, F5, F6): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days, except when the 30-day return is large against the coin's own usual 30-day move: there, the larger that excess, the smaller the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
