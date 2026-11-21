---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days. The rise is larger the narrower that stretch was compared with the coin's 30-day average four-hour range, and larger still the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
Consequence: A trader should weight an upward breakout by how quiet the whole preceding week was, and give little weight to breakouts out of a turbulent week, which is where the book's deepest falls came from.
Why:
- F1: The book misses its Calmar target by a hair: 0.749 against 0.75 (34.1 % a year, deepest fall 45.5 %). The deepest fall runs from w5 to w10 over 556 days, with the book down 33.8 % while the coins fell 52.3 %.
- F2: The quieter a coin's past seven days were against its past 60 days, the better its breakout entries did. Entries in the quietest quarter (7-day mean bar range at 0.32 to 0.76 of the 60-day one) returned +1.47 % over 18 bars (t 2.66, 236 entries) and fell 4.2 % at worst along the way. The other three quarters returned only +0.24 % to +0.44 % (t ≤ 0.69) and fell 5.2 % to 6.5 %, out of 1919 entries from flat.
- F3: The falls come from breakouts made while the coin was already turbulent. Inside the fall windows w5 to w10, entries in the two highest 7-day/60-day range quarters lost −0.27 % and −0.46 % over 18 bars (136 entries). The two quietest quarters gained +1.90 % and +0.90 % there, and those losing entries were held at larger positions (1.26 to 1.34 of the book).
- F4: The quiet-week edge holds across time and coins. The quietest quarter gives +1.48 % in w1 to w12 and +1.45 % in w13 to w24 (t 1.81 and 2.01). It is positive on all six coins (+0.70 % on LTC to +2.00 % on XRP), and it is the best quarter on five of them.
- F6: The tested idea's own move is barely above a trade's cost: +0.20 % unusual move per case, 1.1 times the 0.19 % cost of a trade. Entries in the quietest-week quarter carry a total move of +1.47 %, which is about +1.06 % above the coin's +0.41 % normal drift, so about 5.5 times the cost.
