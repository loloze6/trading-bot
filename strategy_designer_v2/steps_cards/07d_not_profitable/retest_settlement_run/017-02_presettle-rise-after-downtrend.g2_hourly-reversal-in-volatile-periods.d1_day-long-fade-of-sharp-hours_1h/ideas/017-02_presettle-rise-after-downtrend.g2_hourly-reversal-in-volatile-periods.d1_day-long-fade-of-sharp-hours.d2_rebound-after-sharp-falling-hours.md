---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, chiefly as a rebound after a sharp falling hour, the rebound growing with the size of that fall.
Consequence: A trader would buy sharp down hours in volatile periods for a day and refuse to short sharp up hours, the side whose move does not cover the cost.
Why:
- F5: The volatility amplifier sharpens this. In the top |forecast| quintile with 24-hour volatility in the highest third against its 30-day average, the total move is +0.70 % per case, +0.51 % net of cost (t 4.70, 1,759 cases). The same quintile with volatility in the lowest third gives −0.32 % (439 cases). Volatility alone does not carry it: on all grid bars in the high-volatility third, the coin's own 24-hour excess move is only +0.26 %.
- F6: Within those strongest high-volatility cases, the long side (fading a sharp down hour) carries the gain. Longs make +1.34 % total, +1.15 % net (t 5.29, 873 cases). Shorts make +0.07 % total, −0.12 % net (t 1.10, 886 cases). Over all strong cases the picture is the same: longs +0.72 % total (t 5.21), shorts +0.12 % (t 2.44).
- F4: The move is concentrated in the strongest cases. By decile of |forecast|, deciles 0–6 earn between −0.02 % and +0.13 % per 24 hours (t below 1.1), all under the 0.19 % trade cost. The top fifth earns +0.48 % (t 5.0, 3,430 cases), about 2.5 times the cost.
