---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Across the days that follow a short, BTC's average close-to-close return is below its average daily return over all days, so the shorts gain against holding the coin. Larger shorts, set by larger thin-volume up days, should be followed by larger declines.
Reject: The day after a thin-volume up move, BTC's return is at or above its average daily return, so the short loses relative to holding. The same verdict applies if the shorts' P&L does not grow with position size, meaning bigger thin-volume rallies are not followed by bigger give-backs.
Deviation: The short is opened at the close of the up day itself and held for one day only: it is closed whenever the next bar is not also a thin-volume up day. Any reversion that comes later is therefore not captured. "Unusually low volume" becomes volume below its 24-day average, with the current day included in that average. "Sharp" is graded, not a threshold: the day's return is scaled against the last 60 days and squared, with signed_power damping small moves. The brief's contrast with high-volume moves, which should hold or continue, is not tested here.
