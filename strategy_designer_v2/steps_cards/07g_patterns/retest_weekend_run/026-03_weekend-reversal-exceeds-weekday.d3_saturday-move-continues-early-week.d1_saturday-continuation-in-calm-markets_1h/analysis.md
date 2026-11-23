---
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7159 USD
---
## Findings
- **F1:** Sunday's 24-hour move is reversed over Monday and Tuesday: across 1910 Sunday cases the de-drifted 48-hour return against Sunday's direction averages +0.84 % (t 5.06, strength 0.131), and it is positive in every year 2018–2025 (from +0.03 % to +1.82 %) and for every coin (from +0.48 % to +1.21 %).
- **F2:** Sunday's reversal grows with the coin's 30-day volatility of hourly returns: +0.02 % (t 0.10, strength 0.003, 647 cases) in the calmest third, +0.88 % (t 3.51, strength 0.138, 644 cases) in the middle third and +1.65 % (t 4.40, strength 0.257, 619 cases) in the most volatile third. The slope of the 48-hour return on Sunday's raw move has t −3.88 in the most volatile third and +1.16 in the calmest third.
- **F3:** Inside the two more volatile thirds, larger Sunday moves are reversed somewhat more: by quartile of the size of Sunday's move the reversal is +0.93 %, +1.44 %, +1.10 % and +1.58 % (t 2.6 to 3.1, about 316 cases each, slope t −2.1 to −3.2).
- **F4:** Saturday and Sunday act in opposite directions on Monday–Tuesday: in a joint regression of the 48-hour return (1910 cases) on both days' volatility-scaled moves, Saturday's coefficient is +0.0094 (t 4.31) and Sunday's is −0.0047 (t −2.31). The two days' moves are nearly uncorrelated (−0.08). The tested continuation sits on Saturday, while the brief's reversal sits on Sunday.
- **F5:** The reversal is weekend-specific: a weekday's 24-hour move is reversed over the next day by only +0.17 % (t 2.22) in the middle volatility third and +0.12 % (t 1.17) in the top third. A Sunday move in hot markets is reversed by +0.94 % over Monday alone (t 4.39, slope t −3.29), with the hot split taken at the median of 30-day volatility.
- **F6:** The hours 21:00 and 22:00 UTC rise by +5.37 bp (t 6.81) and +4.38 bp (t 5.82) per hour against roughly 0–2 bp for the other hours. The effect holds for each of the six coins (t 2.40 to 4.22) and in 7 of 8 years (2022: −2.2 bp, t −1.09), and on every weekday (+5.9 to +13.1 bp over the two hours).
- **F7:** The two-hour evening rise is largest after the coin fell over the preceding 24 hours: +22.5 bp (t 7.02, 3310 cases) in the bottom quintile of the prior 24-hour return, against +5.6, +7.1 and −0.2 bp in the next three quintiles. After the largest rises it is +13.2 bp (t 4.78). Only the move after the largest falls exceeds the 0.19 % cost of a trade.
- **F8:** The tested Saturday continuation is not stable over time. Its de-drifted 48-hour move is −0.03 % in 2021 and −0.82 % in 2025 (t −2.00, 252 cases), and −0.28 % for ZEC. The book lost in those same years: −3.1 bp a day in 2021 and −1.1 bp a day in 2025.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g1_sunday-reversal-in-volatile-markets` (from F1, F2, F3, F5): A coin's 24-hour return over Sunday is followed over the next two days, Monday and Tuesday, by a move in the opposite direction. This holds only while the coin's 30-day volatility of hourly returns is high against its own past, and the more volatile the coin and the larger Sunday's move, the larger the reversal.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g2_saturday-continues-sunday-reverses` (from F4, F1, F8): A coin's Saturday 24-hour return and its Sunday 24-hour return both point to the move over the next two days, Monday and Tuesday: that move follows Saturday's direction and goes against Sunday's. The larger Saturday's move is against Sunday's, the larger the move in Saturday's direction.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.g3_evening-rebound-after-daily-falls` (from F6, F7): A coin rises over the two hours from 21:00 to 23:00 UTC, and the more it fell over the preceding 24 hours, the larger that evening rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
