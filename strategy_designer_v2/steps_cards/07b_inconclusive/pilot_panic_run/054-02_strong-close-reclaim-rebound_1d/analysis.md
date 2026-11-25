---
line: 7.b inconclusive
backtest: 054-02_strong-close-reclaim-rebound_1d
idea tested: 054-02_strong-close-reclaim-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3616 USD
---
## Findings
- **F1:** Step 5's main result is on the side the idea predicts but well short of the bar: a mean excess 5-day return of +1.06 % with t 0.62 over 76 cases on 49 days, and a total move per case of +1.93 %, 10 times the 0.19 % trade cost. The problem is too few cases for the noise, not a move too small to pay.
- **F2:** The profile matters, and the effect lives in it. In folds B and C, the 35 reclaimed-low pierces inside falling agitated bars beat the coin's drift by +3.8 % over 5 days (t 1.88, 20 days, strength 0.37). The 136 pierces outside the profile fell short of it by −3.6 % (t −3.19).
- **F3:** Inside the profile the effect is on the predicted side on most coins but each coin has only a handful of cases. BTC had 10 cases at +4.2 %, XMR 7 at +9.6 %, ETH 4 at +3.8 %, LTC 3 at +1.7 % and ZEC 8 at +0.9 %. XRP, with 3 cases at −1.1 %, was the only negative coin. The six coins together give a sample too thin for t 2.
- **F4:** The years are mixed, which adds to the noise. 2018 (18 cases, +6.1 %, t 1.87) and 2021 (6 cases, +8.9 %) were positive. 2019 (5 cases, −3.8 %) and 2020 (6 cases, −3.0 %) were negative. Window w15 was −3.8 % against w18 at +8.9 %.
- **F5:** The idea's grading runs the wrong way. Within the profile, the reclaim measure correlates −0.19 with the excess 5-day return. Low-reclaim cases gained +5.6 % (t 1.70) against +2.0 % (t 0.84) for high-reclaim cases. So the supporting check (upper half beats lower half) is likely to fail even if the mean became sure.
- **F6:** What sorts the rebound is where the close sits in the day's range, and in the opposite direction to the idea. Its rank correlation with the 5-day excess return is −0.34. Pierce days closing in the lower half of their range gained +8.2 % (t 2.51, 18 cases, 13 days) against −0.6 % (t −0.29) for those closing in the upper half. Shallower pierces (+7.4 %, t 2.15) and narrower days (+7.8 %, t 2.31) do the same.

## Ideas
- `054-02.b1_reclaim-rebound-all-coins` (from F1, F2, F3): In a falling, agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it rises over the next 5 days, and the rise is larger the higher the close sits above that low, measured against the day's range.
- `054-02.b2_low-close-reclaim-rebound` (from F2, F5, F6): In a falling, agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it rises over the next 5 days, and the rise is larger the lower the close sits within the day's range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
