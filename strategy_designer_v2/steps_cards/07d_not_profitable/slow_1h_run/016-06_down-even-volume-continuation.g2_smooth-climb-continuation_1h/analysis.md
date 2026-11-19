---
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
idea tested: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3273 USD
---
## Findings
- **F1:** The book loses because of fees, not because it forecasts badly: before fees it earns 0.000593 per day (0.000375 from the coins' own rise and 0.000217 from timing), but it pays 0.000921 per day in fees on a turnover of 0.85 of the book per day, which leaves a mean daily return of -0.000338 and a Sharpe of -0.34.
- **F2:** Almost all of that turnover comes from re-sizing inside the trending regime (0.72 per day) rather than from regime switches (0.13 per day), because the forecast moves by 22.5 points per day in total; standardising the 72-hour efficiency ratio against its own past 72 values turns a slow 3-day measure into one that changes every hour.
- **F3:** The raw 3-day up-share does carry the effect, but the standardised forecast loses it: on 2,865 non-overlapping climb cases, the slope of the forward 72-hour excess return on the raw efficiency ratio has t = 3.21, and the raw ratio's terciles rise in order (-0.36%, -0.14%, +0.81%, the top tercile at t = 2.76), while the forecast's terciles do not (-0.14%, +0.37%, +0.08%), even though the two correlate at 0.72.
- **F4:** A position sized on the raw ratio and changed only once a day would cut turnover to 0.054 per day, with an estimated fee of 0.000058 per day against 0.000164 of gross gain, so it would be positive after fees; but this is a hypothetical sum of hourly gains, not the book's daily measure, and it is small next to the 0.0005 per day the check asks for.
- **F5:** Large 3-day climbs made with a small up-share reverse strongly: in the top tercile of 3-day rise, the low-efficiency tercile is followed by a -3.24% excess return over the next 72 hours, against +0.90% for the high-efficiency tercile; among small climbs the high-efficiency tercile gets +1.85% against -0.43% for the low one.
- **F6:** The timing gain depends on the coin: it is positive for BTC, ETH and XRP (+0.00072 to +0.00084 per day), close to zero for LTC and ZEC (-0.00002 and -0.00012), and negative for XMR (-0.00086); XMR also pays the highest fees (0.0013 per day).
- **F7:** The book fell behind holding in every year from 2019 on (in 2023, for example, -0.00134 per day against the coins' +0.00150), so the failure of the leave-one-window-out Sharpe (-0.68) comes from the fees running throughout the period, not from one window.

## Ideas
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.d1_slow-raw-smooth-climb-continuation` (from F1, F2, F3, F4): When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days, except that what carries this is the level of that 3-day share itself, which changes over days, and not how it compares with the coin's own values over the past 3 days.
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.d2_choppy-big-climb-reverses` (from F5): When a coin has risen over the past 3 days but only a small share of its summed absolute hourly moves points up, it gives back part of the rise over the next 3 days, the more so the larger the 3-day rise and the smaller that share.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
