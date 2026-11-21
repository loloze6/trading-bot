---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose price fell over the past 3 days keeps falling over the next 3 days, and the less of its hourly movement over those 3 days went into the net fall (the choppier the fall), the larger the further fall.
Consequence: A trader would refuse longs after a choppy 3-day fall and could go short it, a fall of about 76 bps over 3 days against a 19 bps round trip.
Why:
- F7: Choppy falls keep falling. A 3-day fall in the least efficient third is followed by a 3-day unusual move of -76 bps (t -2.79, 899 cases). A fall in the most efficient third is followed by -11 bps (t -0.36).
- F9: Neither the direction nor the efficiency alone ranks what follows. The Spearman correlation with the next 3-day unusual move is -0.009 for the signed 3-day return and -0.001 for the signed efficiency (5,539 cases). The effect lives in rises that are efficient (F5) and falls that are choppy (F7), not along one signed scale.
