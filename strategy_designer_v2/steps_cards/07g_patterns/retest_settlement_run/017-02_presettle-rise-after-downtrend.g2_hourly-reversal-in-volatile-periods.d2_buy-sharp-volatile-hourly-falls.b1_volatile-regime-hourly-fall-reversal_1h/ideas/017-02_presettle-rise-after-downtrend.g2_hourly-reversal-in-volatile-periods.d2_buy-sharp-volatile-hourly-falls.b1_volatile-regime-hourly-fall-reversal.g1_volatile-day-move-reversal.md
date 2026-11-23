---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 24-hour volatility runs above its 30-day average, its return over the next 24 hours runs against its own 24-hour return. The larger that past 24-hour return in units of the coin's usual daily move, the larger the opposite move.
Consequence: A trader in a volatile stretch would fade the past day's move in proportion to its size, rather than fade one sharp hour, catching a move per case several times the cost of a trade.
Why:
- F1: When 24-hour volatility is at or above its 30-day average, the next 24-hour excess return moves against the coin's past 24-hour return, scaled to the usual move, and it moves in steps: the lowest decile of that past return gives +1.45 % (t 5.0), then +0.61 % (t 2.6), +0.52 % (t 2.3) and +0.30 % (t 1.4), down to −0.43 % (t −1.8) and −0.61 % (t −3.5) in the 8th and 9th deciles, with 605–606 non-overlapping cases per decile.
- F3: This volatile-regime 24-hour reversal holds in each of the 6 coins (+0.47 % to +0.81 %, t 2.2 to 3.3) and is positive in 7 of 8 years (2024: −0.08 %, t −0.4). The falling side holds in both halves of the windows (w1–w12 +0.77 %, t 4.7, 919 cases; w13–w24 +0.94 %, t 4.2, 976 cases), but the rising side fades in the later half (+0.55 %, t 3.3, then +0.24 %, t 1.2).
- F4: Outside raised volatility the reversal is absent: with the ratio below 1, the most-fallen past-24-hour quintile gives +0.09 % (t 0.6, 1225 cases) and the most-risen quintile −0.04 % (t −0.3, 1273 cases).
- F5: The single sharp hour that was tested carries less than the day's move. In raised volatility, hours falling more than 3 usual hourly moves give +2.25 % (t 3.7) but only 185 grid cases, and falls of 1–2 moves give +0.61 % (t 2.9, 788). The tested measure's cases averaged +0.09 % (t 1.58, 9538), about half the 0.19 % cost of a trade, against +0.6 % to +1.5 % per case for the large 24-hour moves in F1–F2.
