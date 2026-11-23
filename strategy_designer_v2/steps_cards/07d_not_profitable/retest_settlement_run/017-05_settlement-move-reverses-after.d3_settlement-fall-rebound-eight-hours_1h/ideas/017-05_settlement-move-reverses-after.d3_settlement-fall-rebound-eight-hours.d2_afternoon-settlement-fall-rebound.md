---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader takes the settlement-fall reversal at the settlement where it is most reliable, and sizes it with the fall.
Why:
- F4: The settlement clock matters even with the fall itself as the condition. The same falls of 3 or more usual moves at 08:00 UTC, where no 00:00/16:00 settlement is tested, give +0.42 % over 8 hours (t 1.29) and +0.62 % over 24 hours. That is against +1.44 % over 24 hours after 00:00, so roughly half the 24-hour move belongs to the settlement situation. Across the day, falls of more than 1 usual move rebound most strongly after the 16:00 close (+0.34 % over 8 hours, t 6.06).
- F1: The rebound is graded and only the largest settlement falls move enough to pay a trade. At 00:00 and 16:00 settlements, a 2-hour fall of 3 or more usual moves is followed by +0.43 % over 8 hours (1136 cases, strength 0.156). Falls of 1 to 1.5 usual moves give +0.21 %, and falls under 1 usual move give +0.02 % to −0.09 %. Against the 0.19 % cost of a trade, only the strongest falls carry the move.
