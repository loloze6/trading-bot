---
line: 7.e profitable but not proven
backtest: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d
idea tested: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6828 USD
---
## Findings
- **F1:** The book's gain is concentrated in one period and a few trades, not spread out. Window w14 carries 0.707 of the 1.197 summed bar gains (59 %), and 2018 carries 0.790. The top 10 of 173 trades hold 135.7 of the 141.0 summed net trade percent. The market's own move contributes −0.080, since all trades are short in falling coins, so the gain is not the coin's drift.
- **F2:** Inside the book, the gain comes only from the widest bounces. The top range quartile of the cases earns 0.943 of the 1.197 book gain. Its cases fall by 2.72 % beyond drift the next day (t 3.43, 53 cases), against −0.76 % and −0.25 % for the two narrowest quartiles. The Spearman correlation of range ratio with the next-day unusual move is 0.26 (p 0.0001).
- **F3:** The effect is not specific to the falling agitated profile; it lives in a falling 60-day trend.
- **F4:** In the falling trend, the two widest quartiles hold up without the dominant window and across all coins.
- **F5:** Outside the falling agitated profile, the same situation still gives back 0.47 % the next day (t 3.09, 978 cases). Inside the profile the figure is 0.68 % (t 1.67, 209 cases), so the profile filter shrinks the sample more than it sharpens the effect. This is why the plan's t stayed at 1.93.
- **F6:** The give-back lasts one to two days, then fades.
- **F7:** The brief's own situation, a 3-day rise graded by its size against usual swing, shows no grading inside the profile. Its quartiles give back −0.21 %, −0.07 %, +1.49 % and −0.11 % the next day, and −0.51 %, +0.35 %, +1.06 % and +0.03 % over 3 days.
- **F8:** Wide down days in the profile rise strongly the next day. The top range quartile of down days rises 2.95 % beyond drift (t −5.45 in the short direction). This is the agitated wide-range-fall rebound the map already holds in many cells, so it is not proposed.

## Ideas
- `058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade` (from F2, F6): In a falling, agitated market, a coin's up day that comes while its 3-day return is still negative is followed by a fall over the next two days, and the wider that day's high-to-low range against the standard deviation of its daily returns over the past 30 days, the larger the two-day fall.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.g1.d1.d2.e1_wide-bounce-fade-falling` (from F2, F3, F4, F5): In a falling market, a coin's up day that comes while its 3-day return is still negative is followed by a fall over the next day, and the wider that day's high-to-low range against the standard deviation of its daily returns over the past 30 days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
