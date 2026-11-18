---
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
idea tested: 012-02_volume-burst-fall-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5138 USD
---
## Findings
- **F1:** Among daily falls of more than one usual move, a higher volume ratio (volume over its 30-day mean) is followed by a larger excess return, but only over short horizons: the slope is 0.0056 (t 4.48, n 1666) at 1 day and 0.0206 (t 5.06, n 526) at 3 days, then -0.0016 (t -0.32, n 345) at 5 days, -0.0069 (t -0.63, n 197) at 7 days and -0.043 (t -1.82, n 87) at 14 days, so the rebound is over within about 3 days.
- **F2:** The coin's 5-day return measured in usual moves (5-day return over the 20-day daily standard deviation times √5) predicts the coin's next 7-day excess return with slope 0.0119 (t 4.23, n 2011 non-overlapping cases), the opposite of reversal; the slope is positive at every horizon from 2 to 14 days (t 2.31 to 4.23) and for all six coins (XRP t 3.28, the others t 0.89 to 1.79).
- **F3:** That 7-day continuation grows with recent volume: by tercile of 5-day mean volume over 30-day mean volume the m5 slope is 0.0069 (t 0.93), 0.0117 (t 2.19) and 0.0137 (t 3.05), and the product m5 × volume ratio gives slope 0.0090 (t 4.48, n 1723).
- **F4:** Over all bars, the day's volume ratio alone predicts the 3-day excess return with slope 0.0054 (t 3.60, n 4283), but among up days of more than one usual move the slope is only 0.0036 (t 1.30, n 609), so the volume effect comes mainly from falls.
- **F5:** The lower wick adds nothing among falls of more than one usual move: the wick slope on the 3-day excess return is 0.0143 (t 0.54, n 577), and by wick tercile the means are 0.0180, -0.0104 and 0.0070 with no order, which goes against the brief's wick reasoning.
- **F6:** The book is in a position on only 44% of days and earns 0.00038 a day against the coins' higher yearly averages (for example 0.0042 in 2020 and 0.0024 in 2024, against the book's 0.00097 and 0.00003), so it gives up most of the market's rise.
- **F7:** The idea's gain is uneven across years: the 3-day excess after forecast > 0 bars is -0.0151 (t -2.76) in 2018 and -0.0120 (t -2.50) in 2022 against +0.0177 (t 3.12) in 2020, and the falls' volume slope is near zero in 2018, 2019 and 2023 (t 0.83, -0.64, 0.24).

## Ideas
- `012-02_volume-burst-fall-reversal.g1_volume-burst-fall-next-day-rebound` (from F1, F4): Among days on which a coin falls sharply, the larger that day's volume relative to its 30-day average volume, the larger the coin's rise over the next day.
- `012-02_volume-burst-fall-reversal.g2_five-day-move-weekly-continuation` (from F2): The larger a coin's 5-day return measured in its usual daily moves, the larger its return in the same direction over the next 7 days.
- `012-02_volume-burst-fall-reversal.g3_volume-backed-five-day-continuation` (from F3, F2): A coin's 5-day return, measured in its usual daily moves, is followed by a larger move in the same direction over the next 7 days the higher its 5-day average volume is relative to its 30-day average volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
