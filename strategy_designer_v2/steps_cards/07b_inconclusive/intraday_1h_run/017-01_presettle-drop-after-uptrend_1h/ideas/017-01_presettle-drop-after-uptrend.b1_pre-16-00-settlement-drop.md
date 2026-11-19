---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run up, the return over the 2 hours before the 16:00 UTC funding settlement is negative, and the stronger the 3-day rise, the larger that pre-settlement decline.
Consequence: Before the 16:00 UTC settlement only, a trader would lean short in proportion to the coin's 3-day rise and refuse longs into that settlement, expecting a give-back in the following hours.
Why:
- F1: The pooled result is near zero because the three settlements point opposite ways: after a 3-day rise, the excess 2-hour return before the 16:00 UTC settlement is -7.5 bp (t -4.27, n 8,592), before 00:00 it is +6.6 bp (t +4.38, n 8,552) and before 08:00 it is +1.5 bp (t +1.11, n 8,569), which nets to the plan's main measure of 9.5e-05 (t 0.85, 26,436 episodes).
- F2: Only before the 16:00 settlement is the effect graded the way the idea predicts: the slope of the 2-hour return on the 72-bar return has t -5.69 (rho -0.031, n 16,985), it is negative in all six coins (t from -0.70 to -4.05), and it is negative in 6 of 8 years (positive only in 2020 at t +3.30 and 2023 at t +1.89).
- F3: Across the three settlements pooled the effect is not graded: the top decile of the 3-day rise gains +4.7 bp before settlement against -0.3 bp in the ninth decile, the plan's top-third-minus-bottom-third check is +2.7 bp (failed), and no coin's mean after a rise reaches |t| 1.4 (range -3.6 to +3.5 bp).
- F4: Before the 16:00 settlement the move reverses afterward: after a 3-day rise the next 2 hours return +8.9 bp, against -3.9 bp after the 08:00 settlement and +3.4 bp after 00:00.
