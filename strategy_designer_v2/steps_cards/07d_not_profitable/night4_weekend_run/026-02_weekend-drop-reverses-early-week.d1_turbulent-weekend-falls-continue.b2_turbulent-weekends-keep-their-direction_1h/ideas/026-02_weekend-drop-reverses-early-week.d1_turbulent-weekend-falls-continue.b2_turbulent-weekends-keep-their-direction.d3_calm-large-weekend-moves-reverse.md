---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's weekend (Saturday 00:00 to Monday 00:00 UTC) return is large relative to its previous week's hourly volatility while its weekend hourly moves were no more volatile than that week's, the coin moves against its weekend return over the next 2 days, more so the larger the weekend return relative to the previous week's volatility.
Consequence: A trader should refuse to follow, and may fade, a large weekend move made on calm hourly trading.
Why:
- F3: The forecast is driven by the size of the weekend return more than by the volatility ratio (Spearman 0.92 with the weekend return scaled by the prior week's volatility, 0.56 with the ratio), so it places large positions where the idea fails: weekends with a large scaled return and a low or middle volatility ratio carry mean allocations of 0.41 and 0.50 and lose −0.45 % (t −0.73, 103 cases) and −0.76 % (t −1.65, 221 cases) per case.
- F4: By the size of the weekend return alone, the largest fifth has an unusual move of −0.47 % (t −1.07) while the second and third fifths show +0.65 % (t 2.07) and +0.56 % (t 1.87), so the cases the forecast sizes largest are, on average, the ones that turn against the book.
