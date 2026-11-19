---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise, the more the coin keeps rising over the next 3 days.
Consequence: A trader would size longs after 3-day rises by the rise's size, not by how evenly it was built.
Why:
- F2: Measured raw, without the standardisation, a more even rise does carry a little more continuation, but only because even rises are bigger. Across residual-share quintiles of all 2,865 three-day rises, the 72-hour excess return goes −0.0055, 0.0000, −0.0006, +0.0040, +0.0110 while the mean rise size goes 0.009, 0.028, 0.051, 0.076, 0.119. The residual's t of 1.12 falls to 0.55 once rise size is controlled.
- F3: The size of the 3-day rise, not its shape, carries the continuation. Rise size predicts the next 72-hour excess return with t 2.98 (n 2,865). Bars inside a rise beat bars outside it by 0.0087 against −0.0017 (Welch t 3.32). Inside the active bars, the forecast adds nothing once the past return is controlled (t −0.55).
