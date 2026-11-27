---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4837 USD
---
## Findings
- **F1:** Among the 10-day grid cases in a choppy, calm market, the 30-day return ranks with the next 10 days' return over the coin's drift (Spearman 0.42, p 0.0002, 76 cases); cases after a month rise ended +9.9 % over drift (39) and cases after a month fall ended −4.0 % (37). The signed gain over 31 days has a t of only 1.38, so the ranking is clearer than the mean.
- **F2:** The choppy, agitated cases are too few to read (20 cases, 13 days, rho 0.34, p 0.14). Over all recorded chop-regime grid cases the 30-day return still ranks with the next 10 days (Spearman 0.18, p 0.013, 198 cases). The two lowest month quintiles were followed by −6.9 % and −5.3 % over drift, and the highest quintile by +7.3 % (t −1.44, −1.94 and +0.89 over 22 to 31 days).
- **F3:** The tested book is a short whose gains and losses come from the coin's own large moves. Its worst 1 % of days (124) came with the coin up +11.9 % and lost −5.6 % each, and its best 1 % came with the coin down −10.2 % and gained +5.5 % each. Each tail alone is about 24 times the book's net total, and the net yearly return is +0.0 % over 7.94 years. The short side also fights a −1.50 % normal drift per case, which turns the unusual move of +1.40 % (t 2.08) into a total move of −0.10 %, below the 0.22 % cost of a trade.
- **F4:** In a falling, calm market the 30-day move also continues over the next 10 days (Spearman 0.21, p 0.03, 107 cases). Cases after a month fall ended −3.7 % over drift (81) and cases after a rise ended +2.4 % (26), with a signed t of 2.15 over 30 days. In a falling, agitated market the month move instead reverses (Spearman −0.21, p 0.01, 146 cases).
- **F5:** A one-day fall large against the coin's 30-day swing is followed by a next-day gain only in agitated markets. The lowest seventh (mean z −1.44) was followed by +1.19 % over drift (t 2.26, 231 days) when agitated and by +0.32 % (t 0.87, 238 days) when calm. The ranking of falls against the next day was negative in every year from 2018 to 2021 (rho −0.06 to −0.12). This is the agitated fall rebound the map already holds in 16 falling-agitated long strategies, so it is no discovery.
- **F6:** The weekday effects in coin returns disappear once cases on the same day are counted as one: the next-day excess by weekday has a t between −1.07 and 1.47 over about 206 days each. The pattern of short-term volatility expansion (10-day against 30-day swing) is not monotone across quintiles (t from −1.61 to 1.45), so neither is a finding.

## Ideas
- `067-01.b1.g1.b1.d1.d2.g1_choppy-calm-month-continuation` (from F1, F2, F3): In a choppy, calm market, the larger a coin's 30-day return is in either direction, the further it moves the same way over the next 10 days, so that a stronger month rise is followed by a larger rise and a deeper month fall by a larger fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-01.b1.g1.b1.d1.d2.g2_falling-calm-slide-continues` (from F4): In a falling, calm market, the deeper a coin's fall over the past 30 days, the more it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
