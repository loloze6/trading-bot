---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days, and the continuation is larger the higher the weekend's volatility compared with the previous week, whatever the size of the weekend return itself.
Consequence: A trader following turbulent weekends should scale the bet by how much more turbulent the weekend was than the week before, not by how far the price moved over the weekend.
Why:
- F2: The effect sits only in the most turbulent weekends: in the top fifth of the weekend-to-prior-week volatility ratio the unusual move is +1.38 % per case (t 3.14, 446 cases, strength 0.197, book +0.92 % per case), while the bottom two fifths show −0.19 % and −0.35 % (t −0.66, −1.05) and the middle fifths +0.10 % and +0.32 %.
- F3: The forecast is driven by the size of the weekend return more than by the volatility ratio (Spearman 0.92 with the weekend return scaled by the prior week's volatility, 0.56 with the ratio), so it places large positions where the idea fails: weekends with a large scaled return and a low or middle volatility ratio carry mean allocations of 0.41 and 0.50 and lose −0.45 % (t −0.73, 103 cases) and −0.76 % (t −1.65, 221 cases) per case.
- F4: By the size of the weekend return alone, the largest fifth has an unusual move of −0.47 % (t −1.07) while the second and third fifths show +0.65 % (t 2.07) and +0.56 % (t 1.87), so the cases the forecast sizes largest are, on average, the ones that turn against the book.
- F5: The worst tenth of cases loses −3.99 % of the book per case at a mean allocation of 0.64, and the best tenth gains +6.23 % at 0.69, with nearly the same volatility ratio (1.08 against 1.12) and scaled weekend return (1.13 against 1.17), so the falls come from heavily sized large-move weekends whose outcome the forecast cannot separate.
