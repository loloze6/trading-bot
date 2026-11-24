---
line: 7.g patterns
backtest: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue_1d
idea tested: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.5849 USD
---
## Findings
- **F1:** How strongly a coin's 14-day return, divided by its usual volatility, predicts the following days depends on the weekday it is read. Read at Wednesday, Thursday or Friday close, the larger it is, the higher the unusual move after it: Wednesday over 3 days has slope t 2.95, Thursday over 2 and 3 days t 3.12 and 2.71, Friday over 1, 2 and 3 days t 3.14, 2.98 and 2.45 (about 1,205–1,250 cases on 201–209 days each, cases on one day taken together). Read at Monday, Tuesday, Saturday or Sunday close, the t lies between −1.03 and 1.06 at every horizon.
- **F2:** At Friday close, the 2-day unusual move rises with the volatility-scaled 14-day return in steps. By quintile: −0.64 % (t −0.99), −0.67 % (t −1.55), +0.84 % (t 2.58), +0.61 % (t 1.78), +1.76 % (t 3.05; 245 cases on 94 days in the top quintile). The plan's grade, the raw 14-day rise times the volatility ratio, does not rise in steps: its quartiles give +1.42 %, +0.42 %, +0.77 %, +2.16 %. This is why the supporting check failed (−0.05 %).
- **F3:** The plan's high-volatility condition is not what carries the effect. At Friday close the slope of the 2-day unusual move on the scaled 14-day return is about the same in both regimes: 0.0082 (t 2.68, 586 cases) with volatility above its 60-day level, 0.0078 (t 1.94, 638 cases) with it below. At Thursday close the 3-day slope is stronger with low volatility: 0.0166 (t 3.23, 665 cases) against 0.0091 (t 1.82, 540 cases) with high volatility. Friday 14-day rises in the low-volatility regime still gain +0.63 % (t 2.14, 233 days).
- **F4:** Thursday's late-week continuation recurs across years. The slope of the 3-day unusual move on the scaled 14-day return is positive in 6 of 8 years, with t above 2 in 2018 (2.57), 2022 (2.10) and 2024 (2.80); it is negative in 2021 (t −0.30) and 2023 (t −1.41).
- **F5:** The book's profit rests on a few days. Its 5 best days (daily mean over the coins up to +12.9 %) add 0.407 of the 0.825 summed daily return. The book's Saturday returns reach a +60.3 % maximum on one coin-day, against a +0.50 % mean over 609 days in a position.
- **F6:** The brief's own angle shows no clear pattern. On a 5-day grid, where the close sits in its 60-day range does not separate later moves: the lowest quintile gives −0.62 % (t −0.47) and the highest +1.08 % (t 1.20). Returns after large daily moves (beyond 2 usual moves either way) give +0.21 % (t 0.19) and −0.11 % (t −0.18) over 2 days.

## Ideas
- `031-01.g1.g1.g2.d1.g1_late-week-scaled-momentum-continues` (from F1, F3, F4): At Thursday's close (UTC), a coin's 14-day return measured in units of its usual daily volatility is followed by a move in the same direction over the next 3 days (Friday to Sunday). The larger that scaled 14-day rise, the larger the gain over those 3 days.
- `031-01.g1.g1.g2.d1.g2_scaled-friday-rise-into-weekend` (from F2, F3, F1): At Friday's close (UTC), a coin's 14-day rise measured in units of its usual daily volatility is followed by a further rise over the next 2 days, at any volatility level. The larger that scaled rise, the larger the weekend gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
