---
line: 7.g patterns
backtest: 061-01.g1.d1.g1_day-move-follow-through-both-sides_1d
idea tested: 061-01.g1.d1.g1_day-move-follow-through-both-sides
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4405 USD
---
## Findings
- **F1:** Over the next day the day's move reverses rather than continues: the slope of the coin's excess 1-day return on the day's move in 30-day swing units is −0.0034 (t −2.47, 7249 cases). The bottom decile of the move (z −1.74) is followed by +1.00 % and the top decile (z +1.87) by −0.17 %.
- **F2:** The next-day reversal comes from heavy volume. Down days beyond 1 swing on volume in the top third of its 30-day average are followed by +1.23 % the next day (t 2.59, 585 cases on 208 days). The same days on low volume give +0.51 % (t 0.77, 59 cases) and on mid volume +0.34 % (t 0.59, 223 cases).
- **F3:** That high-volume reversal lives in agitated markets: 0.85 % (t 3.18, 1399 cases, 596 days) there against 0.03 % in calm ones (t 0.13, 1017 cases). It holds on all six coins (0.13 % to 0.74 % per case) and in both halves of the windows (w13–18 t 2.29, w7–12 t 1.25).
- **F4:** Where the day closes in its range predicts the next day in agitated markets only: slope −0.0178 (t −3.45, 5538 cases) against −0.0015 in calm ones (t −0.28, 3150 cases). Pooled, a close in the bottom fifth is followed by +0.60 % (t 1.91) and a close in the top fifth by −0.34 % (t −1.56). The map already holds this as an agitated long rebound (039-02.d1, 045-01).
- **F5:** The tested 5-day continuation is weak, and it comes only from up days. The slope on up days is t 1.66 (641 cases) and on down days t 0.07 (779 cases). Up days beyond 2 swings gain +6.5 % over 5 days (t 2.29), but on only 38 cases. In calm markets the up-day slope has t 1.64 (284 cases), no stronger than in agitated ones (t 0.98). Among the many angles looked at, none of this stands out from chance.
- **F6:** The book earned less than holding on 5 of 6 coins and in 10 of 12 windows (BTC 0.13 % a day against 0.16 %; LTC −0.03 % against +0.11 %). Its one-day sign is against the reversal of F1, and its 5-day hold sits through it.
- **F7:** Weekday showed no pattern (largest |t| 1.32). Neither did the past 5-day return as a 5-day predictor (quintile |t| ≤ 1.15).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.g1.d1.g1.g1_agitated-heavy-volume-fall-rebound` (from F2, F3, F1): In an agitated market, the larger a coin's one-day fall in 30-day swing units, and the heavier that day's volume against its 30-day average, the more the coin rises the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
