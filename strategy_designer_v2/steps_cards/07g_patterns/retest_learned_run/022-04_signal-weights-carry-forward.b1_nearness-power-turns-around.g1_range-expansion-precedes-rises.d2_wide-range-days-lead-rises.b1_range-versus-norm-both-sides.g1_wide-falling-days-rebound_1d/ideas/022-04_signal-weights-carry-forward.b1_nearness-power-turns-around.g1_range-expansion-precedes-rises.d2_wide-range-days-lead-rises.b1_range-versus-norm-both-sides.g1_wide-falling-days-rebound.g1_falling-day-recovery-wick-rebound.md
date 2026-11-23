---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On days a coin closes lower, the larger the distance from the day's low back up to its close, measured against the coin's average daily high-low range over the past 30 days, the higher the coin's return over the next 3 days above its usual drift.
Consequence: A trader would lean long after a falling day whose intraday sell-off was bought back by an unusually large amount for the coin, more strongly the larger that recovery, holding for 3 days.
Why:
- F2: On falling days, the effect is concentrated in the widest fifth of the range ratio. That fifth showed a 3-day excess return of +1.84 % (t 4.36, 523 cases), while the other four fifths ranged from −0.88 % to −0.13 %. On rising days the range ratio has no slope (t −0.55, 2601 cases), so the falling-day gate is essential.
- F3: On falling days, where the close sits within the day's range adds information of its own. A pooled regression on the range ratio and the close's location in the range (0 at the low, 1 at the high) gives t 4.95 for the range and t 2.90 for the close location (2397 cases). Falling days that closed in the top fifth of their range were followed by +1.48 % excess over 3 days (t 4.00, 480 cases), against −0.81 % to −0.03 % for the middle fifths.
- F1: The tested idea's gain sits entirely on its long side. Bars held long earned +0.0526 % per bar (t 4.35, 5459 coin-bars), while bars held short earned −0.0017 % (t −0.28, 8018 coin-bars). Long trades netted +2.00 % on average over 2146 trades, and short trades netted −1.69 % over 2528 trades. The narrow-falling-day short half therefore holds most of the positions but adds nothing except fees, which drags the mean daily return on days in a position down to 0.0145 %.
