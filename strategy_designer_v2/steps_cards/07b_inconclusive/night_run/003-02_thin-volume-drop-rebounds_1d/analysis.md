---
line: 7.b inconclusive
backtest: 003-02_thin-volume-drop-rebounds_1d
idea tested: 003-02_thin-volume-drop-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3439 USD
---
## Findings
- **F1:** The tested measure lies on the side opposite to the idea at every horizon from 2 to 10 days, not only at the plan's 5 days: forecast-weighted excess return t = -2.50 at 2 days (n=2579), -1.04 at 3 days (n=1735), -1.91 at 5 days (n=1067) and -2.67 at 10 days (n=505). On the positive-forecast cases, the mean excess 5-day return is -0.83% (t -2.57).
- **F2:** The thin-volume down days that do not rebound sit mostly in falling markets and in the early years, and they are not graded by the forecast.
- **F3:** The rebound the brief gives to thin-volume falls appears instead after heavy-volume falls, over about 3 days.
- **F4:** This heavy-volume rebound is strongest in the heaviest-volume falls.
- **F5:** The heavy-volume 3-day rebound is uneven across years and coins, though positive in most.
- **F6:** On the up side, heavy-volume moves carry on as the brief says, but only weakly.

## Ideas
- `003-02_thin-volume-drop-rebounds.b1_heavy-volume-drop-rebounds` (from F3, F4, F5): When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it wins back part of that fall over the next 3 days; the larger the fall and the heavier its volume against that average, the larger the rebound.
- `003-02_thin-volume-drop-rebounds.b2_heavy-volume-rise-continues` (from F6): When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days; the larger the rise and the heavier its volume against that average, the larger the further gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
