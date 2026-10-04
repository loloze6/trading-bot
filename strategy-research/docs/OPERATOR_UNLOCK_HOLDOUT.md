# One-pager — unlock the holdout

**For:** the operator. **Written:** 2026-10-03. Applies with the new-pipeline flags on
(`verdict_routing_retired`, `decide_next`, `profit_bars_every_backtest`, `profit_bars_v2`).
Full detail: `RUNBOOK.md` §3 (pause table) and §4 (resume). Code:
`workflow/run_phase1_research.py` (`_read_holdout_decision`, `_holdout_unlock_route`,
`_unlocked_holdout_evaluation`, `_spent_holdout_ending`).

**The holdout is single-use.** One spend per hypothesis, and a failed spend ends that
hypothesis. Its range comes only from `config/campaign_data_policy.yaml` (`holdout_range`).
Never open its data store to "have a look": looking is spending.

## 0. Not yet: three tickets come first

Before the **first real spend**, fix (all in E-067):
- **CUL-340**: no second spend after a crash; the id bound to the unlock; strict policy parse.
- **CUL-335**: the "already spent" list (`holdout_consumed_by`) moves out of the hand-edited
  policy file into a machine-owned ledger.
- **CUL-348**: the bars-file sha256 depends on line endings. Until fixed, **grade and spend on
  the same checkout**, or the spend is refused as `bars_changed`.

## 1. What starts it

A variant passes **every** profit bar. The run pauses `profit_bars_reached`
(`status: paused_for_human`) and writes `profit_bars_stop_evaluation` (a timestamp) into
`runs/<run>/pipeline_state.yaml`. Nothing else leads to the holdout: a run that reaches it
without an unlock pauses `holdout_refused_under_retired_routing`.

## 2. Decide, and write it down

Create `runs/<run>/artifacts/holdout_decision.yaml`. Closed schema: an unknown or missing key
is refused (`decision_malformed`).

```yaml
decision: "spend"                     # or "continue" (holdout untouched, run ends normally)
run_id: "run_0NN"
profit_bars_stop_evaluation: "<copy from pipeline_state.yaml>"
variant_id: "<the passing variant>"   # required for spend
trial_ledgers_merged: true            # required for spend; unquoted
ratified_by: "<your name>"
ratified_at: "<today, ISO date>"
note: "<optional>"
```

Before `spend`, answer yes to all: the trial ledgers of both writers are merged; the deflated
Sharpe was looked at with every trial counted; the bars file is the one that graded the run.

Then in `pipeline_state.yaml`: clear `flags.profit_bars_reached`, set `status: active`, and run
`../venv/Scripts/python.exe workflow/run_campaign.py --resume`.

## 3. What the code checks on `spend` (any failure = `holdout_unlock_refused`, nothing spent)

The variant passes every bar; the bars file and bar definitions are unchanged; the hypothesis
is not already in `holdout_consumed_by`; no other run has a spend in progress; the deflated
Sharpe, recomputed on today's ledger, still clears its threshold. The reason code is in
`holdout_unlock_refusal`. Fix it, clear `flags.holdout_unlock_refused`, `status: active`,
`--resume`.

## 4. Run the holdout backtest (by hand)

The run pauses `holdout_unlocked_awaiting_result`. Still nothing spent. Then, for that variant
only:

```bash
../venv/Scripts/python.exe tools/run_protocol.py ... --holdout --i-understand \
  --hypothesis-id <id> --legacy-verdict-retired
```

`--legacy-verdict-retired` is required on a new-pipeline protocol. `run_protocol.py` refuses
before any fetch when the protocol's holdout block disagrees with the policy range, or the id
is already spent.

Changed your mind before this step? Write `decision: "continue"` for the same stop, set
`pending_stage: regroup_record`, `status: active`, `--resume`.

## 5. Record the result (once)

Write `runs/<run>/artifacts/holdout_result.yaml`: `status` (`pass` or `fail`), `hypothesis_id`,
and `variant_id`, `trial_id`, `decision_sha256` copied from `holdout_decision_record` in
`pipeline_state.yaml`. Clear `flags.holdout_unlocked_awaiting_result`, `status: active`,
`--resume`. The spend is recorded first (`holdout_consume_record`, then `holdout_consumed_by`),
then the run ends: `pass` → `completed_promoted`, `fail` → `completed_rejected`.

## 6. Never

- Never edit or delete `holdout_result.yaml` or `holdout_consume_record` once the backtest ran.
- Never edit `holdout_decision.yaml` after the unlock (refused as `decision_changed`).
- Never run `--holdout` without an unlock: the run is marked spent and can never be promoted
  (`holdout_spent_without_unlock`).
- Other holdout pauses (`…_result_inconclusive`, `…_result_unbound`, `…_result_relabelled`):
  the seal is spent; follow their row in `RUNBOOK.md` §3. Usually: end the run with
  `pending_stage: completed_rejected`, never rewrite the result.
