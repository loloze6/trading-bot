---
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4330 USD
---
## Findings
- **F1:** The book loses to its fees, not to its forecast. Summed over all coins and windows, its position earned +4.84 before costs and paid 9.38 in fees, about twice what it earned. Its 11085 trades last a median of 120 minutes and average +0.076 % before fees but -0.024 % after, with 48.8 % winning. A 2-hour bet worth +0.14 % per case pays a 0.22 % round trip at hours 19 and 21, so it cannot cover it (F2, F11).
- **F2:** The rebound is real but small and sits in the deepest falls only. From the 20:00 close, the deepest fifth of 24-hour falls beats the coin's drift by 20.0 bps over 2 hours (n 3453). The other four fifths range from -3.7 to +3.9 bps, so the grading the book uses beyond that top fifth carries nothing.
- **F3:** The same deepest fifth keeps rising long after the book has sold. Its excess is +26 bps over 24 hours and +32 bps over 48 hours from the 20:00 close. On a non-overlapping 24-hour grid at any hour, the deepest fifth of 24-hour falls gains +44.8 bps over 24 hours and +42.6 bps over 48 hours (n 3335), against -11 to -34 bps for the other fifths. That 1-to-2-day rebound is twice the 22-bps round trip, while its 2-hour part at an arbitrary hour is -0.6 bps.
- **F4:** The rebound over a day is largest when the 24-hour fall follows a fall over the 48 hours before it. On the any-hour 24-hour grid, deep 24-hour falls in the bottom third of the prior 48-hour return gain +96.5 bps over 24 hours and +66.1 bps over 48 hours (n 1203). After a middling prior 48 hours they gain -21.7 and -6.5 bps (n 948), and after a prior rise +45.6 and +58.0 bps (n 1184).
- **F5:** Among deep 24-hour falls at the 20:00 close, the grind-made ones rebound most, against the brief's jump story. Falls in the bottom third of share-of-move-in-the-largest-hour gain +35.4 bps over 2 hours (t 4.3) and +91.0 bps over 48 hours (t 3.5, n 1115). The middle third gains -18.5 bps over 48 hours and the top third +23.8 bps (t 1.2).
- **F6:** The 2-hour rebound fails in falling-market years, and the book's daily losses follow those years. In 2022 the deepest fifth at 20:00 earned -5.2 bps over 2 hours and in 2023 -6.6 bps, against +16 to +38 bps in the other years. The book's mean daily return was -6.3, -6.4 and -6.7 bps in 2018, 2022 and 2023, when the coins' daily returns were -34.7, -18.0 and +15.0 bps.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound` (from F1, F2, F3): The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_extended-fall-daily-rebound` (from F3, F4): The more a coin has fallen over the last 24 hours, at any hour, the more it rises over the next 1 to 2 days, and the more so the more it had also fallen over the 48 hours before those 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more` (from F3, F5): The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
