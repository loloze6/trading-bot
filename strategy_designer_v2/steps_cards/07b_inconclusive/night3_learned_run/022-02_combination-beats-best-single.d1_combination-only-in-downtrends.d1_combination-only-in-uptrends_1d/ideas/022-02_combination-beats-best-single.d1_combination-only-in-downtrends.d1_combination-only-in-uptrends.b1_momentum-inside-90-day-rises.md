---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the higher its 28-day return, the higher its return over the next 5 days.
Consequence: In a coin's 90-day rise, take the side of its 28-day move, and drop learned weights that carry the reversal sign of declining periods into it.
Why:
- F2: In the 90-day rise, both learned scores point the wrong way, and the book followed them. Betting the sign of the combined score earned -0.80 % of excess 5-day return per case (t -2.79, 1,704 cases). The idea's measured size is -0.43 % unusual and -0.51 % total per case, against a 0.19 % round trip, and the book's Sharpe was -0.98.
- F3: The 28-day return on its own predicts the next 5 days with the usual sign inside the 90-day rise. Its correlation with the excess 5-day return is +0.112 (t 4.03, 1,272 cases). The cases rank from -2.1 % excess in its lowest fifth to +1.4 % and +1.0 % in its top two fifths, a spread of about 3 %, about 16 times the 0.19 % cost of a trade.
- F4: Outside the 90-day rise, the same signals carry the opposite sign: 28-day return correlation -0.084 (t -2.89, 1,178 cases), closeness to the high -0.078 (t -2.82). The 365-day correlation weights learn from a mix of both regimes, so they carry the reversal sign into uptrends. This is why the learned combination anti-predicts where the idea placed it.
