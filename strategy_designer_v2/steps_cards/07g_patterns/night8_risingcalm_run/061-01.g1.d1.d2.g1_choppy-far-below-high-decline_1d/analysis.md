---
line: 7.g patterns
backtest: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline_1d
idea tested: 061-01.g1.d1.d2.g1_choppy-far-below-high-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4009 USD
---
## Findings
- **F1:** In calm markets (30-day swing at or below the coin's median), a coin's 5-day move measured in its own daily-swing units is followed by more of the same over the next 5 days. Weighted by the size of that move, the continuation is +3.15 % in excess of drift (t 2.73, 688 cases on 167 days). In agitated markets it is +0.04 % (t 0.04, 662 cases).
- **F2:** The calm-market continuation after a 5-day move grows with the move's size. By bin of |5-day move in swing units| it is -0.02 % (t -0.04, 330 cases), then +1.12 % (t 1.26, 157), +3.64 % (t 2.61, 93), +4.46 % (t 2.12, 55) and +4.23 % (t 1.68, 53). In agitated markets the same bins fall from +1.01 % to -1.08 %.
- **F3:** The calm 5-day continuation is positive in 11 of the 12 windows shown, w7 to w18. The one exception is w15, at -0.42 % (t -0.09). w12 is the strongest at +1.84 % (t 2.75).
- **F4:** A single day that is large against the coin's prior 20-day swing also continues in calm markets: +2.19 % weighted (t 2.34, 688 cases, 167 days), against +0.79 % (t 0.81) in agitated markets. It holds for both down days (|z|>1.5: +2.93 %, t 1.50) and up days (+4.16 %, t 1.72). Every year 2018–2021 is positive, from +1.37 % to +4.03 %. But the one-day version is weaker and less graded than the 5-day one: in the 0.5–1 swing bin it is -0.20 %.
- **F5:** For the tested idea, the choppy cases in the deepest three gap quintiles were followed by excess 5-day returns of -5.80 % (t -2.07, 25 cases), -4.30 % (t -2.95, 49) and -3.07 % (t -2.97, 49). The two gap quintiles nearest the high gave +0.10 % and +1.52 %. So the coin did keep falling below its high, but the pattern is not graded within the deep cases, which matches step 5's failed median split (-0.07 %).
- **F6:** The book lost on its shorts: 731 SHORT trades averaged -1.79 % net (median -2.38 %). ZEC alone averaged -8.48 % over 94 trades, and the book's daily mean was negative in 7 of 12 windows.
- **F7:** Next-day returns are high from Thursday's close (+0.61 %, t 4.10, 1242 days) and Friday's close (+0.52 %, t 3.87). This late-week gain is already held (045-01, rising market late week gain), so it is left out as a discovery.

## Ideas
- `061-01.g1.d1.d2.g1.g1_calm-swing-unit-move-continues` (from F1, F2, F3): In a calm market, the larger a coin's 5-day return is against its own recent daily swing, the further the coin keeps moving the same way, up or down, over the next 5 days.
- `061-01.g1.d1.d2.g1.g2_calm-big-day-follow-through` (from F4, F1): In a calm market, the larger a single day's return is against the coin's swing over the previous 20 days, the further the coin keeps moving that day's way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
