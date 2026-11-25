---
line: 7.b inconclusive
backtest: 046-01_falling-market-scaled-rise-fade_1d
idea tested: 046-01_falling-market-scaled-rise-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2061 USD
---
## Findings
- **F1:** The tested fade points the way the idea predicts but is too small for this data to show clearly: step 5's |forecast|-weighted next-day unusual move is +0.28 % with a day-clustered t of 1.51 over 2,951 cases on 1,126 days, and its size is +0.25 % per case (t 1.42, 860 days), 0.058 of a usual move, which is the strength real ideas usually show.
- **F2:** In folds B and C the fade after up days in the falling profile is positive on all six coins, 0.13 % to 0.78 % next day. Four coins reach a day-clustered t above 2 on their own: BTC 0.70 % (t 2.30, 201 cases), ETH 0.68 % (t 2.02), LTC 0.78 % (t 2.61) and XMR 0.71 % (t 2.01). XRP is the weakest at 0.13 % (t 0.32, 248 cases).
- **F3:** The fade is uneven over time and lies mostly in the falling years 2018 and 2019. It is 1.03 % in 2018 (t 2.03, 575 cases) and 0.63 % in 2019 (t 2.16, 321 cases), against 0.10 % in 2020 (t 0.21) and -0.10 % in 2021 (t -0.17). By window it ranges from -5.36 % (13 cases) to +1.62 % (188 cases).
- **F4:** The move is not graded by the size of the rise. Across the five quintiles of the scaled up day in the falling profile, the next-day fade is 0.75 %, 0.44 %, 0.72 %, 0.29 % and 0.64 % from smallest to largest rise (about 278 cases each, t 0.70 to 2.16). This matches step 5's negative supporting slope of -2.4e-05.
- **F5:** The fade is not confined to the falling market, which the brief requires it to be. After up days it is also present in the choppy profile at 0.44 % (t 2.13, 1,787 cases), against 0.58 % (t 1.77, 973 cases) in the falling profile and -0.36 % (t -1.27, 908 cases) in the rising profile.
- **F6:** The fade lasts one day only. Over two days after up days in the falling profile the unusual move is 0.31 % (t 0.88, 1,375 cases), no larger than the one-day move, so the plan's one-day horizon is where the effect shows.
- **F7:** The rebound after down days in the falling profile is graded, though it is not significant in any quintile. From the largest fall quintile to the smallest it is 1.16 % (t 1.72), 0.59 % (t 1.77), 0.41 %, -0.16 % and -0.21 %, 316 cases each.
- **F8:** More data is available than the test used. The test ran only the six default coins, while thirteen more coins have daily bars in folds A and D and partly in B and C (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO). Adding them would raise the number of falling-market up-day cases behind a result that F1 shows is short of the bar only in t.

## Ideas
- `046-01.b1_falling-market-rise-fade-more-coins` (from F1, F2, F6, F8): In a falling market, after an up day, a coin falls over the next day, and the larger that day's rise in units of its 30-day daily-return swing, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
