---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d
idea tested: 031-02.b1.b1.b1.g1_wide-day-extends-up-run
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4336 USD
---
## Findings
- **F1:** Inside 6-day up-runs, the whole effect sits in the widest fifth of days by range against the 20-day mean range: +1.40 % drift-adjusted over 3 days (t 2.34, 1143 cases, 373 days, strength 0.135), while the other four fifths run from −0.26 % to +0.11 % (|t| ≤ 0.63). This is the tested idea itself, but convex rather than graded, and it adds no new pattern.
- **F2:** The strongest pattern the idea does not explain is in 6-day down-runs: a day closing in the top third of its range is followed by −1.23 % drift-adjusted over 3 days (t −2.70, 1365 cases, 353 days, strength −0.137). It is not graded, though: the middle third gives +0.87 % (t 1.79) and the bottom third −0.43 % (t −0.86). With about 100 cells examined, a single |t| of 2.7 is about what chance alone would produce.
- **F3:** Also in down-runs, the lowest fifth of 20-day volatility against 60-day volatility is followed by −1.29 % (t −2.55, 997 cases, 336 days). The other fifths are not ordered (+0.08, −0.39, −0.89, +0.52 %), so there is no gradient behind it.
- **F4:** The 6-day and 20-day returns scaled by volatility are U-shaped, not graded. Only the top fifth stands out: +0.87 % (t 2.04) for the 6-day return and +0.99 % (t 2.05) for the 20-day return. The middle fifths are slightly negative (−0.51 %, t −1.55; −0.68 %, t −1.69), which is borderline given how many angles were examined.
- **F5:** The book is mostly a scaled copy of the market. On the market's worst fifth of days it loses −1.34 % against the coins' −5.75 %, and on the best fifth it gains +1.58 % against +5.74 %. Its top 5 % of days carry 223 % of its total gain and its bottom 5 % take back 184 %.
- **F6:** Calendar effects show nothing beyond chance. No weekday's 3-day drift-adjusted return reaches |t| 1.7 (largest: Thursday +0.91 %, t 1.62). No year does either (largest: 2021, +1.57 %, t 1.82), and the book's losing years, 2022 (−0.069 % a day) and 2025 (−0.010 %), are the coins' falling years.

## Ideas
- No ideas: Outside the tested idea, the strongest patterns (down-run closes near the high, F2; quiet volatility in down-runs, F3) do not rise above what chance gives across about 100 cells examined (forward return by 6-day, 20-day and 1-day move, range width, close location, body size, volatility level, weekday, year, and the book against market days), and none of them is graded.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
