---
idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the coin's 24-hour return over Sunday, larger meaning stronger -> kept: 24-bar return read at the Sunday 23:00 UTC bar, whose close is Monday 00:00.
- Comparison: a 48-hour return of the same size ending on any other weekday reverses less -> kept: measured in the supporting check from the recorded closes, per unit of return size.
- Outcome: an opposite move over Monday and Tuesday that grows with Sunday's return -> kept: held 48 bars from Monday 00:00.
- Verdict transfer: yes: the forecast fades exactly Sunday's own return over the stated 48 hours, and the check compares it with weekday returns of the same size.
Forecast: A regime rule selects one bar a week: the bar whose coming bar starts Monday 00:00 UTC (WeekdayComponent = 0 and HourOfDayComponent = 0). On that bar the forecast is minus the coin's 24-bar percent return (Sunday's move), standardised against the mean absolute size of its last 60 hourly values. It is short after a Sunday rise and long after a Sunday fall, and its size grows linearly with Sunday's move. Saturday's move is ignored. On every other bar the regime is null and the forecast is 0. The bet made on Sunday's last bar is then held for 48 bars by the holding period.
Config: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: Take each Sunday-close bar where the forecast is nonzero, one case per coin-week, all inside one window. Regress the coin's return over the next 48 bars, minus its mean 48-bar return over all windows, on forecast / 10. This is before costs. The measure is the slope's t.
- Supporting check: The slope of the next-48-bar return on Sunday's 24-bar return must be more negative than the slope of the next-48-bar return on the prior 48-bar return. The second slope uses 48-bar returns ending at 00:00 UTC on each of the other weekday boundaries, recomputed from closes with one case per coin-day. Measured as the slope difference (Sunday minus other days), its t ≤ -2.
- Confirm: The main slope is positive with t ≥ 2, and the supporting check passes (slope difference t ≤ -2).
- Reject: The main slope has t ≤ -2, meaning Sunday's move continues into the week. Or the main slope confirms but the slope difference has t ≥ 2, meaning weekday returns of the same size reverse more.
- Inconclusive: Any other result is inconclusive, for example a main t between -2 and 2, or a main confirm with a slope difference t between -2 and 2. At least 300 Sunday cases across coins and windows are required, otherwise inconclusive.
