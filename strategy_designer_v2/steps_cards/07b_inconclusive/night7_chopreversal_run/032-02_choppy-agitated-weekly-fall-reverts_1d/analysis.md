---
line: 7.b inconclusive
backtest: 032-02_choppy-agitated-weekly-fall-reverts_1d
idea tested: 032-02_choppy-agitated-weekly-fall-reverts
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3464 USD
---
## Findings
- **F1:** The tested result is zero, not on the side the idea predicts. Step 5's slope of the 7-day excess return on the forecast is -0.00099 (t -0.54, 70 independent cells), and the unusual move per case is -0.39 % (t -0.40 over 171 days, strength -0.040), so the book's +0.56 % total move per case is only the coin's +0.95 % drift.
- **F2:** In folds B and C, falls inside the choppy agitated profile are not bought back. On 36 cases over 23 days, the 7-day excess return after a 7-day fall is -1.5 % (day-clustered t -0.34), and it is also negative at 5 days (-4.5 %, t -1.25) and at 10 days (-4.0 %, t -0.91).
- **F3:** The grading runs the wrong way for the idea. The largest tercile of in-profile 7-day falls (mean -27.4 %) is followed by -4.9 % excess and the middle tercile (-10.9 %) by -3.9 %, while only the smallest (-3.7 %) is followed by +4.1 % (12 cases each). At 14 days the slope of excess return on the past 7-day move is +2.37 (t 2.68, 18 cases), meaning larger falls are followed by weaker returns, which is continuation.
- **F4:** The fall-side result also hangs on one year. 2020 alone gives -9.4 % excess on 11 cases, and without 2020 the fall side's reversal is +1.9 % but still not sure (t 0.48, 25 cases, 17 days).
- **F5:** Only the mirror side gives back its move inside the profile. A 7-day rise is followed by a reversal of +3.65 % over the next 7 days (24 cases, 17 days, day-clustered t 2.46, strength 0.26), with the same sign at 5 days (+3.3 %, t 1.50) and 10 days (+3.8 %, t 0.81) and in every year (2019 -2.8 %, 2020 -3.9 %, 2021 -4.2 % excess). It is uneven across coins, though: BTC and ZEC -7.4 %, ETH -3.7 %, the other three near 0.
- **F6:** Outside the profile there is no weekly reversal on either side. Over the next 7 days, falls show -0.67 % (t -0.55, 511 cases) and rises -0.91 % (t -0.72, 530 cases) in the reversal direction. The in-profile rise reversal in F5 is therefore specific to the choppy agitated profile, though its grading by the size of the rise is not shown (larger half -4.9 % versus smaller half -4.4 %, 6 cases each).
- **F7:** The profile is rare, which leaves the test thin. Only 5.4 % of the 7-day grid cells in folds B and C fall in it (60 of 1,101), so each side rests on a few dozen cases.

## Ideas
- `032-02.b1_choppy-agitated-weekly-rise-fades` (from F5, F6, F2, F3): In a choppy, agitated market, the larger a coin's 7-day rise, the larger its fall over the next 7 days, giving back part of that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
