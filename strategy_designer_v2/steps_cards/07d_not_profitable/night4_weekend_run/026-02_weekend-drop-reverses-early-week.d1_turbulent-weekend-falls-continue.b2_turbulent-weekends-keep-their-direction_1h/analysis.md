---
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3737 USD
---
## Findings
- **F1:** The book failed on its mean daily return, 0.028 % against the 0.05 % required, and on its Calmar, 0.445 against 0.75, with a deepest fall of 21.9 %; it earns only on Mondays (+0.135 % a day) and Tuesdays (+0.075 %) and is flat on the other five days (−0.015 % to +0.011 %), so its yearly return is spread thin while its falls come from a few large Monday bets.
- **F2:** The effect sits only in the most turbulent weekends: in the top fifth of the weekend-to-prior-week volatility ratio the unusual move is +1.38 % per case (t 3.14, 446 cases, strength 0.197, book +0.92 % per case), while the bottom two fifths show −0.19 % and −0.35 % (t −0.66, −1.05) and the middle fifths +0.10 % and +0.32 %.
- **F3:** The forecast is driven by the size of the weekend return more than by the volatility ratio (Spearman 0.92 with the weekend return scaled by the prior week's volatility, 0.56 with the ratio), so it places large positions where the idea fails: weekends with a large scaled return and a low or middle volatility ratio carry mean allocations of 0.41 and 0.50 and lose −0.45 % (t −0.73, 103 cases) and −0.76 % (t −1.65, 221 cases) per case.
- **F4:** By the size of the weekend return alone, the largest fifth has an unusual move of −0.47 % (t −1.07) while the second and third fifths show +0.65 % (t 2.07) and +0.56 % (t 1.87), so the cases the forecast sizes largest are, on average, the ones that turn against the book.
- **F5:** The worst tenth of cases loses −3.99 % of the book per case at a mean allocation of 0.64, and the best tenth gains +6.23 % at 0.69, with nearly the same volatility ratio (1.08 against 1.12) and scaled weekend return (1.13 against 1.17), so the falls come from heavily sized large-move weekends whose outcome the forecast cannot separate.
- **F6:** The continuation comes from falling weekends: cases following a falling weekend have an unusual move of +0.55 % (t 2.32, 1023 cases), and cases following a rising weekend have −0.002 % (t −0.01, 1205 cases).
- **F7:** The move is spread over both days, +0.16 % on day 1 (t 1.36) and +0.11 % on day 2 (t 1.13), and nothing follows on days 3 to 4 (−0.03 %, t −0.20), so holding longer would not add gain.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.d1_volatility-ratio-drives-continuation` (from F2, F3, F4, F5): When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days, and the continuation is larger the higher the weekend's volatility compared with the previous week, whatever the size of the weekend return itself.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.d2_turbulent-weekend-drops-continue` (from F2, F6, F7): When a coin's hourly moves over the weekend (Saturday 00:00 to Monday 00:00 UTC) were more volatile than over its previous week, the coin keeps moving in the direction of its weekend return over the next 2 days, only after a falling weekend, and the further fall is larger the higher the weekend's volatility compared with the previous week.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.d3_calm-large-weekend-moves-reverse` (from F3, F4): When a coin's weekend (Saturday 00:00 to Monday 00:00 UTC) return is large relative to its previous week's hourly volatility while its weekend hourly moves were no more volatile than that week's, the coin moves against its weekend return over the next 2 days, more so the larger the weekend return relative to the previous week's volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
