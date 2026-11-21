---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the higher its relearned combined score of its 28-day return, reversed 1-day return, closeness to its 90-day high and calmness of its 30-day volatility, the lower its return over the next 5 days.
Consequence: In a 90-day rise, a high combined score is a reason to refuse a long, and a low one a reason to take one rather than short.
Why:
- F1: The combined score points the wrong way inside the 90-day rise: its rank correlation with the next 5-day excess return is negative in all 8 years, 2018 to 2025 (from -0.014 to -0.156; 2019 t -2.1; pooled about -0.08 over 1704 cases), and negative on 5 of 6 coins. Its two lowest quintiles are followed by +1.0 % and +1.2 % excess (t 1.6 each) and its fourth quintile by -1.5 % (t -2.7).
- F2: The book lost through its shorts. Short bars summed -10.46 in allocation-weighted gain over 5607 bars (mean -0.19 %), long bars summed +1.16 over 4340 bars (mean +0.03 %). Shorts made on the active grid were followed by +0.85 % excess and longs by -0.73 %.
- F3: The book moves against the coin. Its daily return has a correlation of -0.19 with the coin's. On the coin's best 10 % of days it lost 0.74 %, and on the worst 10 % it gained 0.30 %. The idea's size is -0.43 % unusual move per case, which is -2.2 times the 0.19 % cost of a trade.
- F4: The best-single-signal score fails in the same way. It correlates 0.83 with the combined score. Its lowest quintile is followed by +1.2 % excess (t 2.0), and the combined-minus-best difference has a correlation with the excess return near 0 in most years (from -0.12 to +0.07). The combination adds nothing over the best single signal, which matches the inconclusive verdict (t 0.28).
