---
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3026 USD
---
## Findings
- **F1:** Fees, not a missing edge, sink the book: the position earns 0.000088 per bar before costs (0.00212 per day) but pays 0.000622 per bar in fees (0.01494 per day), so the daily book return is -0.01269 against the coins' +0.00119. The cause is turnover of 0.58 of the book per hour at 0.107% fee per unit turned.
- **F2:** The fade loses to fees in every forecast-size quintile, even the largest: in the top quintile of abs(forecast) the gross is 0.000276 per bar against 0.001023 in fees. Turnover grows with forecast size (0.35 in the bottom quintile, 0.95 in the top), so larger signals also churn more.
- **F3:** The reversal after a sharp hour keeps building over a day while the information per hour thins out:
- **F4:** Faded over the next 24 hours, a large past move pays more than a fee, mostly when 24h volatility is high:
- **F5:** Volatility carries the gain: per-bar gross rises from -0.000006 in the lowest fifth of 24h vol relative to its 30-day average to 0.000283 in the highest fifth.
- **F6:** The reversal is graded and lopsided toward falls.

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours` (from F1, F2, F3, F4, F5): Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly when the coin's 24-hour volatility is high.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_day-long-rebound-after-falls` (from F4, F5, F6): Over the next 24 hours, a coin rises after a fall over its last 24 hours, and the larger that fall relative to the coin's usual 24-hour volatility, the larger the rise, more strongly when the coin's 24-hour volatility is high relative to its 30-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
