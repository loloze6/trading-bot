---
line: 7.b inconclusive
backtest: 054-01.b1_reclaimed-low-all-coins_1d
idea tested: 054-01.b1_reclaimed-low-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4257 USD
---
## Findings
- **F1:** Inside the falling, agitated profile, folds B and C hold only 34 reclaimed-pierce cases on 15 days. They lean the way the idea predicts: +5.0 % unusual 5-day move, t 1.51, hit rate 65 %. The same cases give +7.6 % over 10 days (t 1.77) and +7.3 % over 15 days (t 1.29), against −0.2 % over 1 day. The plan's 5-day horizon catches the move before it has fully shown, and too few independent days (step 5: 67 days over all folds, t 1.29) carry it.
- **F2:** The test already ran on all 19 coins, all four folds and the full daily history, and the hourly bars end earlier than the daily ones. So no more data exists to lift the t of an effect that is +2.43 % per case (strength 0.21) over 148 cases.
- **F3:** The idea's grading by pierce depth does not hold where I can see it. Inside the profile, depth correlates −0.39 with the 5-day excess return: the shallow third gives +13.4 % (t 2.41), the deep third −2.8 % (t −1.45). Over 10 days the shallow half gives +11.3 % (t 2.07) and the deep half +3.8 % (t 0.80). Step 5's all-fold deeper-minus-shallower gap of +3.1 % (Welch t 1.53) therefore rests on folds A and D only, so the deeper-is-larger claim is mixed.
- **F4:** What does grade the rebound inside the profile is how low the day closes within its own range. That position correlates −0.43 with the 5-day and −0.38 with the 10-day excess return. The lowest-close third gives +13.6 % over 5 days (t 3.01, hit 82 %) and the highest-close third −1.0 % (t −0.37). Days that close below their open give +10.9 % (t 2.31), against +0.8 % (t 0.25) for days closing above it.
- **F5:** Outside the falling, agitated profile, the same reclaimed pierce is followed by a fall, not a rebound. Over the 135 cases the 5-day excess return is −4.1 % (t −2.07, 82 days) and the 10-day one −6.1 % (t −3.22, hit 32 %). The fall grows with the coin's 60-day trend over 10 days: falling-calm cases −6.8 % (t −2.52), choppy −11.5 % (t −2.67), rising −12.7 % (t −3.62, 14 cases, hit 7 %).

## Ideas
- `054-01.b1.b1_weak-close-reclaim-rebounds` (from F1, F3, F4): In a falling, agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it rises over the next 10 days. The rise is larger the closer the day's close sits to the day's low.
- `054-01.b1.b2_reclaimed-low-fails-rising` (from F5): In a rising market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days. The fall is larger the higher the coin's 60-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
