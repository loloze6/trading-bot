---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a Saturday-Sunday move made on volume above the mean of the five weekdays before it -> kept: a regime fires on Sunday's last hourly bar when the mean volume of its 48 weekend bars over the mean of the 120 weekday bars before them exceeds 1.
- Comparison: larger with the move, the volume ratio and the coin's calm over 30 days -> kept: the 48h move in 30-day usual 48h moves (larger with the move and when the past 30 days were calm), times the weekend/weekday volume ratio.
- Outcome: the move continues in the same direction over the next 48 hours -> kept: the bet is signed like the weekend move and held 48 bars.
- Verdict transfer: yes: the forecast exists only at the weekend's close, on heavy-volume weekends, follows the move's sign, and grows with move, volume and calm, so its 48h result is the idea's.
Forecast: Only on the bar whose next bar opens Monday 00:00 UTC, and only when the mean volume of the last 48 bars over the mean of the 120 before them is above 1, the forecast is RecentToPriorVolumeScaledReturnComponent (period 48, window 720, base_period 120). This is the 48h return in units of the mean absolute 48h move over the last 30 days, times that volume ratio, standardised over its last 500 values. It is positive after a weekend rise and negative after a weekend fall. It grows with the move, with the weekend volume against the weekdays, and with the calm of the past 30 days. On every other bar it is 0, and the bet is held 48 bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the weekend bets, one per coin and weekend, which do not overlap. For each case, take forecast/10 x (the coin's 48h return from the bet's close minus its normal 48h drift over all windows). The measure is the mean of this over all cases, with its t, before costs.
- Supporting check: none
- Confirm: The mean position-weighted unusual 48h move is positive with t >= 2, over at least 100 cases.
- Reject: The mean is negative with t <= -2, over at least 100 cases: weekend moves are reversed, not continued.
- Inconclusive: Any t between -2 and 2, or fewer than 100 cases, neither confirms nor rejects.
