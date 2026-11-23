---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: At the 08:00 UTC funding settlement, when a coin's 2-hour move into settlement ran against its 24-hour trend, the coin keeps moving against its 24-hour trend over the next 8 hours. The move is larger the stronger the 24-hour trend.
Consequence: A trader should refuse the trend-side snapback at the 08:00 UTC settlement, and expect the counter-trend move there to continue for the rest of the session.
Why:
- F4: The 08:00 UTC settlement (bar opening 07h) does not carry the effect, and it turns against the trade later. Counter-trend cases there give −0.012 % at 2h and −0.146 % at 8h (t −4.4, n 7405); among strong cases, +0.03 % at 2h and −0.26 % at 8h (t −2.9, n 1111).
