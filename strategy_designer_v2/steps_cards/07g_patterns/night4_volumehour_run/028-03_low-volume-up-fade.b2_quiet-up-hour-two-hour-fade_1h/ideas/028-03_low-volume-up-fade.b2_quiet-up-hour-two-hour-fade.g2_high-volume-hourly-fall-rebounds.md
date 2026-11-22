---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its 30-day average hourly volume, the price rebounds over the next two hours. The larger that hour's fall, the larger the rebound.
Consequence: A trader would refuse to chase a high-volume hourly sell-off in the next two hours, and could lean long against it.
Why:
- F2: A large hourly fall on volume more than 3 times its 30-day hourly average reverses over the next 2 hours by +22.6 bp beyond drift (t 3.34, 1167 cases). The same kind of rise does not reverse (+0.8 bp, t 0.14, 1046 cases).
- F3: Among hours with volume above 3 times average, the 2-hour unusual move falls as the hour's move in 30-day mean-absolute units grows. The slope is -2.3 bp per unit on BTC (t -2.33, 1764 cases) and -3.0 bp on ETH (t -2.44, 1995 cases). This is the opposite of the brief's volume-confirmed continuation. It is concentrated in 2020 (t -3.65) and 2021 (t -2.55) and absent in 2023 to 2025 (slopes +0.6, -0.7, +3.2).
