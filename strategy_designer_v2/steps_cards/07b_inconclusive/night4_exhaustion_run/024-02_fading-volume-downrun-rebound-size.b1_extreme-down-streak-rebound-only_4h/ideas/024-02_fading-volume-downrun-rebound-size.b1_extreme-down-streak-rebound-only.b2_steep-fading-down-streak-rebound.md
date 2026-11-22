---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods with declining volume, it rises over the next three days. The larger the streak's loss per four-hour period, counted in the coin's typical four-hour move over the past 30 days, the larger the rise.
Consequence: A trader favours steep, quick down-streaks on fading volume as rebound buys over long, slow ones of the same depth.
Why:
- F2: Recomputed on the bars, the idea's own situation shows a large move. Fading-volume down-streaks whose loss exceeds 4 usual 4h moves are followed by an 18-bar excess return of +2.15 % (t 6.16, 846 cases, one per grid cell), a strength of 0.26 of the usual move. That is about 11 times the 0.19 % cost of a trade, against 0.1 times for the test's bets.
- F3: The rise is graded by the relative loss. By loss band it is +1.48 % (t 3.21) at 4–5 usual moves, +1.45 % (t 2.55) at 5–6, +3.77 % (t 3.60) at 6–8 and +3.45 % (t 3.26) above 10. The slope is +0.34 % per usual move (t 2.06, 846 cases), while ordinary fading streaks of at most 2 moves are followed by −0.35 % (t −2.54, 3,313 cases).
- F6: Among streaks of more than 4 usual moves, the rebound is concentrated in short, steep streaks. Streaks of 2, 3 and 4 bars give +2.45 %, +3.61 % and +1.88 % (t 3.85, 4.48, 3.15). Streaks of 5 and 6 bars give −0.10 % and −0.26 % (98 and 49 cases).
