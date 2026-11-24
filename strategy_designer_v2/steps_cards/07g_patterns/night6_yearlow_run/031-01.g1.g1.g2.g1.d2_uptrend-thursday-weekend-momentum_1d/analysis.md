---
line: 7.g patterns
backtest: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d
idea tested: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4001 USD
---
## Findings
- **F1:** The momentum the tested idea uses sits mostly on the Saturday bar. Across all regimes, the one-day excess return after Friday's close (UTC) rises with the coin's 14-day rise in volatility units: clustered slope 0.0068, t 3.36, 2070 cases on 345 days. After every other weekday's close the same slope has a t between −0.57 and 1.04.
- **F2:** A shorter lookback carries the same Friday-close effect. Using the 7-day rise, the next-day slope after Friday's close is 0.0071, t 3.64, 2070 cases on 345 days. After every other weekday's close it has a t between −1.55 and 0.83.
- **F3:** For the 2-day excess return against the 14-day rise, only the Wednesday-to-Friday closes count. The clustered t is 3.28 after Thursday and 2.94 after Friday, across 341–342 days each, while Saturday to Tuesday sit between −0.69 and 0.39. Inside the 60-day uptrend the slope is 0.0110 (t 2.32) after Wednesday, 0.0172 (t 3.54) after Thursday and 0.0084 (t 2.20) after Friday. In the 60-day downtrend no weekday reaches t 1.3.
- **F4:** The next-day momentum slope after Wednesday-to-Friday closes is positive in 6 of 8 years (t 2.65 in 2021, 2.13 in 2024, 1.86 in 2025) and on all 6 coins. It is strongest on ZEC (t 2.94) and XRP (t 2.44) and weakest on XMR (t 0.25) and BTC (t 0.56). After Saturday-to-Tuesday closes it is zero or negative in 6 of 8 years (2021 t −1.99).
- **F5:** The book's gain comes from a few days. Its 30 largest days by absolute return hold 0.815 of the 1.367 summed daily return (60 %), and 22 of those 30 days are gains. The mean daily return is 0.0013 on Fridays and 0.0021 on Saturdays, against roughly 0 on other days.
- **F6:** Other angles showed nothing that stands out once the number of looks is counted:

## Ideas
- `031-01.g1.g1.g2.g1.d2.g1_friday-close-weekly-momentum-into-saturday` (from F1, F2, F4): The larger a coin's 7-day rise at Friday's close (UTC), the larger its gain over the following day (Saturday), whatever its 60-day trend.
- `031-01.g1.g1.g2.g1.d2.g2_uptrend-wednesday-momentum-into-thursday-friday` (from F3, F4): While a coin trades above its price of 60 days earlier, the larger its 14-day rise at Wednesday's close (UTC), the larger its gain over the following Thursday and Friday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
