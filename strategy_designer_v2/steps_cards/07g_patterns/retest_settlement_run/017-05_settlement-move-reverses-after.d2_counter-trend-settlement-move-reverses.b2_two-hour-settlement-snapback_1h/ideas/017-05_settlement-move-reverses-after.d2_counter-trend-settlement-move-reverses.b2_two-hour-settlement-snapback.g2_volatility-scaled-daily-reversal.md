---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour move in either direction, the larger that move relative to the coin's own recent hourly volatility, the more the coin moves back against it over the next 24 hours.
Consequence: A trader should fade unusually large one-day moves over the following day, not chase them, and size the fade by how extreme the move was.
Why:
- F1: The 24-hour move reverses over the next 24 hours, and more so the larger it is against the coin's own volatility. On a non-overlapping 24-hour grid, with the 24-hour return z-scored by the coin's 30-day hourly volatility, the reversal by |z| quintile is −15, −2, −3, +23 and +52 bp. The top quintile has t 5.09 over 3260 cases and a strength of 0.104. That move is about 2.7 times the 0.19 % cost of a trade. The same holds on the grid that starts at 00 UTC, where continuation in the top quintile is −45.9 bp, t −4.25, over 3416 cases.
- F4: The tested 2-hour snapback is part of a general 2-hour reversal that is not tied to settlement. Across all even hours, the reversal of the 2-hour move rises with its size: +12.3 bp in the top decile of |z| (t 7.76, 19625 cases). It also rises with volatility: 1.5, 2.7 and 8.9 bp by volatility tercile (t 4.2, 5.6, 11.0). Even the largest of these 2-hour moves is below the 19 bp cost, consistent with the backtest's gross trade means of −0.21 % to +0.06 % against net means of −0.31 % to −0.05 %.
