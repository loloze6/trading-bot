---
line: 7.c no effect
backtest: 086-01_heavy-volume-up-day-continuation_1d
idea tested: 086-01_heavy-volume-up-day-continuation
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4420 USD
---
## Findings
- **F1:** In falling calm markets, heavy-volume up days were followed by a fall, not a rise. Over 5 days the unusual move was −1.8 % for a volume ratio of 1.5–2 (t −1.07, 22 cases, 20 days) and −2.0 % for a ratio of 2 or more (t −0.88, 22 cases, 20 days). Light-volume up days moved only −0.34 % (t −0.34, 117 cases, 102 days), so heavier volume brought a worse outcome.
- **F2:** The move does not grow with volume. Among up days in the profile, the Spearman correlation between volume ratio and the 5-day unusual move was −0.194 (54 cases). Within the heavy up days it was −0.11 for a ratio of 1.5–2 and +0.08 for 2 or more. By volume quintile, the q4 up days moved −5.2 % over 5 days (t −1.92, 13 cases).
- **F3:** Heavy up days split by the prior 5-day path. After a 5-day fall they were given back: −4.2 % over 5 days (t −1.44, 18 cases) and −8.3 % over 10 days (t −2.11, 16 cases, 13 days). After a 5-day rise they were flat over 5 days (+0.1 %, t 0.06, 20 cases) and rose over 10 days (+3.4 %, t 1.17, 16 cases, 16 days; volume correlation +0.08).
- **F4:** Heavy-volume down days split by where the day closed in its range. Those closing off their low rose +5.5 % over 5 days (t 2.41, 9 cases, 9 days), and those with the smaller falls rose +2.5 % (t 1.28, 18 cases). Those closing near their low fell −3.7 % (t −1.83, 28 cases), and those with the bigger falls fell −5.1 % over 5 days (t −2.06, 19 cases) and −10.1 % over 10 days (t −3.30, 15 cases).
- **F5:** What the market did instead was keep falling. Light-volume down days in the profile were followed by −0.89 % the next day (t −2.67, 226 cases, 190 days) and −2.6 % over 5 days (t −2.41, 113 cases, 99 days). That is the short side, outside this research's box.
- **F6:** The failure is broad. Heavy up days had a negative 1-day unusual move on BCH (−1.0 %, 7 cases), ETH (−1.1 %, 17) and ZEC (−1.0 %, 19). Only XMR was positive (+1.8 %, t 1.90, 12 cases). The 1-day move was negative in 2018 (−1.9 %, 11 cases) and 2019 (−0.7 %, 25 cases).
- **F7:** The moves in F3 and F4 are 2.5–5.5 % per case. That is about 8–18 times the 0.31 % cost of a trade, against the 0.29 % unusual move of the tested idea.

## Ideas
- `086-01.c1_heavy-volume-off-low-absorption` (from F4, F1, F7): In a falling, calm market, a day on volume heavy against the coin's 20-day average that closes well up from its low is followed by a rise over the next 5 days. The higher the close sits in the day's range, the larger the rise.
- `086-01.c2_heavy-up-day-extends-rebound` (from F3, F2, F7): In a falling, calm market, a day that closes up on volume heavy against the coin's 20-day average is followed by a rise over the next 10 days, only while the coin's 5-day return before that day is positive. The heavier that day's volume relative to its 20-day average, the larger the 10-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
