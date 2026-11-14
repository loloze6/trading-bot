---
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
idea tested: 001-01_rsi-high-extreme-reversal
step 5: not observable
step 6: none
mode: one call
explorations: 2
cost: 0.2188 USD
---
## Findings
- **F1:** The plan's minimum of 30 non-overlapping cases could not be reached even in principle, because the backtest holds one coin (BTCUSD) in one window of 120 daily bars, which gives only 23 non-overlapping 5-bar blocks with a defined forward return. Even if every block had been extreme, the count would have been 23.
- **F2:** ETH and BNB are missing from the data, so the plan's check of "negative in at least 2 of 3 coins" could not be met by construction: 1 coin had extreme cases and 1 coin was negative.
- **F3:** The situation itself is rare. Of the 120 bars, 15 had a forecast of −10 or lower, and they formed only 3 separate runs (median length 2 bars, longest 12), so the 5-bar grid caught just 3 cases. At other grid offsets the count was 2 to 4.
- **F4:** The "high extreme" in this window was a mild RSI rather than a true extreme. RSI(14) never reached 60 (0 bars at 60, 65 or 70; maximum 58.0), and the extreme bin covered RSI 54.0 to 58.0, so the 60-bar standardisation labelled ordinary readings as extremes in a calm period.
- **F5:** The outcome varies far more than the effect. At the 3 extreme grid cases the excess 5-bar return was −6.75% with a standard deviation of 6.35% (t −1.84). Over all 15 overlapping extreme bars it was −2.34% with a standard deviation of 5.66%, and the 5-bar return's overall standard deviation was 7.27%. At the milder −2 threshold, about 35 cases would be needed for t = −2 (6 available, mean −3.2%, t −0.83).
- **F6:** The direction was consistently negative but small. The excess return was negative at every one of the 5 grid offsets (−0.2% to −6.8%), which leaves the reversal reading open rather than refuted.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_daily-rsi-highs-revert-multi-year` (from F1, F2, F3, F5, F6): On each of BTC, ETH and BNB, daily bars where RSI(14) is high relative to its own past 60 daily readings are followed by a 5-day return below that coin's average 5-day return, observed over several years of data so that at least 30 non-overlapping cases accumulate per coin.
- `001-01_rsi-high-extreme-reversal.a2_intraday-rsi-highs-revert` (from F1, F3, F4, F5): On each of BTC, ETH and BNB, 4-hour bars where RSI(14) is high relative to its own past 60 readings are followed by a 5-bar return below that coin's average 5-bar return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
