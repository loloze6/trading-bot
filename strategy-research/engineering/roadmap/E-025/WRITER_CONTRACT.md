# E-025 — Trial-Ledger Writer Contract

**Status:** APPROVED (E-025, workflow-mitigation #2) — reviewed and merged via PR #34, 2026-08-17 (`48e0b09d`). This file's header still read "DRAFT for Jeremy's review" two weeks after approval; flagged by Dorian 2026-09-01.
**Rule this file establishes:** changing this contract is its own PR, announced, **before** any code that depends on the change — so the other writer never lands a conflicting edit to the same two files unseen. Additive > invasive.
**Grounding:** pins what the code does today, verified by reading the source at merge tip `635afa36` (Jeremy's S1/S2 `cf7908bc` + the fork's H2/H4/S3, all ancestors). Not a new design — a written fixture of the current contract.

## Why this exists

Two writers (Jeremy on master, Dorian on the fork) both append to one trial ledger and both edit the two files that maintain it — `strategy-research/workflow/run_phase1_research.py` (writers) and `strategy-research/tools/deflate_sharpe.py` (readers/guards). Twice now a change to one landed hours before the other's session and silently broke assumptions (issue #28's H3 flipped a batch of characterization-suite items that had to be reconciled). A one-page authoritative row spec makes the next such collision a loud, named contract change instead of a silent divergence.

## The ledger

- **File:** `strategy-research/campaign_record/campaign_state.yaml` on `loloze6/trading-bot` master (authoritative; the fork's copy is a working copy — new fork trials land via PR).
- **Key:** `campaign_state["trial_sharpes"]` — a list of trial rows. **This list is the only structure DSR's N reads** (`deflate_sharpe.load_sharpe_trials`, ds:183). No other field in `campaign_state.yaml` feeds N.

## A trial row

Every row is a dict. Common fields (all sources):

| field | type | notes |
|---|---|---|
| `trial_id` | str | the run id. master `run_NNN`, fork `run_d_NNN` (S3). |
| `source` | str | closed vocab: `prescreen` \| `backtest` \| `backtest_failed`. |
| `statistic_valid` | str | closed vocab: `neither` \| `sharpe` \| `expectancy` \| `failed`. |
| `sharpe` | float \| null | median across symbols; null unless a real backtest Sharpe exists. |
| `expectancy_bps` | float \| null | per-trade expectancy; set on sparse-trading candidates. |
| `n_trades` | int | 0 for non-`backtest` rows. |
| `forecast_hash` | str(sha256) \| null | canonical-JSON sha256 of the strategy config. **Mandatory non-null on every new trial**; null tolerated **only** on `backtest_failed`, where the config itself may be the failure. |

Source-specific extra fields (informational; **not** read by DSR):
- `prescreen` → `route`, `ic_pooled`, `cost_pass`
- `backtest` → `below_floor_pct`
- `backtest_failed` → `error`

## Uniqueness key: `(trial_id, source)`

- **One row per `(trial_id, source)`.** This is THE key for every guard, write-side and read-side.
- A single `trial_id` legitimately carries up to two rows: one `prescreen` (every trial — kill or pass) plus one of `backtest` (advanced + completed) or `backtest_failed` (advanced + crashed after touching data).
- **Never key a guard on `trial_id` alone** — it suppresses the legitimate second-source row (measured: would drop a real backtest row when a prescreen row for the same run id exists).
- **Never key a guard on `(trial_id, source, forecast_hash)`** — a re-prescreen with an edited config would append a 2nd `(trial_id, prescreen)` row that the read-side `check_no_duplicate_trial_ids` (2-tuple) then rejects. The **2-tuple is the one key write-side and read-side agree on** — this alignment is load-bearing (drove the fork's H2 upsert + H4 guard down from a 3-tuple).

## `source` vocabulary (closed) — what records each

| source | writer (rpr) | when | sharpe | statistic_valid |
|---|---|---|---|---|
| `prescreen` | `_record_prescreen_trial` (:3023) | every prescreen (kill or pass) | null | `neither` |
| `backtest` | `_record_backtest_trial` (:3072) | a completed full backtest | median or null | `sharpe` \| `expectancy` \| `neither` |
| `backtest_failed` | `_record_failed_backtest_trial` (:3132) | a backtest that raised **after** touching data | null | `failed` |

`prescreen_stub` (rpr:3707) and `operator_ratified` (run_campaign:387) also carry a `source` field but are **not** trial-ledger rows — they live in other artifacts (a protocol-result YAML written via `save_yaml(pr_path, stub)` / a queue entry) and are out of scope.

## Recording ≠ counting (two separate layers)

- **Record** every data-touching look, honestly: a prescreen kill, a completed backtest, and a crashed-after-data backtest all get a row. That is the write contract above.
- **Count toward DSR's N** is a separate policy layer: `load_sharpe_trials` today feeds only `statistic_valid=="sharpe"` rows into N; `neither`/`expectancy`/`failed` are recorded but excluded. Whether kills/failures widen N is **H1** — a DSR-methodology decision (Jeremy: **YES**, kills should count — Slack 2026-08-16), wired separately in `load_sharpe_trials`.
- The write contract does **not** depend on the H1 outcome: rows are recorded regardless; H1 only changes which recorded rows the reader counts. Keep the two layers separate — a writer change must never quietly re-decide H1.

## Binding rules

1. **`forecast_hash` mandatory** on every new trial, both writers (E-025 S1). Fails loud on a missing config, except the `backtest_failed` path where null is legal and kept-unique by `deduplicate_trials` (ds:88-90).
2. **Append-only + upsert-in-slot.** A new independent trial is a NEW run id on its own `(trial_id, source)` key. A re-entered prescreen of the SAME run id is a retry/edit of one slot → **upsert** (replace in place), never a second row (H2). Never widens N.
3. **No DSR until merged.** `deflate_sharpe` refuses to compute against a `campaign_state.yaml` that differs from `origin/master` (`check_ledger_is_merged`, ds:134) and refuses on any duplicate `(trial_id, source)` (`check_no_duplicate_trial_ids`, ds:105).
4. **ID allocation disjoint by construction:** master `run_NNN`, fork `run_d_NNN` (S3). A real `(trial_id, source)` collision across writers is therefore structurally impossible; the read-side check is a **tripwire** for that invariant, not a normal-path gate.

## Enforcement points (today)

- **Write-side guards:** `_record_backtest_trial` (rpr:3091), `_record_failed_backtest_trial` (rpr:3179), `_record_prescreen_trial` upsert (rpr:3058-3065) — all key on `(trial_id, source)`.
- **Read-side backstops:** `check_no_duplicate_trial_ids` (ds:105), `check_ledger_is_merged` (ds:134), `deduplicate_trials` by `forecast_hash` (ds:76), `load_sharpe_trials` N-filter (ds:183).

## Changing this contract

Any change to the row shape, the `source`/`statistic_valid` vocab, or the uniqueness key is a PR to **this file first**, announced on Slack ("touching rpr.py/deflate_sharpe.py now → done, pushed &lt;sha&gt;"), before the code that depends on it.
