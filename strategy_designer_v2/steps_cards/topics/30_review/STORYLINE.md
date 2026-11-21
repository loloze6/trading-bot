# Making hourly ideas pay: the story so far (2026-11-19 to 20)

The operator's objective: "if an idea pays on daily bars, the same kind of idea can pay on hourly bars; prove it and make
the workflow find such ideas." The story is told in four threads. Each step gives what we saw, then **every candidate
cause or option that was on the table**: which one was taken, and why each other one was left, rejected or parked.
Detail lives in the run files and topic cards linked.

Decision words: **taken** (acted on), **confirmed / not a cause** (measured), **rejected** (decided against, with the
reason), **parked** (kept for later, a topic card), **open** (not decided).

## Thread 1. Why the hourly books did not pay (the research question)

**1.1 Seen:** 39 new hourly ideas, 22 confirmed by step 5, 0 profitable books (topic 30's review, code only).
| Candidate cause | Finding (counts) | Decision |
|---|---|---|
| A. Cost-bound: the edge per trade is below its cost | New hourly ideas earn 2 bps per unit traded before costs, a unit costs 10 bps (slow_1h_run); intraday ones 0.3 to 4.6 against 5.7 to 10.6 | **Confirmed: the main cause** (→ 1.2) |
| B. The edge does not reach the book (step 3's config does not trade the effect) | 7 of 8 confirmed books earn before costs | Not a cause |
| C. Search-bound: select_next follows confirmations | Line 7.g kept succeeding (21 ideas tested, many confirmed, none profitable); line 7.d's 80 ideas never tested | **Confirmed: a second cause** (→ thread 2) |
| D. Weak briefs | Brief ideas confirmed as often on 1h as on daily bars (2 of 13 against 6 of 37) | Not a cause |
| E. Bad luck | At the daily rate, 0 of 22 has a 1.3 % chance | Not a cause |
| F. Step 6's values set on daily bars | All 39 books have a Sharpe below 0 after costs; no value would pass them | Not a cause |
| (Close hourly research) | – | **Rejected** by the operator: what pays on 1d can pay on 1h; the outcome is what to change |

**1.2 Seen:** cost-bound. Why do the books trade so much?
| Candidate cause or fix | Finding | Decision |
|---|---|---|
| A bet is not held for the idea's horizon (a 24-hour idea re-sized every hour); step 3 dropped the holding period | Replay of d_line_1h_run's books with a hold of the horizon: net positive for 6 of 7 | **Taken:** a holding period in the engine (thread 3) |
| A wider trade band (`min_allocation_change`) | It only filters small changes, and pays the full change when it passes (operator) | Rejected |
| A hold chosen from the data | It would collect the market's drift | Rejected (the horizon is the idea's own) |
| Hold longer than the horizon to gain more | Bets on a trending market (operator) | Rejected |

**1.3 Seen:** with each bet held, long-horizon books from negative to positive Sharpe (7 of 8), but 0 pass step 6, and
short-horizon ideas unchanged (`HOLDING_NIGHT_RUN`). Why does a real idea still not pay? (operator: "identified too late,
closed too late, or...?"; topic 34; measured by the book's diagnosis)
| Candidate cause | Finding | Decision |
|---|---|---|
| The move is too small for a round trip | Ideas of 1 to 4 bars capture 4 to 13 bps once the bot can act; a round trip costs about 21 bps | **Confirmed** for short horizons (→ thread 2, 2.5) |
| Identified too late (the move happens before the bot can act) | On continuation ideas part of the move is on the signal's bar (grinding +69 bps); on reversals that bar is the trigger, not lateness | Partly: continuation ideas only |
| Closed too late (the move reverses before the book closes) | Short ideas peak at their horizon; the book stays in after its bets 12 to 75 % of its time, but those positions are tiny leftovers (thread 3.4) | Not a cause |
| The gain is the market's rise (trend) | grinding-rises 73 % market; deep-decline and fresh-drop: their bets lose against the drift, their small gain is all market | **Confirmed** for these books; step 6's "beats holding" already catches it |
| The deepest fall too large (Calmar) | volatile evening-fall: a real edge (move 2.6 times a trip, 27 % market), Calmar 0.69 against 0.75 on 6 coins | **Confirmed** for this book (→ 1.5) |

**1.4 Seen:** could the forecast or the position be mis-scaled on hourly bars? (operator: settings counted in bars,
topic 36)
| Candidate | Finding | Decision |
|---|---|---|
| The sizing's volatility window | Already set in time (60 days); volatility makes 0.0 to 0.2 % of the position's movement | Not a cause |
| The `standardise` window (2.5 to 21 days on 1h) | Pilot at 60 days: Sharpe +0.00 to +0.07; replay from 3 days to 1 year: flat | Not a cause |
| The other bar-counted settings (regime windows, `min_periods`, the band's effect on 24 bars a day) | Not measured | **Parked** (topic 36, option C) |
| A lower Calmar threshold for 1h | A patch for one timeframe | Rejected |

**1.5 Seen:** which hourly books pay, and how can the near-miss pass?
| Candidate lever | Finding | Decision |
|---|---|---|
| (Seen) 3 hourly books pay: daily ideas with horizons of days, about as well as on daily bars; move 1.8 to 10.6 times a trip; about half their gain timing; 2 of 3 are "more coins" versions | – | – |
| The near-miss (volatile evening-fall) on more coins (step 7.b): spreading over 19 coins lowers the deepest fall | Run (`MORE_COINS_1H_RUN`, 24 min on the faster engine): the edge travels (19 of 19 coins earn, the same move per bet), but the deepest fall is the same 35 % over the same market-wide stretch, and Calmar falls to 0.49 | **Taken, not the lever.** Next for this idea: read that stretch; a version that knows the market's direction is a new idea for step 7 |
| Close the leftover positions below the band | Replay: +0.01 Sharpe | Rejected (not a lever) |
| A longer horizon (its move peaks just after its 24 bars) | The horizon is the idea's own, not chosen from the data | Rejected as a tuning; a longer-horizon idea is a new idea for step 7 |
| A horizon in price, not only in time | – | **Parked** (topic 35) |

**Answer so far:** the premise holds: a daily idea held for its horizon pays on hourly bars. The ideas written for hourly
bars mostly predict moves too small to pay for their trades, or their gain is the market's.

## Thread 2. Why the workflow did not find or fix it by itself (the process)

**2.1 Seen:** the cost problem was known inside the workflow but not acted on.
| Candidate cause | Finding | Decision |
|---|---|---|
| Step 7's analysts did not see it | They did: line 7.d named costs in 38 of 39 analyses, with the numbers, and wrote 80 ideas aimed at larger moves | Not a cause |
| select_next did not test 7.d's ideas: it counted a confirmed idea as a success, and on 1h confirmations are cheap (a 0.10 % move reaches t 9) | 7.g's record 0.80, none profitable; 7.d's ideas never picked | **Confirmed** (→ 2.2) |

**2.2 Fix for select_next:**
| Option | Finding | Decision |
|---|---|---|
| A success is a profitable book (step 6), not a confirmation (change 1) | Rankings redone: 7.d's ideas move up | **Taken, merged** |
| A higher t threshold for 1h | It holds no cost: a 0.10 % effect at t 50 would pass and lose | Rejected |
| Fewer folds on 1h | Less reliable (topic 31) | Rejected |
| How select_next weighs a line (7.b came before 7.d) | – | **Parked** (topic 32) |

**2.3 Test 7.d's waiting ideas (change 2):** `D_LINE_1H_RUN`, 8 of 17: 0 pay. Cause: step 3 drops the holding period, and
the engine could not hold (→ 2.4). Stopped at 8 (the other 9 would meet the same gap). Its 7 plans were rerun with the
hold (`HOLDING_NIGHT_RUN`, set 1).

**2.4 Step 3 dropped the idea's holding period:**
| Option | Decision |
|---|---|
| Step 3's code sets `min_holding_bars` from the plan's horizon line; "a holding period dropped" removed from its allowed adaptations | **Taken, kept** on the working branch |
| Let the model set it | Rejected: the horizon line is already there; code reads it the same way every time |

**2.5 Ideas proposed with moves smaller than a trip** (thread 1.3): steps 2 and 7 do not know the cost of a trade.
| Option | Decision |
|---|---|
| A definition: an idea predicts a move worth several round trips once the bot can act (`common/idea_definition.md`, read by steps 2 and 7) | **Open** (topic 34, option A; candidate B below) |
| A minimum horizon on hourly bars | Rejected: a limit for one timeframe; a short idea with a large move would be refused |

**2.6 Why a confirmed idea does not pay is not shown to the analysts in numbers:**
| Option | Decision |
|---|---|
| The book's diagnosis (size, opening, closing, holding past the bets, trend) read by step 7's analysts | **Decided long term** (operator); built in a temporary place; step 7's design to do (candidate C) |
| A separate observe-and-advise stage (topic 08) | Superseded by the operator's decision that the analysts read it |
| An informational check in step 6 | Rejected (operator): step 6 is pass or fail on profitability |

**2.7 New: step 5 confirmed 2 ideas whose bets lose** (deep-decline, fresh-drop): step 5's measure and the move the book
captures disagree. **Open** (candidate D).

## Thread 3. The holding rule in the engine (building it right)

**3.1 Which holding rule?**
| Option | Finding | Decision |
|---|---|---|
| The block: no trade for N bars after a trade | A repeated signal did not renew it, a close started a hold: deviated from the definition | Rejected after its run (`D_LINE_1H_V2_RUN`) |
| Its variant (a hold starts on a trade that leaves a position) | Still not the definition | Rejected |
| Option 2: each rise of the forecast is a bet held for the horizon (operator) | Respects the forecast's size at the bet | **Taken** |
| Tranches (each bar buys 1/N of the target, so the position is the average of the last N targets) | Does not respect the forecast's size at the bet (operator) | Rejected |

**3.2 Option 2 checked case by case (operator):** 11 cases written from the definition, replayed against the engine.
| Defect found | Fix | Decision |
|---|---|---|
| A long target drifting down with volatility counted as a short bet: old shorts held against the forecast (up to 50 % of the time on two-sided books) | A bet is a rise of the forecast itself (operator) | **Taken** |
| A flat bar at each side switch (the floor floored at 0 with nothing held) | The floor only while a bet is held | **Taken** |
| Noise rises counted as bets | A bet needs a rise of at least the trade band (operator) | **Taken** |
Built as one module, `core/holding_period.py`, 13 cases as tests, identical files without the setting: **kept** on the
working branch. Two "positive" hourly books from the defect set aside; the paying books rerun: 9 of 10 stay paying.

**3.3 Leftover positions below the trade band:**
| Option | Decision |
|---|---|
| Let a close to 0 always pass the band | Rejected: replay +0.01 Sharpe |
| Leave the band as it is | **Taken** |

## Thread 4. Running the work (infrastructure)

**4.1 Runs cut by the 2-hour limit of a cloud background task:**
| Option | Decision |
|---|---|
| Raise the limit | Not possible from the session (I do not know whether a setting exists) |
| Relaunch automatically after a cut | Rejected: the harness asks not to restart a task stopped at its longest timeout without the person's go; the session first recorded it as allowed by mistake, then corrected |
| Resumable scripts, relaunch on the operator's go | **Taken** |
| The operator's own machine (CLI) for long runs | **Parked** (topic 37, option B) |
| Several cloud sessions side by side | **Taken, tested:** 9 books in 72 minutes instead of about 149 (topic 37, option D) |

**4.2 Hourly backtests take 10 to 60 minutes (topic 33):**
| Option | Decision |
|---|---|
| Speed changes A to D (bootstrap thrown away; volatility recomputed; coins in two waves; pandas glue), each proven by identical files | **Taken:** waits for the operator's go in the speed session |
| A shorter warm-up (about 20 % saved; it can change results) | Not now: its own decision after A to D (operator: only if far too long; it is about 1.8 times what is needed) |
| More cores | Open: not found in the environment's settings |
| Fewer coins, folds or windows; sampling bars | Rejected as speed changes: they change the research (`orchestration/duration/10_round2_brief.md`) |

**4.3 Cheaper answers before backtests:**
| Option | Decision |
|---|---|
| Replays from the bar files ("what if" in seconds, where the recorded columns allow) | Used as review tools; not a step |
| Rerun only the books whose step 6 could change | Used once (6 to 7 hours down to about 3.5); not written into a card |

## Candidate lasting changes to the workflow
| # | Change | Where | From | State |
|---|---|---|---|---|
| A | The holding period for every plan | engine, step 3 | 1.2, 2.4, 3.1, 3.2 | Built and proven on the working branch; master waits for the operator's go |
| B | An idea predicts a move worth several round trips once the bot can act | `common/idea_definition.md`, steps 2 and 7 | 1.3, 2.5 | Topic 34: to design |
| C | Step 7's analysts read the book's diagnosis | step 7 | 2.6 | Decided long term; to design |
| D | Step 5's measure agrees with the move the book captures | step 5, `common/measures.md` | 2.7 | Open |
| E | An hourly idea with a real edge goes to more coins early | step 7, select_next | 1.5 | Tested once: not supported (the fall was market-wide) |
| F | Longer-horizon ideas when a move outlasts its horizon; a horizon in price | step 7; topic 35 | 1.5 | Open, parked |
| G | Faster engine, parallel sessions, the CLI, "rerun only what can change", replays before backtests | engine, orchestration | thread 4 | Topics 33, 37 |

## Links
Runs: `runs/D_LINE_1H_RUN.md`, `runs/D_LINE_1H_V2_RUN.md`, `runs/HOLDING_NIGHT_RUN.md`, `runs/HOLD2_AND_PILOT_RUN.md`.
Topics: 08, 30 (umbrella), 31, 32, 33, 34, 35, 36, 37. Code: `trading-bot/core/holding_period.py`,
`topics/34_review/book_diagnosis.py`.
