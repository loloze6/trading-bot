---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp move in quiet hours or on a weekend, on low volume -> replaced: on 1d bars an intraday quiet-hours move cannot be seen, so only a low-volume day could be measured.
- Comparison: low volume against the coin's usual volume -> adapted: a regime veto (`volume_filter` on a constant) flags days whose volume is below its 20-day mean.
- Outcome: the move is partly given back once busier hours return -> adapted: the next day's return is judged against a position opposite to the low-volume day's move.
- Verdict transfer: no: a result about low-volume days on daily bars would not confirm or reject a claim about moves made inside quiet hours or on weekends.
Reason: The idea's situation is a move made during a coin's quiet hours, which needs intraday bars; a 1d bar merges quiet and busy hours, so the quiet-hours move is not in the data at this bar size. The weekend case needs a day-of-week condition, and no component or rule reads the calendar; that would need new code.
