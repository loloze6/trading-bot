---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of the coin's preceding two days while its 30-day return is positive, the coin rises over the next three days, the more so the deeper its 1-day fall relative to its 30-day volatility of four-hour returns.
Consequence: A breakdown in a rising month that comes with a steep one-day drop is a reason to buy the rebound and to refuse the breakdown short.
Why:
- F5: Within the tested idea's own situation, the cases against it are the larger ones. A close below the 12-bar low while the 180-bar return is positive is followed by a three-day rise when the preceding stretch was wide: the widest tercile shows -1.74 % short-signed (t -3.89, 385 cases). The narrowest tercile, the one the idea backs, shows only +0.80 % (t 1.35, 220 cases).
- F6: That counter-move inside the tested situation is the F1 rebound. Among wide-stretch down-breaks in a rising month, those with a deep 1-day fall rise +2.23 % unusual (t 4.20, 302 cases, strength 0.25). Those with a mild fall show +0.01 % (t 0.01, 81 cases).
- F2: The rebound is concentrated in a rising month. With a positive 180-bar return, the lowest quintile of the scaled 1-day return gains +1.89 % unusual over three days (t 4.04, 401 cases, strength 0.22). With a negative 180-bar return, the same quintile gains only +0.41 % (t 1.10, 457 cases).
- F7: The rebound is large enough to pay for a trade. Its three-day unusual move in a rising month, +1.89 %, is about 10 times the 0.19 % round-trip cost of this backtest. The tested short's total move of +0.14 % per case was 0.7 times that cost. Its book lost money on five of six coins' trades (mean net trade from -1.3 % on BTC to -8.6 % on ZEC; +0.04 % on XRP).
