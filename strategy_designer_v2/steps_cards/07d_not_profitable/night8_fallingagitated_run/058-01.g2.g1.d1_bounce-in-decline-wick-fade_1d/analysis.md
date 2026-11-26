---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d
idea tested: 058-01.g2.g1.d1_bounce-in-decline-wick-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4194 USD
---
## Findings
- **F1:** The failing measure is Calmar (0.62 against 0.75), and it is set by one fall: the book's deepest fall, −2.6 % over 117 days, starts in w14 and ends in w15, and w14 holds the book's two worst days (−2.02 % and −1.50 %, against no other day below −0.56 %); the 15 worst short cases are almost all in w14, with coin rises of 10 to 12 % the next day.
- **F2:** The effect lives in up days that follow a deep 3-day fall: by the 3-day return measured in 30-day swings, the two most negative quartiles of the cases earn +2.0 % and +2.1 % short-side excess next day (48 and 47 cases), while the two shallowest earn −0.8 % and −0.2 % (47 and 48 cases); of the 94 cases with the 3-day return below −0.65 swings, both depth halves earn (+1.8 %, +2.2 %), while the 96 shallower cases lose in both halves (−0.6 %, −0.3 %).
- **F3:** The deep 3-day fall is not an effect of its own: in the profile, on days with the same deep 3-day return but no up day, a short earns −2.7 % (t −4.7, 140 days) and −0.5 % (107 days), against +2.1 % (t 2.6, 49 cases) and +1.8 % (48 cases) when the day rose; only the bounce inside the deep fall gives back.
- **F4:** The falls of w14–w15 come from the shallow cases: the 21 losing cases there had a mean 3-day return of −0.57 swings, a range of 1.13 swings and a depth of 0.45, against −1.15, 1.84 and 0.71 for the 38 winning cases; a rebuilt book keeping only the deep-3-day cases cuts the deepest fall from −2.6 % to −0.91 % and lifts Calmar from 1.05 to 2.42 (Sharpe 1.00 to 1.11, yearly return 2.7 % to 2.2 %, folds B and C, the same rebuild).
- **F5:** The day's range against the 30-day swing is graded too: by quartile of the high-low range, short excess runs −0.86 %, −0.41 %, +1.6 %, +2.6 % (47–48 cases each); the wide range alone is not the effect (in the profile, wide-range days without the signal earn −0.47 % over 471 days, low-range signal days −0.64 % over 98, wide-range signal days +2.1 % over 97), and a rebuilt book with deep 3-day return and wide range together has its deepest fall at −0.91 % and Calmar 2.65.
- **F6:** The close's depth below the high carries the effect only in its top quartile (+2.5 % short excess, 48 cases, against +0.5 %, +0.05 %, −0.1 % in the three lower quartiles), so the tested grading sizes the shallow, losing cases almost as large as the good ones.
- **F7:** The same up-day-in-a-falling-3-days situation outside the falling agitated profile still gives back, though less: +0.46 % short excess, t 2.8, 869 cases, against +1.0 % inside, so the profile concentrates the effect rather than creating it.

## Ideas
- `058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall` (from F1, F2, F3, F4): In a falling, agitated market, a coin's up day that comes after a 3-day fall is followed by a fall over the next day, and the deeper that 3-day fall against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.
- `058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline` (from F1, F4, F5, F6): In a falling, agitated market, a coin's up day that comes while its 3-day return is still negative is followed by a fall over the next day, and the wider that day's high-to-low range against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.
- `058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall` (from F2, F3, F4, F5): In a falling, agitated market, a coin's up day that comes after a 3-day fall is followed by a fall over the next day, and the larger that day's high-to-low range plus the depth of its 3-day fall, both against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
