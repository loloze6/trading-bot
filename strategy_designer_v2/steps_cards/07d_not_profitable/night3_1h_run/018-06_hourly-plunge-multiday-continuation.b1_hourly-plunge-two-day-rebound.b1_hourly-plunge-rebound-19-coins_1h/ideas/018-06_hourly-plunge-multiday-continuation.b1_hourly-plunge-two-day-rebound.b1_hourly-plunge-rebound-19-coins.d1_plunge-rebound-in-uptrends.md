---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the 24-hour drop in those multiples, the larger the rise, only while the coin's 30-day return is positive, and the higher that 30-day return, the larger the rise.
Consequence: A sharp hourly plunge in a coin that has risen over the past month is a reason to buy for two days, and the same plunge in a falling coin is a reason to stay out.
Why:
- F2: The gain sits almost entirely in the strongest drops. Bars with a forecast of 8 to 20 are 2.0 % of bars but carry 65 % of the gain, with timing of +6.8 bps per bar. Bars with a forecast of 0 to 0.5 earn only +0.13 bps of timing.
- F3: The rebound after a drop depends on the coin's 30-day return, which sets the failing mean return and Calmar. Over the 1,372 entries, when the 30-day return is above +6.8 % (top two quintiles) the next 48 hours rise +1.80 % (t 4.1) and +1.72 % (t 1.9). When it is below −3.5 % (bottom two quintiles) they move −0.09 % and −0.08 % (t −0.2), which is less than a 0.22 % round trip.
- F4: On the non-overlapping 48-hour grid the dip rebound holds in both 30-day states, but it is larger in rising ones. With a forecast of 2 to 20, the next 48 hours return +1.30 % (t 3.2, 301 cases) when the 30-day return is positive. They return +1.00 % (t 2.8, 657 cases) when it is negative. Grid cells with no drop return −0.30 % (t −2.5, 3,140) in falling 30-day states.
- F6: The book's deepest fall is 39 %, running over 305 days from window 1 to window 3, all falling-market windows (holding's summed daily returns −0.33, −0.41, −0.21). In window 2 alone the book lost −0.24 of summed daily return, while it bought drops that kept falling.
