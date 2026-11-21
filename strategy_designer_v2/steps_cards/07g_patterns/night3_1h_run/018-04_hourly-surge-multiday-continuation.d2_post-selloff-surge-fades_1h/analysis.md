---
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
idea tested: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3836 USD
---
## Findings
- **F1:** A sharp 24-hour fall is followed by a rebound. On a daily grid of all six coins, the bottom decile of the 24-hour return measured in the coin's 30-day mean absolute 24-hour return beats the coin's normal drift by +0.70 % over the next 24 hours (t 4.30, 1408 cases), +0.82 % over 48 hours and +0.77 % over 72 hours (t 3.25). The second decile beats it by +0.34 % over 24 hours (t 2.59). The middle deciles are near 0 to -0.16 %.
- **F2:** The rebound is graded and appears in every coin. On days with a 24-hour fall, the deeper the fall, the larger the next-24-hour excess return. The Spearman rho on the 24-hour return is -0.066 to -0.157 for all six coins, and every p is below 0.025 (XRP p 4e-8, ETH 6e-4, XMR 1.6e-3, ZEC 1.7e-3, LTC 0.013, BTC 0.024).
- **F3:** The rebound holds in both halves of the windows. In the bottom two deciles, the 24-hour excess is +0.53 % in w1–w12 (t 4.34, 1385 cases) and +0.51 % in w13–w24 (t 3.02, 1431 cases). This makes it the most robust of the roughly 15 angles examined.
- **F4:** The rebound grows with the coin's 30-day volatility. Over 24 hours after the bottom two deciles of the 24-hour return, the excess is -0.002 % in the lowest volatility tercile (t -0.01, 969 cases), +0.35 % in the middle tercile (t 2.19, 982) and +1.30 % in the highest (t 5.17, 865). The top tercile's move is about 6.8 times the backtest's 0.19 % round-trip cost, against 3.7 times for the 0.70 % decile average.
- **F5:** The rebound does not depend on the prior 7-day trend. After the bottom two deciles of the 24-hour return, the 24-hour excess is +0.46 % when the 7-day return was negative (t 3.42, 1951 cases) and +0.67 % when it was positive (t 4.25, 863).
- **F6:** The tested idea's own situation, a large up surge after a 7-day fall, shows no fade. On a 120-hour grid, a surge above 2 usual moves after a negative prior 7-day return is followed by +0.39 % excess over 120 hours (t 0.31, 85 cases). After a positive prior 7-day return it is followed by +3.5 % (t 1.96, 92 cases). The verdict's +0.32 % unusual move at t 0.74 matches this.
- **F7:** A strong 7-day rise tends to continue over the following 5 days, but the evidence is weak. The top quintile of the 7-day return in 30-day volatility units beats the coin's drift by +1.47 % over the next 120 hours (t 2.57, 506 cases), while the other four quintiles lie between -0.66 % and -0.11 %. The effect sits mostly in w13–w24 (t 5.42) rather than w1–w12 (t 1.41).
- **F8:** The calendar patterns are clear but too small or not graded. Friday's next-24-hour excess is +0.48 % (t 4.56, positive in all six coins, t 1.40 to 2.92) and Thursday's is -0.48 % (t -4.01). The 20:00 and 21:00 UTC hours earn +4.8 and +3.7 bps (t 5.98 and 4.85), which is below a round trip in line with the earlier finding F2.

## Ideas
- `018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.g1_sharp-daily-fall-rebounds` (from F1, F2, F3, F4, F5): The more a coin's 24-hour return falls below zero, measured against its 30-day average absolute daily return, the more its price rises above its usual drift over the next 1 to 2 days. The rebound is larger the higher the coin's 30-day volatility.
- `018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades.g2_strong-week-keeps-rising` (from F6, F7): The larger a coin's 7-day return, measured against its 30-day volatility, the more its price rises above its usual drift over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
