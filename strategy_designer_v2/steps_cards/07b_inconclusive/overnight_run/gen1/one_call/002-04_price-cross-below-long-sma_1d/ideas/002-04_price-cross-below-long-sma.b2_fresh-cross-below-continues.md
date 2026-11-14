---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first days after a coin's close crosses below its 200-day average, the coin keeps falling over the next 10 days by more than its usual drift.
Consequence: A trader would short only fresh crosses below the long average rather than holding a short for the whole time the price stays below it.
Why:
- F6: Timing since the cross matters but is not steady: the first 10 bars below the average give +1.7% (t 1.34, n 155), bars 10–30 give −1.95% (t −1.94, n 224), and bars 60–120 give +1.7% (t 1.81, n 210).
- F2: The sign of the result flips by year: shorts gained in 2018 (+3.9%, t 2.32, n 134) and 2022 (+2.3%, t 2.48, n 195), but lost in 2020 (−4.3%, t −2.73, n 88) and 2021 (−5.1%, t −2.32, n 74), and these cancel in the pooled mean.
- F3: The windows split the same way, from w9 (+4.0%, t 3.71) and w7 (+5.8%, t 3.35) to w23 (−6.7%, t −3.12) and w21 (−3.6%, t −2.75), while no coin stands out (coin means range from −0.39% to +0.56%, all |t| < 0.6).
