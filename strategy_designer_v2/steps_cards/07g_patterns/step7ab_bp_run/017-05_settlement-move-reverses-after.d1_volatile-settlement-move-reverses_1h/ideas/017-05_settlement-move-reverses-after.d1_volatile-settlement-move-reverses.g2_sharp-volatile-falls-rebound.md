---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its past 2 hours, measured against its usual hourly move, the larger its rise over the next 8 hours, at any hour of the day, while its 24-hour volatility is above its 30-day average.
Consequence: A trader would buy only the sharpest 2-hour falls in volatile markets, whatever the clock time, and hold for about 8 hours, instead of fading moves at funding settlements.
Why:
- F4: The reversal of a 2-hour move over the next 8 hours is not tied to funding settlement. With volatility at or above its 720-hour mean, its strength is 0.031 on settlement bars (t 3.6, n 18724) and 0.028 on all other bars (t 8.5, n 130686). The strongest hours are the closes at 01, 02 and 12 UTC, with strength 0.097, 0.092 and 0.072. The settlement closes at 08 and 16 UTC give -0.002 and 0.045. This contradicts the brief's third test.
- F5: Only the largest 2-hour falls in high volatility rebound by more than a trade costs. On an 8-hour grid at all hours, the top fifth of 2-hour falls gives strength 0.176 (t 4.5, n 1841) and +55 bps total over 8 hours, about 3 times the cost. The top fifth of rises gives only 0.080 and +20 bps. The lower four fifths of falls give 3 to 23 bps. On settlement bars, only the largest fifth of moves covers a trade, at +29 bps.
- F6: The book's losses come from its shorts. 16476 short trades average -0.84 % before fees, against +0.10 % for 16244 longs, and the median short is negative in every one of the 8 years (-0.33 % to -0.86 %). Fading rises into settlement loses, while fading falls breaks about even before fees.
