---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp price move during the coin's quiet hours or on a weekend, when volume is low -> replaced: a 1d bar holds a whole day, so quiet hours cannot be seen. No component reads the day of the week. The nearest thing would be a daily move weighted by that day's volume against its average, and that is a different quantity. No graded component computes even that: the only volume readers are the on/off `VolumeExpansionHedgeComponent` and the dead-zone `volume_filter`.
- Comparison: the move's volume against the coin's usual volume, and quiet hours or weekends against busy hours -> replaced: the hour-of-day contrast is not in daily bars at all. Only a day-against-day volume ratio could stand in for it.
- Outcome: part of the move is given back once busy hours and normal volume return -> adapted: a return against the move's direction over the next day or days. The "once busy hours return" timing is inside the day and is lost.
- Verdict transfer: no: a test on daily bars would measure whether low-volume days revert, not whether moves made in quiet hours or on weekends revert when liquidity comes back, so neither result would settle the idea.
Reason: The idea's situation and its timing are intraday (quiet hours, then the return of busy hours). On 1d bars that information is not in the coin's own bars, and the config has no day-of-week or time-of-day input. Any daily-bar version would replace the situation with a generic low-volume-day move, which this task forbids.
