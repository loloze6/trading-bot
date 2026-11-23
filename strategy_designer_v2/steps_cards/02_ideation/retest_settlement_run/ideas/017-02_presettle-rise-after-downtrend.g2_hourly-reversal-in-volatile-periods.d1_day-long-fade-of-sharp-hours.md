---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its last hour's move, and the larger that move relative to the coin's usual hourly volatility, the larger the reversal, more strongly the higher the coin's 24-hour volatility stands against its 30-day average.
Consequence: A trader would fade sharp single-hour moves in volatile periods and hold the fade for a day, so the move captured is several times the cost of the trade instead of a tenth of it.
Why:
- F1: The book loses to its own trading, not to the effect: it earned +0.21 % a day before fees but paid 1.27 % a day in fees, because the allocation changed by 0.58 of the book per hour on average; per 1-hour case the total move is +0.01 %, about 0.1 times the 0.19 % cost of a trade, so no sizing or threshold at a 1-hour holding can pay.
- F2: The fade grows with both the horizon and the strength of the situation (|last-hour move in usual hourly moves| × 24h-vol ratio). At 24 hours the strength band (4, 6] gives +1.35 % (t 3.5, 349 independent cases) and the band (1, 2] gives +0.31 % (t 3.0, 2533). At 12 hours the band (4, 6] gives +0.63 % (t 3.0, 640), and at 4 hours the band above 10 gives +0.64 % (t 3.6, 776). All of these exceed the 0.19 % cost, while at 1 hour even moves above 4 usual moves give only +0.18 % (t 4.4, 4322).
- F3: The high-volatility part of the idea carries the effect. For last-hour moves of at least 2 usual moves, the 24-hour fade is +1.20 % (t 3.35, 458 cases) when the 24h-vol ratio is above 1.6, against −0.34 % (t −1.1, 335) when it is 0.8–1.2. As a condition-alone check, high vol without a large move gives +0.42 % (t 2.2, 1218) and a large move without high vol gives +0.17 % (t 0.9, 784), against +1.20 % when both hold. The vol condition adds to the move but is not the effect by itself, which is what the idea's "more strongly when volatility is high" states.
