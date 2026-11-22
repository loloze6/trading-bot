---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 24 hours, and the larger that range multiple, the higher the return. This holds only while the coin's 7-day return before the stretch lies far from zero, and the return grows with how far that 7-day return lies from zero.
Consequence: A trader would buy intense panics that come after a sharp week, either a capitulation or a blow-off, and would refuse panics after a mildly weak week, which kept falling.
Why:
- F4: Among strong cases (forecast ≥ 1), the return was U-shaped in the coin's 7-day return before the panic.
- F5: The book's deepest falls were carried by its strong panic signals.
- F1: The book did not beat holding the coins. Its Sharpe was 0.541 against holding's 0.554, and its mean daily return was 0.000546 against holding's 0.001179. Its Calmar was 0.28, because its deepest fall of -49.2 % over 27 days in w16 is set against a yearly return of only 13.7 %.
