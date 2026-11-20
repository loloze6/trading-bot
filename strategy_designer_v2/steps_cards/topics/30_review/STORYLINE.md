# Making hourly ideas pay: the story so far (2026-11-19 to 20)

The operator's objective: "if an idea pays on daily bars, the same kind of idea can pay on hourly bars; prove it and make
the workflow find such ideas." This page puts in order what was asked, found, changed for a test, and kept. It is the
basis for designing the lasting changes to the workflow. Detail lives in the run files and topic cards linked here.

## 1. The story, in order
| # | Question | What we did | What we found | Status of the change |
|---|---|---|---|---|
| 1 | Why do hourly ideas rarely pay? (topic 30) | Critical review of the 1h runs; frictionless replay of their books | The effects were real, but the books traded too often: 0.3 to 4.6 bps earned per unit traded, against about 10 of cost. select_next followed cheap confirmations; 7.d's 80 ideas were never tested | select_next counts only a profitable book as a success: **kept, merged** |
| 2 | Do step 7.d's ideas pay? | `D_LINE_1H_RUN` (8 of 17 ideas) | 0 pay | – |
| 3 | Would holding each bet for its horizon fix it? (topic 30) | A holding period in the engine, in three tries: the block, its variant, then the operator's option 2 (each rise of the forecast is a bet held for the horizon) | The block deviated from the definition; option 2 adopted | Engine setting `min_holding_bars`, set by step 3 from the plan's horizon: **kept on the working branch** |
| 4 | Does option 2 make confirmed hourly ideas pay? (`HOLDING_NIGHT_RUN`) | Sets 1 to 3: 7.d's plans, the 21 confirmed hourly ideas, the 13 paying books | Holding is necessary, not sufficient. Long-horizon books went from negative to positive Sharpe, but none passed step 6. Short-horizon ideas (1 to 4 bars) cannot pay at any holding | – |
| 5 | Why does a real idea not pay? (operator: "identified late, closed late, or trend?"; topic 34) | Readings on the bar files, then a standard diagnosis of a book: big enough, opening time, closing time, holding past the bets, trend | The move left once the bot can act must be well above a round trip (about 21 bps measured). Most hourly-native moves are 4 to 13 bps | `common/book_diagnosis.md` and `.py`: **built, in a temporary place**; long term part of step 7's analysts (operator) |
| 6 | Was option 2 built right? (operator: "check case by case") | 11 cases from the definition, replayed against the engine | 3 defects: (a) a long target drifting down with volatility counted as a short bet, which held old shorts against the forecast (up to 50 % of the time on two-sided books); (b) a flat bar at each side switch; (c) noise rises counted as bets | Corrected rule: a bet is a rise of the forecast itself of at least the trade band; the hold only while a bet is held. In its own module `core/holding_period.py`, 13 cases as tests, proof of identical files without the setting: **kept on the working branch** |
| 7 | Is the hourly forecast mis-scaled? (operator: settings counted in bars; topic 36) | The sizing window checked; a `standardise` pilot at 60 days; a replay of the window from 3 days to 1 year | The sizing was already in time. The `standardise` window is not the lever (Sharpe +0.00 to +0.07; replay flat) | Nothing changed; the list of bar-counted settings stays in topic 36 |
| 8 | Does the corrected rule keep paying books paying? | 10 paying books rerun | 9 of 10 stay paying (Sharpe −0.06 to +0.19 against no hold); the quick 3-day two-sided reversal stops paying | – |
| 9 | Which hourly books pay, and why? (step back) | Diagnosis of paying and non-paying hourly books; daily twins | 3 hourly books pay, all daily ideas with horizons of days, about as well as on daily bars. Their move is 1.8 to 10.6 times a trip, about half of their gain is timing, and the moves outlast their horizon. Hourly-native ideas: one real edge (volatile evening-fall: 2.6 times a trip, 27 % market), which fails only Calmar on 6 coins | Next: that idea on more coins (step 7.b) |
| 10 | Other levers looked at and set aside | Closing leftovers below the band (replay) | +0.01 Sharpe: not a lever | Nothing changed |

**Side findings on the way:** step 5 confirmed two long-horizon ideas (deep-decline, fresh-drop) whose bets lose against
the coin's drift (their small gain is the market's): step 5's measure and the book's bets disagree. A horizon in price,
not only in time, is an open idea (topic 35). The Calmar threshold is kept the same for every timeframe.

## 2. How we ran it (infrastructure learned)
| Finding | Status |
|---|---|
| A cloud background task stops after 2 hours, and a restart stops it too; scripts resume, but a cut backtest restarts from zero | Topic 37. Relaunching after the limit needs the operator's go |
| Several cloud sessions, each on its own machine, ran 9 books in 72 minutes instead of about 149 (`runs/hold2_parts/`) | Topic 37, option D: tested, works |
| Hourly backtests take 10 to 60 minutes; the engine's time is measured and a plan of 4 speed changes made | Topic 33: speed session, waiting for the operator's go there |
| Replays from the bar files answer "what if" questions in seconds, where the recorded columns allow (`30_review/*replay*`, `36_review/book_sim.py`) | Review tools, not a workflow step yet |
| Rerunning only the books whose step 6 could change cut a rerun from 6 or 7 hours to about 3.5 | A rule used once, not written into a card |

## 3. Candidate lasting changes to the workflow
| # | Change | Where | Evidence | State |
|---|---|---|---|---|
| A | The holding period for every plan (step 3 sets it from the horizon) | engine, step 3 | Rows 3, 4, 6, 8: necessary on hourly bars, neutral on paying books | Built and proven on the working branch; merging into master waits for the operator's go |
| B | An idea predicts a move worth several round trips once the bot can act | `common/idea_definition.md`, steps 2 and 7 | Rows 5 and 9: the paying books are 1.8 to 10.6 times; the hourly-native ones under 1 | Topic 34, option A: to design |
| C | The book's diagnosis read by step 7's analysts | step 7 | Rows 5 and 9: it shows why a confirmed idea does not pay (size, timing, trend) | Decided long term (operator); the step 7 design to do |
| D | Step 5's measure agrees with how the book trades (the move from the bar after the signal, net of the drift) | step 5, `common/measures.md` | Side finding: 2 confirmed ideas whose bets lose | New: to look at |
| E | An hourly idea with a real edge goes to more coins early (7.b) | step 7, select_next | Row 9: 2 of the 3 paying hourly books are "more coins" | To test (next run) |
| F | Horizons: longer-horizon versions of ideas whose move outlasts their horizon; a horizon in price | step 7; topic 35 | Row 9: all 3 paying books still rising at twice their horizon | Topic 35 open |
| G | Runs: faster engine, parallel sessions, the CLI for long runs, a "rerun only what can change" rule, replays before backtests | engine, orchestration | Section 2 | Topics 33 and 37 |

## Links
Runs: `runs/D_LINE_1H_RUN.md`, `runs/D_LINE_1H_V2_RUN.md`, `runs/HOLDING_NIGHT_RUN.md`, `runs/HOLD2_AND_PILOT_RUN.md`.
Topics: 30 (umbrella), 33, 34, 35, 36, 37. Code: `trading-bot/core/holding_period.py`, `common/book_diagnosis.py`.
