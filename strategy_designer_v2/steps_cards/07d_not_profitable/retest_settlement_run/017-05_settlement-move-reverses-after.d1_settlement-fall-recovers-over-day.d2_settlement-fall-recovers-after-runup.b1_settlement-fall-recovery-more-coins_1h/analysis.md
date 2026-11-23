---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5226 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.67 against the 0.75 rule, with a yearly return of +20.4 % over 7.94 years); the book's deepest falls all came in falling markets: −30.6 % in w12–w13 (2018) while the coins' daily means summed to −77.7 %, −25.5 % in w21–w23 (2025, coins −34.5 %) and −22.7 % in w1–w3 (2022, coins −73.0 %).
- **F2:** The cases lose in exactly those years: the mean excess 24-hour return is −0.20 % in 2018 (563 cases), −0.34 % in 2022 (t −3.00, 1672 cases) and −0.32 % in 2025 (t −3.10, 2212 cases), against +0.62 % in 2020 (t 4.30) and +0.31 % in 2023 (t 3.75).
- **F3:** Per case the idea is too small to pay a trade: the unusual move is +0.12 % and the total move +0.30 %, against a cost of 0.22 % per trade (0.6 and 1.4 times the cost); in my recomputation, all signal cases together give only +0.07 % excess (t 1.60, 12554 cases), and 48 % of cases end above the cost.
- **F4:** A deeper fall over the 24 hours into the settlement is the stronger case of the idea's own situation: signal cases in the lowest fifth of the 24-hour return (a fall of 2.5 % or more) give +0.41 % excess (+0.60 % total, t 3.62, 2511 cases), and the other four fifths give −0.01 % (t −0.27, 10043 cases); a crude cost-paying book of those cases has a deepest fall of −1.0 % and a Calmar of 0.41, against −3.6 % and 0.10 for all cases.
- **F5:** That 24-hour fall is not an effect of its own: on settlement bars after a 7-day run-up without the 2-hour fall, a 24-hour return in the same lowest fifth gives −0.13 % excess (t −0.95, 1545 cases); across the quintiles of the 24-hour return, those bars show no ordered pattern (−0.03 %, +0.18 %, −0.05 %, +0.06 %, +0.35 %).
- **F6:** The 16:00 UTC settlement carries the effect and 00:00 does not: signal cases give +0.15 % excess at 16:00 (t 2.64, 7941 cases) and −0.07 % at 00:00 (t −0.90, 4613 cases); 00:00 loses in 2018 (−0.89 %), 2021 (−0.39 %) and 2022 (−0.46 %).
- **F7:** The 16:00 result is not the hour by itself: run-up bars without the fall give +0.07 % at 16:00 (t 1.15) and +0.16 % at 00:00; a crude book on the 16:00 cases has a deepest fall of −2.2 % and a Calmar of 0.26, against −3.6 % and 0.10 for both hours.
- **F8:** The conditions that appear to explain the losses are effects of their own and are left out:

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins.d1_day-long-fall-into-settlement` (from F1, F2, F3, F4, F5): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall into it after a 7-day run up, grows with the size of the coin's fall over the 24 hours before the settlement against its usual daily move, and grows more the larger the 7-day return before the settlement, when longs are the crowded side paying funding.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins.d2_afternoon-settlement-fall-recovers` (from F1, F2, F6, F7): The rise over the 24 hours after the 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move, and grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
