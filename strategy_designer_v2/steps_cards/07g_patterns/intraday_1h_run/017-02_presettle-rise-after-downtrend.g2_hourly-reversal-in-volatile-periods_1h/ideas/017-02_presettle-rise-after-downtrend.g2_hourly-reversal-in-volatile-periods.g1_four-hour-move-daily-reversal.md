---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last 4-hour move. The larger that move relative to the coin's usual hourly volatility, the larger the move back.
Consequence: A trader would fade sharp 4-hour moves and hold for about a day, trading far less often than an hourly fade so the edge can outlast fees, and would refuse the trade if the day-long reversal is not confirmed.
Why:
- F4: The reversal of the scaled one-hour move lasts well beyond one hour on non-overlapping grids. After the bottom fifth of scaled moves, the excess return is +0.000749 (t 4.8, n 20,646) over 4h and +0.002362 (t 2.8, n 3,422) over 24h. After the top fifth it is -0.000494 (t -3.5) over 4h and -0.003228 (t -3.8, n 3,425) over 24h.
- F5: Larger multi-hour moves also revert over the next 24h on non-overlapping grids. After the bottom fifth of volatility-scaled 4h moves, the 24h excess return is +0.003466 (t 3.9, n 3,424), against -0.002018 (t -2.3) in the fourth fifth. After the bottom fifth of scaled 24h moves it is +0.003511 (t 3.8), with the upper fifths near -0.0016 (t about -1.9).
- F1: The fade's edge before costs is far smaller than its costs: the gross gain is 0.000088 per bar against a fee of 0.000622 per bar, from turning over 0.58 of the book per bar. The book loses more on days the coin moves more, from -0.0093 per day in the quietest fifth of coin days to -0.0210 in the most volatile fifth.
