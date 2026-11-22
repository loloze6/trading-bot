---
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3658 USD
---
## Findings
- **F1:** The book's gain comes from its long side only: long bars earned a mean +0.116 % per bar (sum +9.41 over 8106 bars), while short bars, more than half the book's time, lost a mean −0.037 % per bar (sum −3.38 over 9246 bars). The book is also flat on 172 bars.
- **F2:** On the 5-day grid, the short cases have a positive unusual move (+0.57 % per case when the 30-day trend was down, n 1459, t 2.1; +0.78 % when it was up, n 313). The coin's upward drift cancels it, so their total move is nil: −0.02 % and +0.19 %. That is no more than the 0.19 % cost of a trade. The long cases' total move is +0.76 % (n 636) and +1.54 % (n 1010).
- **F3:** The book's deepest fall was −50.8 % over 397 days in w19–w22. Over that stretch the book was short on 55 % of days, with a mean position of −0.03. Holding the coins gained +11.7 % and the coins' 90-day return averaged +34 %. The fall is the short side fading rising coins, which is what fails the Calmar of 0.07.
- **F4:** Short bars lost when the coin's 90-day return was up: −0.018 % per bar, sum −0.17 over 968 bars. They earned +0.075 % per bar (sum +0.99, 1318 bars) when it was down. Long bars earned in both: +0.129 % (868 bars) when the 90-day return was down and +0.064 % (1266 bars) when it was up.
- **F5:** The long cases carry the effect mainly when the coin's 30-day return is up: unusual move +0.95 % per case, t 2.7, n 1010. When it is down the figure is +0.18 %, t 0.35, n 636.
- **F6:** The book's mean daily return is 0.022 % against holding's 0.111 %, with a daily standard deviation of 1.56 % against 4.00 %. Its turnover costs about 0.013 % per bar against a gross 0.035 % per bar, so fees take about 40 % of the gross gain. Most of the rest is lost on the short side.
- **F7:** The effect is not steady across years. The directed unusual move was +1.0 % to +1.8 % per case in each year from 2018 to 2021, about −0.4 % in each of 2022 and 2023, and +0.04 % in 2024 and +0.36 % in 2025.

## Ideas
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation` (from F1, F2, F3, F4, F6): The farther a coin's close sits above the middle of its 30-day closing range, the larger its rise over the next 5 days; the flatter the 30 days were (the smaller the net move against the range), the larger that rise.
- `023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d2_upside-breakout-in-rising-months` (from F5, F1, F2): The farther a coin's close sits above the middle of its 30-day closing range, the larger its rise over the next 5 days, the flatter the 30 days were the larger that rise, only while the coin's 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
