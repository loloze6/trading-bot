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

## Reading (2026-11-20, 19:26 Paris; the run took 24 minutes on the faster engine)

| | 6 coins (`std_time_pilot_run`) | 19 coins (`more_coins_1h_run`) |
|---|---|---|
| Step 5 | confirmed | confirmed |
| Sharpe / beats holding by / Calmar | 1.175 / 0.62 / 0.694 | 0.921 / 0.31 / 0.486 |
| Step 6 | not profitable enough (Calmar) | not profitable enough (Calmar) |
| Move per bet over 24 bars / round trip | 56 / 21 bps | 60 / 23 bps |
| Market's share of the gain | 27 % | 34 % |
| Coins earning (Sharpe above 0) | 6 of 6 | **19 of 19** (0.19 to 1.45) |
| Deepest fall | 35.6 %, windows 12 to 16 (end of fold B into fold C), worst window 14 | 35.3 %, the same windows, worst window 14 |
| Yearly return | 24.7 % | 17.1 % |

**Outcome M2.** The edge travels: every one of the 13 new coins earns, and the move per bet is the same size. But the
deepest fall is the same 35 % over the same stretch (end of fold B into fold C). The coins fall together there, so spreading over more of
them does not shrink it. The new coins earn less each, so the yearly return falls, and Calmar falls with it.

**What it shows.** More coins is not the lever for this idea: its weak point is one market-wide stretch, not one coin.
The idea buys an evening fall in volatile times to sell 24 hours later. In that long decline the falls keep
falling. A practitioner would read that stretch first (does the idea lose on most of its bets there, or on a few large
ones?). Then a version that knows the market's direction would be **a new idea for step 7**, not a tuning of this one
(for example: rebounds only while the coin's longer trend is not down). Candidate E ("more coins early") is not
supported by this run.
