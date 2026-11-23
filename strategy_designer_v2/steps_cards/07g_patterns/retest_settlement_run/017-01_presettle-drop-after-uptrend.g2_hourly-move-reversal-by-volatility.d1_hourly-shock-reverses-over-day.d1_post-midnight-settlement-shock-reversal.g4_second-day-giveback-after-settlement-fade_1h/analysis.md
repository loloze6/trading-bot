---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4204 USD
---
## Findings
- **F1:** The 24-hour reversal is not tied to the 00:00 UTC settlement: across all days, the slope of the next 24-hour unusual return on minus the standardised 24-hour return is 0.00445 (t 11.6, 17086 cases) at hour 0, but equally strong at hour 1 (t 12.7) and still clear at hours 2–5 (t 9.6–10.6) and 23 (t 8.2); it is weakest at hours 13–14 (t 1.0 and 0.7) and positive at almost every hour, so it is mainly an Asian-hours effect and not a settlement-clock one.
- **F2:** At hour 0 the reversal sits almost entirely in the coin's top tercile of 24-hour hourly volatility: slope 0.00546 (t 9.7), unusual move +0.46 % per case (t 5.3, 5712 cases), strength 0.097 and total move +0.46 %, which is 2.4 times the 0.19 % cost of a trade; the middle tercile gives +0.04 % (t 0.7) and the bottom tercile −0.08 % (slope t −1.5).
- **F3:** The same holds for 24-hour volatility relative to its 30-day level: in the top tercile of that ratio the hour-0 unusual move is +0.39 % (t 4.9, slope t 10.6, 5295 cases), against +0.02 % and +0.04 % (t 0.3 and 0.7) in the lower two terciles.
- **F4:** In the high-volatility tercile the reversal is graded and larger after falls. By 24-hour-return quintile the next 24 hours' unusual move runs from +1.19 % (largest falls) to −0.62 % (largest rises). After falls the slope is 0.0139 (t 10.7) and the unusual move +0.56 % (t 4.4, 2873 cases, total +0.70 %); after rises the slope is 0.0022 (t 1.9) and the unusual move +0.36 % (t 3.0, 2838 cases).
- **F5:** The high-volatility reversal holds on every coin (slope t 2.2 to 7.2; unusual move +0.34 % to +0.62 %). It holds in 2018–2023, with slope t between 2.5 and 7.0 in five of those six years. It fades in 2024–2025 (slope t 0.5 and 0.4, unusual −0.04 % and +0.26 %), as does the hour-0 reversal overall (t 1.2 and −0.8).
- **F6:** The hours starting 21:00 and 22:00 UTC carry a positive mean hourly return: +0.055 % (t 6.9) and +0.044 % (t 5.8). It is positive on all six coins (t 3.0–4.6) and in 7 of 8 years. Together it is about 0.1 % a day, below the 0.19 % cost of a trade, and I found nothing that grades it.
- **F7:** The book's yearly mean daily return fell from +0.10 % in 2018 to −0.07 % in 2024 and −0.06 % in 2025, while the coins' mean daily return was +0.24 % and +0.20 % in those years. This matches the fading of the effect in F5.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade.g1_volatile-day-24-hour-reversal` (from F1, F2, F3, F5): The higher the coin's hourly volatility over the past 24 hours relative to its past 30 days, the more its 24-hour return reverses over the next 24 hours, whatever the hour of day.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade.g2_volatile-selloff-next-day-rebound` (from F2, F4, F5): The larger the coin's 24-hour fall during a day of high hourly volatility, the more the coin rises over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
