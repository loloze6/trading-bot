---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, the reversal growing faster than in proportion to the scaled move, so that it is carried by the sharpest hours of the most volatile periods.
Consequence: A trader would put size only on the sharpest hours in volatile stretches, where the day's reversal is several times the cost, and stay small on ordinary hours, whose reversal is below it.
Why:
- F4: The move is concentrated in the strongest cases. By decile of |forecast|, deciles 0–6 earn between −0.02 % and +0.13 % per 24 hours (t below 1.1), all under the 0.19 % trade cost. The top fifth earns +0.48 % (t 5.0, 3,430 cases), about 2.5 times the cost.
- F5: The volatility amplifier sharpens this. In the top |forecast| quintile with 24-hour volatility in the highest third against its 30-day average, the total move is +0.70 % per case, +0.51 % net of cost (t 4.70, 1,759 cases). The same quintile with volatility in the lowest third gives −0.32 % (439 cases). Volatility alone does not carry it: on all grid bars in the high-volatility third, the coin's own 24-hour excess move is only +0.26 %.
- F7: The effect is uneven over years. Its 24-hour excess per case is +0.50 % in 2021 and +0.39 % in 2022, but −0.01 % in 2024 and −0.13 % in 2025. Restricted to the strongest high-volatility cases, it is positive net in 2018–2021 and 2025 (+0.46 %), and negative in 2022 (−0.34 %) and 2024 (−0.36 %).
