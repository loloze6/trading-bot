---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 5 days.
Consequence: A trader should take a long after a close beyond the 90-day high, larger the further beyond, and refuse a short against such a breakout.
Why:
- F1: The test's result is on the side the idea predicts but far short of the bar: on 175 non-overlapping 5-day breakout cases, the slope of the drift-removed return on the forecast is positive with a t of 0.37, and the mean drift-removed return is +0.81 % (t 0.81). The median is −0.64 % and only 47 % of cases are positive, so a few large rises carry the mean.
- F3: The effect is mixed across coins. The 5-day mean is +10.2 % on XRP (13 cases), +2.2 % on ETH (41) and +1.1 % on BTC (43), against −3.8 % on LTC (27), −0.9 % on XMR (26) and −0.1 % on ZEC (25). Within each coin, the correlation of the forecast with the move runs from −0.25 to +0.28.
- F7: Cost is not what limits this idea. The unusual move is +3.17 % per case (strength 0.266, 260 cases), 16.4 times the 0.19 % cost of a round trip. The book's Sharpe of 0.82 beats holding by 0.26, but its mean daily return of 0.016 % and Calmar of 0.64 fail the bar because breakouts are rare (0.025 trades per day).
