---
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4151 USD
---
## Findings
- **F1:** The two hours from 22:00 to 24:00 UTC rise. The coin's return from the 21:00 close to the 23:00 close averages +0.099 % (t 8.8, 16200 cases, one per coin per day). It is positive in all six coins (t 2.9 to 4.6), on all seven weekdays (t 1.7 to 4.3) and in seven of eight years (2022: -0.05 %, t -1.6). The hourly z-returns of the bars closing at 22:00 and 23:00 are the largest of the day (t 6.2 and 5.3).
- **F2:** That late rise grows with the size of the coin's fall over the 8 hours before 21:00, measured in hourly-volatility units. It is +0.23 % in the lowest quintile (mean -4.1 vol units) against +0.04 % in the highest (+4.2 units), and the slope of the vol-scaled 2-hour return on the 8-hour move has t -5.7 (16200 cases).
- **F3:** The late rise grows with the coin's past-week hourly volatility: +0.04 % (t 3.3) in each coin's lowest volatility tercile, +0.09 % (t 5.1) in the middle and +0.17 % (t 6.4) in the highest.
- **F4:** A coin's 24-hour return to 00:00 UTC is partly reversed over the next 24 hours on most days of the week, in non-overlapping daily cases (about 2100 to 2240 per weekday).
- **F5:** The tested 48-hour continuation appears only at Friday 00:00 and is unstable.
- **F6:** Saturday's hourly returns are the highest of the week (mean z +0.018, t 5.3, 58477 bars). The book earns mostly on Friday and Saturday (mean daily +0.107 % and +0.161 %, against -0.027 % to +0.002 % on the other days). Its 2 % largest gains and losses fall almost all on those two days (Friday 188 and 188, Saturday 141 and 110), as its weekly bet makes them.
- **F7:** The bars closing at 04:00 and 15:00 UTC fall (mean hourly z -0.033, t -4.9, and -0.041, t -4.6). Those closing at 03:00 also fall (z -0.022, t -3.1).

## Ideas
- `026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends.g1_late-utc-rebound-after-selloff` (from F1, F2): When a coin has fallen over the 8 hours before 22:00 UTC, it rises over the next 2 hours, and the larger that 8-hour fall measured against the coin's recent hourly volatility, the larger the rise.
- `026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends.g2_late-hours-rise-scales-with-volatility` (from F1, F3): The higher a coin's hourly volatility over the past 7 days, the larger its rise over the 2 hours from 22:00 to 24:00 UTC.
- `026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends.g3_daily-move-reverses-next-day` (from F4): A coin's 24-hour return to 00:00 UTC is partly reversed over the following 24 hours, and the larger that day's move, the larger the opposite move the next day.
- `026-02_weekend-drop-reverses-early-week.d3_pre-weekend-rise-extends.g4_sunday-move-reverses-monday` (from F4): A coin's move over Sunday (its 24-hour return to Monday 00:00 UTC) is reversed over Monday, and the larger Sunday's move, the larger Monday's move against it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
