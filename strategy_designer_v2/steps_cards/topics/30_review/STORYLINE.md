# Making hourly ideas pay: the story so far (2026-11-19 to 20)

The operator's objective: "if an idea pays on daily bars, the same kind of idea can pay on hourly bars; prove it and make
the workflow find such ideas." The story is told in four separate threads, each a chain: what we saw, its root cause,
what we did, what it gave, and whether the change is kept. Detail lives in the run files and topic cards linked.

## Thread 1. Why the hourly books did not pay (the research question)
| # | Seen | Root cause | What we did | Result | Change |
|---|---|---|---|---|---|
| 1.1 | Hourly ideas confirmed by step 5, but 0 of 22 books profitable | **Profit eaten by costs:** the books earned 0.3 to 4.6 bps per unit traded, a unit costs about 10 bps | Frictionless replay of the books (topic 30) | The ideas' effects are real; the books trade too much | – |
| 1.2 | They trade too much | **A bet was not held for the idea's horizon:** a 24-hour idea re-sized every hour | Each bet held for its horizon (the operator's option 2; thread 3) | Long-horizon books from negative to positive Sharpe (7 of 8); 0 pass step 6 (`HOLDING_NIGHT_RUN`) | Kept (thread 3) |
| 1.3 | Still 0 pass, short-horizon ideas unchanged | **The move is smaller than a round trip:** ideas of 1 to 4 bars capture 4 to 13 bps once the bot can act, a round trip costs about 21 | The book's diagnosis (topic 34): move after the bot can act against a round trip, opening time, closing time, holding past the bets, trend | No holding can make them pay | Diagnosis built (temporary place) |
| 1.4 | Long-horizon books positive but failing step 6 | **Their gain is the market's, or their deepest fall too large:** grinding-rises 73 % market; deep-decline and fresh-drop bets lose against the drift; volatile evening-fall a real edge (27 % market) but Calmar 0.69 on 6 coins | Diagnosis per book; daily twins compared | – | – |
| 1.5 | Could the forecast be mis-scaled on hourly bars? (operator) | Settings counted in bars carried from daily bars (topic 36) | `standardise` at 60 days (pilot), replay of the window from 3 days to 1 year | **Not a cause:** Sharpe +0.00 to +0.07, flat | Nothing changed |
| 1.6 | Which hourly books do pay? | – | Rerun of the paying books with the hold; diagnosis | **3 hourly books pay**, all daily ideas with horizons of days, about as well as on daily bars. Their move is 1.8 to 10.6 times a trip, about half their gain is timing, two are "more coins" versions | – |
| 1.7 | The one hourly-native real edge fails only Calmar | A deepest fall on 6 coins | Next: the same idea on 19 coins (step 7.b) | Waits for the engine's speed change B (3 h today, about 30 min after) | – |

**Answer so far:** the premise holds (a daily idea held for its horizon pays on hourly bars). Ideas written for hourly
bars mostly predict moves too small to pay for their trades.

## Thread 2. Why the workflow did not find or fix it by itself (the process)
| # | Seen | Root cause | What we did | Change |
|---|---|---|---|---|
| 2.1 | "Profit eaten by costs" was never acted on by step 7 | **Step 7's analysts do not see why a confirmed idea does not pay:** they read the backtest, not a cost or timing reading | The book's diagnosis (thread 1.3) | Long term part of step 7's analysts (operator); design to do (C below) |
| 2.2 | The loop kept following confirmed but non-paying lines | **select_next counted a confirmed idea as a success**, so cheap confirmations scored high | A success is a profitable book (topic 30, change 1) | **Kept, merged** |
| 2.3 | 7.d's 80 ideas were never tested | How select_next weighs a step 7 line (7.b before 7.d) | – | Topic 32, parked |
| 2.4 | Plans dropped the idea's holding period | **Step 3 was allowed to drop it** ("a holding period dropped" among its adaptations), and the engine had no way to hold | Step 3's code sets `min_holding_bars` from the plan's horizon; the adaptation removed | **Kept** on the working branch |
| 2.5 | Ideas proposed with moves smaller than a trip | **Steps 2 and 7 do not know the cost of a trade** | – | Topic 34, option A: to design (B below) |
| 2.6 | Step 5 confirmed 2 ideas whose bets lose (deep-decline, fresh-drop) | **Step 5's measure and the book's bets disagree** (what step 5 measures is not the move the book captures) | – | New: to look at (D below) |

## Thread 3. The holding rule in the engine (building it right)
| # | Seen | Root cause | What we did | Change |
|---|---|---|---|---|
| 3.1 | First version (the block: no trade for N bars) | Deviated from the definition: a repeated signal did not renew, a close started a hold | Variant, then the operator's option 2: each rise of the forecast is a bet held for the horizon | Superseded |
| 3.2 | Option 2 checked case by case (operator) | **3 defects:** (a) a long target drifting down with volatility counted as a short bet, holding old shorts against the forecast, up to 50 % of the time on two-sided books; (b) a flat bar at each side switch; (c) noise rises counted as bets | 11 cases from the definition; corrected rule: a bet is a rise of the forecast itself of at least the trade band; the hold only while a bet is held | **Kept** on the working branch: `core/holding_period.py`, 13 cases as tests, identical files without the setting |
| 3.3 | Two "positive" hourly books came from defect (a) | – | Their results set aside; the paying books rerun on the corrected rule: 9 of 10 stay paying | – |
| 3.4 | Leftover positions below the trade band | The band refuses closing them (as before the hold) | Replay: closing them adds +0.01 Sharpe | Not a lever: nothing changed |

## Thread 4. Running the work (infrastructure)
| # | Seen | Root cause | What we did | Change |
|---|---|---|---|---|
| 4.1 | Runs cut during the night | A cloud background task stops after 2 h, and a restart stops it; a cut backtest restarts from zero | Resumable scripts; relaunch only on the operator's go | Topic 37 |
| 4.2 | One hourly backtest takes 10 to 60 minutes | The engine's per-bar cost (measured: bootstrap thrown away, volatility recomputed, coins in two waves, pandas glue) | Speed session: 4 changes A to D, proven by identical files | Topic 33: waits for the operator's go there |
| 4.3 | Several books to rerun | One machine, 4 cores | Parallel cloud sessions: 9 books in 72 minutes instead of about 149 | Topic 37, option D: works |
| 4.4 | "What if" questions cost an hour of backtest | – | Replays from the bar files, seconds per book, where the recorded columns allow | Review tools, not a step yet |
| 4.5 | Reruns after an engine change | Everything was rerun | Rerun only the books whose step 6 could change: 6 to 7 hours down to about 3.5 | A rule used once, not written into a card |

## Candidate lasting changes to the workflow
| # | Change | Where | From | State |
|---|---|---|---|---|
| A | The holding period for every plan | engine, step 3 | 1.2, 2.4, 3.2 | Built and proven on the working branch; master waits for the operator's go |
| B | An idea predicts a move worth several round trips once the bot can act | `common/idea_definition.md`, steps 2 and 7 | 1.3, 2.5 | Topic 34, option A: to design |
| C | Step 7's analysts read the book's diagnosis | step 7 | 2.1 | Decided long term; to design |
| D | Step 5's measure agrees with the move the book captures | step 5, `common/measures.md` | 2.6 | New: to look at |
| E | An hourly idea with a real edge goes to more coins early | step 7, select_next | 1.6, 1.7 | To test (next run) |
| F | Longer-horizon versions when a move outlasts its horizon; a horizon in price | step 7; topic 35 | 1.6 | Topic 35 open |
| G | Faster engine, parallel sessions, the CLI for long runs, "rerun only what can change", replays before backtests | engine, orchestration | thread 4 | Topics 33, 37 |

## Links
Runs: `runs/D_LINE_1H_RUN.md`, `runs/D_LINE_1H_V2_RUN.md`, `runs/HOLDING_NIGHT_RUN.md`, `runs/HOLD2_AND_PILOT_RUN.md`.
Topics: 30 (umbrella), 32, 33, 34, 35, 36, 37. Code: `trading-bot/core/holding_period.py`, `common/book_diagnosis.py`.
