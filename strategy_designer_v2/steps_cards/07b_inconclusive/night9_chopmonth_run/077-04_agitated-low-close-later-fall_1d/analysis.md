---
line: 7.b inconclusive
backtest: 077-04_agitated-low-close-later-fall_1d
idea tested: 077-04_agitated-low-close-later-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4209 USD
---
## Findings
- **F1:** The low-close short is on the side the idea predicts at every horizon tried, but it is never clear. Over 6 bars, folds B and C give +1.02 % per case (t 0.88, 545 cases on 248 days). The other horizons are no better: +0.57 % over 1 bar (t 1.17), −0.05 % over 3 bars (t −0.08) and +0.88 % over 10 bars (t 0.55). A different horizon would not make the result clear.
- **F2:** The effect changes sign from period to period, which is why the result is unclear. By window it runs from −8.2 % (w11, t −2.75, 79 cases) to +8.1 % (w13, t 1.99) and +3.2 % (w17, t 2.01). By year it is positive in 2018 to 2020 (+4.2 %, +1.8 %, +2.2 %, t 1.1 to 1.6) and negative in 2021 (−1.2 %, t −0.52, the largest year with 219 cases).
- **F3:** No coin carries the effect clearly. Seven of ten coins are positive, but the best are ZEC at +2.3 % (t 1.44, 94 cases) and ETH at +1.9 % (t 1.17), while XRP is −1.4 % and XMR −0.2 %.
- **F4:** The grading by close location is in order but far too weak to show. Shorts after a previous close at 0.75 to 0.85 of the range move +0.85 % (t 0.76), at 0.85 to 0.95 +1.11 % (t 0.61), and at 0.95 or more +1.52 % (t 0.57, 74 cases).
- **F5:** No narrower condition isolates a clear effect.
- **F6:** The close-location gradient on agitated bars is not specific to agitated markets, so it is not where the brief says. On agitated bars, the move over the following 6 days after the previous close runs from +0.43 % for top closes to −5.3 % for bottom closes (t −1.51, 96 cases), in order through the middle groups. Calm bars show the same order, from +1.40 % at the top to −1.06 % at the bottom (t −0.59).
- **F7:** The market's own rise drowns the effect in the book. The coins' normal drift is −0.86 % per case in the short direction, larger than the +0.52 % unusual move, so the total move per case is −0.35 %. That is −1.6 times the 0.22 % cost of a trade, and the book loses (Sharpe −0.23, yearly −9.8 %).

## Ideas
- No ideas: The test already used every fold and every coin with daily data, so no more data is available. The positive but weak move (t 0.93) changes sign across windows and years (F2), and no coin, trend, range width, prior return or close-location group shows it clearly (F3–F5). The close-location gradient is also as present in calm markets as in agitated ones (F6), so there is no part of the data to narrow the idea to.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
