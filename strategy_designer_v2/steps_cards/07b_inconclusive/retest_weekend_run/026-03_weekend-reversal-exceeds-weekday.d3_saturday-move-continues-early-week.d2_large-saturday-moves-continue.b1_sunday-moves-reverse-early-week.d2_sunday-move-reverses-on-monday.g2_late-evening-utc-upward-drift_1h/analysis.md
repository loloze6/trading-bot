---
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3686 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side, with a position-weighted mean 2-bar excess of +0.078 % and t 7.91 over 16,888 cases. It is positive on every coin (+0.075 % to +0.098 %, t 2.70 to 4.24) and in 7 of 8 years. Only the supporting check failed (above-median minus below-median position −0.018 %), so the inconclusive result comes from the check, not from a missing effect.
- **F2:** The supporting check measured the position, not the volatility. At the 20:00 bar the position held correlates −0.66 with the coin's 30-day hourly volatility, because vol-target sizing divides by volatility. The "above-median position" cases are therefore the low-volatility ones, so the check ran opposite to the idea's grading.
- **F3:** Graded by the idea's own variable, the effect grows with volatility. Within each coin, the 2-bar excess from the 20:00 close rises from +0.042 % (t 2.69) in the lowest 30-day volatility quintile to +0.201 % (t 5.64) in the highest. On the standardised volatility the forecast uses, it rises from +0.003 % (t 0.12) in the lowest quintile to +0.154 % (t 4.56) in the highest.
- **F4:** The evening rise is mostly a rebound after a fall over the preceding three hours. With that fall scaled by volatility, the 2-bar excess from the 20:00 close falls from +0.369 % (t 7.55) in the decile with the largest prior fall (mean prior 3-hour return −2.98 %) through +0.10 % to +0.16 % in deciles 2 to 5, to about 0 or slightly negative (−0.04 % to +0.02 %) in the five deciles with prior rises. The slope of excess on the scaled prior move is −0.0011 per unit.
- **F5:** Volatility and the prior fall compound each other. In the top volatility tercile, a prior 3-hour fall (mean −2.05 %) is followed by +0.411 % (t 8.39, 1,688 cases), against +0.085 % after a fall in the bottom volatility tercile and −0.055 % after a rise in the top one. That +0.41 % is about 2.2 times the 0.19 % cost of a trade, while the tested idea's total move is +0.10 % (0.5 times the cost).
- **F6:** The rebound after a prior fall is specific to the hour, not general mean reversion. After a bottom-decile 3-hour fall, the next-2-hour excess is +0.37 % (t 7.55) from the 20:00 close and +0.42 % / +0.41 % from 11:00 / 12:00, but −0.13 % to −0.15 % from 02:00 and 08:00.
- **F7:** The effect varies by period. The post-fall rebound at 20:00 is +0.28 % to +0.59 % (t 3.0 to 8.9) in 2018–2021 and 2024, but −0.08 % (t −1.08) in 2022 and +0.04 % to +0.08 % (t 0.7 to 1.9) in 2023 and 2025. The 20:00 excess for all cases follows the same pattern (2022 −0.056 %, t −1.84).

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift.b1_late-evening-drift-more-coins` (from F1, F2, F3): A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the higher the coin's 30-day hourly volatility.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift.b2_evening-rebound-after-falls` (from F4, F6, F7): A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the more the coin fell over the three hours before 21:00, measured against its 30-day hourly volatility.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift.b3_volatile-evening-rebound` (from F3, F5, F4): A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the more the coin fell over the three hours before 21:00 and the higher its 30-day hourly volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
