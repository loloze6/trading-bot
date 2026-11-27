---
line: 7.d confirmed, not profitable
backtest: 081-01.d2_deepest-up-days-carry-fade_1d
idea tested: 081-01.d2_deepest-up-days-carry-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6327 USD
---
## Findings
- **F1:** The book loses in a rising market, and that is where the failed Calmar and the failed edge over holding come from. Its position bars earn -0.045 % per bar in a rising 60-day trend (766 bars), against +0.46 % in a falling trend (951 bars) and +0.50 % in a choppy one (312 bars). The deepest up days carry no fade in a rising market: the short-signed excess is +0.02 % (t 0.06, 238 cases) in rising calm and -0.14 % (t -0.25, 84 cases) in rising agitated.
- **F2:** The book's deepest fall on folds B and C came during a strong market rise. It lasted 194 days across 3 windows and took the book down 21.4 % while holding the coins chained +867 % (a mean of +1.32 % a day). In every window the book's daily returns move against holding (correlation -0.39 to -0.72). On the fifth of days when the coins rise most (mean +6.6 %), the book loses -0.77 %.
- **F3:** The rebuilt book is the step 6 book with the rising-market bars removed, at 0.11 % per side; it is a rebuild, so its levels differ from step 6. Outside a rising market its Sharpe goes from 0.90 to 1.09, its Calmar from 1.04 to 1.51 and its deepest fall from -21.6 % to -17.6 %. Holding the coins has a Sharpe of 0.84 on these folds.
- **F4:** The condition alone does not earn the short, so excluding the rising market is not an effect of its own. On down days in a falling or choppy market, with no signal, the short-signed next-day excess is:
- **F5:** The fade is graded in depth and lives on up days only. Up days in the deepest depth quintile fade +0.95 % beyond drift (t 5.26, 1050 cases), and the shallowest quintile rises instead (-0.23 %, t -0.98). Down days in the deepest quintile show -0.62 % (t -1.40).
- **F6:** The book's small positions lose to fees.
- **F7:** The fade is strongest in a falling, agitated market.
- **F8:** The fade holds in every year of folds B and C but is uneven. The short-signed excess on the deepest up days is +1.64 % in 2018 (t 4.70), +0.56 % in 2019 (t 2.26), +0.61 % in 2020 (t 1.05) and +0.69 % in 2021 (t 2.02).

## Ideas
- `081-01.d2.d1_deep-up-day-fade-outside-rises` (from F1, F2, F3, F4, F5): Except in a rising market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, the fall growing faster than the depth so that the up days furthest below the high carry most of it.
- `081-01.d2.d2_deepest-up-days-fade-only` (from F1, F4, F5, F6): Except in a rising market, a day that closes up while sitting far below the coin's 20-day high, in its own 20-day daily swings, is followed by a fall over the next day. The fall is carried by the up days furthest below the high and grows with that depth, while up days near the high are followed by no fall.
- `081-01.d2.d3_deep-up-day-fade-falling-market` (from F1, F4, F7): In a falling market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, the fall growing faster than the depth.
- `081-01.d2.d4_agitated-falling-relief-fade` (from F4, F7): In a falling, agitated market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, the fall growing with the depth.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
