---
line: 7.e profitable but not proven
backtest: 032-02.g1.e1_raw-nearness-to-uptrend-high_1d
idea tested: 032-02.g1.e1_raw-nearness-to-uptrend-high
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3626 USD
---
## Findings
- **F1:** Most of the book's gain is timing rather than the market's own rise: 8.2 bp a day out of 12.4 bp is timing (t 3.10, 8689 coin-days), and only 4.2 bp comes from being long the coins' average drift. The gain is uneven across the sample: timing is -21 bp in w9 and -20 bp in w14, and -6.9 bp in 2018 against +24.6 bp in 2020. The top 50 of 8689 coin-days carry 8.74 of the 10.81 summed gain.
- **F2:** Almost all of the 5-day excess return sits at the 28-day closing high itself. On grid bars, closes exactly at the high gain +4.84 % excess over 5 days (113 cases on 53 days, t by day 2.35). The other distance buckets give +1.35 % (0–2 % below), +0.31 % (2–5 %), +1.22 % (5–10 %), -1.55 % (10–20 %) and -1.20 % (over 20 %). Over 10 days the at-high bucket gives +9.18 % (62 cases).
- **F3:** Raw proximity to the 28-day closing high predicts the 5-day excess return on all grid bars, without the uptrend condition. Its slope t is 5.04 (1278 cases), 4.25 on uptrend bars and 2.62 on bars whose 28-day return is at or below 0. Over 10 days the t is 4.63 on all bars and 3.24 on non-uptrend bars. On uptrend bars the plan's 60-bar standardised forecast is weaker than raw proximity (t 3.68 against 4.25 at 5 days, 2.47 against 3.64 at 10 days).
- **F4:** The proximity effect is much stronger when recent volatility is compressed. Where 20-day volatility over 60-day volatility is below its median, the proximity slope t is 5.70 (423 cases) and closes at the high gain +9.66 % excess over 5 days. On the other bars the t is 2.13 (855 cases) and closes at the high gain +2.40 %.
- **F5:** For a given proximity, a smaller prior 28-day rise predicts a larger 5-day gain. In a joint regression proximity keeps t 5.51 and the 28-day return has t -2.23. Among closes at the high alone, the 28-day return's slope has t -2.20.
- **F6:** The effect is concentrated in a few coins and years. The uptrend proximity t is 4.81 for XRP and 2.12 for BTC, but -0.23 for LTC and 0.27 for ZEC. By year it is 0.35 in 2018 and 0.98 in 2019, against 2.68 in 2020 and 2.50 in 2021.

## Ideas
- `032-02.g1.e1.e1_raw-nearness-to-28-day-high` (from F2, F3, F1): The closer a coin's close is to its highest close of the last 28 days, the larger its rise over the next 5 to 10 days, whether its 28-day return is up or down, with a close at the 28-day high itself followed by the largest rise.
- `032-02.g1.e1.e2_quiet-breakout-to-28-day-high` (from F4, F2): Among coins closing near their highest close of the last 28 days, the quieter the coin's daily returns over the last 20 days compared with the last 60 days, the larger its rise over the next 5 days.
- `032-02.g1.e1.e3_flat-base-high-breakout` (from F5, F2): Among coins closing near their highest close of the last 28 days, the smaller the coin's 28-day return, the larger its rise over the next 5 days, so a new high reached from a flat base is followed by more rise than one reached after a steep climb.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
