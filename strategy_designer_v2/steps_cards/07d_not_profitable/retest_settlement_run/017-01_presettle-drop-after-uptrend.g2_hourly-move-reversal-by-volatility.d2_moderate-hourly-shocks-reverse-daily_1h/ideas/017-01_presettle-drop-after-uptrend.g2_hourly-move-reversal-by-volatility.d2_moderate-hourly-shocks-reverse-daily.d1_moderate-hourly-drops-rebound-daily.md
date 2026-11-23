---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Among hourly drops of up to a few times a coin's 24-hour volatility, the larger its last 1-hour fall relative to that volatility, the more the coin rises over the next 24 hours.
Consequence: A trader would buy moderate hourly drops for a day, more as the drop is larger, and would not short hourly rises, which do not reverse enough to pay.
Why:
- F1: The book loses because its shorts lose. Over all coins, the position's gain before costs is +1.144 bp per bar on the 176,304 long bars and −0.269 bp per bar on the 240,326 short bars. Rebuilt with costs, a short-only book has a Sharpe of −0.359, a yearly return of −34.1 % and a deepest fall of −98.6 %. A long-only book has a Sharpe of 0.894, a yearly return of +34.5 % and a deepest fall of −69.1 %, against holding's Sharpe of 0.673, yearly return of +22.8 % and Calmar of 0.289. The full book has a Sharpe of 0.276, a yearly return of −5.7 % and a deepest fall of −92.9 %.
- F2: The reversal is almost all on the long side. On 24-hour grid cases, the 24-hour return in the fade's direction is +0.303 % after an hourly drop (t 5.60, 8,622 cases) and only +0.048 % after an hourly rise (t 0.88, 8,480 cases). The cost of a trade is 0.19 %, so the long side's move covers it and the short side's does not.
- F3: The book's deepest falls come while the coin rallies hard. The 15 deepest per-coin window falls of the book run from −80 % to −94 %, while the coin gained +75 % to +731 % over the same days. Across windows, the depth of the fall and the coin's return in it have a correlation of −0.51. In windows such as w10 (book −64 %, coin +52 %), w23 (book −37 %, coin +34 %) and w6 (book −30 %, coin +29 %), the book is fading rises inside a strong run up.
