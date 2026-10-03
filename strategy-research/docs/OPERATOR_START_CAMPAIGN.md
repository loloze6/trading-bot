# One-pager — start a campaign on the new pipeline

**For:** the operator. **Written:** 2026-10-03, after C4 (run_065, run_066). The full detail is
`RUNBOOK.md` §0b, §1e and §1f; this page is the order to do it in. Commands run from
`strategy-research/`.

> **Now (2026-10-03): do not start one.** The two follow-up entries decide-next queued after
> C4 are held `blocked_on_e068`: a run today would score a block without testing the idea's
> own claim (O-16/O-18). Use this page once E-068 says go.

## 1. Before anything (no spend)

1. No campaign process is running (`RUNBOOK.md` §2). Never edit
   `config/campaign_queue.yaml` or the flags while one runs.
2. Pre-flight checks: `RUNBOOK.md` §0b.
3. **Flags.** On `master` every new-pipeline flag is off. Switch the whole set in **one edit**
   of `config/campaign_config.yaml` (list in `RUNBOOK.md` §1e step 1, unquoted `true`), and set
   the same flags to `state: "on"` in `config/feature_flag_register.yaml`. C4 kept this edit on
   its own branch (`c4/flag-set`), never merged; do the same.
4. **Bars file signed.** `config/profitability_bars.yaml` was signed 2026-09-29 (PR #269). Do
   not touch it; any edit, even a comment, is a re-signature.

## 2. Write the brief

1. Copy `workflow_artifacts/templates/research_brief_new_pipeline.md` to
   `briefs/<name>.md`. Replace every `<FILL IN…>` (registration refuses any that is left).
2. Set `venue: kraken` and `product: perp` (Kraken is the target venue; O-14).
3. Test period and windows, `RUNBOOK.md` §1f: `end` is the last included day (never the 1st of
   a month); `window_months` 3–12; 5–40 windows; at least 2 years for an edge verdict; never the
   holdout. C4 used `start 2022-01-01`, `end 2023-12-31`, `window_months: 4` (6 windows).
4. No `promotion` block (D-043). The grid and the profit bars decide.

## 3. Register, dry run, launch one step

```bash
PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py register \
  --brief briefs/<name>.md --priority 1 --notes "<why>"
PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --dry-run   # must end DRY RUN PASSED
PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --once
```

Also run `RUNBOOK.md` §1a-bis's check-all-four snippet before `--once`. Background mode (§1c)
stays blocked.

## 4. What a good run looks like (from C4)

- About **30 min** and **~$0.90** of LLM use per run on Haiku 4.5 (run_066). Hourly bars make
  the backtest step the longest (~19 min).
- Stages in order: hypothesis_generation → strategy_config_authoring → innovation_expansion →
  backtest_specification → data_availability_gate → protocol_execution → specialist_readers →
  regroup_record → decide-next.
- Ends `completed_<idea_status>` (C4: `completed_refuted` both times).

## 5. Check after the run (`RUNBOOK.md` §1e step 5)

- `runs/<run>/pipeline_state.yaml` → `audit_log`: `num_turns: 1` on every call. More = stop and
  report.
- `campaign_record/campaign_state.yaml` → one trial row per graded variant, named
  `<run>:<variant>`, refuted ones included.
- `campaign_record/campaign_memory.yaml` has the run; `runs/<run>/artifacts/decision_record.yaml`
  exists.
- `flags.holdout_reserved: false`: the holdout was not touched.

## 6. If it pauses

`pipeline_state.yaml` says why (`status: paused_for_human`, `halt_history`, `last_error`). Look
the reason up in `RUNBOOK.md` §3, fix the cause, then `RUNBOOK.md` §4:

```bash
PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --resume
```

A resume re-runs only the stage that stopped; finished stages are kept (run_065 re-ran only two
readers). A `profit_bars_reached` pause is good news: go to `OPERATOR_UNLOCK_HOLDOUT.md`.
