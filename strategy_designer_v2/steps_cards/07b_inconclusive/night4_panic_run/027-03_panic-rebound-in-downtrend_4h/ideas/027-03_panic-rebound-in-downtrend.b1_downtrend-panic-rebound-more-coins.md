---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: In coins whose 30-day return before the panic was negative, a 24-hour stretch with a range several times its 30-day average and a hard fall is still followed by higher than usual returns over the next 14 days, and the more extreme the panic, the higher the return.
Consequence: The premium pays for providing liquidity, not for following a trend, so it appears even in coins that were already falling.
Why:
- F1: The tested result points the way the idea predicts but is far too noisy for 40 cases. Step 5 gives +2.23 % per case with t 0.99. My rebuild of the cases gives +0.62 % with a spread of 15.6 % per case, t 0.23 on 35 cases, and 51 % of cases end above the drift. At that spread, a +2.23 % mean needs about 196 cases to reach t 2, five times what the six default coins provide.
- F2: The 84-bar outcome swings by period and by coin, so a few cases decide the sign. In 2018 the 6 cases average −22.2 %, while in 2020 the 6 cases average +20.7 %. BTC averages −5.3 % on 7 cases and ZEC +9.9 % on 3.
- F3: Widening the same situation to more cases makes the 14-day premium show. Falls with a 24-hour range at least 2x the 30-day average, in coins with a negative 30-day return, give +3.71 % over 84 bars, t 2.15 on 161 cases. The same falls in all coins give +3.13 %, t 2.47 on 335 cases.
