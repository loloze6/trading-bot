# E-075 PR-5 runbook: the analyst's smoke session and pilot (operator's machine)

Built in E-075 PR-5 (CUL-423, D-092). Nothing here runs in the cloud checkout: it needs model
credentials, the saved runs in the variant layout (065-074) and the campaign record. Every
step that spends money is marked **($)**.

Plain words first:
- **The analyst** is a model session that explores one run's own bars and trades with six
  query tools, then writes either ONE claim (with a test code can run on another period) or
  "no claim".
- **A lens** is the analyst's angle: `forecast` (does the forecast predict the price?) or
  `trade_efficiency` (are some trades better than others?).
- **Code checks every answer**: each number it cites must be in its query log, its claim test
  must have been run, the claim must compile, no date at or after the holdout start.
- **A fold** is a block of past years. A claim found on fold A is confirmed only on fold B
  (then C), which its lineage has never seen.

## 0. Prerequisites (once)

1. Install the pinned requirements (the `mcp` pin matters: `mcp` 2.x breaks the SDK's tool
   server):
   `uv pip install --python .venv/bin/python -r strategy-research/config/requirements-mac.txt`
2. Check: `.venv/bin/python -c "import importlib.metadata as m; print(m.version('mcp'))"` prints
   `1.30.0`.
3. Your model credentials are set in your shell as usual (never in a file of this repo).
4. `cd strategy-research` for every command below.

## 1. Smoke session (about $1-3) **($)**

Goal: four facts the Python source cannot prove (PHASE_A section 1.4).

1. Copy one saved run OUTSIDE the repository (saved runs are never written to; the CLI refuses
   a run under `runs/`):
   `cp -R runs/run_074 /tmp/analyst_smoke/run_074`
2. Run one lens with the real stage function:
   `../.venv/bin/python tools/analyst_session.py --run /tmp/analyst_smoke/run_074 --lens forecast`
   The flags are turned on inside this process only; `config/campaign_config.yaml` is not
   changed. Caps: 40 turns, $1.50, 15 minutes.
3. Read the summary it prints after `--- analyst smoke summary ---` and check:
   - **Tool names:** `audit_log.*.init_tools` lists only `mcp__analyst__<name>` names.
     If the session had any other tool, the CLI stops with `AnalystToolListError` (fail
     closed) and writes no reading: send me the list; do not widen the allow-list yourself.
   - **Tools used:** `tools_denied` is `[]`, and `tool_calls` > 0.
   - **Model:** the session ran (no CLI model error) and `result_subtype` is `success`.
   - **Cost:** `cost_usd` is under $1.50 and `tokens.cache_read` > 0 after the first turns.
4. Open the record (`artifacts/analyst/forecast.yaml` in the copy): `attempts[*].status`,
   and the errors if it was refused.
5. Repeat step 2 with `--lens trade_efficiency`.

If something fails, keep the copy and send me the record and the summary.

## 2. Pilot

### 2a. Offline: both lenses on saved runs 065-074 (about $10-30) **($)**

1. Copy each saved run 065-074 outside the repository, as in step 1.
2. Run both lenses on each copy (20 sessions; each capped at $1.50, so $30 at most).
3. Process checks (D4 of PR5_DESIGN; information, not a pass mark):
   - how many answers were accepted at the first attempt, after the retry, or skipped;
   - the refusal reasons (citations, test not run, `why_query`, dates);
   - claims against `no_claim`;
   - cost and turns per session.

These readings stay in the copies: nothing from them reaches the campaign.

### 2b. Online: claims confirmed on fold B (campaign runs, yours to launch) **($)**

1. In `config/campaign_config.yaml`, set `enabled: true` for `orchestrator.analyst` and the
   flags it needs: `folds`, `specialist_readers`, `reader_findings`, and their own
   prerequisites (`grid_evaluation`, `category_reports`, `claim_tests`,
   `config_direct_authoring`), plus `decide_next` for the fold-B child. The pre-flight check
   refuses a missing one by name.
2. Launch the campaign as usual (`python workflow/run_campaign.py`, or `--once` for one run).
   Under the flag:
   - the `specialist_readers` stage runs the two lenses instead of the five readers;
     `profitability`, `regime_power` and `component_attribution` are written as `skipped`
     (rule `replaced_by_analyst`) with no model call;
   - decide-next ranks the analyst's claims by the simple score (in-run window agreement,
     0..3) and builds a child run on the next fold its lineage has not used;
   - after the child's backtests, the claim is measured on that fold
     (`campaign_record/confirmations.yaml`, `fold_confirmations`).
3. Report per fold, as information: confirmed / not confirmed / not measurable. The score is
   exploratory; only the fold result counts.

## 3. Where things are

| What | Where (inside the run) |
| --- | --- |
| The reading (what decide-next reads) | `artifacts/proposals/<category>.yaml` |
| The session record (answer, attempts, scores, why_query, no-claim block) | `artifacts/analyst/<lens>.yaml` |
| The query log (every call, refused ones too) | `artifacts/analyst_queries/<lens>.yaml` |
| Cost, turns, tool list | `pipeline_state.yaml`, `audit_log.specialist_readers_analyst_<lens>_*` |

## 4. Never

- Never point the CLI at a run under `runs/` or at anything under `local_data/holdout_sealed/`.
- Never edit a reading or a query log by hand: the citations are checked against the log.
- A run of `main.py run_bot` is never part of this.
