---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the lower the coin's 20-day volatility of daily returns.
Consequence: A trader weights the monthly-momentum signal more heavily in calm markets and less in turbulent ones, where it loses.
Why:
- F2: In w1–w9 the momentum effect was absent on both sides: longs earned −0.024 % per coin-bar (2915 bars) and shorts −0.015 % (3574 bars), against +0.291 % for longs in w10–w24 (5626 bars); summed per window, longs gave about −0.12 and shorts about −0.09 of book value over w1–w9.
- F6: The book's gain fades as the coin's 20-day volatility rises: mean bar gain was +0.195 %, +0.203 % and +0.155 % in the three calmest fifths, against +0.014 % and +0.061 % in the two most volatile. Shorts in the most volatile fifth earned −0.087 % (t −1.45).
