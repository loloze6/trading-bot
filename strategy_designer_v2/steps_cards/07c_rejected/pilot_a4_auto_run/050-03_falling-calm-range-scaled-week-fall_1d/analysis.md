---
line: 7.c no effect
backtest: 050-03_falling-calm-range-scaled-week-fall_1d
idea tested: 050-03_falling-calm-range-scaled-week-fall
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3516 USD
---
## Findings
- **F1:** The test found no effect because large scaled falls and moderate scaled falls do opposite things, and the plan's 60-value standardisation mixes them. In falling calm markets (BTC, DOGE, XMR, explore windows), the biggest-fall quintile of the 7-day return over the 30-day mean range (mean −2.9 units) moved −2.4 % against the coin's drift over 3 days (t −1.3, 30 cases), −4.6 % over 5 days (t −1.9, 20) and −4.3 % over 10 days (t −2.3, 9). The second quintile (mean −1.05 units) moved +1.2 %, +1.5 % and +1.7 % over the same horizons.
- **F2:** On the brief's long side, scaled rises in falling calm markets kept rising over the following days. A 7-day scaled rise was followed by an unusual move of +0.4 % over 3 days (t 0.6, 65 cases), +1.9 % over 5 days (t 1.2, 38) and +4.7 % over 10 days (t 1.5, 21). A 14-day scaled rise was followed by +1.1 % over 3 days (t 1.3, 54), +2.6 % over 5 days (t 1.9, 33), +5.1 % over 7 days (t 2.05, 21) and +5.4 % over 10 days (t 1.6, 15).
- **F3:** The carry-on grows with the scaled move as a whole and is clearer at longer horizons. The Spearman correlation of the scaled 7-day return with the next unusual move is 0.01 over 1 day, 0.08 over 3 days, 0.20 over 5 days (p 0.05, 94 cases) and 0.30 over 10 days (p 0.04, 47 cases). Weighting the rises by their size raises the mean move: for 7-day rises, +7.0 % against +4.7 % unweighted over 10 days. For 14-day rises, +10.1 % against +5.4 % over 10 days (Spearman 0.46, p 0.09).
- **F4:** The rises carry on in every coin but not in every year. Over 5 days, the big half of 7-day rises moved +1.4 % on BTC (7 cases), +4.3 % on DOGE (3) and +1.7 % on XMR (9); the small half moved +1.0 %, +4.5 % and +0.8 %. By year, the big half moved +0.1 % in 2018 (7 cases), +1.8 % in 2019 (3) and +2.8 % in 2021 (8). The 2018 cases were flat.
- **F5:** The tested short is too small to pay for a trade. It made +0.07 % per case over 3 bars (t 0.19, 414 days), against a cost of 0.33 % per trade. Its total move is −0.10 %, and its book earned a Sharpe of 0.05 against a holding Sharpe about 0.75 higher.

## Ideas
- `050-03.c1_calm-downtrend-scaled-rise-continues` (from F2, F3, F4): In a falling, calm market, a coin that has risen over the last 14 days keeps rising over the next 7 days, and rises further the larger its 14-day rise is in units of its 30-day average daily high-low range.
- `050-03.c2_weekly-scaled-rise-longer-carry` (from F2, F3, F1): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 10 days, and rises further the larger its 7-day rise is in units of its 30-day average daily high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
