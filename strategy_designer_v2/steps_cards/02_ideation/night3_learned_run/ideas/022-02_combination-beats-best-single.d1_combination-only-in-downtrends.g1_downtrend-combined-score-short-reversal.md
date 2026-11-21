---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is negative, the more strongly its relearned combined score of its 28-day return, last 1-day return, closeness to its 90-day high and 30-day volatility points down, the more the coin rises over the next 5 days.
Consequence: In a 90-day decline, a strongly negative combined score is a reason to refuse the short, and to lean long in proportion to how negative the score is.
Why:
- F1: The book's short trades lose and its long trades earn. The 1,699 short trades average −1.90 % net per trade (median −1.76 %, t −6.3). The 1,766 long trades average +0.86 % (median +0.66 %, t 2.3). The shorts carry the book's loss (Sharpe −0.35).
- F2: Short losses grow with the size of the entry forecast. By tercile of forecast size, shorts lose −1.18 %, −1.94 % and −2.28 % before fees (566 to 567 trades each). Longs show no such order (+0.82 %, +0.47 %, +1.59 %).
- F3: On decline bars (90-day return below zero), the coin rises after the combination says down. On the non-overlapping 5-day grid, after a negative forecast the coin's 5-day return is +0.63 % (764 cases, t 1.9). After a positive forecast it is +0.38 % (786 cases, t 1.1). The losing short trades last a median of 5 days, close to the idea's horizon.
- F4: The losses of F1 and F2 are far above the cost of a round trip (0.19 %). The losing move per short trade is about 6 to 12 times that cost, before fees.
