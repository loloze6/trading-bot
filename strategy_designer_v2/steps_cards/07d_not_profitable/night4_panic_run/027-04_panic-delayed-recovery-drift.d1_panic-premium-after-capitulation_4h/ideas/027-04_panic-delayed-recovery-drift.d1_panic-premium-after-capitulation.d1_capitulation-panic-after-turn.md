---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is higher than usual, only while the coin's 90-day return before the stretch is deeply negative and the coin has already risen off its 30-day low by the close one day after the stretch. The deeper that 90-day fall and the larger that rise off the low, the higher this later return.
Consequence: A trader would buy a post-panic recovery only once a long capitulation has visibly turned up off its low, and refuse panics in shallow declines or panics still making new lows, which were followed by below-usual returns and the deepest falls.
Why:
- F1: The deepest fall of the book is what fails Calmar. Its daily returns chained over 2898 days give a yearly return of 10.2 % and a deepest fall of -76.9 % (Calmar 0.13). Four windows carry most of that fall: w14 at -65.9 %, w2 at -52.9 %, w7 at -44.1 % and w9 at -37.5 %, each held at a mean exposure of 0.72 to 1.10 of the book. The trades last 37 days on average, against a 13-day horizon; their 10th percentile is -31.9 % and their worst is -65.4 %.
- F2: The effect exists only after the most extreme 90-day falls, so the tested multiplier is wrongly graded. Entries whose 90-day return before the stretch was below -51.5 % show an unusual 13-day move of +21.5 % (t 8.66, 94 cases, 85 % positive). Every shallower octile, from -51.5 % up to 0 %, shows -5.3 % to +1.7 %, and the six octiles above -39.6 % are all negative with t between -2.8 and -6.2 (about 560 cases). The forecast still goes long on all of these.
- F3: Most of the book's exposure sits in the zone where the effect is negative. Bars with a 90-day return between -20 % and 0 % were held at a mean allocation of 1.00 and lost 1.34 in summed bar gain over 5183 bars. Bars with a 90-day return between 0 % and +50 % lost 1.17. Bars below -40 % lost 0.25, mostly in w7 (-0.90, allocation 0.79) and w14 (-0.26, allocation 1.70).
- F4: Inside the deep-fall cases, the rise already made off the 30-day low at the entry close grades the move and shrinks the falls that follow. By tercile of that rebound, the unusual move is +8.0 % (t 2.17), +12.4 % (t 4.18) and +14.5 % (t 5.45). The mean worst move inside the 13 days narrows from -16.2 % to -9.9 % to -6.7 %, and the share of positive cases rises from 53 % to 79 %. In the other cases, every rebound quartile shows -0.4 % to -8.0 %.
- F5: Over all 4698 entries, the unusual 13-day move is -0.43 % (t -1.69). Only the top quartile of forecast strength is positive, at +1.49 % (t 2.41); the lower three quartiles show -0.87 % to -1.22 %, with t between -1.87 and -2.66. The total move per case, +1.45 %, is 7.5 times the 0.19 % cost of a trade, so fees are not the cause: the cause is long exposure where the unusual move is negative.
