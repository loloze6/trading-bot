---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the more it rises over the next 5 days, only while its 30-day return is positive.
Consequence: A trader should lean long in proportion to a coin's positive 30-day rise and not take shorts on its 30-day falls.
Why:
- F2: The gain comes entirely from the long side. On all bars, long positions earned +0.18 % per bar before costs (sum +15.65 over 8541 bars), while short positions earned −0.013 % per bar (sum −1.12 over 8765 bars).
- F3: The shorts lost in every coin during the deepest fall. Summed short gains were −1.07 on XRP (while XRP rose +1.00 on those bars), −0.66 on LTC, −0.46 on XMR, −0.42 on BTC, −0.28 on ZEC and −0.04 on ETH.
- F4: Removing the shorts changes the failing measure. Before costs, the long-only book has a deepest fall of 26.1 % against 51.0 % for the full book, a Calmar of 1.27 against 0.52, and a Sharpe of 1.13 against 0.82. The short-only book has a Sharpe of −0.09 and a 56.8 % fall.
- F5: The 30-day effect is one-sided. In the top two sextiles of the 30-day return (mean +17 % and +55 %), the coin's next-bar return is +0.27 % and +0.28 %, against a drift of +0.12 % per day, and the book earns +0.29 % and +0.20 % per bar. In the bottom sextile (mean 30-day return −32 %), the coin rises +0.20 % per bar, above its drift, so the book's shorts lose −0.10 % per bar.
