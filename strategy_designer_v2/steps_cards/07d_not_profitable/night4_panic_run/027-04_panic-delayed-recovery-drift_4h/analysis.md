---
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift_4h
idea tested: 027-04_panic-delayed-recovery-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3621 USD
---
## Findings
- **F1:** The book is effectively holding the coins, and its falls are the coins' falls. It held a long position on 96.2 % of bars, with a mean allocation of 0.97, even though the forecast was positive on only 48.6 % of bars. Its trades lasted 54.2 days on average against a 13-day bet. Its daily returns correlate 0.918 with holding the coins.
- **F2:** The Calmar of 0.41 fails because the book's deepest fall is -71.5 %, and its worst 30-day stretches match holding's in the same stretch. In w16 the book fell -63.1 % against -58.2 % for holding, in w14 -57.4 % against -53.3 %, and in w2 -34.4 % against -33.5 %. The panic signal never steps the book out of these market-wide falls.
- **F3:** The panic effect the book bets on is not in the data overall. The mean 78-bar unusual move over 1266 cases is -0.41 % (t -0.70, strength -0.027). The +1.56 % total move per case, 8.1 times the 0.19 % trade cost, comes entirely from the coins' +1.97 % normal drift.
- **F4:** The size of the panic barely grades what follows. Cases in the weakest forecast group (mean 2.9) have an unusual move of -1.76 % (t -1.75, n 317). The strongest group (mean 18.3) has -0.02 % (t -0.02, n 633).
- **F5:** The coin's prior 90-day trend sorts the cases. Of the 266 cases with a 90-day history:
- **F6:** The 30-day trend before the panic does not separate the cases the same way. All four quartiles of the 30-day return, from -26 % to +47 %, have unusual moves between -0.80 % and -0.09 %, with |t| at most 0.69 (n about 218 each). The premium shows only in the longer, 90-day capitulation, not in a recent slide.

## Ideas
- `027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation` (from F3, F5, F6, F2): After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is higher than usual, only while the coin's 90-day return before the stretch is deeply negative; the deeper that 90-day fall and the more extreme the panic, the higher this later return.
- `027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues` (from F5, F2, F1): After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is lower than usual, the more so the more extreme the panic, while the coin's 90-day return before the stretch is close to flat.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
