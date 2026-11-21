---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days.
Consequence: An evening long after a deep daily fall is paid by holding it for a day or two, where the rebound is larger than a round trip, not by selling two hours later.
Why:
- F1: The book loses to its fees, not to its forecast. Summed over all coins and windows, its position earned +4.84 before costs and paid 9.38 in fees, about twice what it earned. Its 11085 trades last a median of 120 minutes and average +0.076 % before fees but -0.024 % after, with 48.8 % winning. A 2-hour bet worth +0.14 % per case pays a 0.22 % round trip at hours 19 and 21, so it cannot cover it (F2, F11).
- F2: The rebound is real but small and sits in the deepest falls only. From the 20:00 close, the deepest fifth of 24-hour falls beats the coin's drift by 20.0 bps over 2 hours (n 3453). The other four fifths range from -3.7 to +3.9 bps, so the grading the book uses beyond that top fifth carries nothing.
- F3: The same deepest fifth keeps rising long after the book has sold. Its excess is +26 bps over 24 hours and +32 bps over 48 hours from the 20:00 close. On a non-overlapping 24-hour grid at any hour, the deepest fifth of 24-hour falls gains +44.8 bps over 24 hours and +42.6 bps over 48 hours (n 3335), against -11 to -34 bps for the other fifths. That 1-to-2-day rebound is twice the 22-bps round trip, while its 2-hour part at an arbitrary hour is -0.6 bps.
