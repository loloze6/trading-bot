---
line: 7.b inconclusive
backtest: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade_1d
idea tested: 061-01.b1.b1.b1.d2.d2_upper-close-quiet-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3918 USD
---
## Findings
- **F1:** In folds B and C, the whole effect comes from closes near the day's high. Cases closing in the top fifth of the range have a mean unusual 10-day move of +10.6 % (t 3.83, 31 cases), while the rest have −1.4 % (t −0.46, 45 cases). By bin, the move is +14.7 % (t 4.74, 13 cases) for closes at 0.9–1.0 of the range and +7.6 % (t 1.85, 18) at 0.8–0.9, against −3.7 %, +0.1 % and −1.0 % for the three bins from 0.5 to 0.8.
- **F2:** The effect is graded but only switches on at the top. By forecast quartile, the unusual 10-day move is −2.0 % (t −0.30), −3.3 % (t −1.09), +5.8 % (t 2.72) and +13.4 % (t 3.46). Its correlation with the forecast is 0.31, and the forecast is almost the close's place in the range (correlation 0.97). The plan's "upper part" from mid-range therefore mixes losing cases into the winning ones.
- **F3:** The high-close fall is steady:
- **F4:** Closes below 0.8 of the range are mixed. They are positive in 2019 (+5.3 %, t 2.70) but negative in 2020 (−3.5 %) and 2021 (−7.5 %), and these cases dilute the tested result. That result is +1.40 % per case, t 1.68, over 325 cases on 254 days. It is on the predicted side, but the test already used all four folds and all 19 coins, so no more data is available.
- **F5:** The whole test's total move per case is +0.13 %, against a trade cost of 0.22 %, so the idea as tested cannot pay. The high-close cases carry an unusual move of about +10 % over 10 days in folds B and C, far above that cost.

## Ideas
- `061-01.b1.b1.b1.d2.d2.b1_near-high-quiet-day-fade` (from F1, F2, F3, F4, F5): In a choppy, agitated market, when a coin closes at the top of that day's high-low range on a day whose gain is small against its usual daily swing, its price falls over the next ten days. This holds only when the close sits near the day's high, and the nearer the close is to the high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
