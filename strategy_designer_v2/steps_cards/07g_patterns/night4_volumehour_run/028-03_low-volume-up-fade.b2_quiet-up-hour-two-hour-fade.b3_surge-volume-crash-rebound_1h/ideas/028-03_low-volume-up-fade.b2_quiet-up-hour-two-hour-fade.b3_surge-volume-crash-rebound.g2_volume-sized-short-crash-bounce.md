---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls more than its typical hourly move over the past 30 days on volume well above its 30-day hourly average, it rises over the next one to two hours. The rebound grows with that hour's volume against its 30-day average rather than with the depth of the fall.
Consequence: A trader would take only the first two hours of the bounce after a heavy-volume hourly fall, sized by the volume surge, and not hold it longer.
Why:
- F5: The tested heavy-volume fall rebound is not graded. Over 2 hours, falls of 1.5 to 3 standard deviations on volume above 2.5 times its mean are followed by +20.7 bp (t 2.81, 812 cases), and falls beyond 3 standard deviations by about the same, +20.3 bp (t 1.93, 507 cases). Over 6 hours, the deepest falls give −5.8 bp (t −0.15), consistent with the step 5 slope of −4.9e-6.
- F6: The book gives back its 2-hour edge by holding past it. Trades lasting 1 hour or less gross +0.44 % (6724 trades) and those of 1 to 2 hours +0.27 % (10501). Trades of 2 to 5 hours gross −0.81 % (3912). The book's mean daily return is negative in 6 of 8 years (for example −30.5 bp in 2022 and −20.5 bp in 2025).
