---
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d
idea tested: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3474 USD
---
## Findings
- **F1:** The book is almost never in the market, and that is why the mean daily return (1.0e-05), the Calmar (0.10) and the trades per day (0.0013) fail: it made 31 trades over 17,405 coin-days and held a position on 4.0 % of days, while cost was never the obstacle (the total move of +9.77 % per case is 50.6 times the 0.19 % cost of a trade).
- **F2:** The book traded so rarely because most crosses came after a rise, and the plan sized only crosses after a fall: of 163 upward cloud crosses with a known 26-day past return, 137 came after a rise and 26 after a fall, so only 34 had a positive forecast and 20 reached a forecast of 2 or more.
- **F3:** Upward crosses in general are followed by a larger rise than the coin's normal drift, and the plan threw that move away: counted once per 26-day grid cell, the 152 crosses had a mean unusual move of +4.9 % over 26 days (t 1.55, strength 0.146), and the 111 crosses that came after a rise had +4.7 % (t 1.23, overlapping cases).
- **F4:** What lowers the move after a cross is a large prior rise, not the lack of a fall: by tercile of the prior 26-day return, crosses after a fall or a flat stretch had +9.6 % (t 1.35, 36 cases), the middle tercile +10.9 % (t 1.14, 36 cases), and the largest prior rises −2.4 % (t −0.68, 36 cases).
- **F5:** Grading by the depth of the fall is not supported: in step 5 the larger-fall half minus the smaller-fall half was −7.9 %, and the fall and middle terciles above differ by only −1.3 %.
- **F6:** The brief's thin-cloud grading cannot be read in this record and does not show where it can: with windows of about 122 daily bars, only 29 crosses had a full cloud history, and the thin tercile had +5.9 % against +19.6 % for the thick one (t below 1 in each, about 10 cases each).
- **F7:** The move after crosses is concentrated in the more volatile coins and is near zero on BTC and ETH: mean unusual move +0.4 % on BTC (21 cases), +0.2 % on ETH (22), against +4.5 % on LTC, +3.0 % on XMR, +5.1 % on ZEC and +12.6 % on XRP (t at most 1.16 each).

## Ideas
- `021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall.d1_cloud-cross-not-overextended` (from F1, F2, F3, F4, F5): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 26 days, and the smaller the coin's rise over the past 26 days before the cross, the larger the rise, so a cross after a modest rise still carries most of it and only a cross after a large run-up carries little.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
