---
line: 7.g patterns
backtest: 060-01.g1.d2.d1_own-range-close-height-fade_1d
idea tested: 060-01.g1.d2.d1_own-range-close-height-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6338 USD
---
## Findings
- **F1:** Inside the falling agitated profile, close location does not separate up days: up days closing in the upper half of their range are followed by a -0.97 % unusual next day (t -2.07, 171 days, 412 cases) and those closing in the lower half by -1.05 % (t -1.11, 50 days, 88 cases); across all in-profile up days the figure is -0.97 % (t -2.52, 258 days, 613 cases). The fade follows a rise, not a close near the high.
- **F2:** Inside the profile, closes in the top fifth of the range do not fade more than those just below: the 0.8–1.0 location bucket gives -0.48 % (t -1.34, 231 cases) against -0.84 % (t -2.45, 270 cases) for 0.6–0.8. The tested idea's grading by close height is weak in folds B, C.
- **F3:** Inside the profile, the lone up day fades most. When it is the only rise in the last three days, the next day's unusual move is -2.10 % (t -2.95, 87 days, 159 cases), against -0.48 % (t -0.99, 172 days) with two rises and -0.70 % (t -1.03, 58 days) with three.
- **F4:** Inside the profile, wide up days fade and narrow ones do not, measured as the day's range over its 20-day average. The lowest width tercile gives -0.02 % (t -0.04, 108 days), the middle -1.33 % (t -2.62, 114 days) and the highest -1.23 % (t -1.73, 102 days).
- **F5:** Outside the falling agitated profile, an up day that leaves the coin low in its 20-day high-low range falls the next day, graded from low to high. The lowest tercile of 20-day position gives -0.76 % (t -2.92, 414 days, 1001 cases), the middle -0.10 % (t -0.54) and the highest +0.32 % (t 1.21).
- **F6:** Inside the profile, the down side is much larger than the up-day fade. Closes in the bottom fifth of the range are followed by +2.17 % (t 4.97, 243 cases), and days with a fall of more than 1.5 of the 30-day swing by +4.03 % (t 2.08, 24 days). These are long rebounds the profile map already holds in falling agitated (035-01, 039-02, 045-01, 051-01 and others), so they are not a discovery.
- **F7:** Weekday means of the next-day unusual move across all bars range from -0.50 % on Wednesday (t -2.78) to +0.41 % on Thursday (t 2.80). This was one of many angles examined and the t-statistics are not clustered by day, so it does not stand out from chance.

## Ideas
- `060-01.g1.d2.d1.g3_wide-high-close-fade` (from F2, F4): In a falling, agitated market, a coin that closes in the upper part of its day's high-low range falls over the next day, and the wider that day's range against its average range of the last 20 days, the larger the next-day fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.g1.d2.d1.g1_falling-agitated-lone-rise-fade` (from F1, F3): In a falling, agitated market, a coin that rises on a day after falling on the days before falls over the next day, and the more of its previous two days were falls, the larger that next-day fall.
- `060-01.g1.d2.d1.g2_low-range-up-day-fade` (from F5): A coin that rises on a day while its close still sits low in its 20-day high-low range falls over the next day, and the lower that close sits in the 20-day range, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
