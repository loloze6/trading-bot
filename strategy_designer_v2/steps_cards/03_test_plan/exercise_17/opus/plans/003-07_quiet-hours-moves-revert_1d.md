---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: sharp move in quiet hours or on a weekend, on low volume -> replaced: on 1d bars, only by a sharp daily move on a below-average-volume day.
- Comparison: thin-liquidity moves against moves in busy hours -> replaced: low-volume days against other days, since hours within a day are not visible.
- Outcome: price partly reverses once busy hours and volume return -> adapted: the next daily bars move against the move; "after X" becomes "while X".
- Verdict transfer: no: a daily-bar test cannot see quiet hours, so a reject or confirm on low-volume days says nothing about moves made in thin hours.
Reason: The idea's situation is a move made inside a coin's quiet hours, and its reversal comes when busy hours return later the same day or the next. That needs intraday volume and time-of-day, which 1d bars do not carry. The weekend case would also need a day-of-week reading, which no part of the config's logic can take from the timestamp.
