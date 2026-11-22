---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, and the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.
Consequence: A strong 4-hour up-run is a reason to join it for three days rather than to fade it.
Why:
- F1: The tested give-back is not in the data: after four up bars in a row with fading volume, the short's unusual move over 18 bars (3 days) is -0.43 % (t -1.75, 1073 cases) and its total move is -0.83 %. Shorting up-streaks loses before any cost, so the 0.19 % cost of a trade is not what sinks the book.
- F2: Fading volume makes no difference to up-runs. With rising volume the same short has an unusual move of -0.43 % (t -1.96, 1366 cases), which is the brief's own falsifying condition (no larger give-back with fading volume).
- F3: Up-streaks of any volume continue rather than reverse in all but the smallest quartile of scaled gain. Measured long over 3 days, the unusual move is +0.71 % (t 1.99), +0.86 % (t 2.32) and +0.77 % (t 1.66), 466 cases each, at scaled gains of 2.0, 3.0 and 5.4. Only the smallest quartile (scaled gain 1.1) shows a give-back, -0.55 % (t -1.71).
- F5: The loss is concentrated in bull years. Up-streak shorts with fading volume lost -1.23 % in 2020 (120 cases) and -2.12 % in 2021 (164 cases), and earned only in 2018 (+0.38 %), 2019 (+1.49 %) and 2022 (+0.85 %).
- F6: The book's daily return is -0.052 % against +0.119 % for holding the coins. Its 2274 short trades average -2.26 % gross and -2.36 % net, against +1.39 % gross for its 614 long trades.
- F7: The forecast is non-zero on only 2.6 % of bars, yet the book is positioned on 31 % of them, because of the 18-bar minimum hold. On the 2095 bars with a short forecast it gains +0.047 % per bar (allocation -0.55). On the 31099 bars it keeps holding afterwards it loses -0.028 % per bar (allocation -0.30). Any give-back lasts about one 4-hour bar, and the hold then rides the continuation.
