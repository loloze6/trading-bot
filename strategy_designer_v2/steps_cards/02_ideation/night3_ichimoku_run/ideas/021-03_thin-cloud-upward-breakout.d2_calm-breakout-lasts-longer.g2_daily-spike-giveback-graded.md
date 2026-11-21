---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
line: 7.g patterns
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to its usual daily move, the more the coin falls over the next day.
Consequence: A trader would refuse to chase a coin the day after its sharpest daily rises, and would trim longs into them.
Why:
- F1: On daily bars, a coin's next-day return runs against the size of its day's move. Over all days with |z| > 1 (z is the day's return standardised by the coin's own mean and standard deviation), the Spearman correlation of z with the next day's return is -0.129 (p < 0.0001, n = 3510). This is the strongest pattern of the angles examined, and the one that would most clearly survive the many angles looked at.
- F4: Large rises are followed by a small giveback, which is weaker and fading. After days with z > 3 the next day's mean is -0.94 % (t -1.69, n 151). After days with z ≥ 2 the excess next-day return is negative on 5 of 6 coins (XMR -2.57 %, t -4.16; BTC t -2.09; ETH t -2.15). It is negative in every year from 2018 to 2023 but near zero or positive in 2024 and 2025.
