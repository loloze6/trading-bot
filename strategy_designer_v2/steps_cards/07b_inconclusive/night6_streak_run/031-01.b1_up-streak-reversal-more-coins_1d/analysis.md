---
line: 7.b inconclusive
backtest: 031-01.b1_up-streak-reversal-more-coins_1d
idea tested: 031-01.b1_up-streak-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3982 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but small: after short cases the unusual 5-day move is +0.27 % with a day-pooled t of 0.87 (5,838 cases on 1,362 days, strength 0.028). That is about half the coins' normal drift against the short (−0.74 %), so the total move is −0.47 %, which is −2.1 times the 0.22 % cost of a trade.
- **F2:** The effect does not grow with how unusual the streak is. By |forecast| quintile, the unusual 5-day move is flat (+0.27 %, +0.36 %, +0.26 %, +0.38 %, +0.07 %; every t under 0.9), and the supporting check is only +0.05 %. By streak length at the case, it is +0.36 % at 1 day (t 1.11, 5,049 cases), +0.16 % at 2 days (t 0.20, 748 cases) and −0.83 % at 3 or more days (t −0.63, 89 cases).
- **F3:** Most cases are one-day "streaks": 5,049 of the 5,838 cases fall on the first up close. The test therefore mostly measured what follows any single up day, not what follows an unusually long run.
- **F4:** On all bars, the day after an up close grades the wrong way for reversal. The next-day unusual move is −0.21 % after a 1-day up streak (t −1.79, 8,258 bars), then rises steadily to +0.21 % after 5 days (t 0.60) and +0.32 % after 6 or more (t 0.79). Longer up streaks lean toward continuation, not giveback.
- **F5:** The only significant reading is at a 1-day horizon (+0.35 %, t 2.57, 1,410 days), and it fades with the horizon: t 0.16 at 3 days, 0.87 at 5, 0.30 at 10 and 0.04 at 20. It is a short-lived wobble after an up close, not something that builds with streak length.
- **F6:** The sign changes from year to year, so the effect is mixed rather than hidden in one regime. The unusual 5-day move is +3.15 % in 2018 (t 2.66), −1.82 % in 2020 (t −1.85), +1.22 % in 2022 (t 1.82) and −0.47 % in 2024 (t −0.57). By coin it is also mixed: 12 of 18 coins are positive and none has a t above 1.6.
- **F7:** Down streaks show no graded follow-on either. The unusual 5-day move after a down streak swings from +1.49 % at 3 days (t 1.83, 385 cases) to −2.94 % at 4 days (t −1.96, 139 cases) and −2.11 % at 5 days (t −0.80). Neither side of the brief shows a move that grows with streak length.

## Ideas
- No ideas: The test already used every coin and all four folds, so no more daily data is available. The effect is not clearly present in any one part of the data and graded with streak length there (F2, F4, F6, F7). The only significant reading is a 1-day reversal after a single up close (F3, F5), which does not grow with the streak, so no graded idea rests on it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
