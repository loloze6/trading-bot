---
line: 7.g patterns
backtest: 046-01_calm-scaled-rise-second-day-continues_1d
idea tested: 046-01_calm-scaled-rise-second-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4403 USD
---
## Findings
- **F1:** In calm bars, a coin's 5-day return scaled by its 30-day daily swing predicts its excess return over the next 5 days; the slope is +126 to +199 bp per unit, with t 2.03 to 2.79, on every one of the 5 non-overlapping grid offsets (about 760–780 cases each).
- **F2:** The same calm momentum holds at other horizons. For 3 days the slope is +56 to +103 bp, t 1.66 to 3.00, about 1,300 cases per offset. For 10 days it is +195 to +304 bp, t 1.71 to 3.00, about 360–380 cases per offset.
- **F3:** In agitated bars the effect is absent. The 5-day slopes run from −32 to +103 bp with t −0.39 to 0.95, and the 10-day slopes from −178 to +149 bp with t −0.87 to 0.76. The pattern lives in the calm profile only.
- **F4:** Calm 5-day momentum (offset 0) is positive on all 6 coins, from +108 bp (BTC, t 1.60) to +434 bp (XRP, t 1.72), with t above 2 on ETH, XMR and ZEC. It is positive in 2018, 2020 and 2021 (t 1.33 to 1.63) and negative in 2019 (−28 bp, t −0.31). It works on both sides: rises give +212 bp (t 1.67, 398 cases) and falls give +298 bp (t 1.81, 374 cases).
- **F5:** The tested one-day effect is weak.
- **F6:** In agitated bars, the day's close location in its range predicts the next day's excess return negatively.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `046-01.g1_calm-weekly-move-continues` (from F1, F2, F3, F4, F5): In a calm market, the larger a coin's 5-day return is against its 30-day daily swing (the standard deviation of its daily returns), the further the coin moves the same way over the next 5 days, higher after a rise and lower after a fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
