# Run brief: volatile evening-fall on more coins (2026-11-20, written before the run)

**Purpose:** the one hourly idea written for hourly bars with a real edge, 016-03.g1.d2 volatile evening-fall rebound,
fails step 6 only on Calmar (0.694 against 0.75) on 6 coins. Its move after the bot can act is 2.6 times a round trip,
27 % of its gain is the market's (`runs/HOLD2_AND_PILOT_RUN.md`, step back). Two of the three paying hourly books are
"more coins" versions. Does the same idea on 19 coins pass step 6? This is step 7.b's standard move (an idea on more
data), not a change to the idea: the plan is the same, only its coins (the 19 of the paying "more coins" hourly books).

**How:** run `more_coins_1h_run`, the plan `...d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h`
(its idea text and config unchanged; the holding period of 24 bars, corrected rule; the engine with speed changes A to
D, `7826ad81`). Steps 4, 5 (the idea's saved measure: no model call), 6, and the unseen dates if it passes. About 20 to
25 minutes.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| M1. Passes | step 6 profitable enough (Calmar ≥ 0.75), step 5 confirmed; half or more of the 19 coins earn | spreading the bets lowers the deepest fall, as on the other "more coins" books: the first hourly-native idea that pays; next, its unseen dates and candidate E (more coins early for hourly ideas with a real edge) |
| M2. The edge holds, the fall does not shrink enough | Sharpe and the market's share near the 6-coin book's, Calmar still under 0.75 | the deepest fall is common to the coins (one market-wide event); read which window makes it before anything else |
| M3. The edge thins | Sharpe falls clearly, few of the 13 new coins earn | the evening rebound is a feature of the larger coins only; the idea does not travel |

**Already known:** the 6-coin book with the corrected rule and the `standardise` pilot: Sharpe 1.175, beats holding by
0.62, Calmar 0.694 (`std_time_pilot_run`).
