---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past week is high against its past month, a sharp 24-hour fall is followed by a rise over the next 24 hours, and the larger the fall against its usual 24-hour move, the larger the rise.
Consequence: A trader buys deep one-day falls when the market has turned turbulent, and refuses them in calm stretches, where they do not rebound.
Why:
- F1: The large 24-hour fall is what rebounds, whatever the hour. On the non-overlapping 24-bar grid, bars in the bottom decile of the 24-hour return (scaled by the mean absolute 24-hour move of the last 720 bars) are followed by a 24-hour return of +82.6 bp above the coin's normal drift (t 5.21, 1581 cases). The next decile gives only +19.8 bp (t 1.53). The middle and top deciles give between -4 and -26 bp, so the rebound sits in the deepest falls.
- F3: The rebound after large 24-hour falls lives almost entirely in high-volatility stretches. When the 1-week hourly volatility over the 1-month volatility is above its median, it is +103.7 bp (t 6.17, 1277 cases); below the median it is -10.3 bp (t -0.74, 1278 cases).
- F4: The rebound after large 24-hour falls holds on every coin and in every part of the period:
