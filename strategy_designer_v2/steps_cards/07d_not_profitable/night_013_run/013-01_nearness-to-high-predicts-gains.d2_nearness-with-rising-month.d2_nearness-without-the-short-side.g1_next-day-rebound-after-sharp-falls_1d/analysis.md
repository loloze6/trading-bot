---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3382 USD
---
## Findings
- **F1:** The rebound and the book's gain sit almost entirely in high-volatility states, and calm states lose after fees: among forecast>0 bars, the top quartile of 20-day volatility (mean 0.074) gives a next-day excess return of +0.0074 (t 4.69, n 1788) and a net gain of +0.0030 per bar, while the bottom quartile (vol 0.022) gives −0.0013 (t −1.57) and a net of −0.00066, its fee of 0.00065 per bar eating the whole gain.
- **F2:** Volatility rising against its own longer level marks the paying states: in the top quartile of 20-day over 60-day volatility (ratio 1.27) the next-day excess is +0.0062 (t 5.10, n 1788) with a net of +0.0033, while in the bottom quartile (ratio 0.65) it is −0.0019 (t −1.72) with a net of −0.00059.
- **F3:** The forecast's slope on next-day excess return holds only in high volatility, with t 3.49 (slope 0.00054, n 3575) above the median 20-day volatility against t 1.06 (slope 0.00010, n 3576) below it.
- **F4:** The weak half of the forecast costs more in fees than it earns, dragging the mean daily return under its 0.0005 bar: the two lowest forecast quintiles net −0.000078 and −0.000051 per bar (gain 0.00010 and 0.00021 against fees 0.00018 and 0.00026), while the top two net +0.0016 and +0.0035; overall fees are 0.00035 per bar against a gross gain of 0.00080.
- **F5:** The book's falls come from being long in calm downtrends: its worst decile of days (−0.023 on average) holds a mean position of 0.68 with a 20-day coin return of −0.048, and the 785 days spent more than 15% under its peak have lower volatility (0.039 vs 0.045), a falling 20-day return (−0.019 vs +0.044) and a larger position (0.26 vs 0.21) than the other days, which pushes the deepest fall to −30.7% and Calmar to 0.43.
- **F6:** The rebound pays at the two extremes of the coin's 20-day trend and not in the middle: forecast>0 bars give +0.0035 excess where the 20-day return is −25% and +0.0045 where it is +28%, against −0.00035 and −0.0006 in the two middle quartiles; scaled by volatility, the strongest absolute 20-day moves give +0.0043 (t 3.39) against +0.0005 (t 0.54) for the weakest.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.d1_rebound-in-expanding-volatility` (from F1, F2, F3, F5): The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day, and the more so the higher its 20-day volatility of daily returns stands against its own 60-day volatility.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.d2_rebound-inside-strong-trends` (from F6, F5, F4): The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day, and the more so the larger the coin's 20-day return in absolute size measured in its own 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
