---
line: 7.b inconclusive
backtest: 077-01.b1.b1_choppy-agitated-low-close-rebound_1d
idea tested: 077-01.b1.b1_choppy-agitated-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2422 USD
---
## Findings
- **F1:** On the folds shown (B, C), the tested cases rebound clearly over the next day: 73 cases on 58 days with a mean excess return of +2.55 % (t 2.79). Over all four folds, 408 cases give only +0.34 % (t 1.05), so the roughly 335 cases in folds A and D must carry almost no effect.
- **F2:** Inside the profile, on wide days, the next-day excess return falls steadily as the close moves up the range. Closes in the lowest fifth give +3.02 % (t 3.40, 23 cases), the next fifth +2.77 % (t 1.40, 25), the middle −2.26 % (t −0.93, 19), and the top fifth −3.40 % (t −2.08, 20). The effect sits at closes near the low.
- **F3:** The plan's 60-bar standardised forecast lets in closes near mid-range that do not rebound. The lowest forecast quartile (mean close location 0.42) gives −0.75 % (t −0.78, 20 cases). The other three give +4.33 % (t 1.86), +4.50 % (t 2.19) and +2.49 % (t 3.14, mean location 0.07).
- **F4:** The rebound is largest on the widest days. The widest third (range 2.2 times its 20-day mean) gives +4.46 % (t 2.29, 16 cases), against +2.16 % (t 1.14) and +0.73 % (t 0.60) for the two narrower thirds.
- **F5:** The effect is spent within one day: +2.55 % (t 2.79) over the next day, but +1.08 % (t 0.79) over two days and +1.96 % (t 1.54) over three.
- **F6:** The effect is uneven across coins and rests mostly on down days. BTC gives +1.45 % (t 2.49, 17 cases), XMR +4.07 % (t 2.73, 9) and ZEC +5.18 % (t 1.98, 15), while ETH gives −0.14 % (t −0.10, 9). 66 of the 73 cases are down days, at +2.73 % (t 2.70).
- **F7:** Only 4.6 % of bars are in the choppy agitated profile. Outside it, wide days closing in the lowest fifth also rebound, by +1.06 % (t 2.24, 514 cases on 202 days). That is about a third of the in-profile move; this pattern is off the brief's profile and is noted only as context.

## Ideas
- `077-01.b1.b1.b1_choppy-agitated-widest-low-close-rebound` (from F2, F3, F4, F5, F6): In a choppy, agitated market, a wide day that closes near its low is followed by a rise over the next day, larger the wider the day is against the coin's usual daily range of the last 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
