---
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation_1h
idea tested: 028-02_volume-surge-down-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.8990 USD
---
## Findings
- **F1:** The tested down-side idea measures on the wrong side and not clearly: step 5's mean 6-bar unusual fall is -0.024 % with t -1.13 over 11,303 cases, so prices rose slightly after the short bets instead of falling. My own non-overlapping check finds no further fall at any horizon from 1 to 24 hours after falls of at least 3 standard deviations on at least 3 times usual volume (803 cases: 6h -0.073 %, t -0.55; 24h -0.357 %, t -1.55).
- **F2:** Where the down side shows anything, it is a bounce, not a further fall. Over 2 hours, falls on 3 to 6 times usual volume are followed by an unusual rise of 0.214 % (t -2.27 as a fall, 483 cases). The two coins agree over 2 hours (BTC t -1.42, ETH t -1.88).
- **F3:** The down-side result is driven by single years. 2020 alone shows a strong 2-hour bounce (-1.385 % as a fall, t -2.92, 99 cases), while 2019, 2022 and 2025 lean towards a further fall. That mix leaves the pooled t near zero.
- **F4:** The strategy's strongest short forecasts do no better than its weakest. Cases with forecast below -15 (7,112) have a 6-hour unusual fall of -0.017 % (t -0.58). Cases between -2 and -4 have +0.002 % (t 0.06). The cubed forecast does not grade the outcome.
- **F5:** The continuation the brief describes shows on the up side over a day, not on the down side over a few hours. After rises of at least 3 standard deviations on at least 3 times usual volume, the next 24 hours rise 0.551 % more than the coin's drift (t 2.71, 721 cases). Rises on 3 to 6 times usual volume give 0.827 % (t 3.29, 418 cases, strength 0.20).
- **F6:** The up-side 24-hour continuation holds in both coins and every year. BTC gives 0.627 % (t 2.59, 323 cases) and ETH 0.788 % (t 2.20, 282 cases), and all eight years 2018–2025 are positive (from 0.068 % in 2025 to 2.774 % in 2021).
- **F7:** Volume matters on the up side, as the brief's comparison says, though weakly and with a short history behind it:
- **F8:** On the up side, the move per case is large against the cost of a trade. The 24-hour unusual rise of 0.55–0.83 % per case is 5 to 7 times the 0.11 % a trade cost this backtest, before the coin's drift is added. By comparison, the tested idea's total move was -0.6 times that cost.

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong` (from F5, F6, F7, F8): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise times its volume relative to usual, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
