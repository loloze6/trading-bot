---
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4400 USD
---
## Findings
- **F1:** The book loses because its shorts lose. Over all coins, the position's gain before costs is +1.144 bp per bar on the 176,304 long bars and −0.269 bp per bar on the 240,326 short bars. Rebuilt with costs, a short-only book has a Sharpe of −0.359, a yearly return of −34.1 % and a deepest fall of −98.6 %. A long-only book has a Sharpe of 0.894, a yearly return of +34.5 % and a deepest fall of −69.1 %, against holding's Sharpe of 0.673, yearly return of +22.8 % and Calmar of 0.289. The full book has a Sharpe of 0.276, a yearly return of −5.7 % and a deepest fall of −92.9 %.
- **F2:** The reversal is almost all on the long side. On 24-hour grid cases, the 24-hour return in the fade's direction is +0.303 % after an hourly drop (t 5.60, 8,622 cases) and only +0.048 % after an hourly rise (t 0.88, 8,480 cases). The cost of a trade is 0.19 %, so the long side's move covers it and the short side's does not.
- **F3:** The book's deepest falls come while the coin rallies hard. The 15 deepest per-coin window falls of the book run from −80 % to −94 %, while the coin gained +75 % to +731 % over the same days. Across windows, the depth of the fall and the coin's return in it have a correlation of −0.51. In windows such as w10 (book −64 %, coin +52 %), w23 (book −37 %, coin +34 %) and w6 (book −30 %, coin +29 %), the book is fading rises inside a strong run up.
- **F4:** The fade of a drop is strongest when the coin's 7-day return is up. After an hourly drop with the 7-day return positive, the 24-hour raw return is +0.403 % (t 5.33, 3,859 cases). After a drop with the 7-day return negative, it is +0.149 % (t 1.76, 4,120 cases). The 7-day uptrend without the signal (after an hourly rise) gives only +0.043 % (t 0.56, 4,160 cases), so the uptrend is not an effect of its own. In the brief's theory, a drop inside an uptrend is crowded longs leaning out before settlement, a flow that reverses.
- **F5:** High volatility is mostly an effect of its own, so it is no repair. After a drop in the top third of 24-hour volatility, the 24-hour raw return is +0.710 % (t 5.86). On all high-volatility cases it is already +0.403 % (t 4.95, 5,157 cases), and a long-only book restricted to high volatility does worse than long-only (Sharpe 0.456 vs 0.894).
- **F6:** The shock's information lies more in its 24-hour size than in one hour. Faded by the sign of the 24-hour return, the drift-removed 24-hour move is +0.425 % (t 5.33, 5,702 cases) in the top third of |24-hour return|, against −0.046 % and −0.033 % in the bottom and middle thirds. The 1-hour shock bands are uneven: +0.428 % (t 4.64) at 1.0 to 1.5 usual moves, −0.004 % at 1.5 to 2.0, and −0.078 % beyond 3.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily.d1_moderate-hourly-drops-rebound-daily` (from F1, F2, F3): Among hourly drops of up to a few times a coin's 24-hour volatility, the larger its last 1-hour fall relative to that volatility, the more the coin rises over the next 24 hours.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily.d2_hourly-dips-in-uptrends-rebound` (from F2, F3, F4): Among hourly drops of up to a few times a coin's 24-hour volatility, the larger its last 1-hour fall relative to that volatility, the more the coin rises over the next 24 hours, only while its 7-day return is positive.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily.d3_daily-move-reverses-next-day` (from F6, F2): The larger a coin's 24-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
