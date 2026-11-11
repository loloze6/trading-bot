---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: a sharp move in quiet hours or on weekends, on low volume -> replaced: daily bars cannot show quiet hours, and no component reads the weekday.
- Comparison: low volume against the coin's busier hours and volume -> replaced: no graded component measures volume against its average.
- Outcome: the move is partly reversed once busier hours and volume return -> replaced: a reversal within the day cannot be seen on 1d bars.
- Verdict transfer: no: a daily test of large moves does not test moves made in thin hours or on weekends.
Reason: The idea's situation and its reversal both happen within the day, in quiet hours and when busy hours return, and the test runs on 1d bars that cannot show time of day. The config also has no way to pick out weekend bars, and the only volume-aware component is on/off, so the low-volume condition cannot be kept either.
