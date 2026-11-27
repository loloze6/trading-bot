---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.g2_falling-heavy-volume-bounce-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4706 USD
---
## Findings
- **F1:** In a falling market, up days split into width quintiles (range against the 20-day mean bar range) are followed by next-day unusual moves of -0.17 % (t -0.47) and -0.00 % (t -0.00) in the two narrowest quintiles, against -0.87 % (t -2.72), -0.73 % (t -1.56) and -0.91 % (t -1.92) in the three widest (about 375 cases each, 186 to 221 days). The rank correlation of width with the next-day move is -0.070 (p 0.002, 1883 cases). Outside falling markets the five quintiles stay between -0.09 % and -0.27 %, all with |t| < 1.1. In rising markets the widest quintile is followed by +1.39 % (t 1.80).
- **F2:** The grading by width lives in falling agitated markets. There the five width quintiles of up days are followed by -0.22 % (t -0.31), -1.33 % (t -1.71), -1.34 % (t -1.92), -1.46 % (t -1.63) and -2.25 % (t -2.81, 98 cases on 52 days), steadily more negative. In falling calm markets they run -0.14 %, +0.37 %, -0.76 %, -0.56 %, -0.42 %, which is not graded.
- **F3:** Inside falling-market up days, heavy volume does not deepen the fade; within each width third it softens it:
- **F4:** The weakness after a wide falling-market up day comes on the first day and adds little after it. The tested situation's days show -0.64 % at 1 day (t -1.51, 470 cases), +0.10 % at 2 days, -0.43 % at 3 days and -1.00 % at 5 days (t -1.23). The 2-day move of the middle width quintiles (-0.89 %, -0.95 %) is about their 1-day move.
- **F5:** The wide-minus-narrow gap points the same way in 9 of the 12 windows seen. In those windows, falling-market up days in the widest 40 % are followed by a lower next day than those in the narrowest 40 %, for example w12 -1.36 % against +0.65 %, w16 -1.27 % against +0.60 %, and w14 -1.97 % against -0.55 %.
- **F6:** Wide falling-market up days that close near their high fade most: -1.49 % (t -2.43, 252 cases), against -0.41 % for wide days that close near their low. This repeats the held book 074-01.g1.d1 (falling agitated, short: wide close high bounce fade), so it is not new.
- **F7:** The book's short bets were followed by short-direction unusual moves of +1.32 % in 2018 (t 1.72), +0.49 % in 2019, +0.14 % in 2020 and +0.25 % in 2021. They are positive every year but weaker after 2018, which matches the inconclusive t of 1.74 over all folds.

## Ideas
- `074-01.b1.b1.b1.b1.g2.g1_agitated-downtrend-wide-rally-fade` (from F2, F1, F4, F5): In a falling, agitated market, an up day whose high-low range is wide against the coin's mean daily range of the last 20 days is followed by a fall over the next day. The wider that day's range against its 20-day mean, the larger the next day's fall.
- `074-01.b1.b1.b1.b1.g2.g2_falling-thin-volume-rally-fade` (from F3, F1, F4): In a falling market, a wide up day traded on light volume against the coin's 20-day average volume is followed by a fall over the next day. The lighter that day's volume against its 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
