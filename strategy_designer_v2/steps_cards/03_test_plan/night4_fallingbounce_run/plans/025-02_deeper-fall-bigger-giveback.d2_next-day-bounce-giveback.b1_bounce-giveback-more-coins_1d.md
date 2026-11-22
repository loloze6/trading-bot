---
idea: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a coin with a negative 90-day return that just had a one-day rise of several usual daily moves -> adapted: the 90-day fall is a regime (90-bar return below 0), and the rise is today's return over its 20-day volatility, graded with a steep dead zone instead of a "several moves" threshold.
- Comparison: the rise counted in usual daily moves; the larger the rise, the larger the fall -> kept: the position grows with the volatility-scaled rise.
- Outcome: the price falls over the next day -> kept: a short held for 1 bar on daily bars.
- Verdict transfer: yes: the test shorts exactly these bounces in 90-day falling coins for one day, sized by the bounce in usual moves, so its result speaks for the idea.
Forecast: On bars where the coin's 90-bar return is below 0 (regime `mean_reversion`), the forecast is short. Its size comes from today's one-bar return divided by the standard deviation of the last 20 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 20). The steps are: - Standardise it over 60 bars. - Clip it at 0, so only rises count. - Negate it. - Apply `signed_power` with exponent 3 and pivot 20. This is the strongest graded dead zone: ordinary rises give almost nothing, and rises of several usual moves give large shorts. The forecast is never positive. It is 0 on down days. On bars where the 90-bar return is 0 or above, the regime is `unknown`, which is null, so the book is flat.
Config: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.b1_bounce-giveback-more-coins_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The unusual move, in the short direction, on the cases. A case is a bar where the forecast reaches -2 or below. The unusual move is the next-day return minus the coin's mean daily return over all windows, negated. Report its mean over the cases and the ordinary t of that mean. Horizon 1 means every case is independent.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the larger half's mean unusual move exceeds the smaller half's.
- Reject: The main measure's mean is below 0 with t ≤ -2, meaning bounces in falling coins keep rising the next day.
- Inconclusive: Any other result, including |t| < 2, or t ≥ 2 with the larger half not ahead. At least 30 cases across all coins and windows are needed; with fewer, the test is inconclusive.
