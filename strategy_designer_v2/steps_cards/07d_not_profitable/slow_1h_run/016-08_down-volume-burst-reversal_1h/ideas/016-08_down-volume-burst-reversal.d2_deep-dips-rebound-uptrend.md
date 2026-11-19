---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal
line: 7.d not profitable
backtest: 016-08_down-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its 3-day fall measured against its usual 3-day swing over the past 30 days, the more the coin rises over the next 3 days.
Consequence: A trader sizes dip-buys in a rising month by how unusually deep the dip is, so the position is large only where the rebound is large enough to pay fees.
Why:
- F1: The book lost on every coin and in every year (mean daily return -0.00075, coin Sharpes from -1.40 on BTC to -0.29 on XMR), while holding the same coins gained 0.0007 to 0.0016 a day. Its gross gain per bar is close to zero (-0.00002 to +0.00003). Fees take 0.00003 to 0.00004 per bar at about 0.96 trades a day, so the gross timing gain is too small to pay for the trading.
- F4: How deep the fall is matters more than how it was made. Inside falls, the deepest-fall quartile per coin had excess forward return +0.0053 (t 1.38, n=669), and the shallowest-fall quartile had -0.0087 (t -3.11, n=667). The book's held days follow the same order: +0.0009 a day in the deepest volatility-scaled fall quintile against -0.0015 and -0.0012 in the two shallowest.
- F6: In 30-day uptrends the rebound is graded by fall depth against the coin's usual 3-day swing. The two deepest quintiles gave +0.011 (t 1.76, n=126) and +0.011 (t 1.77, n=170), stepping down to -0.0063 (n=208) in the shallowest quintile. In 30-day downtrends every quintile was negative (from -0.0014 to -0.0091).
