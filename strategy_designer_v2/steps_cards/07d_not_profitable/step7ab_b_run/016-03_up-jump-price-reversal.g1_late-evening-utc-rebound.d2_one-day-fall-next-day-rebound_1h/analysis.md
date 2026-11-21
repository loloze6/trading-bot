---
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3674 USD
---
## Findings
- **F1:** Each case's unusual move is +0.12 % per 24 hours (strength 0.025), but a round trip costs 0.19 %, and the book earns 2.3 bps a day against 6.7 to 15.5 bps for holding the coins; its Sharpe is 0.21 against holding's 0.55, its Calmar is −0.003 and its deepest falls per coin are 39 % to 64 %.
- **F2:** The rebound sits almost entirely in one corner: when the 24-hour fall is in its deepest third and the coin's 10-day return is also in its lowest third (mean −17.7 %), the next 24 hours beat the drift by +0.90 % (t 4.26, 1050 cases). That is +1.05 % total, about 5.5 times a round trip.
- **F3:** A deep 24-hour fall gives nothing when the coin is flat or rising over 10 days: −0.08 % (920 cases) and −0.06 % (612 cases). A shallow 24-hour fall inside a deep 10-day fall loses −0.44 % (t −2.05, 751 cases).
- **F4:** The grading is real on the product of the two falls but on neither alone.
- **F5:** The deep-and-deep cases hold everywhere. Their excess per case is +0.77 % to +1.19 % on each of the 6 coins (135 to 208 cases each), and positive in 16 of 24 windows (median +0.56 %).
- **F6:** Cases where the last 24 hours' hourly moves were large against the coin's 10-day average rebound more.
- **F7:** Falls whose volume was spread evenly over the 24 hours rebound more than falls carried by one hour's volume burst.
- **F8:** The book loses most in the windows where the coins fall, which is where buying every 24-hour dip goes wrong: −36.7 bps a day in w14, −27.5 in w7, −19.9 in w9 and −19.3 in w2.
- **F9:** On BTC the book's gain before costs per unit traded (4.8 bps) is below its fee per unit traded (5.1 bps). On the other coins it covers it, but at 11 to 25 bps against 5.5 to 15.7 bps of fees it leaves little.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.d1_dip-inside-deeper-decline` (from F1, F2, F3, F4, F5, F8): The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, only while it has also fallen over its last 10 days, and the more so the deeper that 10-day fall.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.d2_turbulent-fall-rebound` (from F1, F6, F9): The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, the more so the larger its hourly moves over those 24 hours were compared with its hourly moves over the last 10 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound.d3_evenly-traded-fall-rebound` (from F1, F7): The more a coin has fallen over its last 24 hours, the more it rises over the next 24 hours, the more so the more evenly that day's volume was spread across its hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
