---
line: 7.d confirmed, not profitable
backtest: 037-01_wide-day-fall-next-day-rebound_1d
idea tested: 037-01_wide-day-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4315 USD
---
## Findings
- **F1:** The failing measure is Calmar (0.69 against 0.75). On folds B and C the book's deepest falls are -31.8 % in w17, -31.7 % in w16 and -29.4 % in w9. Its daily returns correlate 0.63 with the coins' own. Its 40 worst days (book -6.1 %, coins -10.2 %) carry 52 % of all losses. On the coins' worst 10 % of days the book loses 2.0 % a day, so its falls are long positions held into the coins' crashes.
- **F2:** The vol-target sizing points against the effect. Among strong signals (forecast ≥ 11.7), the next-day excess return rises from +0.24 % in the calmest third of 20-day swing to +1.40 % in the most agitated third. The position falls the other way, from 1.02 to 0.58 of the book. The largest positions sit where the rebound is smallest, and the sizing halves the best cases.
- **F3:** The effect lives where the coin's recent swing is high against its longer swing, and that condition alone does not earn. Strong signals with 20-day swing over 60-day swing in its lowest third lose 0.47 % the next day, against +0.61 % in the middle third and +1.33 % in the top third (289/289/290 cases). Bars with no signal in the most agitated third of 20-day swing lose 0.61 %, while signal bars there earn +0.84 %. The agitation does not carry the effect; it is where the forced-selling overshoot of the theory happens.
- **F4:** The weak half of the signal earns nothing and pays fees. Forecasts up to 5.44 (1707 bars) earn +0.005 % per bar with an excess return of -0.07 %. Forecasts 5.44–11.7 earn +0.12 % per bar. Forecasts above 11.7 (1710 bars) earn +0.56 % per bar and carry 9.6 of the 10.8 summed gain. A trade costs 0.19 %, and the book trades 0.37 times a day.
- **F5:** The rebound grows with how deep the coin has already fallen over the last days, and a deep past fall alone does not rebound. Signal bars in the lowest fifth of 3-day return (below -8.5 %) gain +1.23 % in excess the next day, against -0.35 % for a 3-day return of -3.9 % to -1 %. Signal bars in the lowest fifth of 20-day return gain +0.59 %, while bars with no signal in the same 20-day bin lose 1.27 %.
- **F6:** The size cannot be told from zero, which is why the book's margin is thin. The unusual move is +0.18 % per case (t 1.41 over 1631 days, strength 0.039) against a 0.19 % trade cost, so only the stronger, agitated cases (F2–F5) clear the cost.

## Ideas
- `037-01.d1_wide-falls-rebound-when-agitated` (from F1, F2, F3, F6): The larger a coin's one-day fall and the wider that day's high-to-low range against its own average daily range over the past 14 days, taken together, the larger the rise over the next day, in an agitated market.
- `037-01.d2_only-extreme-wide-falls-rebound` (from F4, F6): The larger a coin's one-day fall and the wider that day's high-to-low range against its own average daily range over the past 14 days, taken together, the larger the rise over the next day, and the rise grows faster than the product itself, so that the move is concentrated in the largest and widest falls.
- `037-01.d3_wide-fall-after-multi-day-decline` (from F1, F5, F6): The larger a coin's one-day fall and the wider that day's high-to-low range against its own average daily range over the past 14 days, taken together with the depth of its 3-day fall, the larger the rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
