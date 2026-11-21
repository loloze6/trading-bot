---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g1_late-evening-rise-after-daily-fall_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 2 hours from the 21:00 UTC bar, a coin's return is positive, and the stronger its 24-hour rise, the larger that rise.
Consequence: A trader would hold the late-evening long only after a daily run-up, sized by its strength, and refuse it after a daily drop, where the rise is absent.
Why:
- F2: The book opens and closes a position every evening (fees summed 4.06 on the 21:00 bar, 1.04 on the 22:00 bar and 4.09 on the 23:00 bar), and the position earns a mean of only +0.000249 per bar on the 21:00 bar and loses -0.000429 per bar on the 22:00 bar (about 7,600 to 7,900 active bars each), so the second hour gives back more than the first gains.
- F4: At 21:00 the 2-hour return rises with the 24-hour return instead of with the 24-hour fall: by 24-hour-return quintile it runs from +0.000060 (t 0.18) in the deepest-fall quintile to +0.001240 (t 4.12) in the strongest-rise quintile, and the 72-hour return sorts it the same way (top quintile +0.001200, t 4.09). The book was long in exactly the cases that do not rise.
- F5: The fall-side long of the tested idea flips sign by year: after a 24-hour fall the 21:00 2-hour return was +0.002198 (t 3.54) in 2018 but -0.001353, -0.001312 and -0.001747 (t -2.42, -2.25, -3.73) in 2020 to 2022, while after a 24-hour rise it was positive in 2020 to 2024 (t 2.26 to 3.35).
