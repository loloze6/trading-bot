---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall the larger the rise, only while the coin's own 20-day return is negative, and the rise is larger the deeper that 20-day fall.
Consequence: Buy weekend falls at Sunday's close and hold through Wednesday in coins already down over the past 20 days, and refuse the weekend falls of coins that have been rising, where the rebound fails and the book's deepest falls came from.
Why:
- F1: The Calmar that failed (0.37) is set by one fall: the book lost 26.4 % over 214 days from w1 to w3 while holding the coins lost 60.6 %, with book returns of −10.9 % in w2 and −10.3 % in w3 (holding −41.7 % and −21.4 %), and the signal trades summed to −1.42 and −1.10 in those two windows.
- F2: Inside that fall the losses came from Sunday falls in coins that had been rising: in w2–w3 the signal cases in the top third of the prior 20-day return (above +4.1 %) had an excess 3-day return of −5.0 % (t −3.2, 78 cases), while the bottom third (20-day return below −13 %) still rebounded +2.1 % (t 2.4, 78 cases).
- F3: Over all windows the rebound is carried entirely by coins already down over 20 days: excess 3-day return +1.99 % (t 5.4, 659 cases) in the bottom third of the 20-day return (below −10.6 %), +0.45 % (t 1.5) in the middle third, and 0.00 % (t 0.0) in the top third (above +5.3 %); the price against its 50-day mean shows the same pattern (bottom third +1.37 %, t 3.5; others +0.2 %).
- F4: The 20-day-fall condition is not an effect of its own: Sundays without the signal in the bottom third of the 20-day return had an excess 3-day return of −1.60 % (t −5.7, 688 cases), against +1.99 % when the weekend fall is present. The rebound belongs to the weekend fall itself and fits the theory: a thin weekend book is pushed furthest when one-sided selling is already under way.
- F5: Restricting the signal to a 20-day return below +5.3 % cut the approximate weekly book's deepest fall from −23.6 % to −9.5 % and raised its Calmar from 0.51 to 1.04, with Sharpe 0.96 against 0.85. The yearly return was nearly kept (9.9 % against 12.1 %), over 197 active weeks.
