---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days, only while its hourly moves over the last 24 hours are larger than its hourly moves over the last 30 days.
Consequence: A grinding daily decline in an agitated market is a long for the next two days, while the same grind in a calm market is no reason to buy.
Why:
- F2: The effect is clear only when the coin is more agitated than usual. Among net 24-hour falls, the slope of the 48-hour excess return on the raw evenness of the losses has t 3.50 when 24-hour hourly volatility is above its 30-day level (1,220 cases, slope 0.073). It has t -0.85 when calmer (2,881 cases, slope -0.014).
- F1: The tested slope is on the side the idea predicts but well short of the bar. Its t is 0.91 on 8,579 grid cases, of which 4,191 have a positive forecast, and grind minus jump is +0.29 %. The effect is small: the unusual move is +0.08 % per case, a strength of 0.011 against the usual ~0.05 (findings F10). That is 0.4 times the 0.19 % round trip, a size that has never paid (findings F11).
- F4: The effect is not graded at the top. Over the positive-forecast quintiles the mean 48-hour excess return rises from -0.24 % through +0.06 %, +0.26 % and +0.33 %, then falls to -0.12 % in the most even quintile (about 854 cases each).
