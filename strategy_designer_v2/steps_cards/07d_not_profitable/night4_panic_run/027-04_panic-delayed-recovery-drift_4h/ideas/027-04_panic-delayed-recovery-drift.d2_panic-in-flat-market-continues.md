---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is lower than usual, the more so the more extreme the panic, while the coin's 90-day return before the stretch is close to flat.
Consequence: A trader would treat a panic that hits a coin with no long prior fall as the start of further weakness over the next two weeks, and stay out rather than buy it.
Why:
- F5: The coin's prior 90-day trend sorts the cases. Of the 266 cases with a 90-day history:
- F2: The Calmar of 0.41 fails because the book's deepest fall is -71.5 %, and its worst 30-day stretches match holding's in the same stretch. In w16 the book fell -63.1 % against -58.2 % for holding, in w14 -57.4 % against -53.3 %, and in w2 -34.4 % against -33.5 %. The panic signal never steps the book out of these market-wide falls.
- F1: The book is effectively holding the coins, and its falls are the coins' falls. It held a long position on 96.2 % of bars, with a mean allocation of 0.97, even though the forecast was positive on only 48.6 % of bars. Its trades lasted 54.2 days on average against a 13-day bet. Its daily returns correlate 0.918 with holding the coins.
