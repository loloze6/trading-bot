---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of the preceding two days after the coin has fallen over the past 7 days, the coin falls over the next three days, and the deeper the past week's fall, the larger the decline.
Consequence: A trader should refuse an upside breakout that comes in a falling week, and the more so the deeper that week's fall.
Why:
- F7: Breakouts after a falling week are worse than ordinary bars after a falling week. In the lowest 7-day quintile, breakout cases lose −1.03 % unusual (t −4.38), against −0.18 % on grid bars, a gap of about 4.7 times the 0.22 % cost of a trade.
- F4: The coin's past 7-day return grades the 18-bar move after breakouts. By quintile of the 7-day return over the 30-day volatility, the unusual move runs from −1.03 % (strength −0.10, t −4.38) to −0.46 %, +0.50 %, +0.51 % and +1.12 % (strength +0.098, t 2.19), about 1000 cases each. The plain 7-day return gives the same order, from −1.16 % (t −4.71) to +1.23 % (t 2.33).
- F2: The breakout itself does not predict a move large enough to pay at any horizon. Recomputed from prices, the first close above the prior 12-bar high in each grid cell is followed by an unusual move of +0.12 % over 18 bars (t 0.80, 5034 cases), +0.25 % over 36 bars (t 0.98, 3530 cases) and −0.67 % over 72 bars (t −1.53, 2114 cases). Its only t above 2 is +0.12 % over 3 bars (t 2.80, 8815 cases), about half the 0.22 % cost of a round trip.
