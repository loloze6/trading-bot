---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a sharp move in quiet hours or on weekends, on low volume -> replaced: no catalogue component measures volume against its own average, and none reads the weekday; quiet hours cannot be seen inside a 1d bar.
- Comparison: low volume against the coin's busier hours and normal volume -> replaced: no relative-volume measure exists to compare against.
- Outcome: the move is partly reversed once volume returns -> adapted: "once volume returns" made "while volume is low"; a negated short-horizon price change can hold the reversal.
- Verdict transfer: no: without a relative-volume measure, the test cannot separate thin moves from ordinary ones, so its result would not speak to the idea.
Reason: The idea's defining condition is a move made on volume that is low against the coin's own normal level. This is computable from the daily bars' volume column. No graded component or regime measure in the catalogue outputs it, and no combination of the catalogue's components builds it. The only volume component, `VolumeExpansionHedgeComponent`, is on/off, covers up bars only, and is refused. With a relative-volume regime measure, the plan would be: a low-volume regime holding a negated, standardised short-period price change, so the forecast fades the move. The other regimes would be flat.
