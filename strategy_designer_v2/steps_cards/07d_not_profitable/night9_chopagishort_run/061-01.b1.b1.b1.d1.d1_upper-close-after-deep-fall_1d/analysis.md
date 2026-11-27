---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall_1d
idea tested: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4773 USD
---
## Findings
- **F1:** The book's gain rests on window w16, and outside it the book earns nothing: w16 sums +23.6 % of daily book return against about 0 for the other eleven windows together (from -1.7 % to +1.6 % each). That leaves a yearly return of +2.6 % against a deepest fall of 5.5 % (w15, 5 days, while the coins rose +3.0 %), so Calmar is 0.43. The holding Sharpe is not beaten because the coins rose +56 % to +161 % in four of the windows.
- **F2:** The effect lives only after a deep 20-day fall. On the grid, signal bars whose 20-day return is below -10 % gain +16.9 % per 5 days in the short direction (t 3.85, 15 cases); signal bars above -10 % lose 1.1 % (t -0.51, 8 cases). Across all signal bars, a 20-day fall deeper than 20 % gives +9.0 % (t 4.22, 47), -20 % to -10 % gives +2.3 % (t 0.66, 15), -10 % to 0 gives -2.7 % (t -1.20, 14), and a positive 20-day return gives +1.6 % (t 1.20, 29).
- **F3:** The deep 20-day fall is not an effect on its own. In the profile without the signal it gives -1.8 % short (t -0.88, 25 grid cases). Out of the profile it gives +0.4 % (t 0.73, 475), and +0.7 % against the short with an upper close and negative 5-day return (t -0.57, 119). The fall is the idea's own situation (squeezed buyers inside a broken range), stretched over a longer past.
- **F4:** Outside w16, the shallow 20-day falls are what lose the book's money. Entries after a 20-day fall below -10 % add about +7.7 % of allocation-weighted 5-day move in the other windows. Entries above -10 % add about -1.1 % over all windows, losing in 8 of 11.
- **F5:** The depth of the 5-day fall grades the move. Signal bars give, by 5-day return:
- **F6:** The move is complete by about 3 to 5 days. At entries the short gains:
- **F7:** The book's falls come from deep-fall shorts that squeeze in their first days. 29 of the 38 short coin-positions held on the 10 worst book days had a 20-day fall below -10 %. Deep-fall entries whose coin rose more than 3 % in the next 2 days went on to lose 8.5 % over 5 days and 15.8 % over 10 days (7 cases), against a 13.0 % gain over 5 days for the other 24.
- **F8:** Entries in the calmest third of 20-day swing gained +7.3 % over 5 days (t 1.86, 16), against -1.3 % (t -0.54, 16) in the most agitated third. Trades win only 36 % of the time, with a median of -1.5 % net and the worst five averaging -28 %.

## Ideas
- `061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall` (from F2, F3, F4, F1): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, while its 20-day return is a deep fall, its price falls over the next five days, and the deeper that 20-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall` (from F5, F6, F1): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been a deep fall, its price falls over the next three days, and the deeper that 5-day fall, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade` (from F8, F7, F5): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the deeper that 5-day fall and the quieter its last 20 days of daily swings against the past year, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
