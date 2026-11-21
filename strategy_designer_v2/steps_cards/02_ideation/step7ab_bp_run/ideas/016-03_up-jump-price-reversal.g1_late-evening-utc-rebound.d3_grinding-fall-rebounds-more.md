---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days.
Consequence: A grinding daily decline is a better long for the next two days than an equally deep one made by a single violent hour.
Why:
- F3: The same deepest fifth keeps rising long after the book has sold. Its excess is +26 bps over 24 hours and +32 bps over 48 hours from the 20:00 close. On a non-overlapping 24-hour grid at any hour, the deepest fifth of 24-hour falls gains +44.8 bps over 24 hours and +42.6 bps over 48 hours (n 3335), against -11 to -34 bps for the other fifths. That 1-to-2-day rebound is twice the 22-bps round trip, while its 2-hour part at an arbitrary hour is -0.6 bps.
- F5: Among deep 24-hour falls at the 20:00 close, the grind-made ones rebound most, against the brief's jump story. Falls in the bottom third of share-of-move-in-the-largest-hour gain +35.4 bps over 2 hours (t 4.3) and +91.0 bps over 48 hours (t 3.5, n 1115). The middle third gains -18.5 bps over 48 hours and the top third +23.8 bps (t 1.2).
