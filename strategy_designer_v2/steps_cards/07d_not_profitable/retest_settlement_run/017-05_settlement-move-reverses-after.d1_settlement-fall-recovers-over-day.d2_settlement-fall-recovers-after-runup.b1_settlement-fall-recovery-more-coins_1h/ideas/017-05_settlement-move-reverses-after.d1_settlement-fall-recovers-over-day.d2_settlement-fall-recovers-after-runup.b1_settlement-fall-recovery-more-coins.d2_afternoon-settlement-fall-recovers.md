---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after the 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move, and grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.
Consequence: A fall into the 16:00 UTC settlement after a run-up is a reason to be long for the next day, sized by the fall and the run-up, while the same fall into 00:00 is a reason to refuse the trade.
Why:
- F1: The check failed on Calmar alone (0.67 against the 0.75 rule, with a yearly return of +20.4 % over 7.94 years); the book's deepest falls all came in falling markets: −30.6 % in w12–w13 (2018) while the coins' daily means summed to −77.7 %, −25.5 % in w21–w23 (2025, coins −34.5 %) and −22.7 % in w1–w3 (2022, coins −73.0 %).
- F2: The cases lose in exactly those years: the mean excess 24-hour return is −0.20 % in 2018 (563 cases), −0.34 % in 2022 (t −3.00, 1672 cases) and −0.32 % in 2025 (t −3.10, 2212 cases), against +0.62 % in 2020 (t 4.30) and +0.31 % in 2023 (t 3.75).
- F6: The 16:00 UTC settlement carries the effect and 00:00 does not: signal cases give +0.15 % excess at 16:00 (t 2.64, 7941 cases) and −0.07 % at 00:00 (t −0.90, 4613 cases); 00:00 loses in 2018 (−0.89 %), 2021 (−0.39 %) and 2022 (−0.46 %).
- F7: The 16:00 result is not the hour by itself: run-up bars without the fall give +0.07 % at 16:00 (t 1.15) and +0.16 % at 00:00; a crude book on the 16:00 cases has a deepest fall of −2.2 % and a Calmar of 0.26, against −3.6 % and 0.10 for both hours.
