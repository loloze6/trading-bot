---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Only on a day whose close is above the previous close and whose volume is below its 20-day average volume (the average includes that day), the forecast is a short position sized by that day's percent rise. The rise is close-to-close over 1 bar. It is divided by the mean absolute 1-day move of the 60 bars before it and multiplied by 10. The result is passed through a signed power with exponent 2 and pivot 10, so small rises give a near-zero short and sharp rises give a large short. It is then negated, giving a forecast between 0 and −20 (an average-sized rise gives about −10, half an average rise about −2.5, 1.4 times an average rise about −20). On every other day (down days, flat days, up days on volume at or above the 20-day average) the forecast is 0. The forecast is never positive.
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: Horizon 1 bar. Take the bars where the forecast is non-zero, pooled over the 6 windows; each event is one non-overlapping next-day return. On those bars, the mean next-day close-to-close return minus the mean next-day return of all window bars must be negative with a t-statistic at or below −2.0, on at least 50 events. Supporting check: the third of events with the largest |forecast| must have a more negative mean excess next-day return than the smallest third.
Reject: Over the same pooled events, the mean excess next-day return is zero or positive, so low-volume up days are followed by price holding or rising at least as much as an ordinary day.
Inconclusive: An excess mean that is negative but has a t-statistic between −2.0 and 0, or fewer than 50 qualifying events. Also a negative excess mean whose size does not grow with |forecast| (the supporting check fails).
Deviation: "Unusually low volume" becomes "volume below its 20-day average" (about half of up days qualify), and "sharp" is a graded damping (signed power) rather than a threshold. "Followed by price falling back" is tested only over the single next day, because the short exists only while the qualifying day is the latest bar. The position is not sized by how thin the volume is, because the only volume component is on/off and can only serve as the regime condition. The high-volume half of the brief is not tested here.
