---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.e profitable but not proven
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the share of a coin's hourly bars over the past 3 days that closed higher, the more the coin rises over the next 3 days.
Consequence: A trader would lean long a coin in proportion to how many of its last 3 days' hours stepped up, rather than by how little its biggest hours contributed.
Why:
- F5: A different grind measure does carry the effect over all moves. Using the share of the past 72 hours that closed up, the next-72h excess return by quintile is -0.0025, -0.0037, -0.0026, +0.0002 and +0.0088. The top quintile's t is 2.80 (n=849 non-overlapping cases), so continuation shows where many hours step up.
- F4: The tested grind measure adds little beyond the rise itself at any horizon. On rising grid bars the forecast's t is 0.20 at 24h (n=8,529), 1.52 at 72h (n=2,865) and 0.83 at 168h (n=1,156). The forecast is zero on about 67% of rising cases.
