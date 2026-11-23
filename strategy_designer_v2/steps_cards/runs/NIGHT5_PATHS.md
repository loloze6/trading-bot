# Night 5: the path of each loop

Per session, the ideas in the order they were tested (starting ideas first), how each was made (the step 7 line
that wrote it, or the brief), steps 5 and 6, and the step 7 lines called on it with the number of ideas each wrote.
Lineage code: the brief idea, then one letter per generation (b: 7.b inconclusive, d: 7.d confirmed not profitable,
e: 7.e profitable not proven, g: 7.g patterns). "not finished": failed (mostly a file name too long, topic 46) or cut.
Built from `orchestration/loop/<run>/loop.jsonl` and `orchestration/run_idea/<run>/table.json`.

### Session 1, weekend (brief 026, 1h)

| # | Idea (lineage code, name) | Made by | Step 5 | Step 6 | Step 7 lines called (ideas written) |
|---|---|---|---|---|---|
| 1 | 026-03.d3 saturday-move-continues-early-week | 7.d | confirmed +4.57 | no: Calmar | 7.d (2), 7.g (2) |
| 2 | 026-03.d3.d1 saturday-continuation-in-calm-markets | 7.d | confirmed +4.14 | no: Calmar | 7.d (2), 7.g (3) |
| 3 | 026-03.d3.d2 large-saturday-moves-continue | 7.d | inconclusive +0.80 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.b (1), 7.g (3) |
| 4 | 026-03.d3.d2.b1 sunday-moves-reverse-early-week | 7.b | confirmed +2.56 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (3) |
| 5 | 026-03.d3.d1.d1 saturday-continuation-with-weekly-trend | 7.d | confirmed +5.86 | **pays** | 7.g (3) |
| 6 | 026-03.d3.d1.d2 calm-up-saturday-continues-higher | 7.d | - | - | - |
| 7 | 026-03.d3.d2.b1.d1 sunday-reversal-grows-with-volatility | 7.d | - | - | - |
| 8 | 026-03.d3.d2.b1.d2 sunday-move-reverses-on-monday | 7.d | confirmed +3.68 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (2) |
| 9 | 026-03.d3.d2.b1.d2.d1 volatile-sunday-reversal-over-two-days | 7.d | confirmed +2.61 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | - |
| 10 | 026-03.d3.d2.b1.d2.d2 sunday-falls-rebound-early-week | 7.d | inconclusive +1.06 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | - |
| 11 | 026-03.d3.d2.b1.d2.d3 moderate-sunday-moves-reverse-most | 7.d | confirmed +3.41 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | - |
| 12 | 026-03.d3.d2.b1.d2.g1 volatile-market-falls-rebound-next-day | 7.g | rejected +4.57 | no: Sharpe minus holding's Sharpe, Calmar | - |
| 13 | 026-03.d3.d2.b1.d2.g2 late-evening-utc-upward-drift | 7.g | inconclusive +7.91 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.b (3), 7.g (2) |
| 14 | 026-04.b2 heavy-weekend-moves-continue | 7.b | confirmed +2.53 | no: Calmar | 7.d (3), 7.g (2) |
| 15 | 026-04.b2.d1 heavy-weekend-continuation-calm-coins | 7.d | confirmed +2.63 | no: Calmar | 7.d (2) |
| 16 | 026-04.b2.d2 trend-aligned-heavy-weekend-continuation | 7.d | inconclusive +1.76 | no: Calmar | 7.b (2), 7.g (2) |
| 17 | 026-04.b2.d3 heavy-weekends-without-xmr | 7.d | inconclusive +3.15 | **pays** | 7.b (2), 7.e (2), 7.g (3) |
| 18 | 026-04.b2.d1.d1 heavy-weekend-extends-week | 7.d | confirmed +3.11 | **pays** | 7.g (3) |
| 19 | 026-04.b2.d1.d2 heavy-weekend-monday-morning-continuation | 7.d | confirmed +2.65 | no: Calmar | 7.d (3), 7.g (2) |
| 20 | 026-04.b2.d1.d2.d1 heavy-weekend-continuation-with-trend | 7.d | confirmed +2.42 | no: Sharpe minus holding's Sharpe, Calmar | 7.d (2), 7.g (2) |
| 21 | 026-04.b2.d1.d2.d2 heavy-weekend-falls-continue | 7.d | confirmed +3.87 | **pays** | 7.g (3) |
| 22 | 026-04.b2.d1.d2.d3 much-heavier-weekend-continuation | 7.d | confirmed +2.45 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (4) |
| 23 | 026-04.b2.d1.d2.d3.d1 heavy-weekend-falls-continue | 7.d | not finished | | |

Generation of the ideas tested, in order: 1 2 2 3 3 3 4 4 5 5 5 5 5 1 2 2 2 3 3 4 4 4 5. Branches (idea and its first child): 2; the most tested: 13 of 23.

### Session 2, learned combination (brief 022, 1d)

| # | Idea (lineage code, name) | Made by | Step 5 | Step 6 | Step 7 lines called (ideas written) |
|---|---|---|---|---|---|
| 1 | 022-04.b1 nearness-power-turns-around | 7.b | inconclusive +1.97 | no: Calmar | 7.b (1), 7.g (2) |
| 2 | 022-04.b1.b1 nearness-power-reversal-more-coins | 7.b | confirmed +2.05 | no: Calmar | 7.d (2) |
| 3 | 022-04.b1.b1.d1 nearness-power-reversal-long-side | 7.d | inconclusive +1.72 | no: Calmar | 7.b (1), 7.g (1) |
| 4 | 022-04.b1.b1.d2 strong-nearness-power-reversals | 7.d | confirmed +2.02 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (2) |
| 5 | 022-04.b1.b1.d1.b1 nearness-reversal-all-coins | 7.b | inconclusive +1.97 | no: Calmar | 7.b (1) |
| 6 | 022-04.b1.b1.d2.d1 nearness-power-reversal-long | 7.d | confirmed +2.48 | no: Calmar | 7.d (3), 7.g (1) |
| 7 | 022-04.b1.b1.d2.d2 reversal-shorts-in-downtrends | 7.d | inconclusive +1.50 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.b (2), 7.g (1) |
| 8 | 022-04.b1.b1.d1.b1.b1 nearness-reversal-after-rises | 7.b | inconclusive +1.99 | **pays** | 7.b (1), 7.e (2), 7.g (1) |
| 9 | 022-04.b1.b1.d1.b1.b1.e1 short-volatility-scaled-momentum | 7.e | not finished | | |
| 10 | 022-04.b1.b1.d1.b1.b1.e2 monthly-return-predicts-week | 7.e | not finished | | |
| 11 | 022-04.b1.b1.d2.d2.b1 nearness-reversal-more-coins | 7.b | inconclusive +1.70 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.b (1), 7.g (5) |
| 12 | 022-04.b2 volatility-power-turns-around | 7.b | inconclusive +0.31 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.g (1) |
| 13 | 022-04.b1.b1.d2.d2.b2 reversal-shorts-on-downtrend-bounces | 7.b | confirmed +3.68 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | - |
| 14 | 022-04.b1.b1.d1.b1.b1.b1 thirty-day-rise-carries-forward | 7.b | not finished | | |
| 15 | 022-04.b1.b1.d2.d2.b1.b1 nearness-reversal-over-20-days | 7.b | not finished | | |
| 16 | 022-04.b1.b1.d2.d1.d1 nearness-reversal-in-uptrends | 7.d | - | - | - |
| 17 | 022-04.b1.b1.d2.d1.d2 nearness-reversal-after-20-day-strength | 7.d | inconclusive +1.07 | **pays** | - |
| 18 | 022-04.b1.b1.d2.d1.d3 nearness-reversal-after-quiet-week | 7.d | inconclusive +1.33 | no: Calmar | 7.b (2), 7.g (3) |
| 19 | 022-04.b1.g1 range-expansion-precedes-rises | 7.g | confirmed +2.56 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3) |
| 20 | 022-04.b1.g1.d1 range-expansion-in-uptrends | 7.d | inconclusive +1.44 | no: Calmar | 7.b (2), 7.g (1) |
| 21 | 022-04.b1.g1.d2 wide-range-days-lead-rises | 7.d | inconclusive +0.02 | no: Calmar | 7.b (1), 7.g (1) |
| 22 | 022-04.b1.g1.d3 range-expansion-ten-day-rise | 7.d | confirmed +2.18 | no: Calmar | 7.d (2), 7.g (1) |
| 23 | 022-04.b1.g1.d1.b1 range-expansion-uptrend-more-coins | 7.b | confirmed +3.86 | **pays** | 7.g (1) |
| 24 | 022-04.b1.g1.d2.b1 range-versus-norm-both-sides | 7.b | confirmed +2.81 | no: Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (1) |
| 25 | 022-04.b1.g1.d2.b1.d1 wide-days-in-uptrends-rise | 7.d | confirmed +3.39 | **pays** | 7.g (1) |
| 26 | 022-04.b1.g1.d2.b1.d2 range-expansion-long-side-only | 7.d | confirmed +2.23 | no: Calmar | 7.d (3), 7.g (3) |
| 27 | 022-04.b1.g1.d2.b1.d3 wide-uptrend-days-held-longer | 7.d | mismatch | no: Mean daily return, on days in a position | 7.g (2) |
| 28 | 022-04.b1.g1.d2.b1.g1 wide-falling-days-rebound | 7.g | confirmed +2.91 | no: Mean daily return, on days in a position, Calmar | 7.d (2), 7.g (2) |
| 29 | 022-04.b1.g1.d2.b1.g1.d1 wide-falling-days-long-only | 7.d | confirmed +3.96 | no: Calmar | - |
| 30 | 022-04.b1.g1.d2.b1.g1.d2 wide-falls-rebound-in-uptrends | 7.d | inconclusive +1.77 | no: Calmar | - |
| 31 | 022-04.b1.g1.d2.b1.g1.g2 down-day-close-near-high | 7.g | inconclusive +3.07 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | - |

Generation of the ideas tested, in order: 1 2 3 3 4 4 4 5 6 6 5 1 5 6 6 5 5 5 2 3 3 3 4 4 5 5 5 5 6 6 6. Branches (idea and its first child): 2; the most tested: 30 of 31.

### Session 3, settlement hours (brief 017, 1h)

| # | Idea (lineage code, name) | Made by | Step 5 | Step 6 | Step 7 lines called (ideas written) |
|---|---|---|---|---|---|
| 1 | 017-05 settlement-move-reverses-after | brief | confirmed +5.12 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (4) |
| 2 | 017-02.g2 hourly-reversal-in-volatile-periods | 7.g | confirmed +13.77 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (2) |
| 3 | 017-01.g2 hourly-move-reversal-by-volatility | 7.g | confirmed +12.28 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (2), 7.g (1) |
| 4 | 017-05.d1 settlement-fall-recovers-over-day | 7.d | confirmed +2.88 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (2) |
| 5 | 017-05.d2 counter-trend-settlement-move-reverses | 7.d | inconclusive +1.25 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.b (2), 7.g (4) |
| 6 | 017-05.d3 settlement-fall-rebound-eight-hours | 7.d | confirmed +5.89 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (2), 7.g (2) |
| 7 | 017-05.d2.b1 settlement-reversal-more-coins | 7.b | confirmed +2.31 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (2), 7.g (4) |
| 8 | 017-05.d2.b2 two-hour-settlement-snapback | 7.b | confirmed +6.71 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (2) |
| 9 | 017-01.g2.d1 hourly-shock-reverses-over-day | 7.d | confirmed +4.83 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (2), 7.g (3) |
| 10 | 017-02.g2.d1 day-long-fade-of-sharp-hours | 7.d | confirmed +5.67 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (2) |
| 11 | 017-05.d1.d1 settlement-fall-recovers-when-volatile | 7.d | confirmed +3.30 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (2), 7.g (3) |
| 12 | 017-05.d3.d1 strong-settlement-fall-day-rebound | 7.d | inconclusive +4.16 | no: Sharpe minus holding's Sharpe, Calmar | 7.b (2), 7.g (2) |
| 13 | 017-01.g2.d2 moderate-hourly-shocks-reverse-daily | 7.d | confirmed +5.03 | no: Sharpe minus holding's Sharpe, Calmar | 7.d (3), 7.g (2) |
| 14 | 017-02.g2.d2 buy-sharp-volatile-hourly-falls | 7.d | inconclusive -0.32 | no: Calmar | 7.b (2), 7.g (2) |
| 15 | 017-05.d1.d2 settlement-fall-recovers-after-runup | 7.d | inconclusive +3.15 | no: Calmar | 7.b (1), 7.g (2) |
| 16 | 017-05.d3.d2 afternoon-settlement-fall-rebound | 7.d | confirmed +5.16 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (4) |
| 17 | 017-02.g2.d3 four-hour-fade-of-extreme-hours | 7.d | confirmed +9.38 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (3), 7.g (2) |
| 18 | 017-05.d1.d3 settlement-recovery-lasts-one-day | 7.d | confirmed +3.77 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (3), 7.g (2) |
| 19 | 017-02.g2.d2.b1 volatile-regime-hourly-fall-reversal | 7.b | inconclusive +1.58 | no: Calmar | 7.b (2), 7.g (2) |
| 20 | 017-05.d1.d2.b1 settlement-fall-recovery-more-coins | 7.b | confirmed +3.05 | no: Calmar | 7.d (2), 7.g (3) |
| 21 | 017-05.d3.d1.b1 settlement-fall-rebound-more-coins | 7.b | inconclusive +1.58 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.b (2), 7.g (2) |
| 22 | 017-02.g2.d2.b2 extreme-hourly-fall-reversal | 7.b | inconclusive +0.51 | no: Calmar | 7.b (1), 7.g (2) |
| 23 | 017-05.d3.d1.b2 deep-two-hour-fall-rebound | 7.b | confirmed +3.81 | no: Calmar | 7.d (3), 7.g (3) |
| 24 | 017-01.g2.d1.d1 post-midnight-settlement-shock-reversal | 7.d | confirmed +8.86 | no: Calmar | 7.d (3), 7.g (4) |
| 25 | 017-01.g2.d1.d1.d1 settlement-shock-extending-crowded-run | 7.d | confirmed +7.87 | no: Calmar | 7.d (3), 7.g (5) |
| 26 | 017-01.g2.d1.d1.d2 convex-post-settlement-shock-reversal | 7.d | inconclusive +8.41 | no: Calmar | 7.b (2), 7.g (3) |
| 27 | 017-01.g2.d1.d1.d3 settlement-reversal-in-raised-volatility | 7.d | confirmed +9.48 | no: Calmar | 7.d (2), 7.g (3) |
| 28 | 017-01.g2.d1.d1.g1 weekend-post-settlement-shock-reversal | 7.g | confirmed +7.37 | no: Calmar | 7.d (2), 7.g (3) |
| 29 | 017-01.g2.d1.d1.g2 high-volatility-hourly-shock-reversal | 7.g | confirmed +5.16 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.d (1), 7.g (3) |
| 30 | 017-01.g2.d1.d1.g3 quiet-market-hourly-breakout-continuation | 7.g | rejected -2.30 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.c (2), 7.g (3) |
| 31 | 017-01.g2.d1.d1.g4 second-day-giveback-after-settlement-fade | 7.g | confirmed +5.20 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.d (2), 7.g (2) |

Generation of the ideas tested, in order: 0 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 4 4 4 4 4 4 4. Branches (idea and its first child): 6; the most tested: 11 of 31.

### Session 4, absorption (brief 030, 1d, new)

| # | Idea (lineage code, name) | Made by | Step 5 | Step 6 | Step 7 lines called (ideas written) |
|---|---|---|---|---|---|
| 1 | 030-01 absorption-close-high-rises | brief | inconclusive -0.39 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.g (2) |
| 2 | 030-02 absorption-close-low-falls | brief | inconclusive -0.66 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.g (2) |
| 3 | 030-03 heavy-flat-high-close-reverses | brief | inconclusive -0.94 | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.b (1), 7.g (2) |
| 4 | 030-04 heavy-flat-low-close-reverses | brief | mismatch | no: Sharpe, Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.g (2) |
| 5 | 030-03.b1 heavy-volume-high-close-continuation | 7.b | inconclusive -0.57 | no: Calmar | 7.b (2), 7.g (3) |
| 6 | 030-03.b1.b1 volume-surge-precedes-rise | 7.b | confirmed +3.26 | no: Calmar | 7.d (2), 7.g (3) |
| 7 | 030-03.b1.b2 heavy-low-close-next-day-rebound | 7.b | confirmed +4.23 | no: Calmar | 7.d (1), 7.g (4) |
| 8 | 030-03.b1.b1.d1 heavy-volume-low-close-rebound | 7.d | confirmed +2.59 | no: Calmar | 7.d (2), 7.g (2) |
| 9 | 030-03.b1.b2.d1 heavy-volume-bottom-close-rebound | 7.d | confirmed +4.83 | **pays** | 7.g (3) |
| 10 | 030-03.b1.b1.d2 volume-surge-next-day-rise | 7.d | confirmed +4.70 | no: Calmar | 7.d (2), 7.g (2) |
| 11 | 030-03.b1.b1.d2.d1 volume-surge-after-falling-day | 7.d | confirmed +4.88 | no: Calmar | 7.d (2), 7.g (2) |
| 12 | 030-03.b1.b1.d2.d2 absorbed-selling-low-close | 7.d | confirmed +5.99 | no: Calmar | 7.d (2), 7.g (2) |
| 13 | 030-03.b1.b1.d2.d2.d1 extreme-surge-low-close-rise | 7.d | confirmed +2.47 | no: Calmar | 7.d (2), 7.g (2) |
| 14 | 030-03.b1.b1.d2.d2.d2 absorption-in-volatile-markets | 7.d | confirmed +6.17 | no: Calmar | 7.d (2), 7.g (4) |
| 15 | 030-03.b1.b1.d2.d2.d2.d1 absorbed-selling-on-down-days | 7.d | not finished | | |
| 16 | 030-03.b1.b1.d2.d2.d2.d2 strong-absorption-down-days-any-trend | 7.d | not finished | | |
| 17 | 030-03.b1.b1.d2.d1.d1 absorption-rebound-in-stressed-markets | 7.d | confirmed +5.00 | no: Calmar | - |
| 18 | 030-03.b1.b1.d2.d1.d2 absorption-rebound-after-declines | 7.d | confirmed +3.30 | no: Sharpe minus holding's Sharpe, Calmar | 7.d (3), 7.g (2) |
| 19 | 030-03.b1.b1.d2.d2.d1.d1 absorbed-selling-two-day-rise | 7.d | not finished | | |
| 20 | 030-03.b1.b1.d2.d2.d1.d2 close-at-low-grades-surge | 7.d | not finished | | |
| 21 | 030-03.b1.b1.d2.g1 heavy-volume-selloff-next-day-rebound | 7.g | confirmed +4.40 | **pays** | 7.g (3) |
| 22 | 030-03.b1.b1.d2.g2 heavy-volume-low-close-reversal | 7.g | confirmed +6.23 | no: Calmar | 7.d (3), 7.g (3) |
| 23 | 030-03.b1.b1.d2.d2.g1 volatility-scaled-fall-next-day-rebound | 7.g | confirmed +4.44 | no: Calmar | 7.d (2), 7.g (1) |
| 24 | 030-03.b1.b1.d2.d1.d2.d1 volume-graded-absorption-rebound | 7.d | not finished | | |
| 25 | 030-03.b1.b1.d2.d1.d2.d2 heavy-volume-fall-next-day-rebound | 7.d | not finished | | |
| 26 | 030-03.b1.b1.d2.d1.d2.d3 one-day-absorption-rebound-fades | 7.d | not finished | | |
| 27 | 030-03.b1.b1.d2.d2.g2 low-close-rebound-in-volatility | 7.g | confirmed +5.64 | no: Calmar | 7.d (2), 7.g (2) |
| 28 | 030-03.b1.b1.d2.d2.d2.g1 wide-range-low-close-rebound | 7.g | - | - | - |
| 29 | 030-03.b1.b1.d2.d2.d2.g2 volatile-regime-one-day-reversal | 7.g | not finished | | |
| 30 | 030-03.b1.b1.d2.d2.d2.g3 volatile-high-close-next-day-fall | 7.g | not finished | | |
| 31 | 030-03.b1.b1.d2.d2.d2.g4 calm-regime-low-close-continuation | 7.g | not finished | | |
| 32 | 030-03.b1.b1.d2.d2.g2.d1 strong-low-close-volatility-only | 7.d | not finished | | |
| 33 | 030-03.b1.b1.d2.d2.g2.d2 joint-low-close-high-volatility-rebound | 7.d | not finished | | |
| 34 | 030-03.b1.b1.d2.d1.g1 volatile-regime-fall-rebound | 7.g | confirmed +5.43 | no: Calmar | 7.d (2), 7.g (3) |
| 35 | 030-03.b1.b1.d2.d1.g2 five-day-rise-continues | 7.g | confirmed +2.82 | no: Calmar | 7.d (3), 7.g (3) |
| 36 | 030-03.b1.b1.d2.g1.g1 heavy-fall-closing-at-low | 7.g | confirmed +4.16 | no: Calmar | 7.g (3) |
| 37 | 030-03.b1.b1.d2.g1.g2 weekend-heavy-volume-selloff-rebound | 7.g | inconclusive +1.94 | no: Calmar | - |
| 38 | 030-03.b1.b1.d2.g1.g3 no-wick-heavy-fall-rebound | 7.g | inconclusive +5.40 | no: Calmar | 7.b (2) |

Generation of the ideas tested, in order: 0 0 0 0 1 2 2 3 3 3 4 4 5 5 6 6 5 5 6 6 4 4 5 6 6 6 5 6 6 6 6 6 6 5 5 5 5 5. Branches (idea and its first child): 5; the most tested: 34 of 38.

### Session 5, weekend rise reverses Monday (brief 011, 1d)

| # | Idea (lineage code, name) | Made by | Step 5 | Step 6 | Step 7 lines called (ideas written) |
|---|---|---|---|---|---|
| 1 | 011-01.b2.b1 sunday-move-reverses-both-ways | 7.b | confirmed +5.72 | no: Calmar | 7.d (2), 7.g (3) |
| 2 | 011-01.b2.b2 weekend-fall-rebounds-monday-tuesday | 7.b | inconclusive -0.55 | no: Sharpe minus holding's Sharpe, Calmar | 7.b (1), 7.g (2) |
| 3 | 011-01.b2.b2.b1 weekend-fall-three-day-rebound | 7.b | confirmed +4.68 | no: Calmar | 7.d (3), 7.g (1) |
| 4 | 011-01.b2.b1.d1 weekend-reversal-in-rising-volatility | 7.d | confirmed +5.46 | **pays** | 7.g (3) |
| 5 | 011-01.b2.b1.d2 volatility-graded-weekend-reversal | 7.d | confirmed +6.18 | no: Calmar | 7.d (2), 7.g (2) |
| 6 | 011-01.b2.b2.b1.d1 weekend-fall-rebound-volatile | 7.d | confirmed +4.34 | no: Calmar | 7.d (2), 7.g (1) |
| 7 | 011-01.b2.b2.b1.d1.d1 weekend-fall-rebound-in-downtrend | 7.d | confirmed +4.84 | no: Calmar | - |
| 8 | 011-01.b2.b2.b1.d1.d2 agitated-downtrend-weekend-rebound | 7.d | confirmed +5.88 | no: Calmar | - |
| 9 | 011-01.b2.b2.b1.d1.g1 thin-weekend-sunday-move-reverses | 7.g | inconclusive +6.58 | no: Calmar | 7.b (1) |
| 10 | 011-01.b2.b2.b1.d1.d1.g1 volatile-weekend-fall-rebound | 7.g | not finished | | |
| 11 | 011-01.b2.b2.b1.d1.d1.g2 weekend-rally-fades-downtrend | 7.g | not finished | | |
| 12 | 011-01.b2.b2.b1.d2 weekend-fall-after-decline | 7.d | confirmed +4.84 | no: Calmar | 7.d (3), 7.g (2) |
| 13 | 011-01.b2.b2.b1.d2.d1 weekend-fall-below-average | 7.d | confirmed +4.12 | no: Sharpe minus holding's Sharpe, Calmar | 7.d (4), 7.g (3) |
| 14 | 011-01.b2.b2.b1.d2.d2 weekend-fall-in-vol-units | 7.d | confirmed +4.95 | no: Calmar | 7.d (2), 7.g (3) |
| 15 | 011-01.b2.b2.b1.d2.d3 weekend-fall-in-turbulence | 7.d | inconclusive +1.57 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Lowest Sharpe, one window left out, Calmar | 7.g (2) |
| 16 | 011-01.b2.b2.b1.d2.d1.d1 weekend-fall-size-rebound | 7.d | not finished | | |
| 17 | 011-01.b2.b2.b1.d2.g1 volatile-weekend-fall-rebound | 7.g | confirmed +3.58 | no: Calmar | 7.g (1) |
| 18 | 011-01.b2.b2.b1.d2.g2 weekend-rise-fades-early-week | 7.g | inconclusive +3.56 | no: Sharpe minus holding's Sharpe, Mean daily return, on days in a position, Calmar | 7.b (2), 7.g (2) |
| 19 | 011-01.b2.b2.b1.d3 large-weekend-fall-rebound | 7.d | inconclusive +3.65 | no: Sharpe minus holding's Sharpe, Calmar | 7.b (2), 7.g (3) |
| 20 | 011-01.b2.b2.b1.d3.b1 turbulent-weekend-fall-rebound | 7.b | confirmed +4.83 | **pays** | 7.g (2) |
| 21 | 011-01.b2.b2.b1.d3.b2 percent-weekend-fall-rebound | 7.b | confirmed +4.88 | no: Calmar | 7.d (2), 7.g (3) |
| 22 | 011-01.b2.b1.g1 sunday-reversal-in-turbulence | 7.g | confirmed +6.91 | no: Calmar | 7.d (1), 7.g (3) |
| 23 | 011-01.b2.b2.g1 thin-sunday-rise-reverses | 7.g | confirmed +6.95 | no: Sharpe minus holding's Sharpe, Calmar | 7.d (3), 7.g (4) |

Generation of the ideas tested, in order: 2 2 3 3 3 4 5 5 5 6 6 4 5 5 5 6 5 5 4 5 5 3 3. Branches (idea and its first child): 1; the most tested: 23 of 23.
