---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: sharp move in quiet hours or on a weekend, on low volume -> replaced: daily bars hide the hour of a move, and no component reads the weekday, so only a daily low-volume move could stand in for it.
- Comparison: thin quiet-period liquidity against the busier hours that follow -> replaced: intraday quiet and busy sessions cannot be told apart on 1d bars.
- Outcome: price partly reverses once busy hours and volume return -> replaced: only a reversal over the next daily bars could be measured, not one tied to the return of busy hours.
- Verdict transfer: no: a daily low-volume reversal test says nothing about moves made in quiet hours or on weekends, so its result would not carry to this idea.
Reason: The idea's situation is a move in a coin's quiet intraday hours or on a weekend, reversed when busy hours return. On 1d bars the hour of a move is not in the data, and the config has no component or rule that reads the calendar to pick out weekends. Testing it would mean replacing the timing with plain low daily volume, which is a different idea.
