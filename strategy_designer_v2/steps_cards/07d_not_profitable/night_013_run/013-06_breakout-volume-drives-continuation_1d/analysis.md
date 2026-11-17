---
line: 7.d not profitable
backtest: 013-06_breakout-volume-drives-continuation_1d
idea tested: 013-06_breakout-volume-drives-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3095 USD
---
## Findings
- **F1:** The book is almost never in the market: the "close above the prior 365-close high" regime is active on only 2.59% of bars (in position on 2.56%), so the mean daily return is 0.000153 against a required 0.0005, even though active days average +0.40%.
- **F2:** The regime switches off at once because it needs a fresh new high every day. The 209 active runs last 2.12 bars on average (median 2), and 93 of them last a single bar, so the book exits long before the 30-day horizon the idea forecasts.
- **F3:** The gain the book leaves behind is large. Over 30 days from the breakout, the book made a mean +5.1% against the coin's +12.1% (59 non-overlapping cases), and after a run ends the coin still rises a mean +7.9% over the next 30 days (t 2.57, n 146 runs, median +1.1%).
- **F4:** The follow-through is graded by breakout-day volume and keeps building past 30 days. Over the next 30 days, high-volume-tercile breakouts returned +30.7%, mid +5.9% and low −0.1%. Over 60 days the figures were +53.3%, +1.1% and −1.6%. The book captured only +8.4%, +5.0% and +1.5% of those 30-day moves.
- **F5:** The falls behind the failed Calmar (0.73 against 0.75) are short holds hit by single sharp down days. XMR holds 4 of the 5 deepest window falls (−21%, −18%, −18%, −12%) and has a negative book mean of −0.0197%/day, while the coin itself rose 14% to 211% in those same windows. The worst book days (−17%, −13%, −12%) are held days on which the coin fell 9% to 21%.
- **F6:** Breakouts carry deep interim dips: the mean worst point within the 30 days is −13.7%, and the close sits below the breakout price on 48% of those days. Because the book's exposure is tied to day-by-day new highs, it is out of the market for the recovery from these dips.

## Ideas
- `013-06_breakout-volume-drives-continuation.d1_volume-breakout-persists-past-high` (from F1, F2, F3, F4, F6): When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 30 days. That return keeps accruing through the days after the close slips back below the new high.
- `013-06_breakout-volume-drives-continuation.d2_breakout-volume-sixty-day-drift` (from F4, F5): When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
