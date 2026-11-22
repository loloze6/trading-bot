---
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size_4h
idea tested: 024-02_fading-volume-downrun-rebound-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3739 USD
---
## Findings
- **F1:** The book fails on its falls: chained over the windows it earns 18.9 % a year but its deepest fall is −57.1 % (Calmar 0.33 against 0.75), and it loses most in the windows where the coin itself falls hard: w7 −32 % (coin −50 %), w14 −40 % (coin −49 %), w2 −20 % (coin −44 %), w1 −22 % (coin −23 %).
- **F2:** The book mostly carries the coin's own direction: it is long on 78–80 % of bars in every 30-day-return quartile, and on the coins' worst fifth of days it loses −3.17 % against the coin's −5.36 %, while on the best fifth it gains +3.05 % against +5.34 %.
- **F3:** The tested effect is absent overall: over 4,578 cases the unusual 18-bar move is about 0.00 % (step 5: t 0.002, strength 0.000), and the +0.41 % total move is only the coin's normal drift.
- **F4:** The rebound appears only when the coin has risen over the past 30 days. In the top quartile of the 30-day return (above +16.4 %, 851 cases) the unusual move is +0.98 % with t 2.96. In the other three quartiles it is −0.35 % (t −1.19), −0.30 % (t −1.36) and −0.09 % (t −0.40).
- **F5:** The book's falls sit in the coin's 30-day down states. On days when the coin's 30-day return is negative, the book's mean daily return is −0.011 % (6,411 coin-days), against +0.181 % when it is positive (6,650). Summed bar gains are +0.08 and −0.90 in the two lowest 30-day-return quartiles, against +6.59 and +9.41 in the two highest.
- **F6:** Inside the 30-day down state, the bets the book takes lose even after drift is removed. Cases with a low forecast lose −0.69 % (t −2.64, 800 cases) and cases with a mid forecast lose −0.89 % (t −2.90, 728). Inside the 30-day up state, the move grows with the forecast: −0.45 % for low, +0.56 % for mid, +0.69 % for high (t 2.55, 984 cases).
- **F7:** The rebound also grows with recent volatility against its usual level. Splitting cases by the ratio of 5-day to 30-day volatility of 4h returns, the lowest quartile has an unusual move of −0.51 % (t −2.09, 852 cases) and the highest +0.69 % (t 2.14, 851 cases).
- **F8:** The forecast's size is graded as the idea says. Its top tier (17.7–20, 2,289 cases) has an unusual move of +0.52 % (t 2.88) and its lowest tier (2–9.9, 1,145 cases) −0.63 % (t −2.92), so the losses come from the weaker streaks.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend` (from F1, F4, F5, F6, F2): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days, only while the coin has risen over the past 30 days. The larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, and the larger the coin's 30-day rise, the larger the rebound.
- `024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst` (from F7, F8, F3): When a coin has just fallen in an unbroken streak of four-hour periods, and the volume across the streak has been declining, it rises over the next three days. The rise is larger the larger the streak's loss relative to the coin's typical four-hour move over the past 30 days, and the higher the coin's volatility over the past 5 days against its volatility over the past 30 days.
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound` (from F4, F6, F5): When a coin has risen over the past 30 days and then falls in an unbroken streak of four-hour periods on declining volume, it rises over the next three days. The larger its 30-day rise, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
