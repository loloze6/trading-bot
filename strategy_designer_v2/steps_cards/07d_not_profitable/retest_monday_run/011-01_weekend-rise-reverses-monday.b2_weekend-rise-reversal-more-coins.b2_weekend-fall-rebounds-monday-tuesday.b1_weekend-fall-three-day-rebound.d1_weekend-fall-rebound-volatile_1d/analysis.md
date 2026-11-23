---
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4952 USD
---
## Findings
- **F1:** The Calmar that failed (0.37) is set by one fall: the book lost 26.4 % over 214 days from w1 to w3 while holding the coins lost 60.6 %, with book returns of −10.9 % in w2 and −10.3 % in w3 (holding −41.7 % and −21.4 %), and the signal trades summed to −1.42 and −1.10 in those two windows.
- **F2:** Inside that fall the losses came from Sunday falls in coins that had been rising: in w2–w3 the signal cases in the top third of the prior 20-day return (above +4.1 %) had an excess 3-day return of −5.0 % (t −3.2, 78 cases), while the bottom third (20-day return below −13 %) still rebounded +2.1 % (t 2.4, 78 cases).
- **F3:** Over all windows the rebound is carried entirely by coins already down over 20 days: excess 3-day return +1.99 % (t 5.4, 659 cases) in the bottom third of the 20-day return (below −10.6 %), +0.45 % (t 1.5) in the middle third, and 0.00 % (t 0.0) in the top third (above +5.3 %); the price against its 50-day mean shows the same pattern (bottom third +1.37 %, t 3.5; others +0.2 %).
- **F4:** The 20-day-fall condition is not an effect of its own: Sundays without the signal in the bottom third of the 20-day return had an excess 3-day return of −1.60 % (t −5.7, 688 cases), against +1.99 % when the weekend fall is present. The rebound belongs to the weekend fall itself and fits the theory: a thin weekend book is pushed furthest when one-sided selling is already under way.
- **F5:** Restricting the signal to a 20-day return below +5.3 % cut the approximate weekly book's deepest fall from −23.6 % to −9.5 % and raised its Calmar from 0.51 to 1.04, with Sharpe 0.96 against 0.85. The yearly return was nearly kept (9.9 % against 12.1 %), over 197 active weeks.
- **F6:** The idea's volatility weighting does not repair the falls: trading only when 20-day volatility is above its 60-day level gave Calmar 0.37 and a deepest fall of −12.4 %, but kept only a 4.6 % yearly return.
- **F7:** Volatility does help inside the falling coins: with a 20-day return in the bottom third, cases with 20-day volatility above its 60-day level had +3.14 % excess (t 5.85, 196 cases) against +0.36 % (t 0.57, 202 cases) below it. Volatility alone on no-signal Sundays earns −0.92 % (t −2.05) in its top third, so it is not an effect of its own.
- **F8:** The weakest cases lose: the smallest third of Sunday falls (above −1.3 %) had an excess of −0.56 % (t −2.1, 804 cases) and the lowest-forecast third −0.34 % (t −1.1). The largest third of falls (below −3.1 %) had +1.57 % (t 3.9) and the top forecast third +1.42 % (t 3.8).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend` (from F1, F2, F3, F4, F5): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall the larger the rise, only while the coin's own 20-day return is negative, and the rise is larger the deeper that 20-day fall.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound` (from F3, F4, F6, F7, F8): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall the larger the rise, only while the coin's 20-day return is negative, and the rise is larger the more its 20-day volatility of daily returns exceeds its 60-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
