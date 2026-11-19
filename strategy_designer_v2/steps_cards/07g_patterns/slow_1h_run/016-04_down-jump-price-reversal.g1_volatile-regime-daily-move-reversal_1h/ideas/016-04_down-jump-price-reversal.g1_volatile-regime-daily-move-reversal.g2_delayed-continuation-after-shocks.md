---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return, measured in units of its past 7-day hourly volatility, the more the coin keeps moving in the same direction over the three days that start one day after the move.
Consequence: Do not hold a fade of a sharp daily move past its first day; from the second day on, lean with the move instead.
Why:
- F4: After the first day, large moves continue rather than reverse. Over hours 24 to 96 after the bar, the top fifth of scaled 24-hour moves gains a further 0.0046 excess (t 3.77, n 3,254). The 24-hour forecast's edge fades to t 0.06 at 72 hours and t -1.27 at 168 hours.
