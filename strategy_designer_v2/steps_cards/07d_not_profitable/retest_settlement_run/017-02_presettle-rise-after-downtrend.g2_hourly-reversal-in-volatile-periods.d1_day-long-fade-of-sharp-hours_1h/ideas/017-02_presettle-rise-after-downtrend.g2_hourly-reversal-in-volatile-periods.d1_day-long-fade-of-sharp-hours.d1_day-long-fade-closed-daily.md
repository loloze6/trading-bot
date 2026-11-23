---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, with the fade's move fully played out within those 24 hours, so that the position is held for one day and then given up.
Consequence: A trader would take the fade at a sharp hour, close it after one day instead of letting it ride for weeks, and so capture the day's reversal rather than the coin's month-long trend.
Why:
- F1: The book never traded the fade it was meant to trade. Its position changed on only 0.85 % of bars, and its sign matched the forecast's sign on 49.7 % of bars, a coin flip. The correlation between position and forecast was only 0.02–0.03 per coin. Trades lasted about 1,160 hours on average against a planned 24. Inside each window every coin sat on one side for the whole window: the window-level share long is 0, 0.17, 0.33, … 1.0, so each coin was all long or all short.
- F2: Because of F1, the book's window returns are the coins' own trend times a fixed side, not timing. The correlation of window book return with coin return × side is 0.82. In w10 the coins rose +54 % while the book, short all window, lost −67 %. In w23 they rose +36 % and the book lost −37 %. Long trades made +24.3 % gross on average and short trades −29.6 %. This window-long directional bet is what produced the Calmar of −0.14, the one-window-out Sharpe of −0.002 and the −0.45 Sharpe gap to holding.
- F3: Measured as it was meant to be traded, the fade earns at 24 hours and nowhere else. On the non-overlapping grid the mean excess return per case is:
