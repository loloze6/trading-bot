---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 2 days, a coin rises after a fall in its 24-hour return, and the larger that fall relative to the coin's usual volatility, and the more its past-week volatility exceeds its past-month volatility, the larger the rise.
Consequence: A trader would buy sharp daily drops in agitated markets and hold them for about two days, trading far less often than an hourly-refreshed fade.
Why:
- F2: The forecast turns over far faster than the 24-hour effect it bets on. Its autocorrelation is 0.94 at 1 hour, 0.70 at 6 hours and -0.05 at 24 hours. Its slope on the next return is insignificant at 1 hour (t 1.44, 416,645 cases) and 6 hours (t 0.91, 69,355 cases), significant only at 24 hours (t 3.90, 17,246 cases), and gone at 72 hours (t -0.33, 5,683 cases).
- F3: The reversal exists only when the coin's recent volatility is raised against its longer baseline (168-hour volatility over 720-hour volatility). On the 24-hour grid the slope of excess return on the negated volatility-scaled 24-hour move is:
- F4: Inside that volatility measure the effect is graded. The 24-hour slope t rises across vol-ratio quintiles: 0.04, -1.44, -1.49, 3.15 (ratio 1.07), 6.45 (ratio 1.38). The hot-state slope also holds at 12 hours (t 5.37) and at 48 hours (t 4.76, slope 0.0075 against 0.0060 at 24 hours).
- F6: The reversal is lopsided toward falls. The bottom decile of the 24-hour scaled move (-1.73 usual moves) is followed by +0.56% excess over 24 hours, while the top decile (+1.89) is followed by only -0.20%. The re-standardised forecast also tracks the raw move more weakly (slope t 3.02 against 3.84).
