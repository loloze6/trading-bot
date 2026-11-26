---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d
idea tested: 032-02.b1.e1.e2_unextended-breakouts-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3740 USD
---
## Findings
- **F1:** The test's result points the opposite way from the idea: the main measure is -2.60 % (Welch t -0.53, 205 cases), the forecast-weighted mean excess is -1.68 %, and the size is -1.83 % per case (t -0.60, 69 days). In folds B and C the recorded forecast is negatively ranked against the 20-day excess return (Spearman -0.235, p 0.017, 103 breaks): the high-forecast half earned -2.76 % and the low-forecast half +7.21 %.
- **F2:** The low-forecast half has a mean forecast of 0.0008, so it consists mostly of breaks that came after a strong run-up. These earned more, and the recorded run-up is ranked positively against the 20-day excess (Spearman +0.179, p 0.07, n 103). The idea's grading by a small prior run-up runs against the data.
- **F3:** What does grade the move is how far the close cleared its prior high. Small clears (mean 0.50 %) gave +13.79 % excess over 20 days, mid clears (2.17 %) +6.15 %, and large clears (9.76 %) -0.76 % (24/23/24 cases). That is 0.50, 0.24 and 0.00 of a usual move. Welch small minus large is 2.14; Spearman distance vs 20-day excess is -0.280 (p 0.018, n 71).
- **F4:** The same gradient holds on breaks with a full 60 prior closes (n 38). By distance quartile the 20-day excess is +28.8 %, +15.8 %, +5.5 % and +3.8 %, with Spearman -0.348 (p 0.032) at 20 days and -0.247 at 10 days.
- **F5:** The distance gradient is negative in 6 of the 7 windows with enough breaks (w8 -0.53, w10 -0.07, w11 -0.60, w12 -0.39, w15 -0.07, w17 -0.70; w16 +0.26). By coin it is mixed: XRP -0.61, ZEC -0.60, LTC -0.16, BTC 0.00, ETH +0.13, XMR +0.46.
- **F6:** The gradient is steepest after a wide prior range. Wide-range breaks gave +12.6 %, +0.75 % and -13.9 % for small, mid and large clears (15/11/9 cases). Narrow-range breaks gave +15.8 %, +11.1 % and +7.1 % (9/12/15).
- **F7:** Pooled, the breaks barely beat the coin's normal drift: the mean 20-day excess is +2.28 % (t 0.89, n 103). The coin's usual 20-day move is 21.24 %, so the market's own swings bury any grading that is not on the break's distance.

## Ideas
- `032-02.b1.e1.e2.b1_narrow-clear-breakouts-keep-rising` (from F3, F4, F5, F6, F1): In a coin that closes above its prior 60-day closing high, the smaller the margin by which that close clears the high, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
