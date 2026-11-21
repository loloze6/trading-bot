---
line: 7.b inconclusive
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
idea tested: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3428 USD
---
## Findings
- **F1:** Across all 156 grid cases the short earns +1.51 % per case over 26 days beyond the coin's drift, with t 0.69, and 59 % of cases are positive. The result is on the side the idea predicts but far short of t 2. The total move is -2.72 %, because the coins' normal drift over 26 days (+1.4 % to +7.4 %) works against a short.
- **F2:** The idea's graded part is clear, and it points where the idea says. The slow-fall half earns +7.32 % beyond drift (t 3.06, 78 cases, strength 0.29), the fast-fall half -4.30 % (t -1.20, 78 cases). Their difference is +11.6 % with Welch t 2.70, and regressing the excess on log slowness gives slope 0.075 (t 2.91, 156 cases). By slowness quartile, from fastest to slowest fall, the excess runs -7.5 %, -1.1 %, +6.8 % (t 1.95) and +7.8 % (t 2.36).
- **F3:** The forecast's own size orders the outcome the same way. The most-short quartile earns +8.3 % (t 1.71) and the least-short quartile -7.2 % (t -1.36), 39 cases each. The main measure averages strong slow-fall cases with fast-fall cases that go against the short, and that mix is what keeps its t low.
- **F4:** The effect depends on the market's own moves by year. The short pays in 2018 (+20.0 %, t 4.86, 34 cases), 2019 (+5.5 %, t 2.44) and 2025 (+9.1 %, t 1.92). It loses badly in the bull years 2020 (-32.8 %, t -3.00, 7 cases) and 2021 (-35.3 %, t -2.91, 12 cases), and those losses come almost entirely from fast-fall cases (-38.4 % and -58.6 %).
- **F5:** Inside the slow-fall half the sign holds on all 6 coins: BTC +5.8 %, ETH +9.4 %, LTC +13.2 % (t 3.17), XMR +3.4 %, XRP +1.4 %, ZEC +11.5 %. Each coin has only 9 to 23 cases, so it is too few cases, not a few coins, that leaves the result unclear.
- **F6:** The move outlasts the 26-day horizon, in the spirit of findings F9 and F10. The raw short-side return is -1.8 % at 10 days (t -1.46) and -8.2 % at 52 days (t -2.44, 117 cases), so 52 days is the coins' drift showing more than the idea's edge. Per case, the unusual move (+2.49 % on step 5's 191 cases) is 12.9 times the 0.19 % cost of a trade, so the idea is large enough to pay if it is real.

## Ideas
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins` (from F1, F2, F3, F5): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the more slowly the cloud has fallen over the past 26 days.
- `021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b2_gentle-cloud-fall-underperforms` (from F2, F3, F4): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days falls short of the coin's normal drift, and by more the more slowly the cloud has fallen over the past 26 days, the coin's slowest-falling clouds giving the largest shortfall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
