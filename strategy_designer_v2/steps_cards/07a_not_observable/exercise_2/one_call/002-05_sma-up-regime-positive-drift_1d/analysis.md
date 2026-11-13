---
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
idea tested: 002-05_sma-up-regime-positive-drift
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1315 USD
---
## Findings
- **F1:** The plan needed at least 100 in-stretch bars and 3 up-cross stretches, but the backtest got 13 in-stretch bars and 1 stretch; it also had 107 out-of-stretch bars, so the shortfall is entirely on the side where the idea's situation holds.
- **F2:** The data is one coin (BTCUSD) and one window (w1) of 120 daily bars covering 119 days. That is shorter than the 200-day slow average itself, so a full cross-to-cross stretch of a 50/200 daily pair can hardly fit inside it.
- **F3:** The only up-stretch was already under way when the window opened, with a raw spread of +50.3 on the first bar. It ended at bar 12, the single down-cross. So the in-stretch sample is the tail of one stretch whose up-cross falls outside the data.
- **F4:** After the down-cross the raw spread never came back. Every 12-bar block from the third onward averaged between -50.2 and -90.8 (low of -92.0, last value -56.9), so the window is one regime and gave no chance of a second up-cross.
- **F5:** The outcome varies far more than the effect being measured. The next-bar return SD was 0.0233 in-stretch and 0.0342 out-of-stretch, against a mean difference of -0.0069 (Welch t -0.95). At a daily SD near 0.03, a true drift of 0.2% per day needs roughly 1,800 bars per side to reach t=2, which means many years of daily bars or many coins.
- **F6:** BTC fell 21.1% over the window. The 13 in-stretch bars averaged -0.76% next-bar against -0.07% out-of-stretch, and their up-share was 13.4 points lower. This is one late, fading stretch, not a sample of stretches.

## Ideas
- `002-05_sma-up-regime-positive-drift.a1_daily-golden-cross-stretch-drift` (from F1, F2, F3, F5): On a coin's daily bars, the days on which its 50-day simple average is above its 200-day simple average are followed by a higher mean next-day close-to-close return than the days on which it is below, measured over many coins and many years so that dozens of up-cross stretches are covered.
- `002-05_sma-up-regime-positive-drift.a2_hourly-up-stretch-positive-drift` (from F2, F4, F5): On a coin's hourly bars, the hours on which its 50-hour simple average is above its 200-hour simple average are followed by a higher mean next-hour close-to-close return than the hours on which it is below. At this scale, cross-to-cross stretches recur many times within a few months.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
