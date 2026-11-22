---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.d confirmed, not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a sharp falling hour, and the larger that fall relative to the coin's usual hourly volatility, and the higher its 24-hour volatility against its 30-day average, the larger the rise.
Consequence: A trader would buy sharp single-hour falls in volatile periods and hold for a day, and would not short sharp rises, which do not reverse.
Why:
- F2: The fade grows with both the horizon and the strength of the situation (|last-hour move in usual hourly moves| × 24h-vol ratio). At 24 hours the strength band (4, 6] gives +1.35 % (t 3.5, 349 independent cases) and the band (1, 2] gives +0.31 % (t 3.0, 2533). At 12 hours the band (4, 6] gives +0.63 % (t 3.0, 640), and at 4 hours the band above 10 gives +0.64 % (t 3.6, 776). All of these exceed the 0.19 % cost, while at 1 hour even moves above 4 usual moves give only +0.18 % (t 4.4, 4322).
- F3: The high-volatility part of the idea carries the effect. For last-hour moves of at least 2 usual moves, the 24-hour fade is +1.20 % (t 3.35, 458 cases) when the 24h-vol ratio is above 1.6, against −0.34 % (t −1.1, 335) when it is 0.8–1.2. As a condition-alone check, high vol without a large move gives +0.42 % (t 2.2, 1218) and a large move without high vol gives +0.17 % (t 0.9, 784), against +1.20 % when both hold. The vol condition adds to the move but is not the effect by itself, which is what the idea's "more strongly when volatility is high" states.
- F4: The reversal is one-sided. At 24 hours with strength of at least 4, the long side after a sharp down hour earns +2.21 % unusual (+2.32 % total, 357 cases). The short side after a sharp up hour earns +0.08 % unusual (−0.03 % total, 333 cases), so shorting adds turnover and cost but no gain.
- F5: The strong 24-hour fade is positive on every coin, from +0.84 % (LTC, 118 cases) to +2.09 % (ZEC, 96 cases). It is concentrated in the years 2018–2021 (+1.2 % to +4.0 % a year-group, 67–98 cases each) and is near zero in 2022–2025 (−0.13 % to +0.17 %, 79–91 cases each).
