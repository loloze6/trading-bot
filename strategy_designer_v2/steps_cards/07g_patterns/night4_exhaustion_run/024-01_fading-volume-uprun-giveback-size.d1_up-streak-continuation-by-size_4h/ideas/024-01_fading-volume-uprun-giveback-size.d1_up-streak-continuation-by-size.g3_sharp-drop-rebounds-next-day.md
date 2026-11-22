---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's single 4-hour fall measured in its usual 4-hour moves over the past 30 days, the larger its rebound over the next day.
Consequence: A sharp single-bar drop is a reason to take a one-day long rather than to sell into it.
Why:
- F4: The larger a single 4h fall in usual moves, the larger the next day's excess return. The slope over falls has t -3.64. After falls of 3 or more usual moves, the next 4h bar's excess is +0.096 standard deviations (t 2.60, n 2406). Falls of 2 or more usual moves rebound in 4 of 6 coins, but 2020 shows -0.309 against +0.423 in 2018, so the effect varies by year.
