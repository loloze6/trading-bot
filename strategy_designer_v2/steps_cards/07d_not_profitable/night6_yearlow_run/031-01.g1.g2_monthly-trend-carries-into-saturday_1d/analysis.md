---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g2_monthly-trend-carries-into-saturday_1d
idea tested: 031-01.g1.g2_monthly-trend-carries-into-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5438 USD
---
## Findings
- **F1:** The losses sit on the short side: short cases (20-day fall at Friday's close) earn a signed excess of -0.03 % per case (n 1298) and +0.008 % per case in position gain, and short trades lose -0.30 % net per trade (1127 trades). Long cases earn +0.61 % signed excess per case (n 1180), and long trades gain +0.52 % net per trade (1035 trades), about 3.2 times the 0.19 % cost of a trade.
- **F2:** Rebuilding the Friday-to-Saturday book approximately, dropping the short side lifts Calmar from 0.45 to 0.72, the yearly return from +6.6 % to +8.9 % and the deepest fall from -14.8 % to -12.5 %. Keeping only the long cases with forecast of 5 or more gives Calmar 0.72 with a -12.5 % fall, while 33 % of days are in a position. These approximate figures are close to the 0.75 threshold but do not clear it.
- **F3:** The Saturday move follows the 20-day return in a graded way. By Friday 20-day return tercile, Saturday's excess is -0.24 % (mean 20-day return -19 %), +0.27 % (-1 %) and +0.71 % (+26 %), with 690 cases each. On the other weekdays the same terciles give only -0.03 %, -0.12 % and +0.07 % (about 4,140 each). So the 20-day gain alone, without the Friday close, carries almost nothing.
- **F4:** Being long every Friday at a flat size, without the signal, gives Calmar 0.23 and a -30 % deepest fall. All Friday-to-Saturday cases together have an excess of +0.30 % (t 3.76, n 2479). The day-of-week condition alone is therefore not the paying book; the grading by the 20-day gain is what cuts its falls.
- **F5:** The effect is largest in the strongest long cases. Longs in the top |forecast| tercile earn a signed excess of +0.98 % and a position gain of +1.01 % per case (n 478). Longs in the lowest tercile earn +0.29 % excess and +0.01 % gain (n 362). Shorts in the lowest tercile earn -0.57 % excess (n 464).
- **F6:** The deepest fall (w19 to w21, 2024, 242 days, -14.9 %) came in calm markets with larger positions. Its 210 cases had a signed excess of -0.45 % against +0.35 % for the rest. Their 20-day volatility was 3.4 % against 4.5 %, and their mean absolute allocation 0.55 against 0.47: the volatility target levered up just when the effect was absent.
- **F7:** The long side holds across years: its excess is negative only in 2018 (-0.19 %, n 67) and 2023 (-0.15 %, n 144), and ranges from +0.30 % to +1.42 % in the other six years.

## Ideas
- `031-01.g1.g2.d1_monthly-gain-lifts-saturday` (from F1, F2, F3, F5, F7): The higher a coin's gain over the past 20 days at Friday's close (UTC), the more it rises over the next day, Saturday, this holding only when that 20-day return is a gain, so that a 20-day fall says nothing about Saturday.
- `031-01.g1.g2.d2_outsized-monthly-gain-into-saturday` (from F2, F3, F5, F6): The higher a coin's gain over the past 20 days at Friday's close (UTC), measured against the coin's usual 20-day moves, the more it rises over the next day, Saturday, the rise growing faster than the gain in the coin's largest 20-day gains.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
