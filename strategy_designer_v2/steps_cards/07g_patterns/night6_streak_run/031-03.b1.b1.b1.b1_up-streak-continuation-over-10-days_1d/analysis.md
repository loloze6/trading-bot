---
line: 7.g patterns
backtest: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d
idea tested: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6242 USD
---
## Findings
- **F1:** Over the next 5 days, the larger a coin's rise over the past 10 days, measured in its own 30-day daily volatility, the larger the unusual move that follows, on cases where that 10-day return is positive: the slope is 0.093, 0.114 and 0.067 of a usual move per standard deviation, with day-clustered t of 2.99, 3.73 and 2.20 on three grid offsets (about 4,400 to 4,600 cases on all coins and signs, about 450 to 466 days).
- **F2:** The same continuation after a rise also shows over the next 10 days, on cases where the 10-day return is positive: the slope is 0.135, 0.140 and 0.165 per standard deviation (t 2.54, 2.21 and 3.69, three grid offsets, about 2,100 to 2,300 cases on 210 to 229 days). In quintiles, the cases after the largest volatility-scaled 10-day rises averaged +2.36 % unusual move (t 1.66), against −1.06 % for the middle quintile.
- **F3:** The rise's size, not the streak's length, carries the effect.
- **F4:** The continuation after a 10-day rise is broad across coins: the per-coin slope over 10 days is positive in 14 of 18 coins. It is highest in ADA (0.153, t 2.63), AVAX (0.246, t 2.30), XRP (0.227, t 2.16) and BTC (0.121, t 1.95). TRX (−0.120) and ONDO (9 cases) are the clear exceptions.
- **F5:** After falls the slope turns negative, so deeper 10-day falls are followed by somewhat larger rebounds, but this side never stands out. On cases with a 10-day return at or below 0, the slopes over 5 days are −0.066, −0.085 and −0.064 (t −1.95, −2.16, −1.58), and over 10 days −0.054, −0.113 and −0.088 (t −1.47, −1.84, −1.40).
- **F6:** The book's gain rests on a few days and on long holds.
- **F7:** The size of the entry forecast does not grade the trades: the top third (forecast 20.0) earns +9.1 % mean net, against +26.1 % for the middle third (19.9) and +16.7 % for the bottom third (13.1), with negative medians in all three. This matches the near-flat top-minus-bottom check of step 5 (+0.05 %).

## Ideas
- `031-03.b1.b1.b1.b1.g1_volatility-scaled-rise-continues-short-term` (from F1, F3, F4): The larger a coin's rise over the past 10 days, measured against its own daily volatility over the past 30 days, the more it keeps rising over the next 5 days.
- `031-03.b1.b1.b1.b1.g2_volatility-scaled-rise-continues-ten-days` (from F2, F3, F4, F7): The larger a coin's rise over the past 10 days, measured against its own daily volatility over the past 30 days, the more it keeps rising over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
