---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4703 USD
---
## Findings
- **F1:** The tested situation is too narrow to trade: on the 5-day grid of folds B and C it gives only 5 cases on 5 days, so the book made 32 trades at 0.004 trades a day and was in a position on 1 % of coin-days. In the same choppy, agitated profile, dropping the 20-day band (a close in the upper half of the range after a negative 5-day return, with any 20-day fall) gives 17 cases on 10 days with a mean short-direction unusual 5-day move of +15.7 % (t 2.26).
- **F2:** The deepest 20-day falls, which the idea's consequence leaves out, carry the most. Among profile closes in the upper half after a negative 5-day return, the mean 5-day short-direction move is +21.5 % (10 cases, t 3.02, 6 days) when the 20-day return is below -20 %. It is +10.2 % for 5 cases between -20 % and -10 %, and +0.0 % for 2 cases between -10 % and 0. In the book, trades entered with a 20-day return below -15 % averaged +5.6 % net (13 trades), against -6.2 % (19 trades) for the rest.
- **F3:** Neither added condition is an effect on its own; the close's place in the range is. In the profile:
- **F4:** Inside the profile, high closes are graded by the depth of the prior 5-day fall. The mean 5-day short-direction move is:
- **F5:** The effect lives in the choppy, agitated profile only. Outside it, upper-half closes after negative 5-day and 20-day returns give +0.5 % over 5 days (178 cases, t 0.27). In a falling market (60-day return below -10 %) they give -2.3 % (85 cases, t -0.83).
- **F6:** The effect grows with a longer holding. Profile closes in the upper half give a short-direction unusual move of:
- **F7:** The losses that sink the Calmar ratio come from one year and from trades held past the horizon.

## Ideas
- `061-01.b1.b1.b1.d1.d1.d1.d3.d1_high-close-fades-deeper-falls` (from F1, F2, F3, F5): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the nearer that close is to the day's high and the deeper its 20-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d1.d3.d2_high-close-after-drop-fades` (from F1, F3, F4, F5): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range, its price falls over the next five days, and the deeper its 5-day fall before that close and the nearer the close is to the high, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d1.d3.d3_high-close-fades-over-ten-days` (from F3, F5, F6, F7): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next ten days, and the nearer that close is to the day's high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
