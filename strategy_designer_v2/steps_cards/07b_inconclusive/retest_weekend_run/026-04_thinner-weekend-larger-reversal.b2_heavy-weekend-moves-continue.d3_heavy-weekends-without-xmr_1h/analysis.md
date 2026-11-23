---
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3436 USD
---
## Findings
- **F1:** The test missed its bar only on the size check, because the move does not grow with |forecast|: the 348 cases rose by +1.63 % (t 3.15), but across |forecast| quintiles the unusual move was +1.51 %, +2.73 %, −0.21 %, +2.63 % and +1.53 %; above-median minus below-median was −0.25 %, and the Spearman correlation of |forecast| with the move was 0.03.
- **F2:** The size of the weekend move does not grade the continuation, and the largest moves continue least: across move-size quintiles of the heavy-volume cases the unusual move was +0.12 %, +3.22 %, +3.11 %, +1.11 % and +0.61 %. Over all 1,901 Sunday closes the largest-move quintile gave −0.10 % (t −0.20), and the Spearman correlation of move size with the move was −0.05. Move size is the part that ties |forecast| to the case (correlation 0.73 against 0.49 for the volume ratio), so it is what makes F1's check fail.
- **F3:** The weekend-to-weekday volume ratio is what grades the continuation. Over all 1,901 Sunday closes, the volume-ratio sextiles gave −0.57 % (t −1.59), −0.50 %, +0.49 %, +0.27 %, +0.34 % and +1.95 % (t 3.55, ratio 1.04 to 9.09), with a Spearman correlation of 0.09. Inside the heavy cases, the top volume quintile (ratio 1.86 to 9.09) gave +3.27 % (t 2.64, 70 cases).
- **F4:** The effect rests heavily on one coin: XRP gave +4.66 % (t 2.84, 74 cases). Without XRP the heavy cases gave +0.80 % (t 1.69, 275 cases); ZEC, with the most cases, gave +0.36 % (t 0.43, 114 cases), BTC +1.71 % (t 1.42, 31 cases), ETH +1.29 % (t 1.14) and LTC +0.76 % (t 1.14).
- **F5:** The continuation is broad over time and on both sides. It was positive in 7 of 8 years (2019, 2020 and 2024 each t ≈ 2.2), with 2025 the only negative year (−0.76 %, t −0.60). Long cases gave +1.67 % (t 2.31, 203 cases) and short cases +1.58 % (t 2.17, 145 cases), and the move was spread over both days (+0.89 % in the first 24 hours, +0.72 % in the second).
- **F6:** Weekends on lighter volume than the weekdays show nothing: 1,552 such Sunday closes gave +0.04 % (t 0.23), so the continuation sits only where weekend volume is heavy.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr.b1_weekend-volume-grades-continuation` (from F1, F2, F3, F6): A coin's Saturday-Sunday move continues in the same direction over the next 48 hours, the more so the heavier the weekend's volume against its mean over the preceding five weekdays.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr.b2_heavy-weekends-on-more-coins` (from F4, F5): A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 48 hours, the more so the larger the move and the heavier the weekend volume against the weekdays.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
