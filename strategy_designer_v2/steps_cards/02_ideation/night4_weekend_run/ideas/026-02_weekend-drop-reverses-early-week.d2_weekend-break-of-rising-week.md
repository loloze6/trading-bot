---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over the weekend after rising over the previous five days, it keeps falling over Monday and Tuesday. The fall is larger the larger the preceding five-day rise was.
Consequence: A trader should treat a weekend drop that interrupts a rising week as the start of a pullback, not as a dip to buy.
Why:
- F1: The idea's effect points the wrong way, so the book cannot pay. After a weekend fall, the coin's unusual 48-hour move over Monday and Tuesday is -0.59 % (t -2.37, 911 cases), not a rise. Per case the total move is -0.22 % against a trade cost of 0.19 %. The book's mean daily return is -4.1e-05, against a required 0.0005.
- F4: Weekend falls continue most when they break a rising week. When the five days before the weekend had risen, the weekend fall is followed by -0.96 % unusual (t -2.74, 445 cases). When those five days had fallen, it is followed by -0.15 % (t -0.42, 418 cases).
