---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 3 hours from 15:00 UTC follows the coin's 3-day move, and the stronger the 3-day rise relative to the coin's 3-day hourly volatility, the larger the rise over those 3 hours.
Consequence: A trader would hold one trend-direction position across the whole 15:00–18:00 UTC stretch, capturing the full afternoon continuation for a single round-trip cost.
Why:
- F1: The book loses because each 2-hour slot pays more in fees than it earns: the mean gross gain is 0.000504 per slot (t 8.08, 17452 slots), the mean fee is 0.001017 (about 0.00107 per unit of turnover, paid on both entry and exit), so the net is -0.000513 per slot and the book's mean daily return is -0.000605, while holding the coin returned 0.001190 a day.
- F2: The losses come from a full round trip every day. Almost all turnover sits on the 15:00-stamped bar (0.474 per bar) and the 17:00-stamped bar (0.479 per bar), against at most 0.0018 on every other hour. Fees exceed the gross gain in every coin, from ZEC (net -0.000122) to XMR (net -0.000878).
- F5: The trend continuation is confined to the late afternoon and stops at about 18:00 UTC. The 2-hour return signed by the 3-day trend is positive for the bars stamped 14:00, 15:00 and 16:00 (0.000479 t 3.64, 0.000687 t 5.72, 0.000368 t 3.28). It turns negative at 18:00 (-0.000284 t -2.47) and during the midday hours 11:00 and 12:00 (t -3.10 and -3.00). From the 16:00 slot, the signed move is 0.000697 over 4 hours and -0.000215 over 24 hours.
