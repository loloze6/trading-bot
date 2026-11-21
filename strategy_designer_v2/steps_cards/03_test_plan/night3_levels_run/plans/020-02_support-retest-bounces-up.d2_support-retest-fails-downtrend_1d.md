---
idea: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: price falls back to a price where it turned up several times in 90 days, while the 90-day return is negative -> adapted: "several times" is made graded as a nearness-weighted count of 90-day swing lows near a falling close; a regime holds both conditions.
- Comparison: none (the deeper the 90-day fall, the larger the further fall) -> kept: the size of the 90-day fall grades the short.
- Outcome: falls further over the next 5 days -> kept: a short held 5 bars, judged on the 5-bar return against holding the coin.
- Verdict transfer: yes: the same situation, direction and horizon are measured, with only the touch count made graded.
Forecast: The forecast is active only on bars where two things hold. The 90-day return is below 0, and SwingLowTouchNearness (90 bars, side 2, band 1.5 %, fall gate 5 bars) is above 0. That second condition means the close has fallen over 5 bars and sits within 1.5 % of at least one 90-day swing low. On all other bars the forecast is 0. When active, it averages two parts with equal weight. The first is the touch nearness, standardised and negated, so the short grows as more past turning lows sit nearer the close. The second is the 90-day return, standardised over 90 bars, which is negative here, so the short grows with the depth of the fall. The forecast is always at or below 0, and its size grows with both the touch strength and the depth of the 90-day fall.
Config: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take the bars of a non-overlapping 5-bar grid in each window where a short bet starts. On each, compute the coin's 5-bar return minus its mean 5-bar return over all windows, signed for the short (negated). Report its mean and its t.
- Supporting check: Split the cases at the median of |forecast|. The mean signed excess fall of the larger-forecast half minus that of the smaller half must be above 0.
- Confirm: The mean signed excess fall is above 0 with t >= 2, and the supporting check is above 0.
- Reject: The mean signed excess fall has t <= -2, meaning the price rises more than usual after the cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure with t >= 2 whose supporting check is not above 0 is also inconclusive. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
