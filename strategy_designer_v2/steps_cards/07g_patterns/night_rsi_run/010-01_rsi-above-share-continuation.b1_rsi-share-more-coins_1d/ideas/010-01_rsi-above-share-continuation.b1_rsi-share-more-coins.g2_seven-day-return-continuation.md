---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's return over the past 7 days, the higher its return over the next 14 days.
Consequence: A trader would lean with the coin's last week's direction over the following two weeks, instead of with how long RSI has sat above its midpoint.
Why:
- F3: Over the next 14 days, the coin's past 7-day return carries forward, not reverses: pooled slope t 3.42 (1008 non-overlapping cases), 2.97 when the past return is scaled by volatility and 2.95 when winsorised; the top past-7-day quintile earns +4.1% excess against -4.6% in the bottom quintile.
- F4: That 7-day continuation is positive in 5 of 6 coins (ZEC t 2.41, ETH 1.85, BTC 1.64; LTC 0.00) but rests mostly on 2025 (t 5.14); 2018 to 2023 range from t -0.49 to 0.93, so it is weaker evidence than F1.
- F5: The tested RSI-share forecast predicts nothing: slope t -0.30 on the forecast and -0.73 on the raw share (1152 cases); its quintiles' 14-day excess returns run from -0.69% to +0.71% with no order; per coin it splits, from XRP t -2.85 to BTC t +1.15.
