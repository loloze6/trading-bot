---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: A 24-hour stretch in which the coin falls while its range widens above its 30-day average is followed by higher than usual returns over the next 3 days, only while the coin's 30-day return before the stretch is positive. The higher that prior 30-day return and the wider the range against its 30-day average, the higher the return.
Consequence: A trader should buy every widening-range dip in a coin that was rising over the past 30 days, not only the rare extreme panics, sizing up with the prior rise, which multiplies the number of profitable trades.
Why:
- F1: The book's trades are strongly profitable but very rare. There are 367 trades, gross +6.33 % and net +6.23 % per trade (t 5.78), held 98 hours on average, so the 0.19 % cost of a trade takes almost nothing. Yet the book holds a position on only 1.5 % (LTC) to 11.4 % (XRP) of bars, with a mean absolute exposure of 1.2 % to 3.0 % of the book. Its mean daily return is therefore 0.0003, below the 0.0005 needed: the gain is lost to rarity, not to fees or to bad timing.
- F2: The cause of the rarity is the regime. It is active on only 0.31 % (LTC) to 0.67 % (XRP) of bars, because it requires the last 24 hours' bars to average at least 3 times their 30-day range. Among non-overlapping 18-bar cases with a 24-hour fall and a prior 30-day rise, only 45 meet that 3x condition, out of 684 with a range of at least 1.5x.
- F3: Milder panics carry the same premium with far more cases. These are a 24-hour fall with the range 1.5 to 2 times its 30-day average and a positive prior 30-day return. There are 525 cases, with a 3-day excess return of +1.68 % (t 4.00, strength 0.18) and a 7-day excess of +1.95 % (t 2.99, strength 0.13). The strict ≥3x panics after a rise give +4.10 % over 3 days (t 1.99) on only 45 cases.
- F4: In the milder panics the prior 30-day rise is what carries the effect. With a prior 30-day fall, the same 1.5 to 2x stretches earn +0.13 % over 3 days (t 0.26, 381 cases), against +1.68 % (t 4.00) after a prior rise.
