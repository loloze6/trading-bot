---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.
Consequence: A fall into settlement after a run up is a reason to be long for the next day, sized by the fall and by the run up, while a fall in a flat or falling coin gives no such reason.
Why:
- F1: The supporting check could not pass as built, because 61 % of the 5,749 cases sit at the forecast cap of 20 and the median forecast is 20, so the "upper half" (strictly above the median) is empty and the check returned None; the inconclusive status comes from this saturation and not from the effect.
- F2: The main measure is on the side the idea predicts (mean 0.00338, t 3.15 on 5,740 cases), and the grading the check was meant to test is there in the uncapped ranks: the lowest forecast quintile (mean forecast 4.8) has an excess 24-hour return of −0.11 % (t −0.86), while the top quintile has +0.40 % (t 2.27).
- F3: The effect is graded by the depth of the fall. The deepest quartile of the 2-hour fall against the coin's usual 2-hour move has an excess 24-hour return of +0.57 % (t 3.85, 1,079 cases), against +0.00 % to +0.03 % in the other three quartiles.
- F4: The effect is also graded by the run-up. By 7-day return quartile, the excess 24-hour return rises from +0.01 % (t 0.07) to +0.04 %, +0.24 % (t 2.13) and +0.37 % (t 2.07), each on 1,348 cases.
