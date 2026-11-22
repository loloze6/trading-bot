---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
line: 7.b inconclusive
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers part of that fall over the next three hours; the further that hour's volume lies above its 30-day hourly average, the larger the recovery.
Consequence: A sharp hourly fall on surging volume is a reason to expect a rebound within three hours, not a continuation of the fall.
Why:
- F1: The idea's grading by volume runs the opposite way to the idea. Among the long cases on the 6-hour grid, the thinnest volume quintile (mean volume ratio 0.24) is followed by a 3-hour unusual move of −0.9 bp (t −0.50, 3,419 cases), while the heaviest (ratio 3.28) is followed by +9.6 bp (t 2.79, 3,419 cases). On the 3-hour grid the volume ratio correlates positively with the 3-hour unusual move (r 0.028, t 4.2, 23,205 cases). This is why the thin-minus-heavy check failed (−0.022 %) although the main mean had t 2.09.
- F3: Inside the deepest fall quintile, the heavier-volume half carries the effect: +13.8 bp over 3 hours (t 4.10, 4,190 cases), against −5.3 bp for the thinner half (t −0.75, 457 cases). Sharp falls on thin volume are rare and show no recovery.
- F4: The move peaks near 3 hours rather than the plan's 6 hours. Over all cases it is +4.05 bp at 3 hours (t 3.52) and +3.96 bp at 6 hours (t 2.48), then fades to +1.6 bp at 24 hours (t 0.51).
