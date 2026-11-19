---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has risen over its past 24 hours relative to its own volatility, as read at the 15:00 UTC close, the more it keeps rising over the two hours to 17:00 UTC.
Consequence: A strong 24-hour move into the 15:00 UTC close is a reason to trade in its direction for the next two hours.
Why:
- F4: Whether the 24-hour move reverses or continues over the next 2 hours depends on the hour, with |t| above 6 even after scanning 24 hours. After the 13:00 UTC close (bar stamped 12:00) and the 20:00 close (stamped 19:00), the slope on the 24-hour volatility-scaled return is −9.24 bp (t −6.88) and −7.87 bp (t −6.50), so the move reverses. After the 15:00 close (stamped 14:00) and the 23:00 close (stamped 22:00), it is +8.89 bp (t 6.44) and +8.23 bp (t 6.42), so the move continues.
