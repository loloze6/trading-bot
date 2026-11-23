---
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4221 USD
---
## Findings
- **F1:** The book never traded the fade it was meant to trade. Its position changed on only 0.85 % of bars, and its sign matched the forecast's sign on 49.7 % of bars, a coin flip. The correlation between position and forecast was only 0.02–0.03 per coin. Trades lasted about 1,160 hours on average against a planned 24. Inside each window every coin sat on one side for the whole window: the window-level share long is 0, 0.17, 0.33, … 1.0, so each coin was all long or all short.
- **F2:** Because of F1, the book's window returns are the coins' own trend times a fixed side, not timing. The correlation of window book return with coin return × side is 0.82. In w10 the coins rose +54 % while the book, short all window, lost −67 %. In w23 they rose +36 % and the book lost −37 %. Long trades made +24.3 % gross on average and short trades −29.6 %. This window-long directional bet is what produced the Calmar of −0.14, the one-window-out Sharpe of −0.002 and the −0.45 Sharpe gap to holding.
- **F3:** Measured as it was meant to be traded, the fade earns at 24 hours and nowhere else. On the non-overlapping grid the mean excess return per case is:
- **F4:** The move is concentrated in the strongest cases. By decile of |forecast|, deciles 0–6 earn between −0.02 % and +0.13 % per 24 hours (t below 1.1), all under the 0.19 % trade cost. The top fifth earns +0.48 % (t 5.0, 3,430 cases), about 2.5 times the cost.
- **F5:** The volatility amplifier sharpens this. In the top |forecast| quintile with 24-hour volatility in the highest third against its 30-day average, the total move is +0.70 % per case, +0.51 % net of cost (t 4.70, 1,759 cases). The same quintile with volatility in the lowest third gives −0.32 % (439 cases). Volatility alone does not carry it: on all grid bars in the high-volatility third, the coin's own 24-hour excess move is only +0.26 %.
- **F6:** Within those strongest high-volatility cases, the long side (fading a sharp down hour) carries the gain. Longs make +1.34 % total, +1.15 % net (t 5.29, 873 cases). Shorts make +0.07 % total, −0.12 % net (t 1.10, 886 cases). Over all strong cases the picture is the same: longs +0.72 % total (t 5.21), shorts +0.12 % (t 2.44).
- **F7:** The effect is uneven over years. Its 24-hour excess per case is +0.50 % in 2021 and +0.39 % in 2022, but −0.01 % in 2024 and −0.13 % in 2025. Restricted to the strongest high-volatility cases, it is positive net in 2018–2021 and 2025 (+0.46 %), and negative in 2022 (−0.34 %) and 2024 (−0.36 %).

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours.d1_day-long-fade-closed-daily` (from F1, F2, F3): Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, with the fade's move fully played out within those 24 hours, so that the position is held for one day and then given up.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours.d2_rebound-after-sharp-falling-hours` (from F5, F6, F4): Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, chiefly as a rebound after a sharp falling hour, the rebound growing with the size of that fall.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours.d3_reversal-concentrated-in-sharpest-hours` (from F4, F5, F7): Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average, the reversal growing faster than in proportion to the scaled move, so that it is carried by the sharpest hours of the most volatile periods.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
