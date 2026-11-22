---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, a 24-hour fall during a range wider than its 30-day average is followed by higher than usual returns over the next 7 days. The higher the prior 30-day return relative to the depth of the 24-hour fall, the higher the return.
Consequence: A trader should hold such dips for about a week and favour shallow dips in strongly rising coins over deep crashes.
Why:
- F3: Milder panics carry the same premium with far more cases. These are a 24-hour fall with the range 1.5 to 2 times its 30-day average and a positive prior 30-day return. There are 525 cases, with a 3-day excess return of +1.68 % (t 4.00, strength 0.18) and a 7-day excess of +1.95 % (t 2.99, strength 0.13). The strict ≥3x panics after a rise give +4.10 % over 3 days (t 1.99) on only 45 cases.
- F4: In the milder panics the prior 30-day rise is what carries the effect. With a prior 30-day fall, the same 1.5 to 2x stretches earn +0.13 % over 3 days (t 0.26, 381 cases), against +1.68 % (t 4.00) after a prior rise.
- F5: Moderate falls pay more than the deepest ones, so the forecast's cubic damping, which gives size only to deep falls, points the wrong way.
