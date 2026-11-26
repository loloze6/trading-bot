---
line: 7.g patterns
backtest: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position_1d
idea tested: 058-02.b1.b2.b1.b2.b1_calm-rising-range-position
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3690 USD
---
## Findings
- **F1:** Across all trends on a 10-day non-overlapping grid of folds B and C, the tested range-position bet works only outside falling markets. The range position (-1 at the 20-day low, +1 at the high) times the coin's excess 10-day return averages +0.0475 (t 4.05, 104 cases) in the tested rising-calm profile. It averages +0.0407 (t 3.43, 77 cases) in choppy markets the book never traded, and -0.0020 (t -0.29, 209 cases) in falling markets.
- **F2:** In choppy markets the move after a range edge is continuation, not the brief's reversion. Closes in the bottom third of the 20-day range are followed by an excess 10-day return of -8.4 % (t -2.67, 25 cases), the middle third by -4.1 % (t -1.41, 34), and the top third by +7.2 % (t 1.48, 18). Taken one day at a time, the choppy range effect is less sure: t 1.84 over 33 days.
- **F3:** The brief's calm condition is not where the choppy effect lives. In choppy markets, range position times excess return is +0.0433 (t 3.36, 37 cases) when 30-day swing exceeds 60-day swing, against +0.0383 (t 1.95, 40 cases) when it does not.
- **F4:** The coin's 20-day direction carries the next 10 days most strongly in choppy markets. The sign of the 20-day return times the excess 10-day return averages +9.0 % (t 4.91, 77 cases) in choppy markets, +4.1 % (t 2.88, 188) in rising markets and +1.6 % (t 1.51, 209) in falling markets.
- **F5:** In all markets together, the excess 10-day return rises with the 20-day return quintile. It runs from -3.5 % (t -3.02) in the second-lowest quintile to +2.2 % (t 1.76) and +4.0 % (t 2.15) in the two highest, about 160 cases each.
- **F6:** The book earns from its long side only. Its 607 long trades net +8.15 % on average, and its 237 short trades net -4.51 %. Shorts lose at every forecast size: -4.78 %, -5.11 % and -1.68 % across the forecast terciles.
- **F7:** The rising-calm long side repeats ideas already held. Within rising markets, the excess 10-day return runs from -6.2 % (t -2.56, 35 cases) in the bottom range third to +5.8 % (t 2.55, 89) in the top third. This is the nearness-to-high continuation that 034-01.b1 and 035-01.b1 already hold, so it is not proposed again.

## Ideas
- `058-02.b1.b2.b1.b2.b1.g1_choppy-range-edge-continuation` (from F1, F2, F3): In a choppy market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 10 days, and the lower it sits, the larger its fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-02.b1.b2.b1.b2.b1.g2_choppy-market-20-day-momentum` (from F4, F5): In a choppy market, the larger a coin's 20-day rise, the larger its rise over the next 10 days, and the larger its 20-day fall, the larger its fall over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
