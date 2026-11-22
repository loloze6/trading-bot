---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.7233 USD
---
## Findings
- **F1:** Coins after the deepest 30-day falls rebound instead of continuing down. In the bottom twentieth of 30-day returns (falls of 35 % to 43 %, mean −42.6 %), the next 5 days' drift-excess return was +2.78 % (median +1.03 %, 55 % positive, t 3.15, 272 non-overlapping cases). The next tenth was −2.5 % worse (Welch t 3.53), and 16 of the 19 coins had a positive mean in that bottom twentieth.
- **F2:** Among 30-day falls, the rebound grows as the fall covers more of the 30-day high-low range. The next 5 days' excess was −1.01 % at share 0.6–0.8 (t −2.20, n 584), +1.29 % at 0.8–0.9 (t 1.16, n 117) and +9.06 % at 0.9–1.0 (t 2.97, n 32). The book's shorts at share 0.8–1.0 lost −1.12 % per 5-day cell (t −2.43, n 151).
- **F3:** The coins that had fallen most from their 30-day high also rebounded. In the deepest tenth of drawdowns, the next 5 days' excess was +1.19 % (t 2.12, n 544), against −1.07 % to −1.96 % in the next four tenths (t −2.2 to −4.0).
- **F4:** Large one-day rises are followed by further rises, but large one-day falls are not followed by further falls. On up days, the next 5 days' excess rose with the day's move in units of 20-day volatility (slope 0.0084, t 3.00, n 2867); on down days the slope was flat (−0.0009, t −0.29, n 2865). Days above 2.5 volatilities averaged +5.0 % (t 1.73, n 151). The effect changed sign across years: 2022 −3.4 % and 2025 −3.3 %, against 2023 +2.9 % and 2024 +4.7 %.
- **F5:** Falls that covered only a small share of their 30-day range kept falling, and the book barely caught it. With a 30-day fall at share ≤ 0.4, the next 5 days' excess was −1.46 % (t −5.0, n 1232). The book's shorts in that bucket gained only +0.17 % per cell (t 1.59).
- **F6:** The book's profit comes from its longs. Long cells gained +1.05 % per 5 days (t 7.6, n 3505) and short cells −0.08 % (t −0.93, n 3699). The shorts earned +0.27 % of excess (t 3.0), but the coins' drift took it back, and short gains were negative in 2023 (t −2.2) and 2024 (t −2.9). Trades held over 40 days carried the book: longs +106 % mean (n 399), shorts +27 % (n 368). Trades held 5 days or less lost: longs −1.8 %, shorts −4.5 %.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days.g1_range-spanning-fall-rebounds` (from F1, F2, F3): The further a coin's 30-day fall has carried it, and the closer that fall comes to spanning its whole 30-day high-low range, the more the coin rises over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days.g2_large-up-day-continues` (from F4): The larger a coin's 1-day rise compared with its 20-day volatility, the more the coin keeps rising over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
