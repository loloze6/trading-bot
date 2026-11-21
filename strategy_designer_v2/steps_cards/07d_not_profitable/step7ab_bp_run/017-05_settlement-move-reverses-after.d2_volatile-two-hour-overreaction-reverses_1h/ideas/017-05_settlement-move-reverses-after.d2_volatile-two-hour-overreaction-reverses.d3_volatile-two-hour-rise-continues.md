---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's large 2-hour rise, made while its 24-hour volatility is high, is followed by a further rise over the next 3 days. The larger the rise against the coin's usual 2-hour move, the larger the further rise.
Consequence: If confirmed, it is a reason never to short sharp rises in volatile markets, and possibly to follow them.
Why:
- F2: The loss comes from the shorts taken after rises. Trades with |entry forecast| above 2 earn +0.29 % to +0.80 % before fees when long. When short they lose -0.60 % to -1.16 % (34,781 trades with |forecast| above 10).
- F3: In high volatility (24-hour volatility at or above its 720-bar average), a 2-hour fall of at least 2 usual moves is followed by a large unusual rise. It is +60 bps over 8 hours (t 4.4, n 1,361), +172 bps over 24 hours (t 4.8, n 447) and +180 bps over 48 hours (t 3.0, n 218). The same-sized 2-hour rise is followed by only +21 bps of decline over 8 hours (t 1.9), +14 bps over 24 hours (t 0.5) and a 141 bps continuation over 72 hours (t -1.8).
