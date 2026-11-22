---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over the weekend (Saturday 00:00 to Monday 00:00 UTC), it keeps falling over Monday and Tuesday. The fall is larger the more volatile the weekend's hours were compared with the coin's previous week.
Consequence: A trader should refuse to buy weekend dips that came on turbulent weekend trading, and may lean short over the next two days instead.
Why:
- F1: The idea's effect points the wrong way, so the book cannot pay. After a weekend fall, the coin's unusual 48-hour move over Monday and Tuesday is -0.59 % (t -2.37, 911 cases), not a rise. Per case the total move is -0.22 % against a trade cost of 0.19 %. The book's mean daily return is -4.1e-05, against a required 0.0005.
- F3: Weekend falls continue most when the weekend was turbulent. When the weekend's hourly volatility was in the top third relative to the prior week's, the fall is followed by -1.34 % unusual over Monday and Tuesday (t -2.96, 277 cases). In the lowest third it is followed by -0.30 % (t -0.85, 297 cases).
- F2: The shallow weekend falls carry the continuation, and the grading runs against the idea. Weekend falls under a quarter of the coin's usual 2-day move are followed by -1.12 % unusual over Monday and Tuesday (t -3.35, 364 cases). The second quintile of the weekend move (mean -1.3 %) is followed by -1.18 % (t -3.47, 405 cases). Only falls deeper than 1.5 usual moves are followed by a rise, +1.65 % (t 1.14, 52 cases), which is not reliable.
