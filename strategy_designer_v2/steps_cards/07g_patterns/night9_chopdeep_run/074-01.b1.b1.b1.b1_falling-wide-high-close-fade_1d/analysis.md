---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade_1d
idea tested: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4693 USD
---
## Findings
- **F1:** The tested fade is real and lasts one day only. In falling markets, wide up days that close in the top quarter were followed by a next-day excess return of −1.26 % (t −2.32, 324 cases on 141 days), and the book's cases gave +0.98 % short (t 2.09, 178 days). Over days 2–3 the short gave −0.41 % (t −0.74), and over 3 days it gave +0.61 % (t 0.84), so the whole move is in the first day.
- **F2:** The fade is strongest when the wide up day comes right after a sharp fall. Among the cases, the third with the weakest prior 5-day return gave +2.85 % short next day (t 2.48, 114 cases on 59 days). The middle third gave −0.15 % (t −0.29) and the top third +0.40 % (t 0.60). This tercile split is one of about 80 groups looked at, so it is suggestive rather than decisive.
- **F3:** The fade belongs to falling markets. In rising markets the same wide, high-close up days were followed by +0.61 % (t 1.07, 166 days), the side opposite a fade. In choppy markets they were followed by −0.65 % (t −0.96).
- **F4:** The book's own grading does not work. The third of cases with the strongest forecast gave only +0.49 % short (t 0.64, 58 days), against +1.21 % (t 1.64) and +1.24 % (t 2.38) for the weaker two thirds. Among all falling-market up days, the next-day result levels off at width quintiles 2 to 4 (−0.87 %, −0.73 %, −0.91 %) after quintiles 0 and 1 near 0.
- **F5:** Relative volume orders the cases. The third with the lowest volume against its 20-day mean gave +0.07 % short (t 0.11, 78 days), against +1.59 % (t 2.17) and +1.64 % (t 1.93) for the middle and highest thirds.
- **F6:** The book fails as a book because its edge sits in a few days. It was non-zero on 316 days, its 10 best days made 153 % of its summed return, and its daily returns had a correlation of −0.52 with the coins'. It earned a Sharpe of 0.47, which is −0.14 below holding the coins.
- **F7:** Wide down days that close near their low were followed by rebounds:

## Ideas
- `074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade` (from F2, F1, F3): In a falling market, a wide up day that comes after a sharp fall over the coin's previous 5 days is followed by a fall over the next day. The deeper the previous 5-day fall, the larger the next day's fall.
- `074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade` (from F5, F1, F3): In a falling market, a wide up day traded on heavy volume against the coin's 20-day average volume is followed by a fall over the next day. The heavier that day's volume against its 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
