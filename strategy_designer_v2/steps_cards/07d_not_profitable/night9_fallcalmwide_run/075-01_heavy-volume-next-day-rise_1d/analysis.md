---
line: 7.d confirmed, not profitable
backtest: 075-01_heavy-volume-next-day-rise_1d
idea tested: 075-01_heavy-volume-next-day-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3935 USD
---
## Findings
- **F1:** The tested idea's effect is concentrated on heavy-volume down days. In the top fifth of the forecast, down days were followed by a next-day excess return of +1.20 % (t 5.92, 1152 cases), while up days earned −0.02 % (t −0.10, 1318 cases). Below the top fifth, the four other fifths of down days ranged only from −0.22 % to +0.47 %. This is the brief's own remark that the heavy side comes mostly from down days.
- **F2:** The short side, built from light-volume days, carries none of the book's gain.
- **F3:** On down days alone, the next-day rise is graded by volume.
- **F4:** On heavy-volume down days, the move per case is many times the cost of a trade.
- **F5:** A large fall alone is only part of the effect.
- **F6:** The heavy-down rebound appears in every 60-day trend; no single profile carries it.

## Ideas
- `075-01.d1_heavy-volume-down-day-rebound` (from F1, F2, F3, F5): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, the larger its rise over the next day. Light-volume days and up days are left aside.
- `075-01.d2_heavy-volume-fall-two-day-rebound` (from F1, F3, F4): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, the larger its rise over the next two days.
- `075-01.d3_heavy-volume-deep-fall-rebound` (from F3, F5): The heavier a coin's volume on a day that closed lower, relative to its own average daily volume over the past 20 days, and the deeper that day's fall against its 30-day daily swing, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
