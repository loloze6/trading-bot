---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the coin's 24-hour fall during a day of high hourly volatility, the more the coin rises over the next 24 hours.
Consequence: A trader would buy into the sharpest volatile 24-hour drops for a one-day rebound, which pays more than shorting volatile rises.
Why:
- F2: At hour 0 the reversal sits almost entirely in the coin's top tercile of 24-hour hourly volatility: slope 0.00546 (t 9.7), unusual move +0.46 % per case (t 5.3, 5712 cases), strength 0.097 and total move +0.46 %, which is 2.4 times the 0.19 % cost of a trade; the middle tercile gives +0.04 % (t 0.7) and the bottom tercile −0.08 % (slope t −1.5).
- F4: In the high-volatility tercile the reversal is graded and larger after falls. By 24-hour-return quintile the next 24 hours' unusual move runs from +1.19 % (largest falls) to −0.62 % (largest rises). After falls the slope is 0.0139 (t 10.7) and the unusual move +0.56 % (t 4.4, 2873 cases, total +0.70 %); after rises the slope is 0.0022 (t 1.9) and the unusual move +0.36 % (t 3.0, 2838 cases).
- F5: The high-volatility reversal holds on every coin (slope t 2.2 to 7.2; unusual move +0.34 % to +0.62 %). It holds in 2018–2023, with slope t between 2.5 and 7.0 in five of those six years. It fades in 2024–2025 (slope t 0.5 and 0.4, unusual −0.04 % and +0.26 %), as does the hour-0 reversal overall (t 1.2 and −0.8).
