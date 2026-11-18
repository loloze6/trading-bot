---
idea: 011-02_weekend-drop-rebounds-monday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the coin fell over the weekend (Saturday-to-Sunday close-to-close return), and the size of the drop matters -> kept: the Sunday bar's one-bar close return, in usual moves, read only when it is a fall.
- Comparison: none in the idea; "the larger the drop, the larger the rebound" is the grading itself -> kept
- Outcome: the price rises over the next 2 days (Monday and Tuesday), more after a larger drop -> adapted: "after the drop" becomes "while the coming bar is Monday or Tuesday", holding a long position sized by the drop.
- Verdict transfer: yes: the long position is held exactly over the Monday and Tuesday bars and sized by the Sunday fall, so its excess gain answers the idea both ways.
Forecast: The forecast is active only at the closes whose coming bar is Monday or Tuesday, using `WeekdayComponent` in the regime detector. On the coming-Monday regime it reads the bar just closed, Sunday: `VolatilityScaledReturnComponent` (period 1, vol_period 20, lag 0), the Sunday close-to-close return in usual 20-day moves. On the coming-Tuesday regime it reads the same Sunday move one bar back (lag 1). The value is standardised over 60/20, negated so that a fall reads positive, and clipped at 0. The result is a long position that grows with the depth of the weekend drop. It is zero after a weekend rise and zero on every other day of the week.
Config: 011-02_weekend-drop-rebounds-monday_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: One case per weekend: a Sunday bar (regime `trending`) with forecast > 0. For each case, compute forecast/10 x (close[t+2]/close[t] - 1 minus the coin's mean 2-bar return over all windows, on the 2-bar grid), all inside one window. Take the t of the mean of these products, pooling all coins. Cases are 7 bars apart, so they do not overlap.
- Supporting check: The mean excess 2-bar return of the top third of cases by forecast, minus that of the bottom third, is above 0.
- Confirm: The main t is 2 or more and the supporting check passes.
- Reject: The main t is -2 or less.
- Inconclusive: Any main t between -2 and 2, or t of 2 or more with the check failing. Fewer than 100 cases with forecast > 0 is also inconclusive.
