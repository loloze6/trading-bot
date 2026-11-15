---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3193 USD
---
## Findings
- **F1:** The 50/200 spread forecast predicts almost nothing at any horizon: the pooled slope's t is 0.20 at 5 days (3349 cases), 0.37 at 10 days (1657), 0.55 at 20 days (811) and -0.06 at 40 days (388), and forward 10-day excess returns are 0.0005 with the forecast on against -0.0005 with it off (Welch t 0.14, 832 vs 825 cases).
- **F2:** Within the forecast-on bars, the coin's own 20-day return separates what follows. When it is up, the 10-day excess return is +0.0221 (361 cases); when it is down, it is -0.0171 (333 cases), Welch t 3.00. The graded slope on the per-coin z-scored 20-day return is 0.0150 with t 2.25 (694 cases).
- **F3:** The same 20-day momentum shows nothing while the 50-day SMA is below the 200-day SMA: the slope's t is -0.73 and up minus down is -0.0037 vs +0.0002 (t -0.40, 681 cases). Pooled over all bars it is only t 2.17, so the effect lives in the uptrend state.
- **F4:** The size of the forecast is not graded. Across forecast quartiles the 10-day excess returns run -0.0094, +0.0049, +0.0060 and +0.0006, with hit rates of 0.47 to 0.51, below the 0.53 of off bars. The widest raw-spread sixth has -0.0069 against +0.0078 just around the cross.
- **F5:** The effect is mixed across coins and years:
- **F6:** Uptrend age matters mildly. In the first 20 days of the on state the 10-day excess return is -0.0058 (304 cases), against +0.0066 at 20 to 60 days (328) and +0.0002 at 60 to 150 days (200), so fresh crosses do not drift upward.
- **F7:** The book's mean daily return of 0.000377 is almost entirely market exposure. The position times the coin's mean daily return gives 0.000353, against 0.000025 of timing, at a mean position of 0.28.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends` (from F2, F3, F4, F7): While a coin's 50-day SMA is above its 200-day SMA, the higher the coin's own 20-day return, the larger its return over the next 10 days.
- `002-01_sma-golden-cross-upward-drift.b2_matured-uptrend-outperforms-fresh-cross` (from F6, F1): While a coin's 50-day SMA is above its 200-day SMA, the longer it has stayed above over the past 20 to 60 days, the larger the coin's return over the next 10 days, relative to the days right after the cross.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
