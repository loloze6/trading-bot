---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is positive, the price rises over the next 5 days by more than the coin's usual 5-day return, and the larger the coin's 30-day return at that hour, the larger the rise.
Consequence: A trader would act on hourly upside surges only in proportion to the month's prior rise, and refuse surges that come after a month-long decline.
Why:
- F1: The 5-day move rises step by step with the coin's own 30-day return at an hourly close. On non-overlapping 120-hour cells, the top fifth of 30-day returns is followed by an unusual move of +1.26 % (t 2.95, 1076 cases, strength 0.107) and the fourth fifth by +0.52 % (t 1.29). The three lower fifths are followed by −0.55 %, −0.99 % and −0.67 % (t −1.57, −3.28, −2.14). The t's pool 19 coins over shared dates, so they overstate independence.
- F2: The book earns almost only while the coin's 30-day return is high. Its hourly position gain is 1.59 and 1.55 bps in the top two fifths of 30-day return, against 0.15, −0.74 and 0.25 bps in the three lower fifths (about 107,500 position-hours each).
- F4: Near the 30-day high, an upside 24-hour return adds to the move:
- F5: The size of the 24-hour surge, on its own, does not grade the 5-day move. By surge decile the unusual move runs +0.35 %, +0.70 %, −0.03 %, −1.11 %, −1.35 %, −0.15 %, +0.22 %, +0.23 %, −0.33 % and +1.43 % (top decile t 1.90). It is not monotone, which matches the tested idea's t of 1.85.
