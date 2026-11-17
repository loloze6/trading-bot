---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin fell over the weekend (Saturday-to-Sunday close-to-close return), seen at Sunday's close -> kept: the 1-bar return on the Sunday bar, active only when the coming bar is Monday.
- Comparison: the larger the weekend fall, the larger the rise -> kept: the long position is sized by the size of the fall.
- Outcome: price rises over the next 2 days (Monday and Tuesday) -> adapted: the 2-day holding period is dropped, so the position lasts only the Monday bar; the 2-bar rise is measured in the criterion.
- Verdict transfer: yes: the forecast is set exactly at Sunday's close by the weekend fall, and the criterion judges the 2-bar return that follows it.
Forecast: The forecast is computed only on Sunday bars. These are the bars whose coming bar, as reported by WeekdayComponent, is Monday (weekday 0). On every other bar the regime is null and the forecast is 0. On a Sunday bar, the forecast starts from PriceEvolutionComponent with period 1, which is the Saturday-to-Sunday close-to-close return. This return is standardised against its own past 60 daily values (minimum 20) and then negated. A clip at minimum 0 removes the case where the weekend rose. The forecast is therefore positive and long after a weekend fall. It grows with the size of the fall relative to the coin's usual daily move, up to the cap of 20. It is 0 when the weekend rose or was flat.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use the Sunday bars with forecast > 0, one case per coin per week, so the cases do not overlap and stay inside their window. For each case, take the position-weighted excess return: (forecast / 10) x (close[t+2] / close[t] - 1 minus 2 x the coin's mean daily return over all windows). The measure is the mean of these values and its ordinary t, before costs.
- Supporting check: Regress the excess 2-bar return on the forecast over the same cases; the slope must be positive.
- Confirm: The confirm needs both parts: - the main measure's mean excess return is positive with t >= 2; - the supporting check's slope is above 0.
- Reject: The main measure's mean excess return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with a slope of 0 or below is also inconclusive. At least 100 cases are required across all coins and windows; with fewer, the result is inconclusive.
