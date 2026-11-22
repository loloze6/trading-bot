---
idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42de60c4e850
---
Fidelity:
- Situation: 90-day return negative, a one-day rise of several usual daily moves just happened, and the 30-day return is negative -> kept: all three are regime rules on today's bar, with "several" set to at least 2 usual moves by the 2-sigma convention.
- Comparison: the deeper the 30-day fall, the larger the next-day fall -> kept: the short's size grows with the depth of the 30-day return.
- Outcome: the price falls over the next day -> kept: the horizon is 1 daily bar, short side.
- Verdict transfer: yes: the test measures the idea's own conditions, its own graded size and its own one-day fall.
Forecast: The forecast is active only on bars where three things hold: the 90-day return is below 0, the 30-day return is below 0, and today's one-day return is at least 2 times its 20-day usual daily move. On those bars the forecast is the 30-day percent return, standardised against its own last 60 values. That value is negative, so the forecast is a short whose size grows with the depth of the 30-day fall, capped at -20. On every other bar it is 0.
Config: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: A case is each bar in the mean_reversion regime with a nonzero forecast. For each case, take the position held after that bar times (the coin's next-day return minus the coin's mean daily return over all its windows). The measure is the mean of this over all cases, with the t of that mean.
- Supporting check: Across cases, the correlation between the forecast and the next-day drift-adjusted return is positive: deeper shorts are followed by larger falls.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting correlation is above 0.
- Reject: The main measure's mean is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming t with a correlation of 0 or less. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
