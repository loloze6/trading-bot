---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the larger its 28-day return measured against its 30-day volatility, the higher its return over the next 7 days.
Consequence: A strong 4-week rise that is large for the coin's own volatility is a reason to expect another week of gains, and a large fall a reason to expect further losses.
Why:
- F5: The 28-day return scaled by 30-day volatility predicts the next 7 days. Its slope is +0.25 (t 3.12, 1779 cases), positive in 6 of 6 coins, with t 3.40 in w13–w24 against 0.58 in w1–w12.
- F3: This continuation is carried mostly by the later windows, so it may not be stable.
- F4: The continuation fades as the past period and the horizon lengthen.
- F1: The tested idea is real but far too small to pay for a trade. Its unusual move is +0.12 % per case over 5 days, a strength of 0.004, about a tenth of the usual 0.05 (findings F10). Its total move is +0.07 %, which is 0.4 times the 0.19 % cost of a round trip. The book earns 0.044 % a day against the 0.05 % required, with a Calmar of 0.26.
