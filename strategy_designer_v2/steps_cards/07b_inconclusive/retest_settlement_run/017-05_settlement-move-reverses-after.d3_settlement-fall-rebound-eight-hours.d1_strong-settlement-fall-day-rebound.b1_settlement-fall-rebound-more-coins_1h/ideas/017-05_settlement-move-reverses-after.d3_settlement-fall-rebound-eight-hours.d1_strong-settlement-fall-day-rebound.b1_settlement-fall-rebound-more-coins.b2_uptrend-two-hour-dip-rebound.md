---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, a fall over the past 2 hours at any hour of the day is followed by a rise over the next 24 hours. The larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader buys sharp 2-hour dips in coins that rose over the past month at any clock time, sized by the depth of the dip, rather than waiting for funding settlements.
Why:
- F4: The settlement clock is not what carries the rebound. Falls of at least 1.5 usual 2-hour moves at any hour rebound +0.354 % over 24 hours (t 9.4, n 27,018). Most non-settlement hours give +0.4 % to +0.8 %, for example hour 0 at +0.70 % (t 6.9) and hour 12 at +0.80 % (t 4.3), while the 15:00 and 14:00 hours just before settlement are among the weakest at +0.146 % and −0.020 %.
- F5: The same rising-month graded rebound appears at any hour, so it is a dip-in-uptrend effect rather than a funding one. With a positive 30-day return, a fall of at least 1 usual move gives +0.224 % with t 4.5 (n 12,612), graded from +0.090 % for falls of 1–1.5 usual moves to +0.540 % for falls beyond 3.
- F3: Inside a rising month the effect is graded by the depth of the fall. The unusual 24-hour move rises from +0.065 % (t 0.40) for forecasts of 2–4 to +0.629 % (t 5.1, n 1,849) for falls at the cap of 20. It also grows with the 30-day rise itself, from −0.035 % in the lowest quartile to +0.717 % and +0.645 % in the two highest quartiles (t 4.65 and 3.34).
