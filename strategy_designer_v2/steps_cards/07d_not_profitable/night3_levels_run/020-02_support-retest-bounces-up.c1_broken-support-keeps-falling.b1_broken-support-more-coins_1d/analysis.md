---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4110 USD
---
## Findings
- **F1:** The book fails mainly because it is short against coins that rise. It is short on 77 % of bars, with a mean position of -0.46. The position held times the coins' mean daily return costs it -0.066 % a day. Its timing adds back about +0.025 % a day, so the book loses -0.040 % a day overall. The coins' drift sinks 18 of 19 coins (DOGE -0.22 %/day, TRX -0.12 %/day).
- **F2:** The forecast separates cases, but on its active side the coin still rises before costs. Over 5 days the active grid cases (n 4943) return +0.41 %, against +1.53 % when flat (n 2185). That makes the unusual move a short gains -0.34 %, while the total move a short earns is negative (-0.46 % per case against a 0.22 % round trip).
- **F3:** Active cases where the coin is already down hard rebound and carry the short's loss. In the deepest quarter of the 90-day return (mean -51 %, n 282), active cases rise +1.92 % over 5 days (excess +1.15 %, strength -0.10). In the other three quarters they fall -0.73 % to -1.05 % (strength 0.11 to 0.13), which is 3 to 5 times the cost.
- **F4:** The 20-day fall shows the same rebound. In the deepest fifth of the 20-day return (mean -29 %), active cases rise +1.10 % over 5 days and +6.8 % over 20 days (excess +3.8 %, n 198). The other fifths range from +0.18 % to -0.05 % over 5 days and from -0.5 % to -1.4 % over 20 days.
- **F5:** Outside the deep-fall quarter, the move grows with the horizon much faster than the cost. Active cases' raw return goes from -0.7 to -1.05 % at 5 days, to -2.5 to -2.7 % at 10 days, to -1.5 to -6.2 % at 20 days (n 36 to 37 per quarter). Strength rises from 0.13 to 0.21 to 0.30 in the middle quarters, and pooled strength from 0.024 at 5 days to 0.045 at 10 days.
- **F6:** The grading by the forecast holds only after a 90-day decline. Where the 90-day return is negative, the slope t is 2.18 at 5 days (n 820) and 2.95 at 20 days (n 97). Where it is positive, the slope t is -0.62 (n 306), although those cases still fall -0.69 % over 5 days.
- **F7:** With no turning-up low above the close (forecast 0), coins rise more than their drift, and more after a stronger 20-day rise. The excess is +0.77 % over 5 days and +3.6 % over 20 days (n 517). Over 5 days it is +0.55 % to +0.77 % in the three lower fifths of the 20-day return and +1.8 % to +2.2 % in the two upper fifths.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse` (from F1, F2, F3, F5, F6): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin has not already lost a large share of its value over the past 90 days.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d2_capitulation-below-broken-support` (from F3, F4): When a coin's daily close sits just below prices where it turned up several times in the past 90 days after a steep fall, it tends to rise over the next 20 days, and the deeper its 20-day fall, the larger the rise.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d3_clear-above-supports-rises` (from F1, F7): The higher a coin's 20-day return while its daily close sits above every price where it turned up in the past 90 days, the more it rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
