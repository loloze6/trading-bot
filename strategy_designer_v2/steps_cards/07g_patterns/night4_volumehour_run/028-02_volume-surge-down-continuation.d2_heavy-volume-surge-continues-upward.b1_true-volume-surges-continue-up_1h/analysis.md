---
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h
idea tested: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3979 USD
---
## Findings
- **F1:** Each coin's 4-hour return, minus its drift, follows a daily cycle by UTC start hour. The cycle was sampled once a day per hour, about 5,836 independent cases per hour. Starts at 17–20 UTC gain +4.6, +9.0, +6.7 and +8.4 bp (t 2.1, 4.4, 3.2, 3.9). Starts at 22–01 UTC lose −4.9, −6.7, −9.0 and −6.1 bp (t −2.3, −3.1, −4.5, −3.2). The other 16 hours lie within |t| < 1.7.
- **F2:** The midnight-UTC weakness holds in both coins: BTC −8.2 bp (t −3.3, 2,918 cases), ETH −9.8 bp (t −3.1, 2,918 cases). It is negative in every year from 2018 to 2023 (−24.2 to −3.1 bp, four years with t ≤ −2.3) and gone in 2024 (+0.1 bp) and 2025 (+4.9 bp, t 1.1). It is at most about 9 bp per 4 hours, below the 0.11 % a trade costs.
- **F3:** A move of more than 2.5 usual hourly moves that is the first in 24 hours (1,784 events) is followed by more movement its own way the higher that hour's volume against its 30-day mean. Over 4 hours: +6.7 bp at under 2×, +14.5 bp at 2–4×, +32.9 bp at 4–8×, +44.0 bp above 8×. Over 8 hours: +8.1, +13.3, +34.1 and +62.9 bp.
- **F4:** The F3 gradient appears on both sides. For the 4–8× volume bucket over 4 hours, down hours give +31.5 bp in their direction (t 2.3, 258) and up hours +34.4 bp (t 2.7, 248). Over 12 hours it is positive in both coins (BTC +18.2 bp t 1.9, ETH +34.0 bp t 2.6) and in 6 of 8 years. The rank correlation with |move| × volume ratio is only 0.07.
- **F5:** Counting every large move on the fixed 4-bar grid instead, repeats inside a burst included, reverses the result. Large moves on volume above 4× are followed by −29.0 bp in their direction (t −1.8, 455 cases). The tested forecast, which fires on every up hour, measures −0.01 % per case (t −0.84, 13,276 cases). So the continuation belongs to the first surge, and later surges in a burst fade.
- **F6:** The book lost −9.4 bp a day and lost in 15 of 24 windows. It was in the market 65 % of the time with 24,971 trades of median length 4 hours. Its per-case move (+0.01 %) is 0.1 times the 0.11 % cost. By contrast, the F3 first-surge moves at 4× volume or more (+33 to +44 bp over 4 hours) are 3 to 4 times that cost.
- **F7:** Weekdays show no pattern beyond chance across the 7 weekdays.

## Ideas
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up.g1_first-volume-shock-continues` (from F3, F4, F5, F6): An hour in which the coin moves far more than its typical 30-day hourly move, being the first such hour in the past day, is followed over the next four to eight hours by a further move in the same direction as that hour, larger the higher that hour's volume against its 30-day average hourly volume.
- `028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up.g2_intraday-utc-return-cycle` (from F1, F2): The coin's return over the next four hours follows a daily cycle in UTC time: highest when the four hours start in the late US session around 18:00–20:00 UTC and lowest when they start around midnight UTC, the move larger the closer the start is to those two peaks.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
