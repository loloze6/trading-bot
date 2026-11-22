---
line: 7.b inconclusive
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3511 USD
---
## Findings
- **F1:** The verdict's mean was on the predicted side (+0.028 % over 2 hours, t 2.38, 14,913 cases), but its slope did not grow with the forecast. On the 8,633 bets with a forecast of at least 2, I find a mean of +4.95 bp (t 2.90). The slope is +0.32 bp per forecast point with t 1.29 (t 1.00 after clipping the 1 % tails), and the Spearman rank correlation is 0.020 (p 0.059). The forecast barely sorts the outcome.
- **F2:** The forecast saturates, so it cannot grade the rebound. 4,912 of the 8,633 bets (57 %) sit at the cap of +20, with a mean of +7.2 bp (t 2.88). The bands below the cap do not rise in order: forecast 2–5 gives +0.3 bp (n 1,585), 5–10 gives +7.8 bp (t 2.14), 10–15 gives −1.2 bp and 15–20 gives −2.9 bp.
- **F3:** Graded by the raw product of the fall's size (in 30-day standard deviations of hourly return, z) and the volume ratio, the rebound grows towards the extreme. The move is +2.5 bp for products 0–5 (n 8,478), +20.2 bp for 5–10 (t 2.87, n 841), +7.8 bp for 10–20, +13.6 bp for 20–40, and +63.8 bp above 40 (t 2.17, n 127).
- **F4:** The rebound sits in the deepest high-volume falls only. With volume at least 3 times its 30-day average, falls of z −6 or deeper rebound +96.7 bp over 2 hours (t 2.48, n 79), +68.8 bp over 1 hour (t 2.64, n 140) and +177.6 bp over 4 hours (t 1.93, n 39). Falls of z −6 to −4 give only +0.9 bp over 2 hours (t 0.05, n 162).
- **F5:** The volume condition matters, on the fall side only. For falls of z −3 or deeper, over 2 hours:
- **F6:** The effect is short and uneven over time. All long bars give +0.91 bp over 1 hour (t 2.57), +1.69 bp over 2 hours (t 2.46), +1.54 bp over 4 hours (t 1.12) and −1.76 bp over 6 hours (t −0.87). Falls of z −4 or deeper on volume at least 3 times average rebound +168 bp in 2020 (t 2.66, n 29), while 2019 shows −14 bp and 2024 shows −22 bp.
- **F7:** At the size the test measured (a +0.04 % total move per case against a 0.11 % trade cost), the book cannot pay. The deepest high-volume falls rebound about +97 bp (F4), which is several times the cost.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound.b1_extreme-surge-crash-two-hour-rebound` (from F1, F2, F3, F4, F5, F7): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next two hours. The rebound grows with that hour's fall multiplied by its volume ratio, and is concentrated in the most extreme of these falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
