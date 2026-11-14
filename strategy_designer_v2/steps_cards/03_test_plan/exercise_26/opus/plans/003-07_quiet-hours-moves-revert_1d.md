---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a sharp price move on a weekend or in quiet hours, when the coin's volume is low -> replaced: no component combines a move's size with low volume for both directions, quiet hours do not exist on 1d bars, and no component reads the weekday.
- Comparison: volume low against the coin's usual volume -> replaced: no graded volume-to-average measure exists; `VolumeExpansionHedgeComponent` is on/off and covers up bars only.
- Outcome: the move is partly reversed once busier hours and volume return -> adapted: "after" becomes "while", as a graded position against the move.
- Verdict transfer: no: without a low-volume measure, the test would only check whether all sharp moves reverse, not thin-volume ones.
Reason: The bars hold everything the weekend and low-volume parts need (`timestamp`, `volume`, `close`), and a regime or graded forecast could carry them. No catalogue component measures volume against its average for both directions, combines that with the move, or reads the weekday. The "quiet hours" part also needs intraday bars, which a 1d run does not provide.
