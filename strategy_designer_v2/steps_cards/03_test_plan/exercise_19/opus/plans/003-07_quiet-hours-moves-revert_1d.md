---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: untestable
---
Fidelity:
- Situation: sharp move during quiet hours or weekends, on thin volume -> replaced: by a sharp move on a low-volume daily bar, because 1d bars hide intraday hours and no component reads the weekday
- Comparison: thin quiet-session liquidity against the busier session that follows -> replaced: by the day's volume against its own recent average
- Outcome: the move partly reverses once busy hours and volume return -> adapted: contrarian position held for the next daily bar only
- Verdict transfer: no: a low-volume-day test neither confirms nor rejects a reversal of moves made in quiet hours or on weekends.
Reason: The idea's situation is a time of day (quiet hours) and a calendar session (weekends). On 1d bars an intraday quiet-hour move is merged into the whole day's bar, so measuring it needs sub-daily bars. The config also cannot express day-of-week, because no component or rule reads the timestamp's weekday. Swapping these for "low-volume day" would replace the situation, not adapt it.
