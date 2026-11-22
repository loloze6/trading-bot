---
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend_4h
idea tested: 027-03_panic-rebound-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2154 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but is far too noisy for 40 cases. Step 5 gives +2.23 % per case with t 0.99. My rebuild of the cases gives +0.62 % with a spread of 15.6 % per case, t 0.23 on 35 cases, and 51 % of cases end above the drift. At that spread, a +2.23 % mean needs about 196 cases to reach t 2, five times what the six default coins provide.
- **F2:** The 84-bar outcome swings by period and by coin, so a few cases decide the sign. In 2018 the 6 cases average −22.2 %, while in 2020 the 6 cases average +20.7 %. BTC averages −5.3 % on 7 cases and ZEC +9.9 % on 3.
- **F3:** Widening the same situation to more cases makes the 14-day premium show. Falls with a 24-hour range at least 2x the 30-day average, in coins with a negative 30-day return, give +3.71 % over 84 bars, t 2.15 on 161 cases. The same falls in all coins give +3.13 %, t 2.47 on 335 cases.
- **F4:** The premium is clearest over the next 3 days (18 bars), and it grows with how far the range exceeds its average. Falls with a range of at least 3x give +4.07 % over 18 bars, t 3.98 on 109 cases. Falls with a range of at least 2x give only +1.72 %, t 3.17 on 335 cases.
- **F5:** Grading by depth of fall did not work in the test, because the forecast saturates. Deep and mid terciles both sit at the forecast cap of 20, so the forecast-weighted check reads exactly 0. The 84-bar returns do not rise with depth: −2.6 % for deep, +7.4 % for mid, −1.2 % for shallow.
- **F6:** Within the falling coins, the deeper the prior 30-day fall, the larger the rebound. Cases with a very negative prior return give +7.5 % over 84 bars (16 cases); those with a mildly negative one give −5.9 % (17 cases).

## Ideas
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins` (from F1, F2, F3): In coins whose 30-day return before the panic was negative, a 24-hour stretch with a range several times its 30-day average and a hard fall is still followed by higher than usual returns over the next 14 days, and the more extreme the panic, the higher the return.
- `027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days` (from F4, F5): A 24-hour stretch in which the coin falls hard while its range is several times its 30-day average is followed by higher than usual returns over the next 3 days, and the further the range exceeds its 30-day average, the higher the return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
