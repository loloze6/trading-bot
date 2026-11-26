---
line: 7.g patterns
backtest: 060-01.b1_agitated-decline-rally-fades-next-day_1d
idea tested: 060-01.b1_agitated-decline-rally-fades-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4186 USD
---
## Findings
- **F1:** In the falling agitated profile in folds B and C, a down day is followed by a next-day rise above the coin's normal drift, and the rise grows with the size of the fall in 30-day swing units. Down days of −1 to −0.3 swings gain +1.13 % (321 cases, t 2.44 with one day's cases taken together, 139 days). Down days of −2 to −1 swings gain +2.15 % (107 cases, t 1.70, 57 days). Down days beyond −2 swings gain +6.27 % (31 cases, t 1.80, 12 days). The slope over all down days is −1.70 % of next-day unusual move per unit of scaled fall. The profile map already holds this rebound: falling agitated long has 12 strategies, among them "falling agitated scaled fall next day rebound".
- **F2:** Among falling agitated down days (beyond −0.3 swings), the next-day rebound grows with the day's volume against its 30-day average. The low volume tercile gains +0.70 % (151 cases, t 1.16, 80 days), the middle tercile +1.31 % (154 cases, t 2.10, 97 days) and the high tercile +3.10 % (154 cases, t 2.92, 82 days).
- **F3:** In folds B and C the tested giveback after falling agitated up days is not graded at one day. Up days of 0.3 to 1 swings are followed by −0.99 % (264 cases, t −1.82). Up days of 1 to 2 swings are followed by +0.35 % (94 cases, t 0.45). Up days beyond 2 swings are followed by −1.86 % (26 cases, t −1.09). The slope of next-day unusual move on the scaled rise is +0.58 % per swing unit, which is opposite to the idea's grading.
- **F4:** Over 3 days, the falling agitated up-day giveback looks graded on the first grid: −1.37 %, then −2.45 %, then −5.17 % from the 0.3–1 bin to the beyond-2 bin, all with t of −1.2 or weaker. The other two grid offsets contradict it: the 1 to 2 swing bin reads +0.48 % and +4.51 %. A longer horizon does not rescue the theme in these folds.
- **F5:** The book's gain is thin against its tails. Over 1449 book days, the 10 best days sum to +21.0 % and the 10 worst to −22.0 %, against a total of +9.0 %. By window, w14 gives +6.27 %, while w11 (−2.88 %) and w17 (−2.69 %) lose. This fits the failed Calmar (0.33) and Sharpe-versus-holding (−0.17).
- **F6:** Outside the falling agitated profile, in a rising 60-day trend, down days of −2 to −1 swings are followed by +1.25 % (189 cases, t 2.90) and down days beyond −2 swings by +1.89 % (33 cases, t 2.42). These t are not clustered by day and come from one of many angles looked at, so I do not count this pattern as a finding.
- **F7:** Next-day returns by weekday range from −0.44 % after Wednesdays (t −2.60) to +0.37 % after Fridays (t 2.85). These are unclustered across co-moving coins, are not distinct from chance over seven groups, and are not used.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.b1.g1_volume-graded-capitulation-next-day-rebound` (from F2, F1): In a falling, agitated market, a coin's down day traded on volume that is larger against its average daily volume of the past 30 days is followed by a larger rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
