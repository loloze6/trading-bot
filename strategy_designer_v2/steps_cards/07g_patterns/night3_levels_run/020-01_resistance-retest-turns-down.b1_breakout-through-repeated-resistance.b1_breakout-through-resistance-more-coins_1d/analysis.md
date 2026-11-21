---
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4666 USD
---
## Findings
- **F1:** The tested breakout has almost no edge of its own. Per case over 10 days, the unusual move is +0.08 % (strength 0.005, t 0.23, 2613 cases), only 0.4 times the 0.22 % cost of a round trip. The total move of +1.47 % is almost all the coin's normal drift of +1.38 %. On the 10-day grid, bars with a positive forecast were followed by an unusual move of -0.35 % (t -0.42, 649 cases), against +0.08 % (t 0.24, 2879 cases) on flat bars.
- **F2:** The book's year-by-year results follow holding the coins. Its Sharpe was -1.33 in 2018 against -1.24 for holding, 2.07 against 1.84 in 2020, 1.47 against 1.96 in 2021, -1.13 against -1.10 in 2022, and 2.01 against 2.16 in 2023. Its gain is mostly exposure to the market's rise, not breakout timing.
- **F3:** The trades that paid were the ones held long. Trades of 9.5 to 11 days (the plan's horizon) lost a mean of -4.25 % net (median -6.19 %, 635 trades). Trades of 20 to 60 days gained +15.09 % (median +3.78 %, 1057 trades) and trades over 60 days gained +29.37 % (151 trades). This is consistent with findings F9 and F8: moves outlast the horizon, and bull periods carry the books.
- **F4:** Coins in the top fifth of their own volatility-scaled 10-day return rose more than usual over the next 10 days. The unusual move was +3.28 % (t 3.58, 590 cases) on one grid and +2.96 % (t 2.44, 541 cases) on the grid shifted by 5 days. The effect is not reliable enough to act on, for four reasons:
- **F5:** The rebound after a large down day does not survive a change of grid. On the first grid, the bottom fifth of the 1-day return was followed by +1.58 % over 10 days (t 2.59). On the grid shifted by 5 days it was +0.12 % (t 0.19), over 5 days +0.02 % (t 0.07), and measured by day its t was 0.15. Its sign flips by year, from -8.62 % in 2018 to +6.28 % in 2024.
- **F6:** The weekday pattern is an artefact of the grid. Thursday starts gained +4.26 % (t 3.99) on the first grid, but -1.11 % (t -1.73) on the grid shifted by 5 days. Volatility level does not separate the cases either: the most volatile third gained +0.80 % (t 1.06) and the least volatile -0.11 % (t -0.22).

## Ideas
- No ideas: I looked at about a dozen angles: past 1-, 3-, 10- and 20-day returns, where the price sits in its 20-day range, volatility level, weekday, year, forecast state, coin group and trade duration. None stood out enough to count. The best candidate, the 10-day momentum in F4, is not graded, is weaker than t 2 once cases are counted by day, disappears over 20 days and flips sign with the year's drift. That fits the year's drift rather than a timing edge that a new idea could rest on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
