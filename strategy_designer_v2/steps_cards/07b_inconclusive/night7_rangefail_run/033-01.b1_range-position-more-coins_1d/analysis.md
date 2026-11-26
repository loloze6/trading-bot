---
line: 7.b inconclusive
backtest: 033-01.b1_range-position-more-coins_1d
idea tested: 033-01.b1_range-position-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3998 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar. The pooled slope of 5-day excess return on the forecast is +0.000424 with t 1.39 (7,270 grid cases, 617 days), and the supporting check passes (+1.09 %). The size is +0.55 % per case (t 1.92, 1,770 days), a strength of 0.041 and 2.4 times the 0.22 % trade cost. The test already used all 19 coins and all four folds on daily bars, so no more data is available to add.
- **F2:** On folds B and C, the same slope has t 2.05 (2,424 cases, 305 days) against 1.39 on all four folds, so folds A and D must carry a weaker or opposite slope. Inside B and C the windows are mixed: 8 of 12 windows have a positive slope, none with t above 1.4, and w7, w11, w12 and w14 are negative.
- **F3:** The effect lives at short horizons and is gone by 20 days. On B and C the forecast slope's t is 1.27 at 1 day, 2.41 at 3 days (4,056 cases, 512 days), 2.05 at 5 days, 1.16 at 10 days and −1.00 at 20 days. The raw range position gives the same shape (t 1.85, 2.10, 1.76, −0.22 at 3, 5, 10, 20 days).
- **F4:** The effect is a step between the two halves of the range, plus the top close, rather than a grade through the whole range.
- **F5:** Closes at the 20-day top carry the largest mean but it rests on outliers. Their mean is +5.73 % (t 2.15 by day, 199 cases, 81 days), while the median is +1.30 % and the 5–95 % trimmed mean +2.91 %. DOGE (7 cases, mean +51.6 %) and XRP (+15.4 %) lift it, and LTC (−0.69 %) and LINK (median −2.5 %) go the other way.
- **F6:** The effect is clearer in calm markets than in agitated ones. The 5-day slope is +0.00378 with t 2.32 when the coin is calm (421 cases, 89 days), against +0.00128 with t 1.20 when it is agitated (371 cases, 72 days).

## Ideas
- `033-01.b1.b1_range-position-calm-market` (from F1, F4, F6): In a calm market, the higher a coin's daily close sits within its own 20-day high-to-low range, the more the coin rises over the next 5 days. A close at the top of the range is followed by the largest rise, and a close at the bottom by the largest fall.
- `033-01.b1.b2_range-position-three-days` (from F1, F2, F3): The higher a coin's daily close sits within its own 20-day high-to-low range, the more the coin rises over the next 3 days. A close at the top of the range is followed by the largest rise, and a close at the bottom by the largest fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
