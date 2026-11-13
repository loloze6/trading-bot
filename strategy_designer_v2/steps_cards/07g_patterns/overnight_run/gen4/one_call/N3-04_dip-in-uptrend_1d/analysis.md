---
line: 7.g patterns
backtest: N3-04_dip-in-uptrend_1d
idea tested: N3-04_dip-in-uptrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3316 USD
---
## Findings
- **F1:** Outside the uptrend regime, a down day larger than the coin's mean absolute daily move (z < -1) in the coin's top third of 20-day volatility was followed by a next-day excess return of +1.40% (t 5.27, n 650, hit 62.6%), and by +2.31% over three days on non-overlapping samples (t 2.94, n 180); the same drop in the lowest volatility third was followed by -1.03% over three days (t -2.26, n 210).
- **F2:** The F1 rebound is positive on every coin, from +1.19% (LTC) to +1.94% (ZEC) next day, with t between 1.50 and 2.92 and n between 93 and 134 per coin; by year it is positive from 2018 to 2024 (2018: +1.35%, t 3.41, n 248) but is -0.28% in 2025 (t -0.48, n 51).
- **F3:** Outside the uptrend, large drops (z < -1) made when price was more than 40% below its 60-day high were followed by +1.69% the next day (t 4.59, n 381), and by +0.55% at 25–40% below (t 2.22, n 541); drops within 10% of the 60-day high were followed by -0.12% (t -0.52, n 213).
- **F4:** Outside the uptrend, a large up day (z > 1) in the coin's top volatility third was followed by a next-day excess return of -0.87% (t -4.03, n 569, hit 39.9%); in the lower two volatility thirds the same up day gave about -0.1% to 0 (t -0.68 and -0.15).
- **F5:** Two consecutive down days of more than half the typical move were followed by a next-day excess return of +0.70% outside the uptrend (t 3.91, n 993) and +0.88% inside it (t 2.62, n 242); all other bars gave -0.20% outside the uptrend (t -4.14, n 8671).
- **F6:** Large drops on volume 1.5 to 2.5 times the 20-day mean were followed by +0.85% next day outside the uptrend (t 3.26, n 410) and +1.20% inside it (t 2.78, n 173); drops on below-average volume gave +0.30% (t 1.68, n 737) and +0.45% (t 1.58, n 273).
- **F7:** In the uptrend regime, the bar after a Friday bar earned +0.84% excess (t 4.50, n 663), while the bars after Wednesday bars gave -0.47% (t -2.68, n 714); the bar after a Monday or Wednesday bar was negative on all six coins (-0.18% to -0.39%). These are 7 weekday groups, so part of this may be chance.
- **F8:** The book's dip edge is a one-day effect: trades held up to 1.5 days averaged +1.15% net (n 1127), trades held 1.5 to 3.5 days averaged -3.47% (n 342), and trades held 3.5 to 7.5 days averaged -3.84% (n 79).
- **F9:** The idea's dip edge comes mostly from 2019 to 2021 (2020: +1.22%, t 5.07, n 375). From 2022 to 2025 the yearly t is never above 1.64, and 2018 was -2.04% (t -2.85, n 56); BTC, XRP and ZEC are not significant alone (t 1.35, 0.41 and 0.87).

## Ideas
- `N3-04_dip-in-uptrend.g1_high-volatility-capitulation-rebound` (from F1, F2, F6): Outside a 20- and 60-day uptrend, when a coin closes a down day larger than its typical daily move while its 20-day volatility is high for that coin, the following one to three days rise more than the coin's average.
- `N3-04_dip-in-uptrend.g2_deep-drawdown-drop-rebound` (from F3): A large down day made when the coin already trades far below its 60-day high is followed by a next-day rise above the coin's average return.
- `N3-04_dip-in-uptrend.g3_high-volatility-spike-fade` (from F4): Outside a 20- and 60-day uptrend, when a coin closes a large up day while its 20-day volatility is high for that coin, the next day returns less than the coin's average.
- `N3-04_dip-in-uptrend.g4_second-down-day-rebound` (from F5): A second consecutive down day, each larger than half the coin's typical move, is followed by a next-day return above the coin's average, in and out of uptrends.
- `N3-04_dip-in-uptrend.g5_uptrend-weekend-bar-strength` (from F7): In a coin's 20- and 60-day uptrend, the daily bar after a Friday bar returns more than the coin's average daily return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
