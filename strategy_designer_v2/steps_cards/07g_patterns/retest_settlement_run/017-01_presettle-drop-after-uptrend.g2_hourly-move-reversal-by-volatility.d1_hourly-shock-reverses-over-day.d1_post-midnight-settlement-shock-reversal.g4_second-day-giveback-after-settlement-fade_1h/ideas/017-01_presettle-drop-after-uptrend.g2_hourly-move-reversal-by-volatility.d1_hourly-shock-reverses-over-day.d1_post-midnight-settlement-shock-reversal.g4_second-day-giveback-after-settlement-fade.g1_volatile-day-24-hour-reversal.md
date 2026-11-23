---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher the coin's hourly volatility over the past 24 hours relative to its past 30 days, the more its 24-hour return reverses over the next 24 hours, whatever the hour of day.
Consequence: A trader would fade a 24-hour move only when that day has been unusually volatile for the coin, and refuse the fade on calm days, where it earns nothing.
Why:
- F1: The 24-hour reversal is not tied to the 00:00 UTC settlement: across all days, the slope of the next 24-hour unusual return on minus the standardised 24-hour return is 0.00445 (t 11.6, 17086 cases) at hour 0, but equally strong at hour 1 (t 12.7) and still clear at hours 2–5 (t 9.6–10.6) and 23 (t 8.2); it is weakest at hours 13–14 (t 1.0 and 0.7) and positive at almost every hour, so it is mainly an Asian-hours effect and not a settlement-clock one.
- F2: At hour 0 the reversal sits almost entirely in the coin's top tercile of 24-hour hourly volatility: slope 0.00546 (t 9.7), unusual move +0.46 % per case (t 5.3, 5712 cases), strength 0.097 and total move +0.46 %, which is 2.4 times the 0.19 % cost of a trade; the middle tercile gives +0.04 % (t 0.7) and the bottom tercile −0.08 % (slope t −1.5).
- F3: The same holds for 24-hour volatility relative to its 30-day level: in the top tercile of that ratio the hour-0 unusual move is +0.39 % (t 4.9, slope t 10.6, 5295 cases), against +0.02 % and +0.04 % (t 0.3 and 0.7) in the lower two terciles.
- F5: The high-volatility reversal holds on every coin (slope t 2.2 to 7.2; unusual move +0.34 % to +0.62 %). It holds in 2018–2023, with slope t between 2.5 and 7.0 in five of those six years. It fades in 2024–2025 (slope t 0.5 and 0.4, unusual −0.04 % and +0.26 %), as does the hour-0 reversal overall (t 1.2 and −0.8).
