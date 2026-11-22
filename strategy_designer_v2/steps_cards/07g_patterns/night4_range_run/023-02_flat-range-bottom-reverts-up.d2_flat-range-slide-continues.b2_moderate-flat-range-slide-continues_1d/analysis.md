---
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6418 USD
---
## Findings
- **F1:** At a Thursday close, a coin's next 2-day unusual return (Friday plus Saturday) rises with its 7-day return. By 7-day quintile: q0 +0.13 % (t 0.43, 468 weeks), q1 −0.31 %, q2 +0.15 %, q3 +0.87 % (t 3.70, 462), q4 +1.70 % (t 4.77, 467). The top-quintile move is about 9 times the 0.19 % cost of a trade.
- **F2:** This is particular to Friday and Saturday. On those days the unusual daily return in the top two prior-7-day quintiles is +0.49 % (t 3.72) and +0.78 % (t 4.36, 936 each). On other weekdays the same quintiles give −0.18 % and +0.05 % (t 0.42, 2,340). Saturday's coin-average return is +0.45 % (t 3.04 over 414 days, one observation per day).
- **F3:** The weekend lift is broad across coins but not across years. Friday-plus-Saturday minus other days is positive in all 6 coins (LTC t 3.88, XMR t 2.03, BTC t 0.78) and comes almost wholly after rising weeks (prior 7-day return up: +0.59 %, t 5.19; down: +0.12 %, t 1.09). The Thursday 2-day move is positive in 7 of 8 years, but 2022 is −0.42 % (t −1.19) and 2018 and 2021 are near zero (t 0.27 and 0.34).
- **F4:** In coins with a clear 30-day decline (signed 30-day net move below −0.3 of its high-low range), a moderate 10-day fall keeps falling over the next 5 days. A fall of 0.5 to 1 usual 10-day moves is followed by −2.81 % unusual (t −3.51, 168 cases); one of 0 to 0.5 usual moves by −1.92 % (t −2.89, 159). Falls beyond one usual move rebound instead (+1.48 %, +2.12 %, +0.96 %, all t below 1.9).
- **F5:** That downtrend continuation holds in 5 of 6 coins (LTC t −2.71, XRP t −2.85, ZEC t −2.68; XMR +0.49 %) and in 7 of 8 years (2022 the exception, +3.39 %, t 2.73). Its total 5-day move is −1.79 % (t −3.43, 327 cases), about 9 times the cost of a trade.
- **F6:** The tested flat-range short has no grading. Quartiles of forecast from most to least negative give long-side unusual moves of −0.29 %, −1.13 %, −2.30 %, −0.66 % (109 each), and the step-5 half check is −0.77 %. Across windows the active cases split 14 negative to 10 positive (w18 −16.4 %, w11 +11.6 %), and ZEC alone carries a t of −2.99.
- **F7:** The brief's range reversion does not show in flat coins. With a 30-day net move at most 0.3 of the range, closes in the top fifth of the range are followed by −1.39 % (t −1.33, 77 cases) and those in the bottom fifth by −0.33 % (t −0.33, 83). In trending coins the top fifth is followed by +1.28 % (t 2.04, 431), which is continuation rather than reversion.
- **F8:** The book loses on its short trades. Trades of up to 5.5 days average −2.45 % after fees (1,155 trades), against +1.29 % for those of 10 to 20 days (185). The 1,872 short trades average −1.50 %, and the book's mean daily return is −0.020 %.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.g1_weekend-momentum-after-strong-weeks` (from F1, F2, F3): The larger a coin's 7-day return at Thursday's close, the more it rises over the next 2 days (Friday and Saturday), beyond its normal drift.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.g2_moderate-slide-continues-in-downtrends` (from F4, F5, F6): In a coin whose 30-day net move is down and large against its 30-day high-low range, the deeper its 10-day fall, while that fall stays within its usual 10-day moves of the last 60 days, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
