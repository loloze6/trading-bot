---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days, except that what carries this is the level of that 3-day share itself, which changes over days, and not how it compares with the coin's own values over the past 3 days.
Consequence: A trader should size a long position on how smooth the 3-day climb is in absolute terms and re-size it only as slowly as that measure changes, so fees no longer eat the edge.
Why:
- F1: The book loses because of fees, not because it forecasts badly: before fees it earns 0.000593 per day (0.000375 from the coins' own rise and 0.000217 from timing), but it pays 0.000921 per day in fees on a turnover of 0.85 of the book per day, which leaves a mean daily return of -0.000338 and a Sharpe of -0.34.
- F2: Almost all of that turnover comes from re-sizing inside the trending regime (0.72 per day) rather than from regime switches (0.13 per day), because the forecast moves by 22.5 points per day in total; standardising the 72-hour efficiency ratio against its own past 72 values turns a slow 3-day measure into one that changes every hour.
- F3: The raw 3-day up-share does carry the effect, but the standardised forecast loses it: on 2,865 non-overlapping climb cases, the slope of the forward 72-hour excess return on the raw efficiency ratio has t = 3.21, and the raw ratio's terciles rise in order (-0.36%, -0.14%, +0.81%, the top tercile at t = 2.76), while the forecast's terciles do not (-0.14%, +0.37%, +0.08%), even though the two correlate at 0.72.
- F4: A position sized on the raw ratio and changed only once a day would cut turnover to 0.054 per day, with an estimated fee of 0.000058 per day against 0.000164 of gross gain, so it would be positive after fees; but this is a hypothetical sum of hourly gains, not the book's daily measure, and it is small next to the 0.0005 per day the check asks for.
