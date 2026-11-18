---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5039 USD
---
## Findings
- **F1:** The next-day reversal of a vol-scaled daily move appears only when 20-day volatility stands high against its own recent level (20-day vol over its 60-day mean). In the top tercile the slope of next-day excess return on the day's z-score is −51.8 bps per unit (t −3.70, n 987), against +1.4 bps (t 0.12) and −0.5 bps (t −0.04) in the lower two terciles. Pooled, the interaction z × relative-vol is −112.7 bps (t −6.73) and z alone is +104.1 bps (t 5.37), so the reversal grows with the volatility expansion.
- **F2:** Ranking volatility per coin over the whole record gives the same gradient. The z-slope is −69.7 bps (t −5.82, n 1612) in the top volatility tercile, −0.5 bps (t −0.06) in the middle and +15.3 bps (t 2.15) in the bottom. Next-day excess return after the lowest z quintile is +107.6 bps in high vol against −26.7 bps in low vol. The thresholds in this split are look-ahead, so it is supporting only.
- **F3:** The reversal lasts one day only. On non-overlapping grids the z-slope is +7.35 bps (t 0.69, n 2403) at 2 days, −0.0002 (t −0.13, n 1571) at 3 days and 0.0001 (t 0.05, n 947) at 5 days.
- **F4:** A wide high-low range on an up day (range in units of 20-day volatility) is followed by a lower next day. Controlling for z, the range slope on up days is −43.1 bps per unit (t −3.16, n 2445), against +10.6 bps (t 0.96, n 2389) on down days. Over all bars it is −2.6 bps (t −0.45).
- **F5:** The pooled one-day reversal is uneven across coins and years. The z-slope is −21.4 bps (t −2.44) for ETH and −11.2 bps (t −1.62) for BTC. It is −55.8 bps (t −2.98) in 2020, but +10.0 bps (t 0.62) in 2022 and +8.1 bps (t 0.67) in 2024.
- **F6:** The book earns mostly from its long side, and BTC shorts lose. BTC long bars average +6.2 bps (n 1393) and BTC short bars −2.1 bps (n 1478); ETH shorts average +2.5 bps (n 1474). The book's mean daily return is 1.2 bps while holding the coins earned more, so its Sharpe is 0.38 below holding's.
- **F7:** The book's worst 5% of days (n 290) come after the coin rose 43.8 bps the day before, and are followed by a +96.0 bps coin day. The best 5% come after a −54.7 bps day and are followed by −24.2 bps. The book's large days sit inside alternating up and down swings.
- **F8:** No weekday stands out once seven were tested. Wednesday returns average 41.5 bps (t 2.66, n 692), the strongest of the seven, and the same weekday by year is negative in 2018 (−49.9 bps) and 2022 (−12.3 bps).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal.g1_vol-expansion-one-day-reversal` (from F1, F2, F3): The more a coin's 20-day daily volatility stands above its own average of the past 60 days, the more strongly its next 1 day reverses the day's move measured in units of 20-day volatility: up after large falls, down after large rises.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal.g2_wide-range-up-day-giveback` (from F4, F3): The wider a coin's rising day's high-low range is in units of its 20-day volatility, the more the coin falls over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
