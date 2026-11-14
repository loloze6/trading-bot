# Stop 09 of 10: The runner: the loop, resume, the knobs, the refusal

## Speech (verbatim)

Stop 09 of 10: The runner. Open on the side: `strategy_designer_v2/run.py` (whole, 167 lines); `strategy_designer_v2/tries/try_12/READING.md`; run 003's `DONE` and `record.yaml`; run 002's `REFUSED`; `strategy_designer_v2/records/` (`claims_tried.yaml`, `shelf.yaml`, `trials.yaml`, `query.py`).

### 1. In one sentence
The runner is one command that takes a brief and runs the whole loop by itself, until the analyst says none or the rounds are used up.

### 2. Why it exists
"Runs on its own": the operator writes a brief and starts one command; everything after is the pipeline's. Every step leaves a file, and a step whose file exists is skipped, so a run restarts where it stopped.

### 3. What comes in, what goes out
In: the brief and three knobs: the fold (A by default), the number of analyst rounds (2), and a cap on the first round's claims (none). The models are fixed in the file. Out: a run folder `runs/<brief>/NNN/` and the records below.

### 4. What happens here, step by step
1. It reads the brief (stop 01) and picks the run folder: the last one if it has no `DONE` mark (a resume), otherwise a new number.
2. It asks for ideas (stops 02, 03), passing the claims already tried under this brief. If no model is reachable it stops and waits for the answer file.
3. For each claim and each coin: a claim missing its id, code, horizon or pass number is recorded as refused; otherwise the engine step runs (stops 05 to 07, with branch 1 at stop 06), then the book summary (stop 08). A folder that already has its verdict is skipped.
4. **The refusal.** If the very first claim is refused because a coin has no history for the fold, the runner writes `REFUSED` and stops: "a fold the coins do not cover costs one ideas call and nothing more".
5. Per claim it combines the coins: pass only if every coin passes; refused if every coin was refused; fail otherwise. It writes the round into `record.yaml` and the records.
6. Unless the rounds are used up, it calls the analyst on the round's claims (stop 08). "None" ends the run; a claim becomes the next round.
7. At the end it writes `DONE` with the time and prints the counts.

With 2 rounds: the first claims, then two analyst claims, each through the engine. Run 003: 8 + 1 + 1 = 10 claims, 20 engine runs, two analyst calls; branch 1 passes 0, branch 3 passes 0, refused 0. Run 002 of your brief stopped on a refusal: ADA has no history before fold A's warm-up.

### What it writes
| Record | One line | Run 003 |
|---|---|---|
| `records/claims_tried.yaml` | Per brief file, one row per claim tried: id, belief, branch 1, branch 3, run; written by `run.py` (`remember`), read by the next ideas call | 10 rows added; 22 under your brief |
| `records/shelf.yaml` | Claims that passed branch 1, `status` validated, or profitable if branch 3 passed too; written by `run.py`; its note: "Nothing on this shelf is valid. Kept as history." | None added; 26 entries, one with a status (from try 12's made-up brief), 25 marked void |
| `records/trials.yaml` | The ledger: one row per engine run (`backtest.py`) and per branch 1 verdict (`judge.py`) | 40 rows (20 engine, 20 judge); 731 in all, most from before the clean-up |
| `records/query.py` | Reads every run's `record.yaml` and cost log and prints one table: claims, passes, cost, done; older runs shown as "old shape" | Run 003 shows 10 claims, 0 and 0 passes, 0.63 USD |

### 5. What it costs
Run 003: 0.63 USD in model calls, 868 seconds of engine; `STEPBACK.md` gives fourteen minutes for the run.

### 6. How it stands against the two rules
It reads no bars: it moves files and reads verdicts the engine and the judge wrote. Nothing on-off reaches a forecast; the combining of coins is a verdict rule.

### Reading map
| Part | File and section | One line |
|---|---|---|
| The command and knobs | `run.py`, docstring, `main` (argparse) | Brief, fold, rounds, max claims |
| Resume | `run.py`, `main` (run folder choice); every "exists" check | Last folder without `DONE` is continued |
| One claim, all coins | `run.py`, `valid`, `engine_claim` | Four-field check, engine, summary |
| The refusal | `run.py`, `NO_HISTORY`, `main` (first claim) | `REFUSED`, exit |
| Combining coins | `run.py`, `entry_of` | Pass only if every coin passes |
| Records | `run.py`, `remember`; `steps/engine/backtest.py` and `steps/judge/judge.py`, ledger lines | Who writes which file |
| The query | `records/query.py` | One table over all runs |
| End to end | `tries/try_12/READING.md` | Made-up brief: 4 claims, 1 validated, 0 profitable |

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> 'exy

(Taken by the guide as "next".)

## Inspector notes

1. The two rules (`V2/run.py`, whole): clean. It reads briefs, prompts, verdict files and records, and writes files; the one market-data path is `E.backtest_claim` (line 51). Its switches are verdicts (`entry_of`, lines 72 to 74). The one place it touches the model's code before the engine is `valid` (line 38): four keys exist. Rule 2 and scar 1 are enforced nowhere in the runner either (stops 03 and 04).
2. "Continuously" has no mechanism (`run.py` `main`; README "Status"; `guided_tour/_post_tour/session_analysis.md` "What the session does not prove": "no queue of briefs, no budget per day"). The runner runs one brief and exits. The only thing that ever chained runs was the night's shell scripts (`runs/_batch*.sh`, `runs/_night_*.sh`, 19 files, void and still in `runs/`). The README's "not built" list at stop 10 should carry the queue and the budget, which it does not today. Related: the fold is a knob (stop 01, note 4), so a queue would need a per-brief fold line first.
3. The refusal leaves a folder the next launch resumes (`run.py` lines 116 to 117 and 136 to 140): on a no-history refusal the runner writes `REFUSED` and returns 2 without `DONE`; the resume rule then picks that folder again on every later launch of the same brief, skips the ideas call (the answer file exists) and refuses again at the first engine call. The brief cannot run on another fold's attempt until a hand writes `DONE` or removes the folder. All five `REFUSED` folders in `runs/` also carry `DONE`, a state the current code never produces; they come from the night's runner or from a hand. Either write `DONE` on refusal or make the resume rule skip a `REFUSED` folder.
4. The speech's reason for run 002 does not match the evidence (speech section 4: "ADA has no history before fold A's warm-up"; `runs/real_01_daily_breadth_fold_a/002/REFUSED`: "coverage: ADAUSD warm-up: 0 bars before the fold, 600 needed; ... W1: 0 of about 120 bars"; no `record.yaml`, so no fold named): run 003 ran ADA on fold A with 117 to 120 bars in every window (`judge_verdict.yaml`), so ADA covers fold A. The `coverage:` wording is the night's deleted coverage check, and STEPBACK "02:40" says the operator's brief "could not run on folds B and C with ADA". Run 002 was most likely a fold B or C attempt from the night. The runner keeps no fold in a refused folder, which is why the speech could not know; one line in `REFUSED` (fold, bar size, symbols) would fix the record.
5. Combining coins loses the "incomplete" case (`entry_of` lines 72 to 74): pass if every coin passes, refused if every coin is refused, otherwise fail. A claim that passes on BTC and is refused on ADA (a longer warm-up than the first claim's, which escapes the first-claim check at line 136) is written as `fail` in `claims_tried.yaml` and never re-proposed. The two-coin rule is the pipeline's real false-pass guard (stop 06, note 5); it should say "incomplete", not "fail", when one coin did not run.
6. Crashes where refusals were meant (`run.py` line 128 `["ideas"]`, line 155 `yaml.safe_load(analysis)`; `ask.py` second parse failure, stop 02): a model answer that is valid YAML without an `ideas` key is a `KeyError` with no marker; the night's lesson (STEPBACK "Wakeup 01:28") covered malformed claims (line 49 to 54), not a malformed file. Scars 4 and 6 again: every write is `write_text` (`dump`, line 33), and there is no cost or time cap; `--rounds` is the only bound.
7. The records (folded stop). (a) `claims_tried.yaml`: 588 rows, 14 in the live shape (`branch1`/`branch3`), 574 in the void judge's shape (`measure`/`verdict`), all sent to the ideas model as "do not repeat" (stop 03, note 6); no void mark. (b) `shelf.yaml`: 26 rows, 25 with `void:`, one `status: validated` from try 12's made-up brief; the file's `note` says "Nothing on this shelf is valid ... A new shelf starts with the first claim judged from the engine's outputs", and that first claim is the one sitting above the note without a mark that it is the new shelf. `remember` (lines 84 to 88) appends to the same list. (c) `trials.yaml`: 731 rows; the live rows carry no run or brief name and refusals get none (stop 05, note 2). (d) `query.py`: reads `record.yaml` per run and sums costs; its last line counts "claims tried 588" and "shelf: 1 validated" over void and live together. The records are one list each for two eras; every reader has to know which rows to believe, and only `shelf.yaml` says.
8. Simplifiable: `--max-claims` (line 112) is a test knob (try 12) with no live use; `MODELS` names one model twice (stop 02); `counts["refused"]` (line 142) counts claim-level `branch3 == refused`, which after `entry_of` means all coins refused, so a per-coin refusal is invisible in the final print; `analyst_extra` recomputes from `engine_verdict.yaml` what `entry_of` already read (lines 99 to 103 against 67 to 71), two readers of the same file in one run.
9. Speech against element: 167 lines, the three knobs, the resume rule, the four-field check, the first-claim refusal, the coin rule, `DONE`, 8 + 1 + 1, 20 engine runs, the records table (22 rows under the brief, 26 shelf rows with 25 void, 40 ledger rows, 0.63 USD) all match the files. Two disagreements: the reason for run 002's refusal (note 4), and the "What it writes" row for `trials.yaml`, "one row per engine run and per branch 1 verdict", which is true and omits that refusals write none and live rows carry no run name.

Running view after stop 09: the runner does what its docstring says for one brief, once; "continuously" is not built and not listed as missing; a refusal blocks the brief until a hand intervenes; the records hold two eras in one list each. The speech misread run 002.
