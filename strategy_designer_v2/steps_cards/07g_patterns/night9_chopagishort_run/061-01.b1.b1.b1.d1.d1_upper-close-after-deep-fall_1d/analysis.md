---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.7081 USD
---
## Findings
- **F1:** Inside the choppy agitated profile the close's place in its day's range grades the next 5 days: the slope of the unusual 5-day move on close location is -0.097 (t -2.01 with one day's cases taken together; 86 cases on 58 days). The top quarter of closes (0.75 to 1) is followed by -5.2 % (t -1.81, 26 cases, 19 days, strength -0.44), and the 0.5 to 0.75 quarter by -9.2 % (t -1.22, 21 cases). This holds without the tested idea's negative 5-day return condition.
- **F2:** The agitation carries the fade, as the brief's second test asks. In choppy markets outside the agitated profile, the top quarter of closes is followed by +5.2 % over 5 days (t 1.22, 40 cases, 24 days). Over all bars outside the profile, upper-half closes are followed by +0.9 % to +1.3 % (t 0.8 to 1.3).
- **F3:** The fade is slower than the brief's two days. Inside the profile the slope on close location is -0.032 at 2 days (t -1.10, 227 cases, 147 days) against -0.097 at 5 days (F1). The top quarter of closes gives -1.4 % at 2 days (t -1.03), -1.0 % at 3 days (t -0.70) and -5.2 % at 5 days.
- **F4:** A few large wins carry the book. Trades in the top forecast tercile average +3.56 % but have a median of -1.31 %, while the two lower terciles average -1.03 % and -0.72 %. The year 2020 holds 1.52 of the 1.60 summed active-day returns. ZEC loses -5.38 % per trade over 28 trades while BTC gains +7.93 % over 8.
- **F5:** Outside the profile, wide days with a low close rebound over 2 days: +1.95 % (t 4.60, 528 cases) in the widest range quintile and +1.16 % (t 2.93) in the next. In rising markets this is +2.5 % (t 2.23 with days together, 200 cases, 68 days). The profile map already holds this as "wide range low close rebound" (039-02.d1, 045-01, 044-01), so it is no discovery.
- **F6:** Other angles showed nothing reliable and graded, or only what the map already holds.

## Ideas
- `061-01.b1.b1.b1.d1.d1.g1_agitated-chop-high-close-five-day-fade` (from F1, F2, F3, F4): In a choppy, agitated market, the nearer a coin's daily close sits to the top of that day's high-low range, the more its price falls over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
