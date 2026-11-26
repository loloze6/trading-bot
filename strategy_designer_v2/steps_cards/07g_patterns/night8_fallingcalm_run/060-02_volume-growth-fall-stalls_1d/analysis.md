---
line: 7.g patterns
backtest: 060-02_volume-growth-fall-stalls_1d
idea tested: 060-02_volume-growth-fall-stalls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4050 USD
---
## Findings
- **F1:** The tested idea's gain comes mostly from its shrinking-volume end. On the active falling-market grid cases (folds B, C), the most negative forecast quintile (the strongest volume dry-up) is followed by a 5-day excess return of -3.09 % (t -3.30, 136 cases). The other quintiles give -0.09 %, +0.34 %, +2.59 % (t 2.33) and +0.44 % (t 0.38). The top quintile adds almost nothing, so the graded effect is steepest where volume has shrunk most.
- **F2:** The dry-up continuation is clearest in calm falling markets. Calm cases with a negative forecast gain -1.68 % over 5 days (t -2.27, 164 cases), while calm cases with a positive forecast give -0.03 % (t -0.04, 62 cases). In agitated falling markets the effect sits on the growth side instead: +1.81 % (t 1.88, 177 cases) against -1.29 % (t -1.28, 136 cases).
- **F3:** In rising markets, outside the tested profile, the 30-day over prior-30-day volume ratio works the opposite way to the tested idea. The 5-day excess return falls with the log ratio (slope -0.0405, t -2.92, 319 grid cases). By volume-ratio tercile the lowest tercile gains +3.52 % (t 2.38, 106 cases), the middle +1.00 % (t 1.23) and the highest -0.47 % (t -0.30). By year the slope is negative in 2019 (t -2.00, 72 cases), 2020 (t -1.01, 120) and 2021 (t -3.92, 119).
- **F4:** The book's gain is timing, not the market's rise. On the book's 5 % worst days it loses -3.70 % while its coins move only -0.43 %; on its 5 % best days it gains +4.24 % while its coins move +1.40 % (435 coin-days each). Long and short trades pay alike: 516 long trades average +3.62 % net and 605 short trades +3.17 % net.
- **F5:** A narrow day's close location looked like a continuation signal but did not hold. On the narrowest-range tercile, low closes were followed by -2.70 % (t -3.31, 125 cases) and high closes by +2.62 % (t 2.68, 187). The day-clustered test fails: t 1.21 over 198 days on 728 cases. The close-location over relative-range slope also reverses by year (2019 t +4.45, 2020 t -2.69), so this is not counted as a pattern.
- **F6:** The other angles show nothing that stands out against the number of angles tried:

## Ideas
- `060-02.g2_calm-fall-volume-dry-up` (from F1, F2): In a falling, calm market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.g1_rising-quiet-volume-rally-continues` (from F3): In a rising market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
