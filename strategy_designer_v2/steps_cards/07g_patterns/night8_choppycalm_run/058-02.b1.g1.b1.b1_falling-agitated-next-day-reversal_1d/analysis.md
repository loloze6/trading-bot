---
line: 7.g patterns
backtest: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d
idea tested: 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.7015 USD
---
## Findings
- **F1:** Fading a day of more than one usual swing pays almost only after down days. Inside the profile, down days were followed by +2.80 % of excess fade gain (t 4.53, 169 cases), while up days gave −0.19 % (t −0.29, 129 cases). The book's position gain shows the same split: 4.00 summed over 780 long bars against 0.80 over 725 short bars. The short half of the tested reversal adds little, and its long half repeats rebound ideas the map already holds in falling agitated (047-01, 051-01, 038-01).
- **F2:** The fade grows with how much the coin's last 10 days swung against its last 60. Across the four quartiles of that ratio, days beyond one swing gave −0.07 %, −0.10 %, +0.35 % and +1.29 % (t 4.89). On down days in the top quartile the fade gave +1.90 % (day-clustered t 2.64, 266 cases on 101 days), and it was positive in rising calm (+1.72 %, t 1.91) and falling calm (+2.67 %, t 1.77). This is the agitated-rebound family the map already holds, so it is not a discovery.
- **F3:** Where a day closes inside its own range predicts the next day against it, in a graded way. Next-day excess falls from +0.55 % (t 3.59, 1,320 cases) for closes in the bottom fifth to −0.42 % (t −3.37, 1,864 cases) for closes in the top fifth. Fading the close location gives +0.18 % with day-clustered t 2.97 over 1,448 days, and the effect grows with the day's range against its usual swing: +0.05 %, −0.00 %, +0.18 % and +0.52 % (t 3.70) across the range quartiles.
- **F4:** The short side of the close-location effect lives on wide days and outside rising markets. After a close in the top 30 % of the day's range, next-day excess went from −0.13 % on the narrowest range quartile to −0.88 % on the widest (day-clustered t −2.23, 736 cases). On closes near the high with a range in the top half, the next day was:
- **F5:** A Monday move beyond one swing continued into Tuesday rather than reversing. The fade lost −0.93 % (t −3.44, 429 cases), the up-side Monday fade lost −0.99 % (day-clustered t −2.06, 80 days), and the Monday fade was negative in 3 of 4 years. Every other weekday was positive or flat. Among the many angles looked at, this is too weak to stand as an idea.
- **F6:** The book's gain sits in a few days and windows. Its 10 best days carry 68 % of the summed daily returns, and windows w14 and w16 carry 0.43 of the 0.70 total over 12 windows.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-02.b1.g1.b1.b1.g1_falling-calm-wide-high-close-fade` (from F3, F4): In a falling, calm market, the wider a coin's day range against its usual daily swing over the last 20 days, and the nearer that day's close is to its high, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
