---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly when the coin's 24-hour volatility is high.
Consequence: A trader would hold a fade of sharp hours for about a day instead of re-sizing it every hour, so the reversal gathered per trade exceeds the fee.
Why:
- F1: Fees, not a missing edge, sink the book: the position earns 0.000088 per bar before costs (0.00212 per day) but pays 0.000622 per bar in fees (0.01494 per day), so the daily book return is -0.01269 against the coins' +0.00119. The cause is turnover of 0.58 of the book per hour at 0.107% fee per unit turned.
- F2: The fade loses to fees in every forecast-size quintile, even the largest: in the top quintile of abs(forecast) the gross is 0.000276 per bar against 0.001023 in fees. Turnover grows with forecast size (0.35 in the bottom quintile, 0.95 in the top), so larger signals also churn more.
- F3: The reversal after a sharp hour keeps building over a day while the information per hour thins out:
- F4: Faded over the next 24 hours, a large past move pays more than a fee, mostly when 24h volatility is high:
- F5: Volatility carries the gain: per-bar gross rises from -0.000006 in the lowest fifth of 24h vol relative to its 30-day average to 0.000283 in the highest fifth.
