---
line: 7.g patterns
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
idea tested: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3918 USD
---
## Findings
- **F1:** A coin's 24-hour unusual move runs against its past 24-hour return, graded by that return measured in usual 24-hour moves. The slope is −0.0020 per unit, t −3.90, on 5552 non-overlapping 24-hour cases pooled over both coins. The slope is negative in all four coin and half-period splits: BTC early −0.0003 (t −0.4), BTC late −0.0026 (t −2.6), ETH early −0.0020 (t −1.9), ETH late −0.0032 (t −2.5). The 72-hour past return shows no such slope (t 0.36).
- **F2:** After a 24-hour fall deeper than two usual 24-hour moves, the next 24 hours end +1.29 % above the coin's normal drift (t 2.58, 149 cases). That is about 12 times the 0.11 % cost of a trade. The bins in between are graded: +0.09 % after −2 to −1, −0.09 % after 0 to +1, −0.21 % after +1 to +2, −0.35 % above +2. The deep-fall effect sits in the late half (BTC +2.43 %, t 2.72; ETH +3.55 %, t 2.58), not the early half (BTC −0.11 %, ETH −0.34 %).
- **F3:** How the next 6 hours follow the past 6-hour return depends on the coin's 30-day hourly volatility.
- **F4:** The tested idea's situation, a fall of 1.5 to 4 usual hourly moves, is followed by a 6-hour unusual move of +0.08 % to +0.36 % in every volume tercile, none with t above 1.2.
- **F5:** The 1-hour unusual move at 20:00 and 21:00 UTC is positive.
- **F6:** Thursdays are negative for both the bars and the book.
- **F7:** The book's gain is concentrated in its strongest forecasts.

## Ideas
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.g1_daily-overshoot-reverses-next-day` (from F1, F2): A coin moves against its past 24-hour return over the next 24 hours, and the larger that 24-hour return measured in the coin's usual 24-hour moves (from its 30-day hourly volatility), the larger the opposite move. It is largest after the deepest 24-hour falls.
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.g2_calm-market-six-hour-momentum` (from F3): When a coin's 30-day hourly volatility is low against its own history, its next 6 hours continue its past 6-hour return, and the larger that return in usual 6-hour moves, the larger the continuation.
- `028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.g3_turbulent-market-six-hour-reversal` (from F3): When a coin's 30-day hourly volatility is high against its own history, its next 6 hours move against its past 6-hour return, and the larger that return in usual 6-hour moves, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
