---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5614 USD
---
## Findings
- **F1:** In a falling market, the next-day fade after wide up days sits in agitated stretches. Using my agitation proxy (the 30-day swing against its own recent median, not the profile's one-year median), up days in the widest fifth were followed by -2.07 % unusual next-day move in falling agitated bars (t -2.82, 128 cases, 61 days), against -0.52 % in falling calm bars (t -0.79, 117 cases). The narrowest-fifth up days showed +0.30 % (agitated) and +0.38 % (calm).
- **F2:** The book earns mostly where the market is agitated. Its mean gain per position-day was 1.89 % on agitated days (87 cases) against 0.44 % on calm days (100 cases). Its best fifth of position-days had a higher agitation ratio (1.31 against 0.97 for its worst fifth), wider days (2.02 against 1.77) and heavier volume (2.18 against 1.75).
- **F3:** In falling bars, the next-day weakness after up days grows with the day's width. The unusual next-day move by width fifth was -0.00 % (t -0.01), -0.32 % (t -0.91), -0.72 % (t -2.21), -0.90 % (t -1.90) and -0.77 % (t -1.54). In non-falling bars the same fifths showed no gradient: -0.24 %, -0.23 %, -0.06 %, -0.13 %, -0.03 %, every t under 0.9.
- **F4:** Wide up days do not fade in rising markets. The widest-fifth up days in rising agitated bars were followed by +1.29 % (t 1.22, 187 cases), and in rising calm bars by +0.46 % (t 0.77).
- **F5:** The fade on wide up days in falling bars is spent in one day. The next day was -0.84 % (t -2.16, 697 cases, 283 days), the day after was +0.21 % (t 0.65), and the 3-day total was -1.09 % (t -1.92).
- **F6:** In falling bars, the fade does not grow with the size of the day's gain. Up days of about 0.0 usual moves were followed by -0.66 % (t -2.05), and up days of about 1.8 usual moves by only -0.37 % (t -0.82). The range carries the effect, not the return.
- **F7:** The other patterns I saw in falling bars are rebounds the profile map already holds in its falling agitated long cell (16 strategies), so they are not discoveries:
- **F8:** Weekday cells, volume terciles of up days and choppy-market cells produced no pattern that stands out against the number of angles tested: the largest |t| was 2.05, in one choppy cell. The book's 2018 position-days carry 1.58 of its 2.42 summed gain.

## Ideas
- `074-01.b1.b1.b1.b1.g1.e1.g1_agitated-drop-depth-bounce-fade` (from F1, F2, F5): In a falling, agitated market, a wide up day is followed by a fall over the next day, and the deeper the coin's fall over the 5 days before that up day, measured in its usual 5-day moves, the larger that next-day fall.
- `074-01.b1.b1.b1.b1.g1.e1.g2_agitated-range-graded-bounce-fade` (from F1, F3, F4, F5, F6): In a falling, agitated market, an up day is followed by a fall over the next day, and the wider its high-low range against the coin's own daily ranges of the last 20 days, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
