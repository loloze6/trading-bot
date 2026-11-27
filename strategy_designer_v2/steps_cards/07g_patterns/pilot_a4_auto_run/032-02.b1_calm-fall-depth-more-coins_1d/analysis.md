---
line: 7.g patterns
backtest: 032-02.b1_calm-fall-depth-more-coins_1d
idea tested: 032-02.b1_calm-fall-depth-more-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3485 USD
---
## Findings
- **F1:** The tested depth signal carried nothing: its slope t was -0.44 on 1016 grid cases over 425 days, and its short-direction unusual move was -0.19 % per 3 days (t -0.47, 407 days). That is smaller than the 0.33 % a trade costs. The raw 30-day depth from the high, re-measured here in falling calm bars, also failed to predict the 3-day excess return (slope t 1.12, 181 cases, 123 days).
- **F2:** In falling calm bars, a coin's last 3 days predicted its next 5 days in the same direction. The 3-day return predicted the 5-day excess return with clustered slope t 3.02 (113 cases, 77 days). Scaled by the coin's 30-day swing, it gave t 2.86 (104 cases, 70 days). The sign held in both halves (Spearman 0.26 up to 2019, 0.19 after) and on BTC (0.14) and XMR (0.37), but not on DOGE (-0.07, few cases).
- **F3:** Over 3 days the same pattern was weaker but pointed the same way. The 3-day return's top quartile was followed by +1.47 % excess and its bottom quartile by -1.43 % (Spearman 0.14, p 0.06, 190 cases). Out of the profile, the swing-scaled 3-day return had no such slope (t 0.92, 572 days), so the continuation is specific to falling calm markets.
- **F4:** A coin's distance above its lowest close of the past 30 days predicted higher excess returns in falling calm bars at every horizon. The slope t was 2.46 over 3 days (181 cases), 2.31 over 5 days (108 cases) and 2.50 over 10 days (54 cases). Distance from the 30-day high did not (t 1.12, 0.84, 0.64).
- **F5:** The swing-scaled 10-day return predicted the 10-day excess return with t 3.86, but on only 50 cases over 34 days, and the effect sat mostly after 2019 (Spearman 0.78, against 0.22 up to 2019). It is suggestive, not firm.
- **F6:** About 20 slope tests were run across three horizons, plus quartile, weekday, window and next-day checks. Only the short-term momentum family (F2 and F4) passed t 2.5 to 3.9. The in-profile mean excess return was itself flat (+0.14 % per 3 days, t 0.29, 197 cases), so the gain comes from grading by the recent move, not from being in the profile.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-02.b1.g1_calm-decline-rebound-continuation` (from F2, F3, F6): In a falling, calm market, the more a coin has risen over the last three days relative to its usual daily swing, the more it rises over the next five days.
- `032-02.b1.g2_calm-decline-lift-from-low` (from F4, F1, F6): In a falling, calm market, the further a coin's close sits above its lowest close of the past 30 days, the more it rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
