---
line: 7.g patterns
backtest: 050-03.c1_calm-downtrend-scaled-rise-continues_1d
idea tested: 050-03.c1_calm-downtrend-scaled-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3569 USD
---
## Findings
- **F1:** Inside the falling calm profile, the tested idea's grading holds clearly on the explore half: the slope of the coin's 7-day excess return on its 14-day return scaled by the 30-day mean high-low range has a t of 3.58 (61 non-overlapping cases, Spearman 0.33). Cases with a positive scaled rise gain +5.1 % over the coin's drift (t 2.34, 21 cases).
- **F2:** The same scaled 14-day move grades weaker at other horizons: t 2.44 over 3 days (155 cases, Spearman 0.16, mean of the rising cases +1.05 %, t 1.38) and t 1.15 over 14 days (25 cases). The 7-day horizon the idea uses is where it is clearest.
- **F3:** The other angles give nothing that stands out beyond chance after about 25 groupings:
- **F4:** The only large quintile gap is on the short side, outside this research's long-only box: the second-lowest 14-day-return quintile loses -7.6 % over the next 7 days (t -2.07, 15 cases), and the lowest loses -3.1 %.
- **F5:** The book's gain is concentrated:

## Ideas
- `050-03.c1.g1_calm-downtrend-rise-continues` (from F1, F2, F5): In a falling, calm market, a coin that has risen over the last 14 days keeps rising over the next 7 days, and rises further the larger its 14-day rise is in units of its 30-day average daily high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
