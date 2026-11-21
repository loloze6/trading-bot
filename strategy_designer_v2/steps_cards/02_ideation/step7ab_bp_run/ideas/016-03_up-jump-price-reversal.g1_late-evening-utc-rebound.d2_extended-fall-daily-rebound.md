---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the last 24 hours, at any hour, the more it rises over the next 1 to 2 days, and the more so the more it had also fallen over the 48 hours before those 24 hours.
Consequence: A long after a deep day's fall that extends an earlier two-day fall is a multi-day trade large enough to pay its costs, and a reason not to short after such a slide.
Why:
- F3: The same deepest fifth keeps rising long after the book has sold. Its excess is +26 bps over 24 hours and +32 bps over 48 hours from the 20:00 close. On a non-overlapping 24-hour grid at any hour, the deepest fifth of 24-hour falls gains +44.8 bps over 24 hours and +42.6 bps over 48 hours (n 3335), against -11 to -34 bps for the other fifths. That 1-to-2-day rebound is twice the 22-bps round trip, while its 2-hour part at an arbitrary hour is -0.6 bps.
- F4: The rebound over a day is largest when the 24-hour fall follows a fall over the 48 hours before it. On the any-hour 24-hour grid, deep 24-hour falls in the bottom third of the prior 48-hour return gain +96.5 bps over 24 hours and +66.1 bps over 48 hours (n 1203). After a middling prior 48 hours they gain -21.7 and -6.5 bps (n 948), and after a prior rise +45.6 and +58.0 bps (n 1184).
