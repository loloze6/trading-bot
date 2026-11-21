---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4073 USD
---
## Findings
- **F1:** The combined score points the wrong way inside the 90-day rise: its rank correlation with the next 5-day excess return is negative in all 8 years, 2018 to 2025 (from -0.014 to -0.156; 2019 t -2.1; pooled about -0.08 over 1704 cases), and negative on 5 of 6 coins. Its two lowest quintiles are followed by +1.0 % and +1.2 % excess (t 1.6 each) and its fourth quintile by -1.5 % (t -2.7).
- **F2:** The book lost through its shorts. Short bars summed -10.46 in allocation-weighted gain over 5607 bars (mean -0.19 %), long bars summed +1.16 over 4340 bars (mean +0.03 %). Shorts made on the active grid were followed by +0.85 % excess and longs by -0.73 %.
- **F3:** The book moves against the coin. Its daily return has a correlation of -0.19 with the coin's. On the coin's best 10 % of days it lost 0.74 %, and on the worst 10 % it gained 0.30 %. The idea's size is -0.43 % unusual move per case, which is -2.2 times the 0.19 % cost of a trade.
- **F4:** The best-single-signal score fails in the same way. It correlates 0.83 with the combined score. Its lowest quintile is followed by +1.2 % excess (t 2.0), and the combined-minus-best difference has a correlation with the excess return near 0 in most years (from -0.12 to +0.07). The combination adds nothing over the best single signal, which matches the inconclusive verdict (t 0.28).
- **F5:** A large up day relative to the coin's 30-day volatility is followed by a higher 5-day return. Up days in the top quintile of size were followed by +1.8 % excess (t 2.5, 281 cases) and the fourth quintile by +1.3 % (t 1.7). Down days of any size were followed by -1.0 % to 0.0 %. The correlation of the day's size with the next 5-day excess is +0.049 (p 0.01, 2726 cases), positive on 6 of 6 coins and in 6 of 8 years. Many angles were looked at, so this is only moderate evidence.
- **F6:** 5-day stretches starting on a Sunday were followed by -1.5 % excess (t -2.9, 466 cases), and by -2.8 % in 2022 to 2025 (t -4.7). This is a calendar condition with no grade to it, so no idea is written from it.
- **F7:** The 90-day return gives no graded pattern. Its middle quintiles were followed by -1.9 % and -2.1 % (t about -3), while both extreme quintiles were positive (+0.8 %, +1.5 %, t below 1.4). The response is not monotone, so a positive 90-day return cannot grade the effect as the tested idea assumed.

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.g1_combined-score-reverses-in-uptrends` (from F1, F2, F3, F4): While a coin's 90-day return is positive, the higher its relearned combined score of its 28-day return, reversed 1-day return, closeness to its 90-day high and calmness of its 30-day volatility, the lower its return over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends.g2_large-up-days-continue` (from F5, F2): The larger a coin's last 1-day rise relative to its 30-day volatility, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
