---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
line: 7.g patterns
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, the price keeps rising over the next 24 hours, and the heavier that hour's volume against its 30-day average hourly volume, the larger the further rise.
Consequence: A trader would buy into a sharp hourly rise that comes on surging volume rather than fade it, and refuse to chase one that comes on ordinary volume.
Why:
- F2: Up hours on heavy volume (rise of at least 2.5 typical hourly moves, volume at least 2 times its mean) are followed by a further rise over the next 24 hours in both halves of the windows: +0.47 % (t 2.16, 446 cases) in w1–w12 and +0.40 % (t 1.71, 463 cases) in w13–w24, about +0.44 % over 909 cases. Adding the coin's normal long drift of about +0.15 %, the total move is about 0.59 %, roughly 5 times the 0.11 % cost of a trade. The effect is stronger in ETH (+0.70 %, t 2.72, 424 cases) than in BTC (+0.21 %, t 1.03, 485 cases), and it is positive in all 8 years (from +0.02 % in 2018 to +1.63 % in 2021).
- F3: Among up hours of 3 to 5 typical moves, the 24-hour continuation grows with the hour's volume ratio: +0.39 % (t 1.11, 124 cases) at 1–2 times the mean volume, +0.61 % (t 2.08, 323) at 2–4 times and +0.97 % (t 3.27, 294) above 4 times. It does not grow with the size of the move times the log of volume: the strength quartiles give +0.12 %, +0.60 %, +0.78 % and +0.25 %, the slope is negative and the correlation is -0.025. The cell above 4 times volume is one of about 38 cells examined, so it is only marginal against chance.
