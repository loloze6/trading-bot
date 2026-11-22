---
idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise of several usual daily moves -> adapted: the threshold "several" is made graded through the strongest graded dead zone on the volatility-scaled one-day return.
- Comparison: a 90-day return that is negative, and a rise that is larger in usual daily moves -> kept: the 90-day return below 0 is a regime condition, and the size is the return over the 20-day volatility.
- Outcome: a larger fall over the next day -> kept: a short, held for 1 bar, whose size grows with the rise.
- Verdict transfer: yes: the forecast shorts exactly the coins in a 90-day fall after a large scaled one-day rise, more for larger rises, over the next day.
Forecast: A regime rule makes the strategy active only while the coin's 90-day return is below 0 (`mean_reversion`). On all other bars the forecast is flat. While the rule holds, the forecast reads today's one-day return divided by the 20-day standard deviation of daily returns. That value is standardised over its last 60 values and clipped at 0, so only rises count. A signed power with exponent 3 and pivot 20 then shrinks ordinary rises to near 0 and lets the largest rises reach a full position. The result is negated, so the forecast is short. It is 0 on down days and when the 90-day return is not negative, and it grows more negative, about as the cube of the rise, the larger the rise in usual moves.
Config: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Cases are short bets: bars where the forecast falls by at least 2 points from its last level on the short side. For each case, take the coin's next-day return minus its mean daily return over all windows, with the sign flipped so a fall counts as a gain. The measure is the mean of this value over all cases, with its t-statistic.
- Supporting check: The same mean excess fall is larger in the cases whose |forecast| is in the top half than in the cases in the bottom half (Welch t > 0).
- Confirm: The main measure has t ≥ 2 over at least 30 cases, and the top-half cases show a larger mean excess fall than the bottom-half cases.
- Reject: The main measure has t ≤ -2 over at least 30 cases: the coin rose more than its usual drift after the bounces.
- Inconclusive: Any t between -2 and 2, or a main t ≥ 2 while the size check fails, or fewer than 30 cases over all coins and windows.
