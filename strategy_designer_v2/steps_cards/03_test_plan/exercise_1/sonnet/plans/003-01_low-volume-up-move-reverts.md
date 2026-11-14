---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Across the bars with a short position, the next-day BTC return is negative on average, and below the coin's unconditional average daily return. Gains before costs also grow with position size, so the biggest shorts (largest low-volume up-moves) earn the most.
Reject: Next-day returns after the held shorts are zero or positive, or no lower than the coin's average daily return. The short's gross P&L is not positive, or it does not rise with position size. This would mean low-volume rises are not given back.
Deviation: The config uses a regime of "up day with volume at least 20% below its 20-day average", which stands in for "unusually low volume". The size of the move is the one-day return, and the short grows with it. The position exists only on bars meeting that condition and goes flat on the next bar that does not, so "falls back afterwards" becomes mainly the next bar's return. Partial give-back over several days is not measured. The high-volume half of the brief (moves that hold or continue) is not tested here, because this single config trades only the low-volume leg.
