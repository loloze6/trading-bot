---
line: 7.b inconclusive
backtest: 031-03.b1_up-streak-continuation-more-coins_1d
idea tested: 031-03.b1_up-streak-continuation-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3783 USD
---
## Findings
- **F1:** The tested slope is essentially zero (0.000184, day-clustered t 0.54, 6157 grid bars on 617 days), and the bets' mean unusual 5-day move is the wrong sign (−0.27 %, t −0.87 over 1362 days), so the pooled effect is too small and too mixed to show either way.
- **F2:** The effect splits by the coin's own 30-day return. While the 30-day return is positive, the mean 5-day excess return rises steadily with the forecast: +0.04 % at forecast 0 (1069 bars), +0.34 % at 5–10 (302), +0.85 % at 10–15 (314) and +1.41 % at 15–20 (661). The slope there is 0.000658 (t 1.42, 2346 bars, 365 days), and bets with forecast > 0 average +1.02 % (t 1.46, 1277 bars, 273 days).
- **F3:** While the 30-day return is zero or negative, the same streak forecast points the other way: slope −0.000434 (t −0.80, 2257 bars, 368 days), and bets with forecast > 0 average −1.09 % (t −1.24, 1022 bars, 241 days). The two halves cancel in the pooled test.
- **F4:** Letting the 30-day trend's sign set the sign of the streak's effect (up-streak length × sign of the 30-day return) gives a slope of 0.0044 with day-clustered t 2.64 (4603 bars, 466 days). This is the first reading with t above 2.
- **F5:** Inside the positive 30-day trend, the streak slope is positive in 7 of 8 years (t 2.53 in 2019), but only 2025 is slightly negative (slope −0.000368, t −0.23). The mean of the bets by year still swings: +5.99 % (t 3.33) in 2021 against −7.21 % (t −3.30) in 2018. The grading is steadier than the level.
- **F6:** No coin shows the tested effect on its own: the mean 5-day excess return after up streaks lies between t −1.20 (LINK) and t +1.41 (ZEC) for all 19 coins. No more data is available either, since the test already used all 19 coins over folds A–D on daily bars.
- **F7:** At other horizons, raw up-streak length gives no steady ordering at 5 days (streak 3: +1.10 %, t 1.71; streak 4: −0.91 %, t −1.07). The plan's horizon did not miss a cleaner effect elsewhere, apart from a short one-day giveback after a single higher close (−0.21 %, t −3.84).

## Ideas
- `031-03.b1.b1_up-streak-continuation-in-uptrend` (from F2, F3, F4, F5): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 5 days, only while its 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
