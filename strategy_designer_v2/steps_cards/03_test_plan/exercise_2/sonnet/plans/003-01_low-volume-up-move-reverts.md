---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Over the next 5 bars, the bars with a nonzero (short) forecast are followed by a BTC return below its unconditional average 5-bar return, so the short position gains net of the coin's own drift. The gain also grows with the size of the short (larger |forecast| followed by a larger fall).
Reject: The 5-bar return after the active bars is equal to or above BTC's unconditional average 5-bar return, so the short does no better than holding. The gain also does not grow with |forecast|, or the larger moves rise further.
Inconclusive: Fewer than about 30 active bars over the sample, or a 5-bar shortfall versus holding that is too small to tell apart from the spread of 5-bar returns across active bars, or a gain that appears only in the smallest positions and not in the largest.
Deviation: The config tests only the upward-move, low-volume half of the theory. It does not compare against high-volume moves, which the brief says should hold or continue, so the volume-dependence claim is not tested. "Sharp" is the single-day move, graded by its size, with small moves damped. "Unusually low volume" is a day's volume at or below 75% of its 20-day mean (the engine's on/off low-volume-up-bar component is used only as a regime measure, not as the forecast). The position exists only on the bar the condition holds and goes flat on the next bar that does not meet it, so it is not held for the 5-bar evaluation horizon. The 5-bar result is read from the recorded forecast rather than from a held position.
