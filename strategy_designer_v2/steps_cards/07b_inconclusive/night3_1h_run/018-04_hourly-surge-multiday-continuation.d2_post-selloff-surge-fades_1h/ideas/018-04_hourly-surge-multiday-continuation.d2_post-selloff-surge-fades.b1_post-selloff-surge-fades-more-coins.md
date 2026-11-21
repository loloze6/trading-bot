---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside after its 7-day return before that day was a fall, the price rises less than the coin's usual 5-day return over the next 5 days; the deeper that 7-day fall, the larger the shortfall.
Consequence: A trader would treat a sharp up day after a week of heavy selling as a relief bounce to fade or ignore, not a breakout to hold for days.
Why:
- F1: The tested shortfall is on the side the idea predicts but too small to show at 5 days: the mean is +0.32 % per case (t 0.74, 559 cases, strength 0.033). On the same cases it is +0.53 % over 24 hours (t 2.51, 572 cases), +0.60 % over 72 hours (t 1.60), and nearly gone at 240 hours (+0.06 %, t 0.08). The fade happens in the first day, and the plan's 5-day horizon dilutes it with four days of noise.
- F3: At 5 days the effect is mixed across coins and years, which is why the t stays low. The shortfall is +1.84 % on ETH (t 2.15) and +1.13 % on XRP, but -1.40 % on ZEC. By year it runs from +1.57 % in 2025 (t 1.65) to -2.66 % in 2024 (t -2.42, the price rose more than usual).
