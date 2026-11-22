---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation_1h
idea tested: 028-02_volume-surge-down-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3737 USD
---
## Findings
- **F1:** Large hourly falls on heavy volume were followed by rebounds, not further falls. On hours where the fall in 30-day standard deviations times the 30-day volume ratio exceeded 12 in absolute size, the coin's unusual move against the fall's direction was +0.278 % over 2 hours (t 2.85, 619 independent cases, strength 0.23). Over 4 hours it was +0.464 % (t 2.33, 322 cases, strength 0.29), and over 12 hours +1.32 % (t 1.90, 93 cases, strength 0.49).
- **F2:** The tested idea failed because it bets in the wrong direction. Its 6-bar unusual fall per case was -0.02 % (t -1.13, 11303 cases, strength -0.012), and the total move in the bet's direction was -0.06 %, which is -0.6 times the 0.11 % cost of a trade. The rebound in F1 has a total move of +0.287 % over 2 hours, about 2.6 times that cost.
- **F3:** The book lost money before costs, on top of paying fees. It was short on 72 % of bars (BTC 72.0 %, ETH 73.0 %). Summed bar gains before fees were -3.47 for BTC and -3.08 for ETH, against fees of 3.81 and 3.25. Its mean daily return was -0.24 % (BTC) and -0.21 % (ETH), while holding returned +0.12 % and +0.14 %. A near-constant short against a rising coin plus heavy turnover (about 7636 and 6070 allocation units) carried the loss.
- **F4:** The rebound grows with the size of the fall, but not with the volume ratio.
- **F5:** The rebound weakens over time. For hours with a product above 6, the 2-hour reversal was +0.24 % in 2018, +0.10 % in 2019, +0.26 % in 2020 (t 2.10) and +0.67 % in 2021 (t 3.53). It then fell to near zero in 2022–2024 (+0.01 %, -0.02 %, +0.00 %) and was -0.12 % in 2025 (t -1.71).
- **F6:** Large rises on heavy volume did not reverse; if anything they continued. For a product above 12 on the rise side, the reversal over 6 hours was -0.455 % (t -1.97, 174 cases, strength -0.23). Over 2 hours it was -0.02 % (t -0.22, 580 cases).

## Ideas
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds` (from F1, F2, F3, F4, F5): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two to four hours, and the larger that hour's fall relative to its typical 30-day hourly move, the larger the rebound.
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward` (from F6, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next six hours, and the larger that hour's rise relative to its typical 30-day hourly move, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
