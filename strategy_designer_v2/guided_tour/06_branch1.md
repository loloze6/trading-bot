# Stop 06 of 10: Branch 1: was the idea right?

## Speech (verbatim)

Stop 06 of 10: Branch 1, "was the idea right?". Open on the side: `strategy_designer_v2/steps/judge/judge.py` (whole, 69 lines); `runs/real_01_daily_breadth_fold_a/003/engine_r0_short_horizon_reversal_3d_BTCUSD/judge_verdict.yaml`; `strategy_designer_v2/tries/try_10/READING.md`.

### 1. In one sentence
Branch 1 checks, from the engine's own daily log, whether the claim's forecast lined up with what the price did next: a bigger forecast should come before a bigger rise.

### 2. Why it exists
It answers "was the idea right?" separately from "did the book make money?" (branch 3). It is the claim's own test, with the pass number the model wrote before the backtest.

### 3. What comes in, what goes out
In: the engine folder of one claim and coin (stop 05), and the claim's `horizon_bars` and `min_effect`. Out: `judge_verdict.yaml` (pass, fail or refused, with the numbers) and one row in `records/trials.yaml`.

### 4. What happens here, step by step
1. For each of the six windows, it opens the engine's per-bar output of the full-size run. It needs three columns: the forecast, the close, and the claim's `event` flag (written there at stop 04). If a window lacks the forecast or the flag, the verdict is "refused".
2. For each bar it computes the return over the next `horizon_bars` bars from that log's closes, inside the window only.
3. On the event bars it measures the rank correlation (IC) between the forecast and that return: per window, and for the fold as a whole.
4. Pass needs all three: the fold's IC at least `min_effect`; the same sign as the fold in at least 5 of the 6 windows; at least 30 event bars in the fold. Two numbers are kept as information only: the IC on all bars, and a t-statistic.

It measures the graded forecast (after standardise and its cap), not the raw strength. The claim format speaks of "at least 30 event bars per window group" (`CLAIM_FORMAT.md`, "The common rule"); the code counts 30 over the whole fold.

Run 003, the 3-day reversal on BTC: 712 event bars; IC over the fold −0.013 against a pass number of 0.04; the six windows gave +0.02, −0.02, +0.25, −0.20, +0.12, −0.04 (three with the fold's sign). Fail. All 20 pairs of run 003 failed. Six cleared their pass number on the fold as a whole; none had the same sign in 5 of 6 windows.

Live: called by the engine step after every run that is not refused.

### 5. What it costs
No figure in the files.

### 6. How it stands against the two rules
It opens only the engine's output files, never the stored prices; the closes it uses are those the engine wrote. Nothing on-off reaches a forecast: `event` only chooses which bars are measured, and pass or fail is a verdict.

### Reading map
| Part | File and section | One line |
|---|---|---|
| What it measures | `steps/judge/judge.py`, docstring | Rank correlation of forecast and forward return on event bars |
| The pass rule | `judge.py`, `MIN_EVENTS, AGREE` and comment | IC ≥ `min_effect`, 5 of 6 windows same sign, 30 event bars |
| The reading | `judge.py`, `judge_engine_run`, the window loop | Per-bar output of the full-size run, three columns |
| The rank correlation | `judge.py`, `spearman` | Ranks with ties averaged, then a plain correlation |
| Output and ledger | `judge.py`, last lines of `judge_engine_run` | `judge_verdict.yaml`; one `judge` row |
| Run 003 example | `runs/.../003/engine_r0_short_horizon_reversal_3d_BTCUSD/judge_verdict.yaml` | IC −0.013, 3 of 6 same sign: fail |
| A pass, for contrast | `tries/try_10/READING.md` | Try 09's claim, BTC hourly: IC +0.16 on event bars, pass |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Sp here "is the idea right" is answerred by computing from potential return from bar's with lenghts of horizon and the forecast at start of lenght ? Do not get what claim.s event flag is . Do not get how it could allow to test any idea from step idea . It is a simple correlation.

> Next

## Inspector notes

1. The two rules (`V2/steps/judge/judge.py`, whole): clean. It opens `bars.csv` of the engine's full-size run (line 30), uses the engine's own `close` and `forecast` columns, and never the cache. Its only switch is the verdict. The forward return at line 33 pairs the forecast at bar t's close with the return from that close to t+h's close, inside the window: no lookahead in the measure.
2. What is measured is the engine's forecast, not the idea's number (`judge.py` lines 36 to 39: `forecast`; the raw `strength` sits in the same file as `debug_info.components.<id>.strength`, written by the opt-in at stop 04). Standardise divides by a 500-bar rolling mean and caps at ±20, so the cross-time ranks of `forecast` differ from those of `strength`: 6% to 20% of bars are tied at the cap for this claim (stop 04), and the divisor drifts. "Was the idea right?" is therefore answered about the idea after an engine constant has reshaped it. One more Spearman on the `strength` column, same loop, would give the operator the clean split they asked for at stop 05 (the idea on its own number; the book on the engine's) at no engine cost. Whether the verdict should then be on `strength` or `forecast` is a ruling.
3. `event` did nothing in run 003 (`judge_verdict.yaml` of all 20 pairs: `ic_event` equals `ic_all` in every window, checked across the 20 files): every claim of run 003 sets `event` true everywhere, as the "dense strength" rule invites. The flag earns its place only for a sparse claim (try 10: +0.16 on 190 event bars, −0.02 on all bars). So the operator's "do not get what the event flag is" has a plain answer from the files: on this run it is a column of ones; the format kept it for the case the format now discourages. Either keep it and say so on the page, or drop it with `spaced()` and `compared_to` (stop 03, notes 1 and 3).
4. The sign rule throws away a consistent reversed effect (`judge.py` lines 45 to 49: same sign as the fold, and fold IC ≥ `min_effect` > 0): `trend_efficiency_follow` on BTC had the same sign in 6 of 6 windows with IC −0.021; the verdict is fail with no mark that the idea was consistently wrong-way. A claim whose IC is reliably negative is a claim whose opposite is reliably right; nothing records it, and the analyst sees it only if it reads the sign of `fold_totals.ic_event`. Information the pipeline could keep for one line.
5. Statistics the page should say (`judge.py` lines 44 to 51): the pooled IC pools six windows of overlapping h-bar returns; the t-statistic (line 51) assumes independent pairs and overstates by about √h for h = 3 to 20 (information only, but the morning file quotes it as a number). Under no effect, the two checks together pass roughly one claim-and-coin pair in twelve (IC above 0.03 on about 700 pairs is about one in five; 5 of 6 same sign is about one in five), which is the noise floor STEPBACK "01:35" measured (about 6%). The guard that makes a false pass rare is not here but in `run.py` `entry_of`: a claim passes only if every coin passes. The page for branch 1 should name that guard; the common rule in `CLAIM_FORMAT.md` does not.
6. Reproducibility (`judge.py` line 30, `ROOT / w["run_dir"] / "bars.csv"`; `.gitignore` line 143 `strategy_designer_v2/**/results/`): branch 1 reads files the repository does not keep. `judge_verdict.yaml` carries the numbers and not the inputs; the verdict cannot be recomputed from the checkout, and the "judge and engine must see the same events" check (STEPBACK "mid-night") is a one-machine fact. Scar 5's row (`try: judge`, no run name, stop 05 note 2) does not help find it later either.
7. Text against code inside the element: `CLAIM_FORMAT.md` says "at least 30 event bars per window group", the code counts 30 pooled over the fold (the speech says so); the docstring says "Spearman rank correlation (Pearson of ranks)", correct; `MIN_EVENTS, AGREE` are fixed in code while `min_effect` is the model's (stop 03 note 4). `len(rows) < 6` handling (lines 46, 54) is the try-09 one-window case, live only through `--windows`.
8. On the operator's remark, from the files: yes, branch 1 is exactly "for each bar, the forecast at its close against the return from that close to h bars later, one rank correlation over those pairs, per window and pooled", and nothing else. It tests one thing for every idea: does the claim's number rank the next return. An idea whose content is that sentence is tested; an idea whose content is a state, a comparison, an exit or a size (stop 03, note 8) is not tested by it, and today no other test exists. "A simple correlation" is the design, chosen on 2026-11-06 (`CHANGES.md`, try 09: "one fixed rank-correlation measure") and not named as a choice on any page; the README still calls the claim "its own pass condition" (README "The path" step 2).
9. Speech against element: 69 lines, three columns, the three checks, the two information numbers, 712 events, IC −0.013, the six window ICs and 3 of 6, six pairs clearing `min_effect` all match. One error: "none had the same sign in 5 of 6 windows" is wrong; two pairs did (`trend_efficiency_follow_BTCUSD`, 6 of 6, IC −0.021; `efficiency_excess_fade_BTCUSD`, 5 of 6, IC +0.012) and failed on `min_effect`; no pair cleared both. The speech's section 2 "the claim's own test" is the number, not the test (note 8).

Running view after stop 06: branch 1 is sound, small and honest about what it computes; it measures the engine's forecast rather than the idea's number, keeps `event` for a case the format discourages, discards reversed consistency, and reads files the repo does not keep. The pipeline's real false-pass guard is the two-coin rule in the runner, named nowhere.
