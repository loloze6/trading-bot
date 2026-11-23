---
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4030 USD
---
## Findings
- **F1:** Over 7 days and 3 days, momentum shows at the extreme: on a non-overlapping 3-day grid, the decile of the largest 7-day returns (scaled by 30-day daily volatility × √7) is followed by a 3-day return +1.99 % above the coin's drift (t 3.98, 429 cases). The middle deciles 1–8 run from −0.49 % to +0.16 %. The effect is positive in 4 of 6 coins (BTC +1.80 % t 3.07, ETH +2.02 % t 2.56, XRP +6.42 % t 3.29) and in 6 of 8 years (2024 +3.56 % t 3.54, 2020 +3.43 % t 2.62). Its Spearman correlation with the next 3 days, among positive 7-day returns, is +0.065.
- **F2:** Large one-day falls are followed by a rebound the next day, graded by the size of the fall. On a daily grid, the next day's excess return is +0.51 % in the decile of the largest falls (scaled by 30-day volatility; t 3.34, 1307 cases), +0.28 % in the second decile (t 2.31) and +0.03 % in the third. It is positive in all 6 coins (XMR +1.11 % t 3.38) and all 8 years, though near zero in 2024 and 2025 (+0.02 %, +0.04 %). Large one-day rises show no matching reversal (top decile −0.04 %, t −0.29).
- **F3:** The pooled hour-of-day excess concentrates in the bars stamped 20:00 (+4.83 bp, t 5.98, n 17403) and 21:00 (+3.74 bp, t 4.85). On a non-overlapping 6-hour grid, the 18:00–24:00 block is +0.093 % above drift (t 4.86, n 17287), and the next block, 00:00–06:00, gives it back at −0.079 % (t −4.57). Both are well under the 0.19 % cost of a trade, as was the tested idea's total move of +0.10 % per case.
- **F4:** The tested stretch, 21:00–23:00, is not stable across coins or years: per coin from −1.22 bp (XRP) to +2.72 bp (ZEC), no coin with |t| ≥ 2, and positive mainly in 2018 (t 2.48) and 2023 (t 5.20).
- **F5:** By weekday, Saturday's daily return is +0.335 % above drift (t 4.08, n 2484), while Thursday is −0.299 % (t −2.70) and Tuesday −0.242 % (t −2.53). This is a weekend rise followed by early-week weakness, the opposite of a reversal of the weekend's own move only in sign of drift, not tested per move.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift.g1_strong-week-continues-three-days` (from F1): A coin whose 7-day return is large and positive relative to its 30-day daily volatility keeps rising over the next 3 days, by more than its normal drift, and the stronger the 7-day rise relative to that volatility, the larger the 3-day gain.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift.g2_large-daily-fall-rebounds` (from F2): After a one-day fall that is large relative to the coin's 30-day daily volatility, the coin rises over the next day by more than its normal drift, and the larger the fall in units of that volatility, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
