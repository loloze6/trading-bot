---
idea: 003-03_high-volume-up-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp up move on unusually high volume -> adapted: "unusually high" becomes a regime veto (the bar's volume at or above its 20-day mean); "sharp" becomes graded by the size of the one-day rise.
- Comparison: unusually high volume against normal volume -> adapted: the bar's volume is compared on/off with its 20-day mean, because no graded volume-ratio component exists.
- Outcome: price keeps rising after the move -> adapted: "after X" becomes "while X", so the long is held through the next bar only and the holding period is dropped.
- Verdict transfer: yes: the test measures whether sharp up days on above-average volume lead to rises beyond holding, sized by the sharpness of the move, which is the idea's claim.
Forecast: Each day the regime checks the one-day move. If the close rose and the day's volume is at or above its 20-day mean, the bar is "trending". Otherwise it is flat, with forecast 0. In the trending regime the forecast is the one-day percent rise: - it is standardised against its own last 60 values (target 10, cap 20); - it is clipped at 0, so it is long only; - it is passed through signed_power with exponent 2, so ordinary rises give small longs and sharp rises give large ones (5 becomes 2.5, 10 stays 10, 15 becomes 22.5, and the total is clipped at 20). The forecast is never negative. It is zero on down days and on low-volume days.
Config: 003-03_high-volume-up-move-continues_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the coin's next-bar return on every active bar (forecast > 0), weighted by the position. Compare it with the coin's mean daily return over all bars of the same windows. Each bar counts once, so returns do not overlap.
- Supporting check: On active bars, the next-bar return is higher in the top third of positions (the sharpest high-volume rises) than in the bottom third.
- Confirm: Pooled over the 6 windows, the position-weighted mean next-bar excess return is above 0 with t ≥ 2, and the supporting check has the same sign.
- Reject: The position-weighted mean next-bar excess return is ≤ 0. Or the top third of positions has a lower next-bar return than the bottom third, with t ≤ -2.
- Inconclusive: A positive excess return with t < 2, or a positive main measure whose supporting check has the opposite sign. At least 60 active bars are needed in total; fewer makes the test inconclusive.
