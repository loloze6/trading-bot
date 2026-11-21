---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 20-day return, measured as a plain percentage change, the higher its return over the next 5 days.
Consequence: A trader should weigh the coin's raw 20-day rise, not its rise rescaled by recent history, when deciding how strongly to be long over the coming days.
Why:
- F3: The unscaled 20-day return predicts the next 5 days better than the components the book uses. Its slope t is 2.69 (2843 non-overlapping cases), against 2.31 for the standardised nearness to the 90-day high, 1.40 for the 20-day return standardised over 60 days, and 1.90 for the combined forecast (3419 cases).
- F4: The cost of trading is not what fails. Per case the total move is +0.47 % against a 0.19 % round trip, 2.5 times the cost. Fees were 0.0038 % of the book per bar against a gain before costs of 0.024 % per bar.
- F6: Most of the forecast's spread sits at its top. Across forecast quintiles the 5-day excess return goes from -0.35 % and -0.37 % in the two lowest quintiles to +0.27 % and +0.61 % in the two highest, so the long end carries the larger move.
