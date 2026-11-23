---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader keeps the long reversal on these two settlements and holds it until the next settlement, instead of paying a full trade's cost for a 2-hour move at every settlement.
Why:
- F2: The short side loses before fees and the long side carries all the gross gain. SHORT trades averaged −0.303 % gross (−0.403 % net, 32 573 trades). LONG trades averaged +0.144 % gross (+0.044 % net, 32 993 trades). At the 00:00 and 16:00 settlements over 8 hours, a fall into settlement in the 50–95th percentile of |pre-move| was followed by +21.5 bp and +23.1 bp total (unusual +16.8 bp, t 4.13, n 5 007; +18.5 bp, t 2.83, n 2 559). A rise in the same bands was followed by only +4.4 bp and +2.9 bp, and by −0.5 bp to +3.7 bp over 16 hours.
- F3: The effect on the long side grows with the horizon past the 2 hours the book holds, and with the size of the fall, until the extreme 1 %. For falls into settlement on the long side, the total move was:
- F4: The 08:00 UTC settlement carries none of the effect.
- F6: The settlement clock adds most in the middle band of falls. Falls in the 50–80th percentile at hours away from settlement gave +7.2 bp total and +2.6 bp unusual over 8 hours. At the 00:00 and 16:00 settlements the same band gave +21.5 bp and +16.8 bp. In the 80–95 band other hours gave +19.9 bp, close to settlement's +23.1 bp.
- F8: The book's gross gain sits entirely in the first 2 hours after settlement, at +0.38 and +0.75 bp per bar with a mean |allocation| of 0.43. The other six hours hold about 0.014 and earn about 0. The book pays the full cost every 8 hours for a 2-hour move, and that move is below the cost.
