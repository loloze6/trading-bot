---
line: 7.g patterns
backtest: 031-01.b1.b2_wide-day-extends-strong-run_1d
idea tested: 031-01.b1.b2_wide-day-extends-strong-run
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3318 USD
---
## Findings
- **F1:** Of the roughly fifty groupings I examined, the largest effect was the top quintile of the day's range against its 20-day mean: mean unusual 3-day move +0.85 %, strength 0.094, t 1.92 over 383 days. Given how many angles were looked at, this does not stand out from chance, and the middle quintiles do not rise in order (+0.04 %, −0.33 %, −0.33 %).
- **F2:** The 5-day return has an ordered but unsure effect on the next 3 days: its quintiles give −0.56 % (t −1.03, 379 days) rising to +0.72 % (t 1.68, 440 days). This is the run-continuation the tested idea bet on, and it is not established.
- **F3:** The brief's own situation does not show its reversal. After a 5-day rise, wide-range flat days (top range tercile, |body| < 0.25 of range) are followed by an unusual 3-day move of +0.47 % (t 0.69, 115 days, 144 cases). After a 5-day fall they give −0.52 % (t −0.55, 89 days). Both point to continuation rather than a move back, and neither can be told from 0.
- **F4:** The 20-day return (quintiles −0.10 % to +0.58 %, top t 1.20) and the 5-day over 60-day volatility ratio (quintiles −0.64 % t −1.52 to +0.22 %, not ordered) show nothing reliable. Neither does the day's close location, body, last 1-day return, or weekday: every |t| is ≤ 0.95.
- **F5:** The book behaves like a scaled long holding of its coins rather than a timer. Its daily return correlates 0.67 with the coins' mean daily return. It captures about the same share of the coins' worst and best day quintiles: −1.55 % against −5.36 %, and +1.78 % against +5.34 %. Bars where it was long were followed by an unusual 3-day move of only +0.09 % (t 0.39, 922 days), against −0.17 % when flat (t −0.55).
- **F6:** The book's yearly mean daily return follows the coins' year: 2022 −0.10 % against coins −0.19 %; 2020 +0.27 % against +0.42 %; 2018 −0.003 % against −0.35 %. Its profit rests on the market's drift, which F5 also shows.

## Ideas
- No ideas: Across range, run, body, close location, trend, volatility, weekday, position and year, no pattern reached a t of 2 (largest 1.92 among about fifty groups), so no finding stands out enough from chance to support a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
