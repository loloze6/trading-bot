---
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4650 USD
---
## Findings
- **F1:** The Calmar fails because the chained book fell 75.3 % at its deepest, against a yearly return of 28.3 %; the book held a long position on 99.7 % of bars, so its five deepest falls follow the coins' own falls (w12–w14: coin −81.9 %, book −75.3 %, mean allocation 0.73; w1–w3: coin −73.0 %, book −68.1 %; w6–w7: coin −59.5 %, book −49.0 %).
- **F2:** The volume behind the signal sorts its cases strongly. Volume is measured as the mean of the last 3 bars (12 hours) against the 180-bar (30-day) mean. Cases in the lowest volume quartile show an unusual move of −1.04 % over 18 bars (t −6.1, 2276 cases, total move −0.51 %). Cases in the highest quartile show +1.22 % (t 5.0, 2276 cases, total +1.75 %). The quartiles in between are graded: −0.40 % (t −2.3) and −0.18 % (t −1.0).
- **F3:** The volume grading holds inside the drawdown windows. There, low-volume cases lose −1.45 % unusual (t −5.7, 1139 cases) and high-volume cases gain +0.86 % (t 2.6, 1091 cases). It also holds when the coin's 30-day return is negative: low-volume cases −1.38 % (t −6.0, strength −0.14) against high-volume cases +0.90 % (t 3.1, strength +0.10).
- **F4:** The volume effect is broad and steady. The top-minus-bottom volume-quartile difference is positive in all 19 coins (from +0.61 % for BTC to +5.9 % for NEAR). High-volume cases have a positive mean total move in 75 % of windows, against 29 % for low-volume cases.
- **F5:** The tested forecast's own size does not grade the move. Its quartiles give unusual moves of −0.14 %, −0.29 %, +0.14 % and +0.19 %, all with |t| < 1.9. On the volume of the signal bar alone, the lowest quartile gives −0.73 % (t −4.1) and the highest +0.77 % (t 3.3).
- **F6:** In size, the high-volume cases' total move of +1.75 % per case is about 8 times the 0.22 % cost of a trade, with a strength of about 0.15 when the 30-day trend is up. The low-volume cases' give-back of −0.51 % total, taken short, is about 2.3 times the cost.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins.d1_volume-backed-up-run-continuation` (from F1, F2, F3, F4, F5, F6): When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, and the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise, only while the volume of its last 12 hours is high against its 30-day average volume, the further rise growing with that volume ratio.
- `024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins.d2_fading-volume-up-run-give-back` (from F2, F3, F4, F6): When a coin has just risen in an unbroken streak of four-hour periods while the volume of its last 12 hours is low against its 30-day average volume, it ends the next three days below its normal drift, and the lower that volume ratio, the larger the shortfall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
