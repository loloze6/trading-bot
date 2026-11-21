---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day return against its own 20-day volatility, the higher its return over the next 5 days, while its 20-day volatility is low or middling against its own past.
Consequence: In a calm market, a strong up day on a coin is a reason to be long for the next week, and a down day a reason to refuse a long.
Why:
- F1: On the non-overlapping 5-day grid, a coin's 1-day return predicts its next-5-day return beyond drift when the coin's 20-day volatility is in its lower two thirds, and reverses in its upper third. The slope of the standardised 5-day move on the standardised 1-day return is 0.075 (t 3.14, 1043 cases) in the calm third, 0.081 (t 2.75, 1044) in the middle third and -0.042 (t -1.17, 1044) in the high third. Scaling the 1-day return by the 20-day volatility gives the same result (t 3.10, 2.79, -0.84).
- F2: In the calm and middle volatility thirds the 1-day-return effect is concentrated in the largest up days and is large next to cost. The top fifth of 1-day returns is followed by +2.29 % over 5 days beyond drift (t 3.88, 420 cases), about 12 times the 0.19 % round trip. The second-lowest fifth is followed by -0.93 % (t -2.16).
- F3: The calm-and-middle 1-day continuation has a positive slope on all 6 coins (0.047 to 0.150; XRP t 3.38, XMR 1.69, ETH 1.45). It is positive in 6 of 8 years (2019 t 4.06, 2021 t 2.42, 2023 t 2.18) and negative in 2018 (t -2.24) and 2025 (t -0.79). It is not a one-coin artefact, but it is not stable in every year.
