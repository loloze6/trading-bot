---
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
idea tested: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3958 USD
---
## Findings
- **F1:** Across all 6 coins, a coin's daily return scaled by its 20-day volatility predicts the next day's excess return with the opposite sign: the pooled slope is +0.16 % of next-day return per unit of fall, t 4.03 on 14,356 days. The effect holds in both halves of the windows (w1–w12 t 3.63, w13–w24 t 2.23), is positive on all 6 coins, and is strongest on XMR (t 4.46) and ETH (t 2.22).
- **F2:** That next-day reversal is mostly a rebound after falls. After a day down more than 1 volatility unit, the next day's excess return is +0.50 % (1,804 days), against −0.05 % after a day up more than 1 unit (1,983 days). After a fall of 1–2 units the t is 3.57 (1,444 days); after a fall of more than 2 units it is +0.61 % with t 2.00 (400 days). These one-day moves are 2.6 to 3.2 times the backtest's 0.19 % round trip.
- **F3:** A coin's past 5-day return predicts its excess return over the next 26 days on non-overlapping grids: slope +4.7 % per standard deviation, t 2.95 on 432 cases. The top quintile gives +9.2 % and the bottom −2.5 %. All 6 coins have a positive slope (lowest coin t 0.26), but the effect sits mostly in w13–w24 (t 3.02) against w1–w12 (t 1.08). It also shows over the next 10 days (t 2.95, 1,547 cases).
- **F4:** The past 26-day return also predicts the next 26 days (t 2.79, 432 cases), but its sign flips between halves (w1–w12 t −0.44, w13–w24 t 3.62). Over 10 days its early half is flat (t 0.03). It is not a stable pattern, unlike the shorter 5-day lookback in F3.
- **F5:** The tested regime does select better periods: in-regime grid cases have a 26-day excess return of +4.8 % (149 cases) against −1.7 % outside (427). Inside the regime, however, the thickness forecast leans the wrong way (t −1.62 on 107 cases). The past 26-day return (t 1.92) and the distance above the 26-day mean (t 1.84) grade the outcome better than thickness does.
- **F6:** Next-day excess returns by weekday are negative after Tuesday's and Thursday's bars (t −2.57 and −2.53, about 2,070 days each). Out of the roughly 15 angles examined, this does not stand out enough to count as a pattern.
- **F7:** The book earned a mean daily return of 0.033 % against 0.119 % for holding the coins (17,380 coin-days). It was flat on most days (interquartile range of daily returns 0 to 0), so it missed most of the coins' drift.

## Ideas
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.g1_sharp-daily-fall-rebounds-next-day` (from F1, F2): The more a coin's daily return falls below zero, measured against its recent 20-day volatility, the more the coin rises over the next day above its normal drift.
- `021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.g2_last-week-s-move-continues-monthly` (from F3, F4, F5): The larger a coin's 5-day return, the larger its return over the next 26 days above its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
