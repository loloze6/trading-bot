---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.c rejected
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 4 hours from the 21:00 UTC bar, a coin that has risen over its last 24 hours keeps rising, and the larger that 24-hour rise relative to its recent days, the larger the late-evening rise.
Consequence: A trader would hold or add to longs into the late evening after a strong up day, rather than expecting a pre-settlement pullback.
Why:
- F2: The continuation is stronger over 4 hours from the 21:00 bar: slope +6.94 bp per unit (t 5.36, 17124 cases), and on the raw 24-hour return t 5.33. Here the deepest-fall fifth loses 11.64 bp (t -2.92) and the strongest-rise fifth gains 15.87 bp (t 4.35). It fades by 12 hours (t 0.69) and 24 hours (t -0.49).
- F4: Both sides carry the 4-hour continuation, the rise side more strongly than the fall side: slope t 2.83 (8389 cases) where the 24-hour move is above its norm, against t 1.69 (8735 cases) where it is below.
- F3: The 4-hour continuation from 21:00 has a positive slope in all six coins (t 3.13 BTC, 2.46 ETH, 2.10 LTC, 3.76 XRP, 1.31 ZEC, 0.89 XMR). It is positive in 7 of 8 years, strongest from 2018 to 2022 (t 2.20 to 3.56) and weak from 2023 on (t -0.63, 1.28, 0.14).
