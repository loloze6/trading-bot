---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 14 days, only while its volatility over the past 7 days is above its volatility over the past 60 days, the excess growing with how far that ratio stands above it, and the premium is concentrated in those 14 days after the panic.
Consequence: A trader would buy a panic only when the week's volatility already exceeds its two-month level, and hold for about two weeks rather than staying long through later declines.
Why:
- F1: The book's deepest fall is −76.5 % against a yearly return of 26.8 % (Calmar 0.34). The fall ran 277 days across windows w12 to w14, while the coins fell −79.0 % together. So the book fell almost exactly as much as the coins did.
- F2: The book is long on 98.7 % of bars on average (median 99.9 % per coin-window), with a mean allocation of 1.07. Its forecast is positive on only 48.9 % of bars, so on 50.2 % of bars it is long with a forecast of zero. Trades last a median of 78 days, against the 14-day horizon. In practice the book is the coin held with leverage, and its falls are the coin's falls.
- F3: On the 84-bar grid, the long bars that carry a forecast of zero (517 cells) have an unusual move of +0.01 %. These long-but-no-signal bars, which are half the book's exposure, add drift and drawdown but no timing.
- F4: The effect depends on the 7-day/60-day volatility ratio at the signal bar:
- F5: Forecast size separates the cases only slightly. Cases with a forecast of 7.2 to 20 (n 859) have +0.11 %, against −0.52 % for 2.0 to 7.2 (n 287). The cubed product of range multiple and volatility ratio lets ratios below 1 still give full-size signals.
