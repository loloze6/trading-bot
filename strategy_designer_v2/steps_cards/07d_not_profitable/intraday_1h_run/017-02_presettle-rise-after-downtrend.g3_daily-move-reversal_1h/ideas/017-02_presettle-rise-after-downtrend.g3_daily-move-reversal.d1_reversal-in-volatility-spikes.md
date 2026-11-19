---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its 24-hour return, and the larger that return relative to the coin's usual volatility, the larger the reversal, only while the coin's past-week volatility is raised above its past-month volatility, and the more raised it is, the larger the reversal.
Consequence: A trader would fade sharp daily moves only when the coin has turned volatile against its month. They would stay out in calm weeks, where the reversal is absent but the fees remain.
Why:
- F1: The book loses almost entirely to fees. Its mean daily gain before costs is +0.000066, against fees of 0.00278 a day, which leaves -0.00274 a day net. The fees come from turnover of 2.56 times the book per day at 0.00109 per unit turned over.
- F3: The reversal exists only when the coin's recent volatility is raised against its longer baseline (168-hour volatility over 720-hour volatility). On the 24-hour grid the slope of excess return on the negated volatility-scaled 24-hour move is:
- F4: Inside that volatility measure the effect is graded. The 24-hour slope t rises across vol-ratio quintiles: 0.04, -1.44, -1.49, 3.15 (ratio 1.07), 6.45 (ratio 1.38). The hot-state slope also holds at 12 hours (t 5.37) and at 48 hours (t 4.76, slope 0.0075 against 0.0060 at 24 hours).
- F5: The book's gain before costs follows the same split. It is +0.0015 a day in the hot state, against -0.0013 in the calm state and +0.00006 in the mid state, but fees run 0.0025 to 0.0030 a day in every state. So even the hot state alone does not cover costs at the current turnover.
