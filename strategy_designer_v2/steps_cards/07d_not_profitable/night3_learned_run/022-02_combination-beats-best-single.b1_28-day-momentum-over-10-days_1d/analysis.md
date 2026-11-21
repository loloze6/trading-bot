---
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3627 USD
---
## Findings
- **F1:** The Calmar fails because of one long fall, not because the gain is too small. The book's yearly return is 18.8 %, its deepest fall is 60.9 %, and Calmar comes out at 0.31. That fall ran from w2 to w8: 741 days to the trough and 1,102 more to recover. Over those days the book's daily returns summed to -0.85 while holding the coins summed to +0.20.
- **F2:** Only the long side earns. Overall, long days earn +15.5 bps a day (8,657 days) and short days -1.1 bps (8,671 days). Outside w2-w8, longs earn +21.7 bps a day (t 5.07, 6,322 days) and shorts +0.4 bps (t 0.13, 5,946 days). Inside w2-w8, both sides lose: longs -1.3 bps (t -0.23), shorts -4.5 bps (t -0.87).
- **F3:** Shorts did most of the damage in the falls. Their summed daily gains were -1.23 in w2-w8 and -1.08 in w19-w21, which hold the two deepest falls (-61 % and -37 %). Longs summed -0.31 in w2-w8 but +8.28 in w9-w18 and +3.96 in w19-w21.
- **F4:** Shorts lose most after the deepest falls, where the coin has been rebounding rather than continuing.
- **F5:** Longs are graded by the 28-day rise and by nearness to the 60-day high.
- **F6:** Cost is not the cause. The total move per case is +0.57 % over 10 days, 2.9 times the 0.19 % cost of a buy and a sell. The weakest fifth of forecasts loses only -4.5 bps a day, against +26.8 bps for the strongest fifth.
- **F7:** The year 2023 lost -9.0 bps a day on all positions, while every other year earned (+0.3 to +27.1 bps). The gain is carried by 2020 (+27.1 bps, longs on 69 % of days) and 2024 (+13.3 bps).

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward` (from F1, F2, F3, F5): The higher a coin's 28-day return, the higher its return over the next 10 days, only while that 28-day return is a rise; the larger the rise, the larger the 10-day gain that follows.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs` (from F1, F4, F5): The higher a coin's 28-day return, the higher its return over the next 10 days, only while the coin trades near its 60-day high; the closer to that high, the stronger the continuation.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls` (from F3, F4): The deeper a coin's 28-day fall and the closer it is to its 60-day low, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
