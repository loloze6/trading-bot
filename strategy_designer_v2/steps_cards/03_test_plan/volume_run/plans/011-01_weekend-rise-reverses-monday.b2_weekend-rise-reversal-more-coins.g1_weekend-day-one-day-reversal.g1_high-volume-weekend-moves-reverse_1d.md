---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a Saturday or Sunday one-day move, scaled by the coin's 20-day volatility -> kept: a WeekdayComponent rule selects bars stamped Saturday or Sunday, and VolatilityScaledReturnComponent (period 1, vol_period 20) measures the move.
- Comparison: that day's volume against the coin's usual volume over the past 20 days, with the reversal growing as that ratio grows -> replaced: a weighted mean can only add VolumeRatioComponent to the move, not multiply the two, and an added unsigned volume term biases the direction.
- Outcome: the move reverses over the next day -> kept: the standardised move is negated, so the forecast fades it over 1 bar.
- Verdict transfer: no: without the volume-scaled size, a confirm or reject would judge plain weekend reversal, not reversal weighted toward heavy-volume weekend moves.
Reason: The idea sizes the fade by the product of the vol-scaled weekend move and the day's volume ratio. The config combines components only by a weighted sum, and no catalogue component computes that product. A volume regime would turn the graded volume weighting into fixed steps.
