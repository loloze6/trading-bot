---
idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's absolute 3-day return, up or down -> kept: |72-bar return|, built as the positive part plus the negated negative part of one standardised 72-bar return.
- Comparison: bigger moves against quiet 3 days, "the larger, the more" -> kept: the position grows with the move's size and is near zero after a quiet 3 days.
- Outcome: the coin rises over the next 3 days, more after bigger moves -> kept: return over the next 72 bars, long side, against the coin's average.
- Verdict transfer: yes: the forecast is the idea's graded long lean on the 3-day move size, and its payoff over 72 bars is the idea's claim.
Forecast: Two copies of PriceEvolutionComponent(period 72), each standardised over the last 73 stored values. One is clipped at 0 from below (the up move). The other is negated, then clipped at 0 (the down move). With equal weights the forecast is |standardised 72-bar return| / 2. It is never negative. It is near 0 after a quiet 3 days and grows linearly with the size of the 3-day move in either direction. It reaches about +5 for a move of usual size and up to +10 at the cap.
Config: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: - Sample bars 0, 72, 144, ... of each window. - On each sampled bar, take the forward 72-bar return minus the coin's mean 72-bar return over all its windows. - Regress that excess return on the forecast, pooling all coins and windows, and report the slope's t.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) is above 0.
- Confirm: The slope is positive with t >= 2, and the timing part of the book is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any |t| < 2, or t >= 2 with a timing part at or below 0. At least 500 independent sampled cases are required; about 5,700 are expected.
