---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.c rejected
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 4 hours from the 21:00 UTC bar, a coin's return follows the sign of its 24-hour return, and the larger that 24-hour move relative to its recent days, the larger the late-evening move in the same direction.
Consequence: A trader would lean with the day's direction into the late-evening UTC hours, leaning harder after a larger daily move, rather than fading it before settlement.
Why:
- F1: The market did the opposite of the idea at 21:00 UTC: the excess 2-hour return rises with the standardised 24-hour return (slope +3.43 bp per unit, t 3.80, 17265 daily cases), so the deepest-fall fifth loses 4.48 bp (t -1.65) while the strongest-rise fifth gains 9.98 bp (t 3.87). Late-evening moves continue the day's trend rather than reverse it.
- F2: The continuation is stronger over 4 hours from the 21:00 bar: slope +6.94 bp per unit (t 5.36, 17124 cases), and on the raw 24-hour return t 5.33. Here the deepest-fall fifth loses 11.64 bp (t -2.92) and the strongest-rise fifth gains 15.87 bp (t 4.35). It fades by 12 hours (t 0.69) and 24 hours (t -0.49).
- F3: The 4-hour continuation from 21:00 has a positive slope in all six coins (t 3.13 BTC, 2.46 ETH, 2.10 LTC, 3.76 XRP, 1.31 ZEC, 0.89 XMR). It is positive in 7 of 8 years, strongest from 2018 to 2022 (t 2.20 to 3.56) and weak from 2023 on (t -0.63, 1.28, 0.14).
- F4: Both sides carry the 4-hour continuation, the rise side more strongly than the fall side: slope t 2.83 (8389 cases) where the 24-hour move is above its norm, against t 1.69 (8735 cases) where it is below.
- F5: The continuation belongs to the evening clock and not to all hours. Pooled over every even hour, the 2-hour return shows no order across fifths of the standardised 24-hour return (+0.84, -1.96, +1.03, -0.29, -0.48 bp). The hourly slope is reversal-like at 03:00–06:00 (t -3.8 to -5.5) and at 19:00–20:00 (t -5.25, -4.11), and positive at 14:00 (t 7.38) and 21:00–22:00 (t 3.80, 5.96).
