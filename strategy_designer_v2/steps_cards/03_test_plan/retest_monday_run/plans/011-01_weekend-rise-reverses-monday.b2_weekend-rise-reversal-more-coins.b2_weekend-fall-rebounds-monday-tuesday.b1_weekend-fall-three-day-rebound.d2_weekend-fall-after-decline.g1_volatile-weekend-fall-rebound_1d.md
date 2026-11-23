---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a coin fell over the weekend (Saturday-to-Sunday close-to-close return) -> kept: the Sunday bar's return, read at Sunday's close (coming bar Monday), long only on falls.
- Comparison: rise grows with the size of the weekend fall and with the coin's 20-day volatility of daily returns -> kept: the fall in percent times the 20-day standard deviation of daily returns.
- Outcome: the coin rises over the next 3 days -> kept: each Sunday bet is held 3 daily bars.
- Verdict transfer: yes: the test measures the weekend fall, its volatility weighting and the 3-day rise as stated.
Forecast: The forecast is computed only on the Sunday bar, the bar whose coming bar is Monday, using a weekday regime rule; it is 0 on every other day. On that bar it is VolatilityWeightedFallComponent (vol_period 20), which is max(0, −Sunday's daily return) in percent × the 20-day standard deviation of daily returns. This is standardised against its own past 60 values (min_periods 20). The forecast is 0 when Sunday closed up or flat. It is positive (long) after a Sunday fall. Its size grows continuously with the depth of the fall and with the coin's recent volatility, up to the +20 cap. It is never negative, and each bet is held 3 bars.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Each case is a Sunday bar with forecast ≥ 2 (one bet; Sundays are 7 bars apart, so cases never overlap). For each case, take the coin's 3-bar return from that close minus the coin's normal 3-bar drift (its mean over non-overlapping 3-bar stretches of all windows). The measure is the mean of this excess return over all cases, with its ordinary t.
- Supporting check: The forecast-weighted mean excess return over the cases is larger than the unweighted mean. This shows that larger fall × volatility readings are followed by larger rebounds.
- Confirm: The mean excess 3-bar return is positive with t ≥ 2 over at least 100 cases, and the supporting check passes.
- Reject: The mean excess 3-bar return is negative with t ≤ −2 over at least 100 cases.
- Inconclusive: Any t between −2 and 2, or a confirming t with a failed supporting check. Any result with fewer than 100 cases is also inconclusive.
