---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days. The rise is larger the larger the weekend fall and the higher the coin's 20-day volatility of daily returns, so the same weekend fall in a volatile coin is followed by a much larger rebound.
Consequence: Favour buying weekend falls in coins whose recent 20 days were volatile, and refuse those in calm coins, where the rebound is too small to pay.
Why:
- F1: The weekend-fall rebound grows steeply with the coin's own 20-day volatility. For Sunday falls after a 20-day fall, the excess 3-day return is +0.47 % (t 0.99, n 388) in the calmest third, +1.29 % (t 3.14, n 384) in the middle third and +3.25 % (t 5.75, n 396) in the most volatile third, and the strength rises from 0.05 to 0.15 to 0.37 of a usual move.
- F2: Inside each volatility third, the deeper half of the Sunday falls rebounds more. In the calmest third it gives +0.87 % against +0.18 %, in the middle third +2.27 % against +0.32 %, and in the most volatile third +4.60 % (t 4.66, n 195) against +1.86 %. The deepest fifth of Sunday falls gives +3.89 % (t 4.79) and the deepest fifth of 20-day falls +4.22 % (t 5.56).
- F4: The rebound is tied to Sunday. The same 1-day fall after a 20-day fall gives an excess 3-day return of +1.68 % (t 5.91) on Sunday, against −0.76 % (t −3.27) on Friday, −0.50 % on Saturday and between −0.48 % and +0.39 % on Monday to Thursday. In the most volatile third the gap is +3.25 % on Sunday against −0.48 % to +1.50 % on the other days.
- F3: Much of the confirmed effect is one move shared by all coins in the same week, not each coin's own. Averaged by week, Sunday fall-after-fall cases give +0.17 % (t 0.29, 210 weeks), and with each week's cross-coin mean removed they give about zero (−0.14 %, +0.09 %, +0.30 % by volatility third). Only the most volatile third keeps a week-clustered +2.19 % (t 2.04, 97 weeks), so the step-5 t of 4.84 on 1427 cases counts roughly 200 independent weeks.
