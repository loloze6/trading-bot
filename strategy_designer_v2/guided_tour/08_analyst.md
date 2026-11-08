# Stop 08 of 10: Branch 2: the analyst observes the book

## Speech (verbatim)

Stop 08 of 10: Branch 2, "what did the book do?": the analyst. Open on the side: `strategy_designer_v2/steps/analyst/summarise.py` (whole, 95 lines); `strategy_designer_v2/steps/analyst/PROMPT.md` (whole); `strategy_designer_v2/run.py` (`engine_claim`, `analyst_extra`, the analyst call in `main`); from run 003, `engine_r0_short_horizon_reversal_3d_BTCUSD/book_summary.yaml`, `analysis_r1.yaml`, `analysis_r2.yaml`; `strategy_designer_v2/tries/try_11/READING.md`.

### 1. In one sentence
Code first turns each engine run into a page of numbers about the book; then a model, the analyst, reads what it is given, writes eight to twelve observations, and proposes one next claim or none.

### 2. Why it exists
Branches 1 and 3 say pass or fail; they do not say why. The analyst is the step that reads the book as a trader would and picks the next idea from what it saw: the pipeline choosing its own next step.

### 3. What comes in, what goes out
The summary: in, the engine's per-bar output, trade list and metrics of each window; out, `book_summary.yaml`, per size and window. The analyst: in, its prompt, the claim format, the brief, and a compact block per claim of the round; out, `analysis_rN.yaml` (observations, `next_claim` or `none`, one line why).

### 4. What happens here, step by step
1. **The summary.** After each engine run that is not refused, the runner writes `book_summary.yaml`. Per window and size: net return, two Sharpes and two drawdowns (per-trade and per-bar), fees, gross and net profit, cost drag; trades (count, win rate, average, largest win and loss, hold in bars, long and short profit); exposure, turnover; the forecast's spread, share at the cap, share near zero; how often the forecast's sign matched the next bar; on event bars, the forward return when strength was positive and when negative; the equity curve in ten points; the five worst and five best bars.
2. **What the analyst is given.** For each claim of the round just run that was not refused: its belief and claim block; the full branch 1 verdict; the branch 3 verdict, slimmed to the checks and, per window, net return, trades, Sharpe and drawdown. The book summary is added only where branch 1 passed (`run.py`, `analyst_extra`). No list of claims already tried is passed.
3. **What it is asked** (`PROMPT.md`): question 1, what did the book do: 8 to 12 one-sentence observations, each tied to a number in `book_summary.yaml` (where the money came and went, whether the forecast's size tracked the outcome, the drawdowns, the costs). Question 2, one next claim in the claim format, dense and signed, distinct from every claim already tried, or `none` with one line why.
4. The proposed claim becomes the next round's only claim and goes through the engine (stops 05 to 07).

Run 003: no claim passed branch 1, so neither analyst call received a book summary; both say so in their first observation and cite the verdict files instead. Round 1 saw the 8 first claims and proposed `efficiency_excess_fade` (horizon 10, pass number 0.05). Round 2 saw only that claim and proposed `trend_with_short_pullback`. Both failed.

Live: every round of every run, two rounds by default (stop 09).

### 5. What it costs
Run 003 (`model_calls.yaml`): round 1, 0.31 USD; round 2, 0.12 USD.

### 6. How it stands against the two rules
The summary reads only the engine's files (per-bar output, trades, metrics), never the stored prices; it computes returns from the engine's own closes. The analyst reads no data, only text. Its proposal must carry a dense signed strength, in words; nothing in code checks it beyond the runner's four-field check (stop 09).

### Reading map
| Part | File and section | One line |
|---|---|---|
| The summary | `steps/analyst/summarise.py`, `window`, `summarise_engine_run` | Per window and size, numbers only, no dates |
| When it is written | `run.py`, `engine_claim` | After every engine run not refused |
| What the analyst gets | `run.py`, `analyst_extra` | Claim, both verdicts slimmed; summary only where branch 1 passed |
| What it is asked | `steps/analyst/PROMPT.md`, questions 1 and 2, "Output" | Observations tied to numbers; one next claim or none |
| The call | `run.py`, `main`, the analyst `A.ask` | Prompt, claim format, brief, the block above |
| Run 003 example | `runs/.../003/analysis_r1.yaml`, `analysis_r2.yaml`; `engine_r0_short_horizon_reversal_3d_BTCUSD/book_summary.yaml` | No summary supplied; two proposals, both failed |
| First test | `tries/try_11/READING.md` | The summary on try 09's one window |

**Correction (2026-11-08, guide).** Left out of step 1 above: the summary takes the claim's horizon from `claims.yaml` in the run folder and uses 12 bars when the claim is not found there (`summarise.py`, `horizon_of`). Claims proposed by the analyst sit in `claims_r1.yaml` and `claims_r2.yaml`, so their summaries use 12: in run 003 both analyst claims have `horizon_bars` 10 and their book summaries show `event_horizon_bars: 12`. Try 12's reading names this (`tries/try_12/READING.md`, "Defects").

Remarks? Mark a remark 'direct' for an answer before the next stop; say 'next' to continue.

## Operator remarks (verbatim, with the guide's direct answers)

> Next

## Inspector notes

1. The two rules (`V2/steps/analyst/summarise.py`, whole; `V2/steps/analyst/PROMPT.md`): clean. The summary reads `bars.csv`, `trades.json`, `metrics.json` of the engine run (lines 30 to 32) and nothing else; its forward-looking lines (37, 38) are measures of the outcome, not forecasts. The analyst sees text. Its two proposals in run 003 (`analysis_r1.yaml` line 31, `analysis_r2.yaml` line 28) are dense, signed, continuous: rule 2 kept, by the model's manners (stop 03, note 1).
2. The book is withheld from the analyst exactly when the operator's rule says to read it (`run.py` `analyst_extra` lines 105 to 106: `book_summary.yaml` is sent only where `branch1 == "pass"`; `engine_claim` lines 56 to 57 compute it for every non-refused run). In run 003 nothing passed branch 1, so neither analyst call received a book; both open by saying so (`analysis_r1.yaml` line 3, `analysis_r2.yaml` line 3) and cite the verdict files instead. The step's page says "You observe the book" (`PROMPT.md` line 3) and asks for observations "each tied to a number in `book_summary.yaml`"; the runner guarantees that number is absent for every failed claim. The root `CLAUDE.md` working rule ("at a refuted run, read the equity curve and the exposure before the bars table") is the case the gate removes. One condition in `run.py`, and 0.31 USD of round 1 bought observations on the verdict files instead of the book.
3. What the slimming strips (`run.py` `analyst_extra` line 94 `keep`: window, net_return, trades, sharpe, max_drawdown): `exposure_pct` and `cost_drag_pct` are deleted from every window row before the analyst sees it. Both are in `engine_verdict.yaml`; both are what a practitioner reads first (stop 07, note 7). Without them the analyst estimated fees "at 0.15% a round trip" as "up to about 84% of notional" (`analysis_r1.yaml` line 9) and "an upper bound, not a measurement" (`analysis_r2.yaml` line 13), with the prompt's fee rather than the engine's, when the measured number (`cost_drag_pct`) was two keys away.
4. Defect (`summarise.py` `horizon_of` lines 18 to 25): it looks for the claim in `claims.yaml` beside the engine folder and falls back to 12 silently. Analyst-round claims live in `claims_r1.yaml`, `claims_r2.yaml` (`run.py` line 158 to 160), so their book summaries carry `event_horizon_bars: 12` where the claim says 10 (`engine_r1_efficiency_excess_fade_BTCUSD/book_summary.yaml` line 2 against `claims_r1.yaml` line 14; same for round 2). The `event_bars` block of those summaries measures a 12-bar forward return for a 10-bar claim. STEPBACK "02:50" fixed the same `claims_rN.yaml` lookup in the deleted replication step; this copy of it stayed. `summarise_engine_run` already receives the engine folder; the runner knows the claims path and could pass the horizon.
5. A finding about the judge that the analyst made twice and nothing keeps (`analysis_r1.yaml` lines 4 to 6, `analysis_r2.yaml` line 4): per-window ICs consistently one sign (6 of 6 at −0.21 to −0.44; later 5 of 6 at +0.13 to +0.44) while the pooled fold IC sits near zero (−0.021, +0.012): "pooling across windows dilutes it". The judge pools ranks across six windows whose forecast levels drift (standardise is scale-only, no mean subtraction, stop 04), so a within-window ranking that holds can pool to nothing; the mean of window ICs would say the opposite. This is a measurement question for `judge.py`, surfaced by the model, recorded only inside two analysis files that no record reads. The pipeline has no place for "a finding about the pipeline" (the working rule "build only what a run asked for" needs the run's asks to be written somewhere; they are not).
6. Round 2 is blind to round 1 (`run.py` lines 151 to 153: `reached` is the current round's entries only; the speech: "no list of claims already tried is passed"): `PROMPT.md` line 16 requires the next claim to be "distinct from every claim already tried", and the analyst in round 2 is shown one claim, its own. The ideas call gets the tried list (`run.py` line 123); the analyst does not. Same list, one more `extra`.
7. Simplifiable or stale: `ALLOC = "previous_allocation"` (`summarise.py` line 11) is defined and never used; `PROMPT.md` line 23 `run: <the try folder>` is tries-era wording and nothing reads `run`; the summary carries two Sharpes and two drawdowns per window (lines 54 to 55), honest, but the bar uses one pair (stop 07, note 3) and the analyst is not told which; `sign_agreement_next_bar` (line 67) is next-bar agreement for claims whose horizon is 3 to 20 bars, information the prompt then asks the model to interpret ("whether the forecast's size tracked the outcome").
8. Speech against element: the 95 lines, the fields of the summary, the gate on branch 1, the slimming, the no-tried-list, the two rounds and their proposals, the costs all match. The speech states the gate and the step's purpose side by side (sections 2 and 4) without naming them as the contradiction they are (note 2). The speech's "Round 2 saw only that claim" is right and is note 6. Section 6 says the analyst's proposal is checked by "the runner's four-field check": `run.py` `valid` checks `id`, `code`, `horizon_bars`, `min_effect`; four, yes.

Running view after stop 08: branch 2 is the one step built to read the book, and the runner hands it the book only when the idea already passed; the fields a practitioner reads first are stripped; analyst-round summaries carry the wrong horizon. The analyst found a real property of the judge twice and the records have no slot for it.
