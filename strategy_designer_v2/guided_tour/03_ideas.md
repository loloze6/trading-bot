# Stop 03 of 10: The ideas step

## Speech (verbatim)

Stop 03 of 10: The ideas step. (After Rectification 1 the tour has stops 00 to 10.) Open on the side: `strategy_designer_v2/steps/ideas/PROMPT.md`, `strategy_designer_v2/steps/ideas/CLAIM_FORMAT.md`, `strategy_designer_v2/runs/real_01_daily_breadth_fold_a/003/claims.yaml`, `strategy_designer_v2/records/claims_tried.yaml` (your brief's list), `strategy_designer_v2/run.py` (`main`, the `already_tried` lines).

### 1. In one sentence
Two instruction pages ask the model to turn the brief into six to twelve distinct ideas, each a claim: plain words, a few lines of code the engine can trade, and a pass number fixed before any data is seen.

### 2. Why it exists
This is where the pipeline's candidates come from. The pass number is written before the backtest, so the idea is judged by its own bar (README scar 3).

### 3. What comes in, what goes out
In, pasted into one prompt (stop 02): `PROMPT.md`, `CLAIM_FORMAT.md`, the whole brief, and, if any, the claims already tried under this brief's file name from `records/claims_tried.yaml` (each with id, belief, branch 1 verdict, branch 3 verdict, run). Out: `claims.yaml` in the run folder.

### 4. What happens here, step by step
`PROMPT.md`: produce 6 to 12 ideas; "distinct" means a different mechanism (a window or threshold change is the same idea); stay inside the brief. Constraints: only open, high, low, close, volume bars unless the brief names more; hourly or daily; a one-line no-lookahead reason; no strategy settings; contradicting ideas kept; calendars in UTC; no repeat of `already_tried`. Method: list what the brief implies, write, reread and strike what cannot be computed or does not test its belief.

`CLAIM_FORMAT.md` fixes the shape of each idea: an id, a one-sentence belief, the claim (when, then, compared to, all in plain words; the horizon in bars; `min_effect`, the pass number; and the code), the no-lookahead line, and one line on how it trades. The code is a few lines of pandas (a Python table library) and must define two things: `event`, the bars where the claim is measured (true or false per bar, may be true everywhere), and `strength`, a signed continuous number on every bar, positive for up, negative for down, its size the size of the belief; no direction field, no plus or minus one. Names already defined: the bars, each bar's return, hour, weekday, a spacing helper. Looking forward is forbidden ("Never `shift(-n)`; the code is refused").

The one measure: the rank correlation (IC) between the engine's graded forecast and the return over the horizon, on event bars, at least `min_effect`. The common rule, which the model must not restate: the same sign in at least 5 of the fold's 6 windows, at least 30 event bars per window group, cost 0.15% per round trip, one coin at a time. A section from try 09, "dense strength", warns that a strength that is zero on most bars saturates (it pins at the engine's cap: an on-off book by another route) and one that is raw noise churns (trades constantly).

Run 003: with 12 claims already tried (run 001 of your brief), the model wrote 8 ideas, from a 3-day reversal to a 60-day skewness tilt; all measure on every bar; horizons 3 to 20 bars; `min_effect` 0.03 or 0.04. Its notes: a weekday idea left out as churn against the 0.15% cost; two contradicting pairs kept on purpose.

Also in the folder: `check_claims.py`, try 01's structural checker. The runner does not call it; it checks fields of the earlier format (`measure`, `pass_if`) the current format lacks.

Live: both pages on every run (`CLAIM_FORMAT.md` also goes to the analyst, stop 08).

### 5. What it costs
Run 003's ideas call: 0.19 USD (`model_calls.yaml`).

### 6. How it stands against the two rules
No bars are read here; the model sees none and writes code the engine runs later. The format asks for a continuous strength in words; `event` is true-or-false but marks only where branch 1 measures, not a position. The format allows a strength that is zero outside events, with the warning that it makes a sparse book. Whether code enforces any of this is stop 04.

### Reading map
| Part | File and section | One line |
|---|---|---|
| The task | `steps/ideas/PROMPT.md`, "What you produce", "What "distinct" means" | 6 to 12 ideas, one mechanism each |
| The limits | `PROMPT.md`, "Constraints", "How to work" | Bars only, no lookahead, no config, no repeats |
| The shape | `steps/ideas/CLAIM_FORMAT.md`, first block | id, belief, claim, why_no_lookahead, how_it_trades |
| The code | `CLAIM_FORMAT.md`, "The code block", "Example" | Defines `event` and `strength` |
| The measure and the rule | `CLAIM_FORMAT.md`, "The one measure", "The common rule" | IC at least `min_effect`; 5 of 6 windows; 0.15% cost |
| Dense strength | `CLAIM_FORMAT.md`, "Dense strength"; last line of `PROMPT.md` | Sparse saturates, noise churns |
| Already tried | `run.py`, `main`; `records/claims_tried.yaml` | Earlier claims of the same brief file |
| The output | `runs/.../003/claims.yaml` | 8 ideas and the model's notes |
| Not called | `steps/ideas/check_claims.py` | Try 01's checker for the earlier format |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> This stop did not allow me to identify if a claim is correctly structured and if the fields inside make sense. Would make a sense for an agent to independantly assess if we are having here a standardized/ open / way to generate trading ideas. Remember an idea in my words is a pattern that can be tested quantitatively, and that would allow us to predict a market behavior. This idea should serve as "thesis" (partially at least) for building a linear trading strategy. 
> Direct : Please try to understand my vision here and rephrase it to confirm your understanding, help me to see clearer

**Guide's direct answer (2026-11-07)**

*Your vision, rephrased (to confirm).* An idea is a pattern in market data that (1) can be computed at a bar's close, (2) says what the market will do next, (3) has a reason to exist, (4) can be tested with numbers against a pass mark fixed beforehand, and (5) gives the thesis of a linear strategy: the stronger the pattern, the larger the position in its direction, with no on-off. Ideas should come out in one standard shape, so that each can be checked field by field, yet stay open to any mechanism inside the brief. You would like an independent agent to assess whether v2's ideas step does that (recorded; not done). From this stop you could not see whether a claim is well formed or whether each field makes sense.

*One claim of run 003, field by field, against those five parts.* Claim `short_horizon_reversal_3d` (`runs/real_01_daily_breadth_fold_a/003/claims.yaml`).

| Part of your idea | Field (`steps/ideas/CLAIM_FORMAT.md`, first block) | Run 003 example | What code does with it |
|---|---|---|---|
| (1) the pattern | `when` (words); `event` in `code` | "every daily bar"; `event` true on every bar | `when`: no code reads it; it reaches the analyst as text (`run.py`, `analyst_extra`). `event`: run in the engine by the component (`trading-bot/strategies/claim_linear.py`, docstring), written to the per-bar output; branch 1 measures on those bars (`steps/judge/judge.py`, the `event` column) |
| (2) what happens next | `then`, `compared_to` (words); `horizon_bars` | "the next 3 days' return leans against the sign and size of the last 3 days' vol-scaled move"; horizon 3 | `then`, `compared_to`: no code reads them; to the analyst as text. `horizon_bars`: branch 1's forward return (`judge.py`), the book summary (`steps/analyst/summarise.py`); passed to the component as `horizon`, "accepted and ignored" (`claim_linear.py`, docstring) |
| (3) why it should exist | `belief` | "moves over a few days overshoot because liquidity providers widen out and late chasers pile in" | No check; kept in `records/claims_tried.yaml` and the shelf (`run.py`, `remember`); sent to the analyst (`run.py`, `analyst_extra`) |
| (4) the test, pass mark fixed before | `min_effect`; the common rule (`CLAIM_FORMAT.md`, "The one measure", "The common rule") | 0.04 | `min_effect` read by branch 1 (`judge.py`). The measure is the same for every claim: rank correlation of the graded forecast with the forward return. The 5-of-6 windows and the 30 event bars are fixed in `judge.py` (`MIN_EVENTS`, `AGREE`), not per claim |
| (5) the linear thesis | `strength` in `code`; `how_it_trades` (words) | strength = minus (3-day return / (60-day volatility × √3)); "positions are graded against the recent 3-day stretch, faded toward the mean and held a few days" | `strength`: the component emits it on every bar; the engine's standardise grades it into the position (`claim_linear.py`; stop 04). `how_it_trades`: no code reads it, and it is not sent to the analyst (`analyst_extra` sends `belief` and `claim` only) |
| no lookahead | `why_no_lookahead` (words) | "the 3-day return and the 60-day volatility use closes at or before the bar's close" | No code reads it; not sent to the analyst. Code with a future shift is refused (`claim_linear.py`, docstring) |

*What checks the structure.* One check in code: `run.py`, `valid`: the idea has an `id` and its claim has `code`, `horizon_bars` and `min_effect`. Nothing in code checks the plain-word fields, or that `then` and `horizon_bars` describe what `strength` computes. `steps/ideas/check_claims.py` is not called (it checks the earlier format).

*Three facts that sit next to your words.*
- "Predict a market behaviour": in the files, the behaviour tested is always the forward return over `horizon_bars`, its sign and rank (`CLAIM_FORMAT.md`, "The one measure"). A claim about another behaviour (volatility, range) has no measure in the format.
- "Thesis, partially at least, for a linear strategy": in v2 the same `strength` series is both what branch 1 tests and what the book trades; the rest of the strategy (sizing, costs, the standardise settings) is set by the engine step, not by the idea (`PROMPT.md`, "Do not design the strategy config"; stop 05).
- "Standardised and open": the shape is fixed in `CLAIM_FORMAT.md`; openness is asked in words (`PROMPT.md`, "What "distinct" means": several points of view, any mechanism inside the brief's scope).

Is this your vision? Correct me where it is off.

> Direct: "Predict a market behaviour" could be too restrictive, no ?. To illustrate my vision, an idea could be "sma diff with price can predict price fluctuation in trending market", "rsi above 20 is a goood indicator to identify trending markets", "a strategy using sma at 200 is closing too late and an ema at 20 compensates with early closing" ... 
> You see ?

**Guide's direct answer (2026-11-07)**

*Your vision, rephrased (to confirm).* An idea is any statement that can be tested with numbers and that helps build a linear strategy, not only a forecast of the next return. Your three examples are three kinds: (a) a signal that predicts how price moves, in a given market state; (b) an indicator that recognises a market state (a trend detector); (c) a design choice inside a strategy (one exit closes too late, another closes earlier). Each is "partly a thesis": (a) is the forecast, (b) tells when to trust a forecast, (c) tells how to trade it.

*What the files can express today, example by example.*

| Your example | Kind | What the format has for it | What the format has no field or measure for |
|---|---|---|---|
| "sma diff with price can predict price fluctuation in trending market" | (a) signal → move, in a state | `strength` = price minus its average, in volatility units; `event` = trending bars; `horizon_bars` (`CLAIM_FORMAT.md`, "The code block") | If "fluctuation" means the size of the move whatever its direction, the one measure (rank correlation of strength with the signed forward return, "The one measure") does not test it. `event` limits where branch 1 measures, not where the book trades: the component emits strength on every bar (`trading-bot/strategies/claim_linear.py`, docstring), unless strength is 0 outside trending bars, which the format calls a sparse book ("Dense strength") |
| "rsi above 20 is a good indicator to identify trending markets" | (b) indicator → state | "RSI above 20" can be written as `event` (true or false per bar) | The thing predicted is a state (trending), not a forward return: no measure. A threshold is on-off: as `strength` it is what the format forbids ("No direction field, no plus or minus one") and README rule 2 rules out. README "Status", "Not built": "a use for validated filters". `records/shelf.yaml` holds entries of `kind: filter` from before the clean-up; the shelf is void |
| "a strategy using sma at 200 is closing too late and an ema at 20 compensates with early closing" | (c) design choice → book behaviour | Nothing: one claim is one `strength` series on one coin; the model is told "Do not design the strategy config" (`PROMPT.md`, "Constraints") | A comparison of two strategies, or a claim about exits: no field, no measure. Branch 3 measures the book's profit (stop 07), and the analyst reads what the book did (`steps/analyst/PROMPT.md`, question 1), but its proposal must use the same claim shape (question 2) |

*So, to your question.* In the files, yes: of your three kinds, only (a) has a measure, and only when "behaviour" means the signed forward return over `horizon_bars`. (b) and (c) cannot be written as a v2 claim with a pass number today.

Is this your vision? Correct me where it is off.

> seems you are aligned. Then the question would be "is the ai call allowing to generated those ideas and related fields" ?

## Inspector notes

1. The two rules (`V2/steps/ideas/PROMPT.md`, `CLAIM_FORMAT.md`): no bars read here. Rule 2 is asked in words ("No direction field, no plus or minus one"; "dense strength") and enforced by no code: `run.py` `valid` checks three keys exist, nothing reads the code before the engine runs it. One disagreement inside the element: the "Example" block of `CLAIM_FORMAT.md` (lines 48 to 53) is `event = spaced(ret.abs() >= 3 * sd, 12); strength = ret / sd`: a sparse event and a strength that is a bar's return in volatility units. The "Dense strength" section of the same file (line 22) names both as the two shapes that fail, and `tries/try_09/READING.md` line 7 says of exactly this strength that it "is noise on most bars and churns the book" (2514 trades, net -95%). The format's own worked example is the anti-pattern it warns against; the second, one-line example (line 54) is the right one. The `spaced()` helper (line 28) exists only for sparse events.
2. The claim has a horizon, the book has none (`CLAIM_FORMAT.md` `horizon_bars`; `trading-bot/strategies/claim_linear.py` docstring: horizon "accepted and ignored"; run 003 `claims.yaml` `how_it_trades` lines: "held a few days", "held about two weeks", "held for weeks"). The engine trades the strength on every bar whatever the horizon; branch 1 measures at the horizon. So the `how_it_trades` line, which nothing reads (`run.py` `analyst_extra` sends `belief` and `claim` only), describes a book that is not run, and the analyst reads a book the claim never described. Either the horizon should reach the book (a hold, a smoothing) or the format should stop asking for a holding period. To weigh at stops 04 and 07.
3. `compared_to` is a fiction in code (`CLAIM_FORMAT.md` line 11; `PROMPT.md` line 12 "differs from those other bars (a baseline)"; `steps/judge/judge.py` lines 35 to 50): the judge computes the IC on event bars and tests it against `min_effect`; `ic_all` is recorded as information; no baseline is compared. The prompt tells the model the claim is a difference against a baseline; the code tests a level on event bars. For run 003 it does not matter (every `event` is true everywhere), but a sparse-event claim is told it is being judged on a comparison that is not made.
4. The pass number is the model's to choose, with no floor (`CLAIM_FORMAT.md` line 13 "e.g. 0.03"; `judge.py` line 25 reads `min_effect` as given; no minimum anywhere in `judge.py`, `run.py` or `backtest.py`). Scar 3 says the bar is fixed before the backtest, and it is; but the model that writes the idea also sets how high its own bar is, and nothing stops 0.001. The common rule (5 of 6 windows, 30 events) is the only part of the verdict the model does not set. Run 003 chose 0.03 and 0.04 throughout. For continuous autonomous running, a floor in code (or a fixed `min_effect` for all claims, the model dropping the field) is the difference between "judged by its own bar" and "judged by a bar it lowers".
5. The prompt asks for what the format forbids (`PROMPT.md` line 9: "several points of view ... cross-asset, market structure"; `CLAIM_FORMAT.md` line 45 "One symbol at a time; no formula that needs two symbols", line 26 OHLCV only). Cross-asset and market-structure views cannot be computed from one symbol's OHLCV; the model is invited to spend ideas on them and then strike them (line 24 "strike any that is not computable"). `PROMPT.md` line 16 "Bar size: hourly or daily" is addressed to a reader who does not choose the bar size (it comes from the brief head, stop 01).
6. The already-tried list carries void verdicts as if live (`records/claims_tried.yaml`, `real_01_daily_breadth_fold_a.md`: 12 rows from run 001 with `measure`/`verdict`, the old judge's shape, and 10 from run 003 with `branch1`/`branch3`; `run.py` line 123 to 124 sends all 22 to the model as "do not repeat these"). Run 001 was judged by the deleted judge and the on-off book: void by the README's own word, and the shelf says so, but `claims_tried.yaml` does not. In run 003 the model wrote in `notes` (line 126 to 131) that it avoided "monthly reversal" and "turn-of-month calendar flows" because they "already failed": they failed under a void regime and have never been tested under the rules. The same 12 rows were hand-copied into `real_01b_daily_breadth_ltc.md`'s list. Two record shapes in one file (query.py tolerates it with a `new` flag). A void mark per row, or a purge of pre-clean-up rows, is one line of work; without it the live search excludes ideas on void evidence.
7. Simplifiable or dead: (a) `steps/ideas/check_claims.py`: checks `measure`, `pass_if`, fields the format no longer has; nothing calls it (grep over `V2/*.py`, `V2/steps/`); delete or rewrite as the check `valid` in `run.py` already half does. (b) `brief: <brief file name>` in the format (line 4): written by the model, read by nothing (grep for `["brief"]` and `get("brief")` in `run.py`, `steps/`, `records/query.py`: none; `run.py` takes the name from argv). (c) "Dense strength" is said twice (`PROMPT.md` line 27 and `CLAIM_FORMAT.md` line 22) and the common rule's numbers live in two places (`CLAIM_FORMAT.md` lines 43 to 44 and `judge.py` line 10, `backtest.py` line 14), where the fee already disagrees (stop 01, note 3). (d) Run 002 of the real brief exists and is `REFUSED`; the speech says "run 001"; no row of 002 is in the tried list, which is right.
8. On the operator's question, "is the AI call allowing to generate those ideas and related fields", from the files only: the call can produce ideas of kind (a) (a signal that predicts the signed forward return) and run 003 shows eight well-formed ones, dense, with a reason each. It cannot produce (b) a state detector with a pass number: `event` can hold the state, but the only measure is the IC of `strength` on those bars, and no baseline is computed (note 3), so "the state is informative" has no number; nor (c) a design claim about exits or holding, since the book has no horizon and no exits a claim can name (note 2), and `PROMPT.md` line 18 forbids strategy design. The guide's two tables say the same; the files agree with them. Whether a second measure (IC on event bars minus IC off them, which the judge already half computes as `ic_all`) should exist is the operator's ruling, not the inspector's.
9. Speech against element: counts and fields match (8 ideas, horizons 3 to 20, `min_effect` 0.03 or 0.04, two contradicting pairs, the weekday idea struck, `check_claims.py` stale). One thing the speech leaves unsaid: the common rule it quotes ("0.15% per round trip") is not the engine's number (stop 01, note 3). No disagreement of substance.

Running view after stop 03: the ideas step is the best-written page in v2 and the one with the most words that code does not back: `compared_to`, `how_it_trades`, `horizon_bars` in the book, the example, the floor on `min_effect`. The tried list carries void verdicts into the live search.
