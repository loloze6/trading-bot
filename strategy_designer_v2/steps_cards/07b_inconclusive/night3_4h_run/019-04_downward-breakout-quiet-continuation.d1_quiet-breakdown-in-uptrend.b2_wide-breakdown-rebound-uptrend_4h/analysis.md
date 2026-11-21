---
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
idea tested: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3589 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but small: the mean 18-bar excess return is +0.24 % with t 0.97 over 1182 independent cases, a strength of 0.023. At 6, 12 and 36 bars it is +0.07 %, +0.10 % and +0.04 %, all with t below 1, so no other horizon clears it either.
- **F2:** The rise is all in the widest broken stretches, measured as the prior two-day span counted in average 4h bar ranges, with no standardisation. The three narrowest fifths (spans of 1.0 to 3.0 bar ranges) each lose -0.32 % to -0.52 % over 3 days, with t from -0.58 to -0.94 on about 184 cases each. The two widest fifths (3.0 to 14 bar ranges) gain +1.44 % (t 2.60, 184 cases) and +2.23 % (t 2.99, 185 cases).
- **F3:** The test's forecast sees this ordering less sharply than the plain width does. Its Spearman with the excess return is 0.078, against 0.127 for the plain width count, and its standardisation against its own past 180 values mixes narrow and wide stretches across its quartiles.
- **F4:** The forecast's top quartile (forecast 8.8 to 20) gains +1.42 % over 3 days (t 2.66, 300 cases), a strength of 0.158. That is about 7 times the 0.19 % cost of a trade. The rise keeps growing to +1.84 % at 6 days (t 2.32, 287 cases).
- **F5:** The effect is mixed across periods, which drowns the pooled mean:
- **F6:** By coin the pooled result is mixed. BTC (-0.36 %) and XMR (-0.29 %) are negative, while LTC (+0.98 %, t 1.77), ETH (+0.59 %) and ZEC (+0.54 %) are positive. Among the widest-forecast cases, 5 of 6 coins are positive (ZEC +3.79 %, t 2.37); BTC is the exception at -0.70 %.
- **F7:** As tested, the idea barely pays for itself. Its total move of +0.64 % per case is 3.3 times the cost of a buy and a sell, but its unusual move of +0.24 % is only 1.2 times that cost. Cases in the widest stretches carry an unusual move of +1.4 % to +2.2 %, many times the cost.

## Ideas
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins` (from F1, F5, F6): When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The wider that stretch was compared with the coin's 30-day average four-hour range, the larger the rise.
- `019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b2_wide-span-breakdown-rebound` (from F2, F3, F4, F7): When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The rise is larger the more of the coin's 30-day average four-hour ranges that two-day stretch spans.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
