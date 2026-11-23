---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4298 USD
---
## Findings
- **F1:** The close's position in the day's range carries none of the tested edge. Alone, its 10-day slope is t 0.42 (n 1691) and its quintiles are not ordered (−0.41 %, −0.48 %, +1.56 %, −0.71 %, +0.03 %). Alongside the volume ratio, past 20-day return and range ratio it is t −0.74 (n 1403), while the volume ratio stays at t 4.15.
- **F2:** The volume ratio carries the edge. The day's volume over its prior 20-day mean has a 10-day excess-return slope of t 4.68 (n 1403). Its top decile (ratio 3.2) gains +2.94 % excess (strength 0.157, total +4.16 %), and its bottom decile (ratio 0.29) loses −2.01 % (t −2.10). The 5-day mean volume ratio also works (t 3.72, n 1259). At 5 days the slope is only t 1.53 (n 2843) and at 20 days t −0.53 (n 683).
- **F3:** Heavy volume predicts a rise only when the coin was going up. On up days the volume-ratio slope is t 5.26 (n 655), against t 0.74 on down days (n 748). With the past 20-day return positive it is t 5.03 (n 694), against t 0.24 when negative (n 709). Volume signed by the day's direction gives t 4.20 (n 1403). This is a continuation pattern, the opposite of the low-close absorption story.
- **F4:** The volume effect is not spread evenly, and that limits trust in it. By coin it is t 4.80 in ZEC and t 2.00 in XRP, but negative in BTC, ETH and LTC (t −0.49, −0.35, −0.97). By time it is t 8.06 in windows w19–w24, against −1.40, 0.29 and 1.02 in the three earlier window groups. By year it is t 3.94 in 2024 and t 6.74 in 2025, and between −1.88 and 0.88 in 2018–2023.
- **F5:** The tested forecast is also carried by few cases. It is significant only in ZEC (t 2.28; the other coins range from t 0.20 to 1.52) and in 2020 (t 3.07). Its top quintile gains +1.67 % excess (t 1.98); its other quintiles range from −1.01 % to +0.21 %.
- **F6:** The book is close to leveraged holding. Its daily returns correlate 0.86 with the coin's, the mean allocation is 0.85 (median 0.84, 90th percentile 1.54), and it is in a position on 98 % of days. Its mean daily return of 0.131 % is barely above the coin's 0.119 %. Its best and worst 2 % days (+15.0 % and −12.7 %) are the coin's own large moves (+14.0 % and −11.7 %).
- **F7:** The coin's prior trend predicts the next 10 days on its own: past 20-day return slope t 2.86 (n 1403), past 5-day return slope t 3.59 (n 1547). This is again only significant in ZEC (t 2.05), and BTC, LTC and XMR are slightly negative.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound.g1_heavy-volume-up-day-continuation` (from F2, F3, F1, F4): The heavier a coin's volume on a day that closes higher, relative to its own prior 20-day average volume, and the larger that day's rise, the more the coin keeps rising over the next 10 days.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound.g2_volume-surge-within-uptrend` (from F3, F7, F2, F4): The heavier a coin's volume relative to its prior 20-day average while its 20-day return is positive, the more it rises over the next 10 days, more so the stronger that 20-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
