---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: a sharp price move during the coin's quiet hours or on a weekend, when its volume is low -> replaced: daily bars hide the hours, the config cannot read the weekday, and no graded low-volume component exists.
- Comparison: low-volume moves against moves of similar size on normal or busier volume -> replaced: no graded measure of volume against its average exists outside the on/off `VolumeExpansionHedgeComponent`.
- Outcome: the move is partly reversed once busier hours and volume return -> adapted: "once busier hours return" becomes "while" a contrarian position is held on the following daily bars.
- Verdict transfer: no: a test on daily bars cannot isolate quiet-hour or weekend moves, so neither a confirm nor a reject would speak to the idea.
Reason: On 1d bars, the idea's quiet intraday hours and the later return of busier hours do not exist in the data. The config also has no way to express a calendar condition such as a weekend, since no component or rule reads the bar's weekday.
