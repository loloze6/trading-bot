---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, except when the coin stands far below its 90-day high after rising over its last 7 days: there, the deeper it stands below that high and the larger its 7-day rise, the higher its return over the next 10 days.
Consequence: A trader would stop leaning short a coin that is deep under its three-month high and has begun to climb over the past week, and would lean long instead, more so the deeper and the stronger the climb.
Why:
- F3: Two of the book's deepest falls came while the coins rose.
- F4: Shorts taken deep below the 90-day high lose. The deepest quartile (mean −54 % below the high) earns −4.3 bps a day (t −1.48). The quartile at −23 % earns +3.2 bps.
- F5: Shorts taken after a rise over the last week lose. The quartile with the highest 7-day return (mean +11.8 %) earns −4.0 bps a day (t −2.07, 2,039 bars). The quartile at −4.5 % earns +3.1 bps.
