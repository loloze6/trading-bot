---
brief: 010_rsi-midline-regime-direction
source-idea: 010-08_rsi-below-streak-reversal
line: 7.d not profitable
backtest: 010-08_rsi-below-streak-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days, only while the coin's close stands well below its highest close of the past 60 days, the effect growing with the distance below that high.
Consequence: A trader would buy long RSI-below-50 runs only after deep falls from the 60-day high, and would refuse them when the coin is near that high.
Why:
- F1: The book loses because its long bars come when the coin does worse than usual: the book's mean gain per bar is -0.000046, made of +0.000296 from the coin's own rise and -0.000345 from timing. On long bars the next-day return is 0.000004 for BTC against a coin mean of 0.001183, and -0.000491 for ETH against 0.001368.
- F2: The long bars pay only when the coin is deep below its 60-day high. Split into terciles of the 60-day drawdown (574 long bars each), the mean gain is +0.001435 in the deepest tercile (summed +0.82), -0.001085 in the middle (summed -0.62) and -0.000606 in the shallowest (summed -0.35).
- F3: On the 14-day grid (bars with a run below 50), the run-length slope holds only in deep drawdowns. Its t is 1.97 in the deeper half of 60-day drawdowns (n=56) against 0.24 in the shallower half (n=57). Run length times drawdown depth has t 1.96, against 1.79 for run length alone (n=113).
- F5: The book's losses follow the bear years, when holding was also negative. The book's mean daily return was -0.000407 in 2018 (holding -0.002958), -0.001228 in 2022 (holding -0.002347) and -0.000537 in 2025. It was positive in 2019–2021 and 2023–2024, while holding earned far more.
