---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d1_weekend-fall-rebound-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell on Sunday while its 20-day return is negative rises over the next 3 days, and the rise is larger the higher the coin's 20-day volatility of daily returns, for a given Sunday fall.
Consequence: Concentrate weekend-fall rebound buys in coins that are currently volatile, and refuse them in quiet coins, where the rebound is too small to carry the drawdowns.
Why:
- F2: The rebound is graded mostly by the coin's own volatility. Split into terciles of 20-day volatility, the strength (the unusual 3-day move over the coin's usual move) was 0.06 (t 1.3), 0.10 (t 2.4) and 0.41 (t 6.3), with about 390 cases each. Deep Sunday falls in the top tercile gained +4.55 %, against +0.79 % in the bottom tercile.
- F1: The weekend rebound is tied to Sunday's close. A coin that fell on the day while its 20-day return was negative gained an unusual 3-day +1.68 % (t 5.9, n 1168) when that day was Sunday. On the other weekdays the same situation gave between −0.76 % (Friday, t −3.3) and +0.39 % (Monday, t 1.0). Sunday's raw forward return in that situation built from +0.59 % over 1 day to +2.17 % over 3 days (t 7.6). Wednesday's stayed near 0 at every horizon from 1 to 7 days (+0.27 % over 7 days, t 0.6).
- F3: The depth of the 20-day fall grades the rebound too. Its deepest quintile gained +4.14 % (t 5.3), against +0.49 % to +1.66 % in the other four. The deepest quintile of the Sunday fall gained +3.95 % (t 4.7), against −0.45 % and +0.55 % for the two shallowest.
- F6: The book lost most of its edge in falling-market years and its Sunday days were negative. Its yearly Sharpe was −0.58 in 2018 and 0.14 in 2022, against 0.95 to 1.81 in the other years. Its Sunday day returns averaged −0.014 % (t −3.8), while Monday to Wednesday averaged +0.07 % to +0.13 %.
