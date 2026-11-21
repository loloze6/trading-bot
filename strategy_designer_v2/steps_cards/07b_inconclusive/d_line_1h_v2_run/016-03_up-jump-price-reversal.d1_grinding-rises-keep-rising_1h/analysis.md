---
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea tested: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2027 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but falls short of the bar. On the plan's non-overlapping 72-bar grid of rising cases, the forecast's coefficient beyond rise size is +0.000341 with t = 1.52 over 2,865 cases. The raw grind measure gives +0.0214 with t = 1.76 over the same cases.
- **F2:** The grind measure is degenerate for most rises and is entangled with rise size. In the bottom three grind quintiles (60% of the 2,865 rising cases) it is exactly 0, because the top-3 hourly gains exceed the whole 3-day rise. Those quintiles earn -0.0017, -0.0038 and +0.0019 excess over 72 bars. The top quintile (mean grind 0.40) earns +0.0108, but it also holds the largest rises (mean past rise 0.132, against 0.027 to 0.035 in the zero quintiles).
- **F3:** The effect is mixed across coins and years. The grind t is 2.74 for BTC and 2.08 for LTC, but -0.21 for ETH, -0.39 for ZEC and 0.35 for XMR, each on about 460 to 500 cases. By year it is 1.95 in 2019 and 2.00 in 2024, but -0.64 in 2018 and -0.46 in 2025.
- **F4:** The effect appears only at the plan's own 3-day horizon. The forecast t is -0.29 over the next 24 hours, 1.52 over the next 72 hours and 0.54 over the next 144 hours, on 2,926, 2,865 and 2,802 cases.
- **F5:** Within rise-size terciles, the grind effect sits in mid-sized rises. Its t is 2.71 (n 955, mean past rise 0.042) there, against -0.41 for small rises (0.011) and 0.49 for large rises (0.127).
- **F6:** On the down side the mirror effect is clearer than on the up side. On 2,669 falling grid cases, the share of the 3-day fall not made by its 3 biggest hourly losses has coefficient -0.0315 with t = -2.06 on the next 72-bar excess return, net of fall size. The more evenly spread the fall, the more the coin keeps falling.

## Ideas
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b1_grinding-rises-more-coins` (from F1, F3): When a coin has risen over the past 3 days, the smaller the share of that rise that came from its few biggest hourly gains (a grind of many small hourly steps), the more the coin keeps rising over the next 3 days.
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.b2_grinding-falls-keep-falling` (from F6, F4): When a coin has fallen over the past 3 days, the smaller the share of that fall that came from its few biggest hourly losses (a grind of many small hourly steps down), the more the coin keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
