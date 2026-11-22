---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a fall over the next 3 days, and the larger the rise in standard deviations, the larger the fall.
Consequence: A trader would fade large up days in falling coins over about three days, not hold the short for a week.
Why:
- F3: In falling coins (90-day return negative), the fade the brief describes shows at 3 days, not at 5. Among up days, the slope of the 3-day move on the rise is −0.099 usual moves per standard deviation (t −2.67, n 1243). At 5 days it is −0.025 (t −0.45, n 641), which is why the tested 5-day measure stayed inconclusive (t 1.08).
- F5: The book lost because its shorts were wrong-footed and held too long. Shorts entered at the full forecast (|forecast| ≈ 20) returned a mean of −4.39 % per trade before fees (n 1490), against −2.14 % (n 497) for weaker entries. Trades held 12 to 14 days lost 7 % to 12 % on average. The book was negative in 17 of 24 windows.
