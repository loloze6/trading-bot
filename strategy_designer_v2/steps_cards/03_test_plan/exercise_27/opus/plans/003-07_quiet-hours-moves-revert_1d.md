---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: sharp move in quiet hours or on weekends, on low volume -> replaced: 1d bars cannot show intraday hours, and no component reads the weekday.
- Comparison: volume low against the coin's usual volume -> replaced: no graded relative-volume component exists; the only volume reader is on/off and fires on up bars only.
- Outcome: move partly reversed once busier hours and volume return -> replaced: a return of busy hours is intraday, so it can only become a next-day drift.
- Verdict transfer: no: a daily low-volume reversal test says nothing about moves made in quiet hours and undone when busy hours resume.
Reason: The idea's situation and outcome are intraday: a move in a coin's quiet hours, reversed when its busy hours return. On 1d bars each day is one bar, so the hours are not in the data. Dropping the hours would replace the idea with a different one: daily low-volume moves.
