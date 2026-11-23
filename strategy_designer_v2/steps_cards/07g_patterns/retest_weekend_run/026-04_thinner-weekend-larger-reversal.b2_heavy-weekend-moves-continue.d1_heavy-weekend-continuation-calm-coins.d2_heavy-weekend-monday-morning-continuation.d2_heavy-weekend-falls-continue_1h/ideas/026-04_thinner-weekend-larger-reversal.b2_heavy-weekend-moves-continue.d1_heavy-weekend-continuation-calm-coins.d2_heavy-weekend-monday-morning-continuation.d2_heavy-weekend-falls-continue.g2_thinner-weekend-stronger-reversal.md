---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday return is partly reversed over the next 12 hours. The reversal is the larger the larger the weekend move and the lighter the weekend's volume against its mean over the preceding five weekdays.
Consequence: Lean against weekend moves made on thin volume on Monday morning, and lean harder the thinner the weekend was.
Why:
- F3: At Sunday 23:00, volume flips the sign of the follow-through. The least-squares slope of the next 12 hours' excess return on the weekend's 48-hour return is +0.177 when weekend volume is heavier than the weekdays' (t +3.84, 436 cases, continuation). It is -0.123 when lighter (t -3.21, 1889 cases, reversal), and -0.145 over 24 hours (t -2.56).
- F4: Within light-volume weekends, the reversal grows as the weekend gets thinner against the weekdays. The slope is -0.30 in the lightest volume tercile (t -3.89, 630 cases), -0.14 in the middle tercile (t -1.89) and -0.05 in the least-light tercile (t -0.94).
- F5: Light-volume reversal is not specific to weekends, and it is not stable across years. On Tuesday-to-Thursday 23:00 closes with light volume the same slope is -0.080 (t -3.24, 2928 cases). The Sunday light-volume slope ranges from -0.42 in 2021 (t -3.78) and -0.32 in 2019 (t -3.70) to +0.19 in 2022 (t +1.90) and +0.18 in 2023 (t +1.56).
