---
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
idea tested: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4512 USD
---
## Findings
- **F1:** The two failing measures sit together: the mean daily return is 0.00028 against the 0.0005 asked, and the Calmar is 0.48 against 0.75. The deepest fall is 20.5 %, running 308 days from w1 to w3. In those windows both the book (mean daily -0.00066, -0.00042, -0.00041) and the coins (-0.0028, -0.0034, -0.0017) lost, and the windows' own falls reached 8 %, 14 % and 21 %.
- **F2:** The rebound depends on the coin actually rising around the case. Cases in windows where the coins' 18-bar mean was negative lost -1.51 % of unusual move (-1.06 % total, 639 cases). Cases in the other windows gained +1.62 % (+2.09 % total, 1349 cases). This split is not known at a bar's close, so it explains the falls but cannot be traded directly.
- **F3:** The sharpness of the coin's past-day fall, against its 30-day typical 4h move, separates the cases much more strongly than the range width does.
- **F4:** The coin's 6-day volatility against its 30-day volatility, known at the close, also grades the rebound. The highest quintile (ratio 1.35) gives +2.84 % unusual move and the lowest (ratio 0.61) gives -1.10 %, with 398 cases each.
- **F5:** The width the book is sized by grades unevenly. Its quintiles give +0.58 %, -0.58 %, +0.14 %, +1.16 % and +1.97 %, so the book's size is spread over cases that earn nothing.
- **F6:** Weakly rising coins with a mild or middling break lose money.
- **F7:** Costs do not explain the failure; the book is simply small.

## Ideas
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins.d1_sharp-breakdown-rebound-uptrend` (from F1, F3, F5, F6, F7): When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The sharper the coin's fall over the past day, compared with its typical four-hour move over the past 30 days, the larger the rise.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins.d2_turbulent-breakdown-rebound-uptrend` (from F1, F2, F4, F5): When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The higher the coin's volatility over the past 6 days compared with its volatility over the past 30 days, the larger the rise.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins.d3_sharp-dip-strong-uptrend` (from F1, F2, F3, F6): When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The larger that 30-day return is against the coin's typical 30-day move, and the sharper its fall over the past day, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
