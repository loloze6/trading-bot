---
line: 7.g patterns
backtest: 072-03.b1.b1_deep-bounce-fades-more-coins_1d
idea tested: 072-03.b1.b1_deep-bounce-fades-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4641 USD
---
## Findings
- **F1:** Across all bars outside the choppy profile, the next-day move after an up day falls step by step with the close's depth below its 20-day high, in units of the 20-day daily swing. By depth quintile, from deepest to shallowest, the move net of drift is -1.13 % (t -4.58, 597 cases), -0.49 % (t -2.70, 791), -0.43 % (t -2.27, 750), -0.15 % (t -0.88, 813) and +0.26 % (t 1.35, 1406).
- **F2:** The deepest up days fall the next day in every trend, though the effect is clearest in choppy markets. Measured with day-clustered t, the deepest quintile's next-day move net of drift is -1.45 % in choppy (t -2.11, 72 days), -1.05 % in falling (t -1.80, 136 days), -1.31 % with the trend unknown (t -1.36) and -0.81 % in rising (t -1.21).
- **F3:** The gap between the deepest and shallowest up-day quintiles is negative in every year explored: -1.15 % in 2018, -0.28 % in 2019, -1.83 % in 2020 and -1.65 % in 2021.
- **F4:** After down days the same depth predicts nothing the next day. In choppy markets the deepest quintile's next-day move is -0.09 % (t -0.10, 132 days), and every choppy and falling quintile has |t| < 1.2. The fade belongs to up days.
- **F5:** The book loses on its shallow positions. Its gain per held bar is +0.42 % in the deepest raw-depth quintile (t 2.67, 658 bars), then +0.02 %, -0.13 %, -0.20 % (t -2.38) and -0.79 % (t -1.37) in the shallowest. The forecast's 60-bar standardisation shorts closes that are only shallow in absolute terms.
- **F6:** In choppy markets the move over 10 days after up days sits on the same depth gradient but on few cases. The two deepest quintiles move -13.8 % (t -3.85, 10 days) and -12.9 % (t -3.08, 10 days), while the shallowest quintile moves +16.0 % (t 1.36, 14 days).
- **F7:** In choppy markets the next-day fade also concentrates at the deep end rather than growing smoothly. The Spearman correlation between depth and the next-day move on choppy up days is only 0.024 (890 cases): the deepest quintile carries the effect (-1.45 %) and the others sit between -0.48 % and +0.04 %.

## Ideas
- `072-03.b1.b1.g2_choppy-deep-bounce-next-day` (from F2, F5, F7): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-03.b1.b1.g1_deep-bounce-next-day-fade` (from F1, F2, F3, F4): On a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
