---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a fall over its last 24 hours, and the deeper that fall measured in units of its 30-day volatility, the larger the rise.
Consequence: A trader would buy deep volatility-scaled daily falls for a day, the side of the reversal that carries most of its size.
Why:
- F1: The fade pays most over 24 hours. On non-overlapping 24-hour cases, a coin's 24-hour return standardised by its 30-day hourly volatility predicts the opposite excess move over the next 24 hours, with a slope of -42.4 bp per standard deviation (t -11.05, 17102 cases). The top tenth by size fades 99.6 bp (t -5.46), against 20.3 bp for the tested 1-hour situation over 4 hours (t -6.30, 95448 cases), and the 24-hour fade is about 5 times the 0.19 % cost of a trade.
- F4: The reversal is lopsided toward rebounds after falls. The decile of largest 24-hour falls (mean -1.72 standardised) gains 80.9 bp in excess over the next 24 hours (t 5.07, 1581 cases), and the next decile gains 23.3 bp (t 1.83). The decile of largest rises loses only 25.7 bp (t -1.86).
- F3: The 24-hour reversal holds on every coin: slopes from -16.3 (BTC, t -2.47) to -44.9 (XMR, t -4.53), with top-fifth fades from 9 to 77 bp. It is negative in 7 of 8 years, with t from -1.39 to -5.39; 2024 is the exception (+5.4, t 0.60).
