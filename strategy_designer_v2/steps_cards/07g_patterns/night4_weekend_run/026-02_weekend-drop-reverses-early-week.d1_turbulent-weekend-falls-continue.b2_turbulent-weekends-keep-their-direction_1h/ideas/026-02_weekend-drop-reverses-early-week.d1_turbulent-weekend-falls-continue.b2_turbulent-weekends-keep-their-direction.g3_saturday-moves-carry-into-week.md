---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over Saturday (Saturday 00:00 to Sunday 00:00 UTC) continues in the same direction over the 2 days after Monday 00:00 UTC. The continuation is larger the larger Saturday's move.
Consequence: A trader may follow Saturday's direction over Monday and Tuesday, sized by how large Saturday's move was, while treating Sunday's move separately.
Why:
- F3: Saturday's 24-hour return continues over the 48 hours from Monday 00:00 (slope +0.208, t 4.60, 1,789 cases), while the whole weekend's 48-hour return predicts nothing (−0.023, t −0.70). The two halves cancel, so the tested idea's whole-weekend signal is weak.
- F4: The Saturday continuation is less steady than the Sunday reversal: it shows in 4 of 6 coins (t 2.27 to 2.75; LTC and ZEC near 0) and in 5 of 8 years (t 2.7 to 5.0), but 2018, 2021 and 2025 are negative (t −0.36 to −1.45).
- F7: The tested idea's gradation shows only at the top: weekends in the top tercile of volatility ratio continue by +0.109 usual 48-hour moves (t 2.23, 596 cases), against −0.037 (t −0.91) in the bottom tercile. This matches the inconclusive verdict (t 1.95).
