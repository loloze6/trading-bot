---
line: 7.g patterns
backtest: 032-02.b2.g2_volatile-close-near-low-rebound_1d
idea tested: 032-02.b2.g2_volatile-close-near-low-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3950 USD
---
## Findings
- **F1:** On the 3256 regime bars (880 days), a regression of next-day excess return on the day's return scaled by its 30-day volatility (z1) and on the close's location in the range together gives z1 −0.91 % per standard deviation (t −2.30) and close location −0.12 % (t −0.40). The tested idea's close-near-low effect is carried by the size of the day's fall, not by where the close sits.
- **F2:** Over all bars (7537 bars, 1257 days), z1 predicts the next day's excess return with a coefficient of −0.40 % per standard deviation (t −2.51). The bottom z1 fifth (mean z −1.38) is followed by +0.75 % (t 2.50, 1508 bars) and the top fifth by −0.26 % (t −1.11). The z1 correlation is negative in every year from 2018 to 2021 (−0.05 to −0.13), in 5 of 6 coins (XRP +0.00) and in 10 of 12 windows.
- **F3:** The reversal is concentrated where ranges are wide. In the regime (30-day ranges wide against 90-day) z1's coefficient is −0.91 % (t −2.30), outside it +0.12 % (t 0.67). On bars whose range is above the median relative to its 30-day mean it is −0.55 % (t −2.42, 3725 bars), against −0.14 % (t −1.04) on the rest.
- **F4:** The bottom fifth of raw 1-day returns is followed by +0.89 % (mean fall −8.3 %, t 1.74, 770 regime bars) and +0.64 % outside the regime (mean fall −5.9 %, t 2.34, 954 bars). Both are 3 to 4.7 times the 0.19 % cost of a trade, against +0.23 % unusual move for the tested idea.
- **F5:** A fresh 30-day closing low, the brief's own situation, is followed by +0.32 % excess (t 0.56, 624 bars), which cannot be told from 0. No weekday stands out (all |t| < 1.6).
- **F6:** On the book's worst 5 % of days (73) it lost −3.88 % while the coins fell −8.48 %. On its best 5 % (73) it gained +3.87 % against coins +8.14 %. Its largest swings are the market's own moves at about half exposure, not timing.

## Ideas
- `032-02.b2.g2.g1_volatile-large-fall-next-day-rebound` (from F1, F2, F3, F4): When a coin's daily high-low ranges over the past 30 days are wide compared with the past 90 days, the larger its 1-day fall measured against its past 30 days' daily volatility, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
