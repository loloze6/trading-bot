---
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
idea tested: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4257 USD
---
## Findings
- **F1:** The tested idea's edge lives at short horizons. Among 24-hour falls only (non-overlapping 1-day grid), the slope of the scaled 1-day excess return on fall depth has t 5.90 over 7706 cases. The deepest fifth (mean depth 2.54 usual moves) earns +0.59 % above drift (t 4.04) and the next fifth +0.38 % (t 3.03), against -0.13 % for the shallowest. This 1-day move in the deepest fifth is about 3 times the 0.19 % cost of a trade.
- **F2:** The rebound after a deep 24-hour fall holds across coins and years at the 1-day horizon. The falls-only slope is positive in 5 of 6 coins (t 1.99 ETH, 1.85 LTC, 2.18 XMR, 4.26 XRP, 4.94 ZEC; BTC -0.18) and in all 8 years (t 2.8 in 2018, 4.3 in 2021, 2.5 in 2024, 2.9 in 2025, only 0.4 in 2022).
- **F3:** The rebound fades with the horizon:
- **F4:** The 1-day reversal is one-sided, on falls only. Over all bars the slope of the 1-day excess on the 24-hour scaled return is t -6.69 (n 15793), but on rises alone it is t -0.98 (n 8069).
- **F5:** The 4-hour bar that opens at 08:00 UTC reverses in the next 4-hour bar, graded by its size. The slope of the next bar's scaled excess return on this bar's scaled return is -0.053 (t -8.34, n 16077). This is the strongest of the six bar hours; the next are 20:00 UTC at t -5.23 and 00:00 UTC at t -4.27, while 04:00 and 12:00 UTC show continuation (t 2.78, 3.57).
- **F6:** Returns differ by bar hour, but the effect is unstable across years:
- **F7:** The day starting Friday 00:00 UTC earns +0.40 % above drift (t 4.33, n 2478), positive in all 6 coins. It is unstable by year, though: t 6.29 in 2019 and -1.92 in 2022.
- **F8:** The book mostly tracked holding the coins. Its daily mean beat holding in only 5 of 8 years and fell short in 2021 (0.25 % vs 0.41 %). This fits a 14-day long position whose signal adds nothing at 14 days.

## Ideas
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.g1_deep-fall-short-rebound` (from F1, F2, F3, F4): The deeper a coin's 24-hour fall, measured in its usual 24-hour moves of the last 30 days, the more it rises above its normal drift over the next 1 to 3 days.
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.g2_morning-move-reverses-afternoon` (from F5): The larger a coin's move over the 4 hours from 08:00 to 12:00 UTC, measured in its usual 4-hour moves of the last 30 days, the more it moves the opposite way over the following 4 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
