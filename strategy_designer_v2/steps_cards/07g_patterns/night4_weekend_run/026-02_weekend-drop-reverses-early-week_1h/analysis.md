---
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week_1h
idea tested: 026-02_weekend-drop-reverses-early-week
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3609 USD
---
## Findings
- **F1:** The tested idea fails in the opposite direction, but not only at weekends. After a weekend fall, the next 48 hours from Monday 00:00 run 0.63 % below the coin's normal drift (t -2.83, 2331 coin-weeks). The second weekend-return quintile is the worst, at -1.09 % (t -3.52, 466 cases), while the deepest quintile is flat (+0.05 %). Yet the slope of the next 48 hours on the past 48 hours is not significant on Monday (t -1.24). Sunday 00:00 shows a similar drop after falls (-0.42 %, t -2.15). Weekend drops do not reverse, and the weakness is not specific to the weekend.
- **F2:** Hours 21 and 22 UTC have the largest hourly mean returns of the day: +0.055 % (t 6.87, 17417 bars) and +0.044 % (t 5.76, 17359 bars). Every other hour averages about 0, between -0.035 % and +0.027 %. With 24 hours examined, this still stands out.
- **F3:** The late-evening rise is broad. It is positive in all 6 coins (t 3.04 to 4.56, means +0.043 % to +0.056 % per hour), in 7 of 8 years (t 1.9 to 5.7; only 2022 is negative, -0.022 %, t -1.46) and on all 7 weekdays (t 1.98 to 4.02). Outside those two hours the hourly mean is near 0 in every year (t between -2.6 and +2.5).
- **F4:** The late-evening rise is graded by the coin's prior 24-hour fall. In the deepest-fall quintile (mean 24h return -5.9 %), hours 21–22 rise +0.122 % per hour (t 7.08, 6898 bars). That falls to +0.038 %, +0.026 % and +0.008 % across the next three quintiles. The top quintile (+6.4 %) shows +0.055 % (t 3.70).
- **F5:** The late-evening rise is also graded by recent volatility. When the past 24 hours' volatility is high against the past 30 days (top quintile, ratio 1.60), hours 21–22 rise +0.117 % per hour (t 6.12, 6494 bars). The calmest quintile (ratio 0.45) rises only +0.019 % (t 2.29), and the middle quintiles show +0.034 % to +0.038 %.
- **F6:** A Wednesday–Thursday rise is followed by a Friday–Saturday rise, from Friday 00:00. The pooled slope of the next 48 hours on the past 48 hours is +0.070 (t 4.15, 2337 cases), the strongest of the seven days, where the others range from t -1.24 to +1.08. The top past-return quintile (+10.0 %) is followed by +1.20 % above drift (t 3.53, 470 cases), and the bottom quintile by +0.10 %. The slope is positive in 5 of 6 coins, but only in 5 of 8 years (2019, 2020 and 2023 negative, t -1.9, -1.6, -2.4), so it is less stable than F2–F5.
- **F7:** The move per case is small against the cost of a trade, 0.19 %. The late-evening mean is about 0.05 % per hour, or about 0.10 % over the two hours. Only in its strongest situation, after a deep 24-hour fall, does it reach about 0.12 % per hour, or about 0.24 % over the two hours. Only there does it exceed one trade's cost.

## Ideas
- `026-02_weekend-drop-reverses-early-week.g1_late-evening-rebound-after-falls` (from F2, F3, F4, F7): Over the two hours from 21:00 UTC, a coin rises, and the deeper its fall over its previous 24 hours, the larger that rise.
- `026-02_weekend-drop-reverses-early-week.g2_late-evening-rise-after-turbulence` (from F2, F3, F5, F7): Over the two hours from 21:00 UTC, a coin rises, and the higher its volatility over its past 24 hours relative to its past 30 days, the larger that rise.
- `026-02_weekend-drop-reverses-early-week.g3_midweek-rise-carries-into-weekend` (from F6): When a coin rises over Wednesday and Thursday (its 48-hour return at Friday 00:00 UTC), it keeps rising over Friday and Saturday, and the larger the midweek rise, the larger the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
