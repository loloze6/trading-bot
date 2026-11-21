---
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
idea tested: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3222 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but is small against its spread: the mean short-direction excess return over 26 days is +1.51 %, the median +4.35 %, and 59 % of cases are positive, but the standard deviation is 27.4 % with a skew of -1.05, so t is only 0.69 on 156 independent cases.
- **F2:** The effect is swamped by the market's own year. Cases in 2018 earn +20.0 % (t 4.86, 34 cases, 88 % positive) and in 2019 +5.5 % (t 2.44, 30 cases). Cases in 2020 lose -32.8 % (t -3.00, 7 cases), in 2021 -35.3 % (t -2.91, 12 cases) and in 2023 -10.9 % (t -2.15, 11 cases). Coins below a falling cloud kept falling in bear years and rebounded hard in bull years.
- **F3:** The sign differs by coin. BTC, ETH, LTC and ZEC show +3.1 %, +3.2 %, +5.6 % and +3.4 % (t 0.54 to 1.29, 25 to 32 cases each). XMR and XRP show -4.4 % each (t -0.85 and -0.57, 20 and 23 cases).
- **F4:** The grading by thinness is weak and not monotonic. The thinness quartiles, thickest to thinnest, give -8.8 %, +8.3 %, +0.6 % and +6.0 % (39 cases each). The Spearman of thinness against the excess return is 0.14 (p 0.08).
- **F5:** The effect shows only at the plan's own horizon. The excess return is -0.4 % at 5 days, -0.6 % at 10 days, +1.5 % at 26 days and -1.8 % at 40 days (t -0.45, -0.47, 0.69, -0.71; 156 cases each). No other horizon gives a clearer answer.
- **F6:** The total move, which keeps the coins' upward drift (+1.4 % to +7.4 % per 26 days), goes against the short at every horizon. It is -1.0 % at 5 days, -1.8 % at 10, -2.7 % at 26 and -6.5 % at 40 (t -2.61). This is why the book's Sharpe is -0.31, even though the unusual move is 14 times the 0.19 % cost of a trade.
- **F7:** Splitting by how far the coin sits below its 100-day average gives +19.7 % and +14.1 % in the two milder terciles (t 2.35 and 2.43) and -12.7 % in the deepest one. Each tercile has only 13 cases, too few to turn into a condition.

## Ideas
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud.b1_falling-cloud-more-coins` (from F1, F2, F3): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
