---
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
idea tested: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6416 USD
---
## Findings
- **F1:** In coins whose 90-day return is not negative, the 5-day unusual move after a day's rise grows with the rise measured in 20-day standard deviations: −0.77 % (t −2.08, 1092 cases) for 0–1 units, +1.42 % (t 1.77, 247) for 1–1.5, +2.31 % (t 2.29, 163) for 1.5–2 and +8.58 % (t 2.65, 134; winsorised +5.91 %, t 4.05; median +2.35 %, 66 % of cases positive) above 2, a strength of 0.55 of the coin's usual 5-day move in the top bucket.
- **F2:** That grading in rising coins is steady across years and coins: over the 1636 rising-coin up-day cases, the Spearman correlation of the rise with the 5-day unusual move is 0.124 and stays between 0.10 and 0.14 when any one year is left out; 17 of 19 coins have a positive median after rises above 1.5 units; averaged per day it is still +4.65 % with t 2.31 over 126 independent days.
- **F3:** The fade that the tested idea relies on does not hold up. In falling coins, rises above 2 units are followed by −3.77 % over 5 days (t −2.72, 79 cases), but one year carries it: −12.9 % (t −6.34, 24 cases) in 2025 against +7.6 % (t 3.15) in 2021 and +2.2 % in 2023. Averaged per day it is only −1.07 % (t −0.68, 71 days), and the correlation of the rise with the next 5 days' move is −0.04 to −0.08.
- **F4:** The book loses on the coins' drift and not on its timing: per bar the position earns −0.0112 %, of which −0.0294 % is the market's own rise against a short held on 44 % of the bars, while timing adds +0.0182 %. That matches step 5's size: total move −0.14 % per case against a cost of 0.22 %.
- **F5:** Among rising coins with a rise above 1 unit, the following 5-day move is larger the larger the 90-day gain: −0.91 % for a 90-day gain of 0–20 %, +0.74 % for 20–50 %, +2.51 % for 50–100 % and +16.7 % above 100 % (winsorised t 2.54, 40 cases). This is suggestive only, on few cases.
- **F6:** Two other patterns did not survive averaging per day, so I give them no weight. The rebound after a 90-day fall of more than 50 % (+3.15 %, t 2.62, 139 cases) drops to t 0.16 over 41 days. The weekday pattern of next-day moves has every weekday's |t| below 1.91 once averaged per day.

## Ideas
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.g1_rising-coin-breakouts-keep-going` (from F1, F2, F4): In a coin whose 90-day return is positive, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, and the larger that rise in units of the usual daily move, the larger the rise that follows.
- `025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.g2_stronger-trend-stronger-continuation` (from F1, F5): In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a larger rise over the next 5 days the larger the coin's 90-day gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
