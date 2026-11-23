---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's Sunday close-to-close move, a fall or a rise -> kept: the Sunday bar's one-day return, read at Sunday's close (the regime is on when the coming bar is a Monday).
- Comparison: the weekend's volume against the coin's usual 20-day volume, thinner meaning a larger share undone -> adapted: the 20-day base volume over the Saturday-Sunday mean volume multiplies the move, so the fade shrinks smoothly on heavy volume instead of being refused outright.
- Outcome: the move is partly undone over the next 3 days, against its direction -> kept: a fade held for 3 daily bars.
- Verdict transfer: yes: the forecast is the Sunday move faded and weighted by weekend thinness, held for the idea's 3 days, so the test's result is the idea's result.
Forecast: The forecast is non-zero only at the close of each Sunday bar. On every other bar it is 0, and the 3-bar holding period keeps each Sunday bet from Monday to Wednesday. The single component is `ThinVolumeScaledReturnComponent` with these settings: `period` 1 (Sunday's close-to-close return), `window` 20 (divided by the mean absolute one-day move of the last 20 days), `volume_period` 2 (Saturday and Sunday mean volume), `base_near` 2 and `base_far` 21 (the 20 days before the weekend). The component is the move in usual moves times the base volume over the weekend volume. It is standardised over 60 bars and negated. The forecast is short after a Sunday rise and long after a Sunday fall. Its size grows with the size of the move and with how thin the weekend's volume was against the 20-day base. It shrinks toward 0 for small moves or heavy weekend volume.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are Sunday bars with a non-zero forecast, which are 7 days apart and so never overlap over 3 bars. For each case, take forecast/10 x (the coin's 3-bar return from Sunday's close minus the coin's mean 3-bar return over all its windows). Measure the mean of this over all cases, with the ordinary t of the mean. It is a position-weighted gain before costs, judged against holding the coin.
- Supporting check: Split the cases at the median of the volume factor, base 20-day mean volume over Saturday-Sunday mean volume, recomputed from the recorded volume. In the fade direction, compute the unusual 3-bar move divided by the coin's usual 3-bar move. The thin half minus the heavy half must have a Welch t of 1 or more.
- Confirm: The main measure has t ≥ 2 over at least 200 cases, and the supporting check passes.
- Reject: The main measure has t ≤ -2 over at least 200 cases, meaning Sunday moves continue rather than fade.
- Inconclusive: A main t between -2 and 2 is inconclusive. So is a main t ≥ 2 when the thin-minus-heavy t is below 1, and so is any result on fewer than 200 cases.
