---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, only while the coin's 30-day return is positive. Inside that state, the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader buys deep settlement falls only in coins that rose over the past month, where the day's rebound is about 2.5 times the cost of a trade, and refuses them in falling coins.
Why:
- F1: The main measure is on the predicted side but small: the 13,768 settlement-fall cases (forecast ≥ 2) end their 24 hours +0.075 % above the coin's normal drift with t 1.58. The rebound is clearer early, at +0.155 % with t 5.5 over 8 hours, then fades to −0.024 % with t −0.37 over 48 hours.
- F2: The effect lives entirely in coins in a rising month. When the coin's 30-day return is positive, the cases' unusual 24-hour move is +0.379 % with t 4.95 (n 4,884), and their total move is +0.561 % with t 7.3, 2.5 times the 0.22 % trade cost, a strength of 0.071. When the 30-day return is negative, the unusual move is −0.093 % with t −1.54 (n 8,884), which drowns the pooled result.
- F3: Inside a rising month the effect is graded by the depth of the fall. The unusual 24-hour move rises from +0.065 % (t 0.40) for forecasts of 2–4 to +0.629 % (t 5.1, n 1,849) for falls at the cap of 20. It also grows with the 30-day rise itself, from −0.035 % in the lowest quartile to +0.717 % and +0.645 % in the two highest quartiles (t 4.65 and 3.34).
- F6: The effect is not stable across years. The pooled cases lose −0.60 % (t −5.2) in 2022 and −0.35 % (t −3.5) in 2025, and even in a rising month 2022 gives −0.13 % and 2025 gives −0.18 %, against +0.87 % to +1.05 % in 2020–2021.
