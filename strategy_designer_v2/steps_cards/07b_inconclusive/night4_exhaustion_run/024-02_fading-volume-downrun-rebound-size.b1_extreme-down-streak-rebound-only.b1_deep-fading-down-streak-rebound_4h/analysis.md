---
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3918 USD
---
## Findings
- **F1:** The test's bets fired mostly on shallow streaks, where the rebound is absent or negative. The two lowest forecast quintiles (forecast 3.8 and 10.0, loss 1.0 and 1.4 usual moves) give −0.55 % (t −1.91, 756 cases) and −0.83 % (t −2.72, 755 cases). The forecast also saturates at 20 from a loss of only about 2.7 usual moves onward. Together these dilute the main measure to +0.05 % (t 0.37, 4039 cases).
- **F2:** Counted directly in usual moves, the effect is concentrated in the deepest fading-volume down-streaks. The deepest decile (mean loss 5.9 usual moves) rises +2.02 % over 18 bars beyond the drift (t 4.10, 433 cases), and the deepest quintile (4.6 usual moves) rises +1.34 % (t 4.35, 866 cases). Every decile below the eighth is at or below zero, down to −0.79 % (t −2.09).
- **F3:** Inside fading streaks the rise grows with the loss. The correlation of the loss in usual moves with the 18-bar excess return is 0.105 for fading streaks and 0.033 for non-fading ones. It is positive in each 30-day trend state: 0.099 when the coin is down over 30 days, 0.083 when it is up.
- **F4:** The deep-streak rebound is larger when volume fades. The deepest fading quintile minus the deepest non-fading quintile is +0.86 % over 18 bars (Welch t 1.96; 866 against 910 cases), and the deepest non-fading decile reaches only +0.60 % (t 1.48).
- **F5:** The deep fading-streak rebound builds through three days: +0.68 % over 6 bars (t 3.76), +0.86 % over 12 bars (t 3.27) and +1.34 % over 18 bars (t 4.35), 866 cases each.
- **F6:** The deep fading-streak rebound holds across coins and most years, but not in the bear years 2018 and 2022.
- **F7:** The measured cases could not pay their own cost apart from the drift: the unusual move is 0.3 times the 0.19 % trade cost. In the deepest fading decile, however, the unusual move of about 2.0 % per case is roughly ten times that cost.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound.b1_deepest-fading-down-streak-rebound` (from F1, F2, F3, F4, F5, F6, F7): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only when the streak's loss is among the deepest the coin makes, many times its typical four-hour move over the past 30 days, counted directly in that typical move and not against the sizes of the coin's other recent streaks; among these deepest streaks, the larger the loss relative to that typical move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
