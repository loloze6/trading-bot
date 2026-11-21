---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the closer its close is to its 90-day closing high, the higher its return over the next 5 days.
Consequence: In a coin's 90-day rise, favour long bets on coins trading near their recent highs and avoid those far below them.
Why:
- F4: Outside the 90-day rise, the same signals carry the opposite sign: 28-day return correlation -0.084 (t -2.89, 1,178 cases), closeness to the high -0.078 (t -2.82). The 365-day correlation weights learn from a mix of both regimes, so they carry the reversal sign into uptrends. This is why the learned combination anti-predicts where the idea placed it.
- F5: Closeness to the 90-day high also predicts with its usual sign inside the rise. Its correlation is +0.080 (t 3.00, 1,417 cases), with excess returns of -1.24 % in its lowest fifth against +1.0 to +1.3 % in its top three fifths. The reversed 1-day return and the negated volatility add little (t -2.08 and +0.65).
