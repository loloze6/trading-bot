---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last 24 hours' move, and the larger that move measured in units of its 30-day volatility, times its 24-hour volatility over its 30-day average, the larger the reversal.
Consequence: A trader would fade large volatility-scaled daily moves for a day in turbulent periods, where the reversal per case is several times the cost of a trade, and refuse fades in calm periods.
Why:
- F1: The fade pays most over 24 hours. On non-overlapping 24-hour cases, a coin's 24-hour return standardised by its 30-day hourly volatility predicts the opposite excess move over the next 24 hours, with a slope of -42.4 bp per standard deviation (t -11.05, 17102 cases). The top tenth by size fades 99.6 bp (t -5.46), against 20.3 bp for the tested 1-hour situation over 4 hours (t -6.30, 95448 cases), and the 24-hour fade is about 5 times the 0.19 % cost of a trade.
- F2: The 24-hour reversal is concentrated where the coin's 24-hour volatility is high against its 30-day average. In the top tercile of that ratio, the slope is -36.5 bp per unit (t -6.71, 5269 cases) and the top-fifth fade is 84.9 bp. In the low tercile, the slope is +8.1 bp (t 0.64) and the fade is -0.4 bp. The product of the 24-hour move and the volatility ratio gives a slope of -18.4 (t -8.03, 15806 cases) and a top-fifth fade of 72.5 bp.
- F3: The 24-hour reversal holds on every coin: slopes from -16.3 (BTC, t -2.47) to -44.9 (XMR, t -4.53), with top-fifth fades from 9 to 77 bp. It is negative in 7 of 8 years, with t from -1.39 to -5.39; 2024 is the exception (+5.4, t 0.60).
