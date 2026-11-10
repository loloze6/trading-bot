---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp price move made during the coin's quiet hours or on a weekend, while its volume is low -> replaced: on 1d bars the quiet hours sit inside a single bar and cannot be seen. A weekend day can only be told apart through the timestamp's day of week, and no component reads that. The most a config could hold is "a sharp daily move on a day whose volume is below its average", which is a different quantity.
- Comparison: low volume during those hours, judged against the coin's normal (busier) volume -> adapted: volume below its N-bar average can be set as a regime condition (a veto with volume_filter), but only per day, not per hour.
- Outcome: the move is partly reversed once the busier hours and normal volume return -> replaced: the return of the busy hours, and any reversal it brings, usually happens within the same day, so it falls inside the same daily bar. A daily config could only measure whether the next days move against the previous day's move.
- Verdict transfer: no: the idea's move and its reversal both happen within the day. A daily test of low-volume days could confirm or reject something without bearing on quiet-hour or weekend moves, and an intraday reversal would never appear in it.
Reason: The idea's situation (quiet hours) and its outcome (reversal when the busy hours return) both happen within a single 1d bar, so the data this test runs on does not contain them. The weekend part would also need the day of the week, which no part of the config can read.
