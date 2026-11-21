---
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d
idea tested: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3230 USD
---
## Findings
- **F1:** The book's deepest fall is 55.6 % and lasts 1677 days, from w2 to w16, while the coins' daily returns summed +2.13 over the same days. The book summed only +0.27 over that stretch, against a yearly return of 23.2 %, which gives the failing Calmar of 0.42.
- **F2:** The gain comes entirely from the long side. On all bars, long positions earned +0.18 % per bar before costs (sum +15.65 over 8541 bars), while short positions earned −0.013 % per bar (sum −1.12 over 8765 bars).
- **F3:** The shorts lost in every coin during the deepest fall. Summed short gains were −1.07 on XRP (while XRP rose +1.00 on those bars), −0.66 on LTC, −0.46 on XMR, −0.42 on BTC, −0.28 on ZEC and −0.04 on ETH.
- **F4:** Removing the shorts changes the failing measure. Before costs, the long-only book has a deepest fall of 26.1 % against 51.0 % for the full book, a Calmar of 1.27 against 0.52, and a Sharpe of 1.13 against 0.82. The short-only book has a Sharpe of −0.09 and a 56.8 % fall.
- **F5:** The 30-day effect is one-sided. In the top two sextiles of the 30-day return (mean +17 % and +55 %), the coin's next-bar return is +0.27 % and +0.28 %, against a drift of +0.12 % per day, and the book earns +0.29 % and +0.20 % per bar. In the bottom sextile (mean 30-day return −32 %), the coin rises +0.20 % per bar, above its drift, so the book's shorts lose −0.10 % per bar.
- **F6:** Shorts also lose where the coin sits deepest below its 60-day high. In that quintile they earn −0.09 % per bar, while longs earn +0.27 %, which is consistent with rebounds after deep falls rather than continuation.

## Ideas
- `020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues.d1_upside-only-thirty-day-momentum` (from F2, F3, F4, F5): The larger a coin's 30-day return, the more it rises over the next 5 days, only while its 30-day return is positive.
- `020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues.d2_rebound-after-deep-monthly-falls` (from F5, F6, F3): The deeper a coin's 30-day fall, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
