---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the more the coin fell over the three hours before 21:00, measured against its 30-day hourly volatility.
Consequence: A trader would buy a coin at 21:00 UTC after a fall over the preceding three hours, more heavily the larger that fall relative to its volatility, and hold it until 23:00 UTC.
Why:
- F4: The evening rise is mostly a rebound after a fall over the preceding three hours. With that fall scaled by volatility, the 2-bar excess from the 20:00 close falls from +0.369 % (t 7.55) in the decile with the largest prior fall (mean prior 3-hour return −2.98 %) through +0.10 % to +0.16 % in deciles 2 to 5, to about 0 or slightly negative (−0.04 % to +0.02 %) in the five deciles with prior rises. The slope of excess on the scaled prior move is −0.0011 per unit.
- F6: The rebound after a prior fall is specific to the hour, not general mean reversion. After a bottom-decile 3-hour fall, the next-2-hour excess is +0.37 % (t 7.55) from the 20:00 close and +0.42 % / +0.41 % from 11:00 / 12:00, but −0.13 % to −0.15 % from 02:00 and 08:00.
- F7: The effect varies by period. The post-fall rebound at 20:00 is +0.28 % to +0.59 % (t 3.0 to 8.9) in 2018–2021 and 2024, but −0.08 % (t −1.08) in 2022 and +0.04 % to +0.08 % (t 0.7 to 1.9) in 2023 and 2025. The 20:00 excess for all cases follows the same pattern (2022 −0.056 %, t −1.84).
