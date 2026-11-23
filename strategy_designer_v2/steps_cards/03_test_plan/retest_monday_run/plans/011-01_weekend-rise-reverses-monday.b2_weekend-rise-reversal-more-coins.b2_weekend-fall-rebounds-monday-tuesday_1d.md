---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin fell over the weekend, measured as the Saturday-to-Sunday close-to-close return -> kept: the return of the Sunday daily bar, read at Sunday's close.
- Comparison: the larger the weekend fall, the larger the rise -> kept: the long position grows with the size of the fall.
- Outcome: the coin rises over the next 2 days (Monday and Tuesday) -> kept: the bet is bought at Sunday's close and held 2 daily bars.
- Verdict transfer: yes: the test measures the same Sunday fall, the same 2-day rise and the same size relation the idea states.
Forecast: The forecast is computed only on the bar where the coming bar is a Monday, which is the Sunday bar. A weekday regime rule selects that bar; every other bar is flat. On the Sunday bar, the forecast is the 1-bar price change of the coin, standardised against its last 60 daily changes, then sign-flipped and clipped at 0. It is positive only when Sunday's close is below Saturday's close. It is 0 when Sunday closed flat or up. It grows linearly with the fall measured in the coin's usual daily move: a typical fall gives about +10, and the cap is +20. It is never negative.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The sample is Sunday bars with forecast > 0, one case per coin per Sunday; cases do not overlap because Sundays are 7 bars apart. For each case, take the 2-bar return close[t+2]/close[t] - 1 minus the coin's mean 2-bar return over all its windows, inside one window only. Average these excess returns weighted by forecast. The t uses the per-Sunday cross-coin means as independent cases.
- Supporting check: Fit the excess 2-bar return of the cases on their forecast. The slope must be above 0, so that larger falls are followed by larger excess rises.
- Confirm: The forecast-weighted mean excess 2-bar return is above 0 with t >= 2, and the slope check is above 0.
- Reject: The forecast-weighted mean excess 2-bar return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a slope at or below 0 is also inconclusive. The test needs at least 100 Sundays carrying a case and at least 300 cases in total; with fewer, the result is inconclusive.
