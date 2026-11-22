---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is higher than usual, only while the coin's 90-day return before the stretch is deeply negative; the deeper that 90-day fall and the more extreme the panic, the higher this later return.
Consequence: A trader would buy the drift after a panic only when it ends a long capitulation, and refuse to buy panics inside a flat or rising market, where they were followed by below-usual returns.
Why:
- F3: The panic effect the book bets on is not in the data overall. The mean 78-bar unusual move over 1266 cases is -0.41 % (t -0.70, strength -0.027). The +1.56 % total move per case, 8.1 times the 0.19 % trade cost, comes entirely from the coins' +1.97 % normal drift.
- F5: The coin's prior 90-day trend sorts the cases. Of the 266 cases with a 90-day history:
- F6: The 30-day trend before the panic does not separate the cases the same way. All four quartiles of the 30-day return, from -26 % to +47 %, have unusual moves between -0.80 % and -0.09 %, with |t| at most 0.69 (n about 218 each). The premium shows only in the longer, 90-day capitulation, not in a recent slide.
- F2: The Calmar of 0.41 fails because the book's deepest fall is -71.5 %, and its worst 30-day stretches match holding's in the same stretch. In w16 the book fell -63.1 % against -58.2 % for holding, in w14 -57.4 % against -53.3 %, and in w2 -34.4 % against -33.5 %. The panic signal never steps the book out of these market-wide falls.
