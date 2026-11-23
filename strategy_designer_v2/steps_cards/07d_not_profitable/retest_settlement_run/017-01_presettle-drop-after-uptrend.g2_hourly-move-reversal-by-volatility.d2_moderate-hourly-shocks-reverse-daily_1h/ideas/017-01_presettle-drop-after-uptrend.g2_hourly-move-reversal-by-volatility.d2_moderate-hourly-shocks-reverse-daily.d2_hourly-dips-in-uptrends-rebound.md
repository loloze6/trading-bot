---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Among hourly drops of up to a few times a coin's 24-hour volatility, the larger its last 1-hour fall relative to that volatility, the more the coin rises over the next 24 hours, only while its 7-day return is positive.
Consequence: A trader would buy moderate hourly dips inside a 7-day uptrend for a day, larger as the dip is larger, and would stay out of the fade when the week is down.
Why:
- F2: The reversal is almost all on the long side. On 24-hour grid cases, the 24-hour return in the fade's direction is +0.303 % after an hourly drop (t 5.60, 8,622 cases) and only +0.048 % after an hourly rise (t 0.88, 8,480 cases). The cost of a trade is 0.19 %, so the long side's move covers it and the short side's does not.
- F3: The book's deepest falls come while the coin rallies hard. The 15 deepest per-coin window falls of the book run from −80 % to −94 %, while the coin gained +75 % to +731 % over the same days. Across windows, the depth of the fall and the coin's return in it have a correlation of −0.51. In windows such as w10 (book −64 %, coin +52 %), w23 (book −37 %, coin +34 %) and w6 (book −30 %, coin +29 %), the book is fading rises inside a strong run up.
- F4: The fade of a drop is strongest when the coin's 7-day return is up. After an hourly drop with the 7-day return positive, the 24-hour raw return is +0.403 % (t 5.33, 3,859 cases). After a drop with the 7-day return negative, it is +0.149 % (t 1.76, 4,120 cases). The 7-day uptrend without the signal (after an hourly rise) gives only +0.043 % (t 0.56, 4,160 cases), so the uptrend is not an effect of its own. In the brief's theory, a drop inside an uptrend is crowded longs leaning out before settlement, a flow that reverses.
