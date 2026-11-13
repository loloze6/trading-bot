---
line: 7.g patterns
backtest: N3-02_breakout-shock-continues_1d
idea tested: N3-02_breakout-shock-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3513 USD
---
## Findings
- **F1:** A large down day that closes at a new 21-day closing low (standardised one-day return ≤ -10) is followed by a mean excess 5-bar return of +1.28% (t = 2.40, 485 merged non-overlapping cases); the 466 cases below the 50-bar average give +1.37% (t = 2.47); new lows without a large down day give -0.25% (t = -0.38, n = 321); and the excess is positive in all six coins, from +0.39% in XMR to +2.48% in ZEC, though no single coin reaches t = 2.
- **F2:** Large down days still help when they are not at a new low: those cases give +0.71% excess over 5 bars (t = 2.22, n = 1060). On all non-overlapping bars, days with z ≤ -20 give +0.96% (t = 1.56, n = 168). The large down move itself, more than the new low, seems to come before the rebound.
- **F3:** Shock-up new highs depend on how volatile the coin has been. When the coin's 20-day volatility ranks in the lower two thirds of its past 250 bars, the 5-bar excess is +3.18% (t = 2.01, n = 69) and +2.76% (t = 2.21, n = 70). In the top third it is +0.89% (t = 0.51, n = 95). Across coins, five of six are positive in the calm cases.
- **F4:** The shock-up new-high effect is unstable by year: 2023 gives -1.69% (t = -2.65, n = 80) and 2022 gives -1.92% (t = -1.38, n = 56), while 2024 gives +2.06%. My own pooled recount of all shock-up new highs is +0.10% (t = 0.19, n = 527), against the verdict's t = 2.03, so the confirmed effect is fragile.
- **F5:** The book's trades split sharply by holding time. The 935 trades held one day or less lose on average (-1.87% net, median -1.35%). Trades held 1–2, 2–5 and 5–10 days gain +3.74%, +9.78% and +13.87% (n = 286, 224, 62). The 80 trades held over 10 days lose -7.52%. Most of the loss comes from breakouts that fail at once.
- **F6:** The day after a Friday bar beats the coin's mean daily return by +0.24% (t = 2.71, 2070 days). This holds in five of six coins and in six of eight years (2019 t = 2.51, 2025 t = 2.85). The days after Monday and Wednesday bars are below the mean, at -0.26% (t = -2.59) and -0.30% (t = -2.53). These come from scanning seven weekdays, so the weekday results are weaker than their t suggests.
- **F7:** The book's best 2% and worst 2% of days both come the day after a coin rose about +11% (t = 10.5 and t = 9.3, n = 85 each). The book's tail outcomes are set almost entirely by what follows one-day shock-ups.

## Ideas
- `N3-02_breakout-shock-continues.g1_shock-low-capitulation-rebound` (from F1, F2): After a large down day relative to the coin's own recent day sizes, especially one that closes at a new 21-day closing low, the coin rises over the next five days by more than its average five-day move. Late sellers capitulate and the selling then runs out.
- `N3-02_breakout-shock-continues.g2_calm-market-breakout-shocks-continue` (from F3, F4, F5): A shock-up day closing at a new 21-day closing high is followed by a larger five-day rise when the coin's recent 20-day volatility is low or middling against its own past year, compared with when volatility is already high.
- `N3-02_breakout-shock-continues.g3_post-friday-weekend-drift-up` (from F6): The day that follows a Friday daily bar closes higher than the coin's average day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
