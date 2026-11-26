---
line: 7.d confirmed, not profitable
backtest: 061-01_calm-big-up-day-continues_1d
idea tested: 061-01_calm-big-up-day-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.2227 USD
---
## Findings
- **F1:** The idea's effect lives entirely on its long side. In folds B and C, calm cases after an up day are followed by a directional excess 5-day move of +1.63 % (t 3.19, 498 non-overlapping cases). Cases after a down day give only +0.31 % (t 0.64, 470 cases). In the book, long bars summed a gain of +3.64 against −0.42 for short bars (2,178 and 2,052 coin-bars), and the short side lost in 2018, 2020, 2022, 2023 and 2024.
- **F2:** The long side is graded and the short side barely is. Long cases rise with the size of the day: +0.81 % (t 1.1), +1.41 % (t 1.7) and +2.83 % (t 2.8) from the smallest to the largest third of |z|. Short cases go from −0.42 % to +1.02 %, none with a t above 1.2.
- **F3:** Removing the short side repairs most of what failed, before fees. This rebuild's Calmar runs slightly below the official 0.338, so it is a lower bound. The book as tested has a Sharpe of 0.548, a deepest fall of −42 % and a Calmar of 0.28, the same Sharpe as holding the coins (0.548, Calmar 0.24). The long-only book has a Sharpe of 0.781, a deepest fall of −29 %, a yearly return of +18.2 % and a Calmar of 0.63. That beats holding on Sharpe, though it is still under the 0.75 Calmar bar.
- **F4:** Inside the calm profile, the long effect concentrates in a rising 60-day trend. There, up-day cases are followed by +3.01 % (t 3.12, 172 cases), against +0.62 % in choppy (t 0.77) and +0.50 % in falling (t 0.43). It stays graded inside rising: +1.24 %, +2.84 % and +4.78 % (t 2.8) by forecast third.
- **F5:** The rising-trend condition alone does not carry this move. Every calm bar has a non-zero forecast, so the comparison is with calm-rising bars after a down day: they are followed by +0.02 % (t 0.01, 128 cases), against +3.01 % after an up day. The gain is the up day's continuation, not the trend's drift, which fits the theory's "deliberate flow worked over several days".
- **F6:** Restricting the long-only book to rising-trend bars still leaves the falls high. Its Sharpe is 0.70 with a deepest fall of −39 % and a Calmar of 0.33, so the profile helps the per-case move more than the book's falls. In agitated markets the same z gives −0.10 % (1,288 cases), as the brief says.

## Ideas
- `061-01.d1_calm-big-up-day-long-only` (from F1, F2, F3): In a calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days, traded on the long side only: a one-day fall in a calm market carries no follow-through.
- `061-01.d2_rising-calm-up-day-continuation` (from F4, F5, F2, F6): In a rising, calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
