---
line: 7.g patterns
backtest: 074-01.b1.d1.d2_depth-graded-run-break-fade_1d
idea tested: 074-01.b1.d1.d2_depth-graded-run-break-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3964 USD
---
## Findings
- **F1:** In a falling market (60-day return below -10 %), an up day ending a run of at least 2 down days was followed by a next-day excess return of -1.36 % (t -2.59, 275 cases, cases of one day summed). In a rising market the same day was followed by +0.40 % (t 0.77, 176 cases). The tested effect is present, lives in the falling trend, and is already held in the map as 074-01.b1.d1.d1 (falling, short).
- **F2:** The book's losses come from squeezes and its gains from the fall it bets on. On its worst 5 % of days (19 days) the book lost -1.54 % while its coins rose +6.75 % on average. On its best 5 % of days (19 days) the book gained +3.38 % while the coins fell -7.16 %. The failed Calmar (0.55) is carried by those few relief rallies that keep going.
- **F3:** Splitting falling-market up days that follow any down run into thirds by that day's volume against its 30-day mean, the high-volume third was followed by -2.12 % the next day (t -3.05, 186 cases). The middle third was followed by -0.68 % (t -1.29) and the low-volume third by -0.62 % (t -1.21). The heavier the relief day's volume, the larger the fade: this is a grading the tested idea does not use. The gap between top and bottom thirds is about 1.5 %, roughly t 1.7, so it is suggestive rather than decisive given the many angles looked at.
- **F4:** The same up days split by the coin's 5-day fall in units of its 30-day swing confirm the tested idea's own grading rather than adding to it. The deepest third was followed by -2.15 % (t -2.67, 184 cases), against -0.63 % (t -1.30) and -0.66 % (t -1.30) for the other two.
- **F5:** Several other angles show no pattern that stands out from chance.

## Ideas
- `074-01.b1.d1.d2.g1_heavy-volume-relief-fade` (from F3, F1): In a falling market, an up day that ends a run of down days is followed by a fall in the coin's close over the next day. The fall is larger the heavier that up day's volume, measured against the coin's average daily volume over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
