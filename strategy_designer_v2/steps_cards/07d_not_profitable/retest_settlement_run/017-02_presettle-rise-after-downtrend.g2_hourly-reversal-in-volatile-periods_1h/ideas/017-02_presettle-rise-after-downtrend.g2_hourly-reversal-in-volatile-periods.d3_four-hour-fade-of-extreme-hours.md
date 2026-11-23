---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 4 hours, a coin moves against its last hour's move, and the larger that move times the coin's 24-hour volatility over its 30-day average, the larger the reversal.
Consequence: A trader who wants a shorter holding would fade only the largest volatility-scaled hourly moves for a few hours, where the reversal per case exceeds the cost of a trade.
Why:
- F1: The book loses to its own trading, not to the effect: it earned +0.21 % a day before fees but paid 1.27 % a day in fees, because the allocation changed by 0.58 of the book per hour on average; per 1-hour case the total move is +0.01 %, about 0.1 times the 0.19 % cost of a trade, so no sizing or threshold at a 1-hour holding can pay.
- F2: The fade grows with both the horizon and the strength of the situation (|last-hour move in usual hourly moves| × 24h-vol ratio). At 24 hours the strength band (4, 6] gives +1.35 % (t 3.5, 349 independent cases) and the band (1, 2] gives +0.31 % (t 3.0, 2533). At 12 hours the band (4, 6] gives +0.63 % (t 3.0, 640), and at 4 hours the band above 10 gives +0.64 % (t 3.6, 776). All of these exceed the 0.19 % cost, while at 1 hour even moves above 4 usual moves give only +0.18 % (t 4.4, 4322).
