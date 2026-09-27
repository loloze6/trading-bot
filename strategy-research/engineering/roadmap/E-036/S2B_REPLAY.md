# E-036 S2b — read-only corpus replay of the exact-match repeat gate (slice 8)

Measured 2026-09-27 on `feat/e036-s2b-corpus-replay` (branched from `origin/master` at
`b27e6ce9`), re-derived after code review. Script: `tools/replay_repeat_gate.py`.
Machine-readable result: `engineering/roadmap/E-036/s2b_replay_result.yaml` (one row per
run, every column, plus the totals below). Read-only: no backtest, no market data, no
API call, the holdout not opened; a listing of `runs/` with sizes and mtimes (8,791
entries) was identical before and after the replay. `orchestrator.variant_anti_adjacency_gate`
stays **off**; nothing here recommends switching it on — that is the operator's call.

---

## What switching it on would have changed (read this first)

**Under today's live rules, over these 60 runs, the gate would have refused nothing.**
Two separate reasons, both measured:

- **Its memory would be empty.** The live writer (`campaign_memory.build_memory_entry`,
  run by `regroup_record`) admits none of these runs: no run has the grid files
  (`idea_status.yaml`) it requires, and the trial ledger holds only 3 `backtest` rows
  (run_054, run_057, run_059), none carrying the `forecast_hash` the writer also
  requires. With nothing in memory, nothing can be a repeat. (And switched on as the
  repo stands, with `campaign_memory.yaml` absent and `regroup_record` off, the gate
  does not admit anything either: it raises a `RuntimeError` for every run, by design,
  because nothing would ever fill its memory.)
- **Most runs would stop before any lookup.** Of the 42 runs with a config, 33 make the
  gate itself raise while resolving the run's protocol: 32 because that protocol
  carries the unratified generic promotion block, which the protocol resolver's D-3
  guard refuses (a guard added after these runs, unrelated to E-036), and run_027
  because its protocol at that point could not be opened at all. Only 5 runs
  (run_036, run_054, run_057, run_059, run_060) get a key; all are NOVEL.

**Setting both of those aside** — the D-3 guard switched off and the memory rebuilt with
the missing ledger hashes filled in from each run's config file (a made-up ledger value,
clearly a counterfactual) — the gate still refuses nothing: 37 NOVEL, 1 fail-loud. The
corpus holds exactly one true re-test, **run_027 = run_024** (identical config, identical
backtest results), and the gate does not call it a repeat: at 5a, run_027 was going to
run a 4h escalation protocol whose file name had been built from prose and could not be
opened, so the gate would have **raised on it** (stopping the run) rather than matched
it. Only if you key run_027 on the 1h baseline it actually ended up running is it a
REPEAT of run_024.

The old family check refused 3 runs (run_012, run_032, run_034); each is a real config
change from the run it was flagged against. In no column does the new gate refuse any
run the old one refused.

---

## 1. Headline

Columns are *protocol mode* × *memory mode*. **PRIMARY** is the live gate on the live
writer's memory; every other row is a labelled counterfactual.

| column | protocol keyed on | memory | REPEAT | NOVEL | FAIL_LOUD | UNKEYED |
|---|---|---|---:|---:|---:|---:|
| **5a_live / strict (PRIMARY)** | live resolver at 5a | live writer | **0** | **5** | **33** | **22** |
| 5a_live / counterfactual | live resolver at 5a | backfilled | 0 | 5 | 33 | 22 |
| 5a_d3_aside / strict | resolver, D-3 guard off | live writer | 0 | 37 | 1 | 22 |
| 5a_d3_aside / counterfactual | resolver, D-3 guard off | backfilled | 0 | 37 | 1 | 22 |
| executed / strict | protocol the backtest ran | live writer | 0 | 38 | 0 | 22 |
| executed / counterfactual | protocol the backtest ran | backfilled | **1** | 37 | 0 | 22 |

| memory | entries | variants | why the other runs are out |
|---|---:|---:|---|
| strict (live writer) | **0** | 0 | no `protocol_result.yaml` 22, no hypothesis card 2, no `idea_status.yaml` 36 |
| counterfactual (backfilled) | 29 | 29 | no `protocol_result.yaml` 22, no hypothesis card 2, not backtested (prescreen stub) 7 |

Trial ledger (`campaign_state.yaml: trial_sharpes`, per run): `backtest` row without a
`forecast_hash` 3 (run_054, run_057, run_059); no `backtest` row 57; a `backtest` row
with a hash 0. So even with the grid requirement waived, the live ledger rule alone
admits no run.

Runs 60; candidate variants 42 (one per run with a `candidate_strategy_config.json` —
counted from the candidates; no run has `variants/index.yaml`).

**Old layer 2** (the retired caller): refuse (`repeat`) 3, `neighbour` 26, `novel` 18,
not evaluable 13 (11 no card, 2 card YAML unparseable).

**Old × PRIMARY:**

| old \ new | REPEAT | NOVEL | FAIL_LOUD | UNKEYED |
|---|---:|---:|---:|---:|
| repeat (refuse) | 0 | 0 | 3 | 0 |
| neighbour | 0 | 0 | 22 | 4 |
| novel | 0 | 4 | 7 | 7 |
| not evaluable | 0 | 1 | 1 | 11 |

**Old × 5a_d3_aside / counterfactual:**

| old \ new | REPEAT | NOVEL | FAIL_LOUD | UNKEYED |
|---|---:|---:|---:|---:|
| repeat (refuse) | 0 | 3 | 0 | 0 |
| neighbour | 0 | 21 | 1 | 4 |
| novel | 0 | 11 | 0 | 7 |
| not evaluable | 0 | 2 | 0 | 11 |

**Old × executed / counterfactual:** identical to the table above except run_027, which
moves from FAIL_LOUD to REPEAT in the `neighbour` row. The YAML has all six matrices.

## 2. Method

- **Order.** Runs in run-number order (`run_0001` … `run_060`), taken as chronological —
  not independently checked against timestamps (`pipeline_state.yaml` carries only an
  `updated_at`). Each run is checked against the memory of **earlier** runs only, with
  its own run id excluded as live; its own memory entry is added after its check. The
  protocol files and the index are built incrementally (each file read once, each entry
  indexed once).
- **Candidate at 5a** — as `run_phase1_research._repeat_gate_context` /
  `_check_variant_repeat`: `novelty.forecast_hash_of_config` of
  `artifacts/candidate_strategy_config.json` (the file F4d writes and the trial row
  hashes), the protocol's `symbols` read strictly, `anti_adjacency_gate.candidate_key`,
  `layer2_digest_check`, and the recorded key shape `novelty.key_dict` (now shared with
  the live code).
- **Protocol at 5a** — the live resolver itself, `protocol_resolution.resolve_protocol_path`
  (what `_resolve_protocol_path` delegates to), run read-only on each run's own
  `run_context.yaml`. **Declared approximation:** runs whose `run_context.yaml` names no
  `run_type` take the resolver's B10 branch, which reads the campaign-wide
  `campaign_state.last_escalation` *as it was then*; that history is not kept (git holds
  3 revisions of `campaign_state.yaml`; today's value is claimed by run_049). For those
  runs `last_escalation` is reconstructed as a claim by the run itself on the earliest
  protocol path its own artifacts record: (1) a `protocols/...` path quoted by an OSError
  in `pipeline_state.yaml: last_error` (the path the resolver produced and could not
  open — run_027 only), else (2) `prescreen_result.yaml: protocol_version`, else (3)
  `protocol_result.yaml: protocol_file`. No such record → UNKEYED (`b10_no_evidence`),
  not a guess. A resolver exception → FAIL_LOUD (`promotion_unratified` for the D-3
  guard's `UngatedProtocolError`, else `resolver_raises`); an unreadable resolved file →
  FAIL_LOUD (`novelty_error`); no usable `symbols` → FAIL_LOUD. A fail-loud run is never
  keyed on a fallback.
- **Counterfactual protocol modes.** `5a_d3_aside`: the same resolver with its D-3
  promotion check made a no-op for the call (process-local, restored after; a test pins
  the restore). `executed`: keyed on `protocol_result.yaml: protocol_file` (else the
  prescreen's protocol) — what the backtest ran, not what the gate reads.
- **Memory, strict** — exactly what `regroup_record` would write: component errors via
  `campaign_memory.protocol_component_errors` (moved there verbatim from
  `run_phase1_research._protocol_component_errors`, which now delegates to it; variant
  `protocol_result.yaml` files included) → `build_fault_entry`; otherwise
  `build_memory_entry` (reader categories empty — proposals do not enter the key).
  Whatever it raises keeps the run out.
- **Memory, counterfactual** — the key-relevant helpers of `build_memory_entry`
  (`_variants_block`, `protocol_ref_of`, the card timeframe) with the grid requirement
  waived and a missing ledger `forecast_hash` **backfilled** with
  `novelty.forecast_hash_of_config` of the run's `candidate_strategy_config.json`. That
  value is fabricated for the replay: it is what the ledger writer would have computed
  from that file today, not what the ledger holds. The only hashed row in the whole
  ledger (run_060's prescreen row) does equal the replay's hash for run_060 — one data
  point, not a validation.
- **Self-consistency (counterfactual memory, 29 of 29).** Each entry's key equals the
  run's own candidate key on the protocol it executed. Both sides hash the same config
  file, so this checks symbols / timeframe / windows alignment only; it does **not**
  validate the backfilled hash.
- **Protocol content is today's file** (as live). Every parseable git revision of the
  protocols this corpus ran has the same windows hash, symbols and timeframe as today.
- **Old layer 2** — the retired 5a caller (`_route_post_variant_selection` before
  E-036 S2a) reproduced: the hypothesis card merged with `variant_selection.yaml`'s
  `variant_definition` where that file exists (none does in this corpus); ONE lookup at
  the selection's instrument(s)/timeframe, else `extract_instruments()[0]` /
  `extract_timeframes()[0]`; `backtest_spec.yaml`'s `config` for the fingerprint;
  precedence repeat > neighbour > first; the digest from earlier runs only. "Old refuse"
  counts `repeat` only. Layer 1 (KB) is replayed on neither side.
- **Fail loud.** An unreadable or malformed `campaign_state.yaml` aborts the replay. An
  unreadable run artifact is its own reason (`artifact_unreadable`), never "absent".

## 3. Every new REPEAT

PRIMARY and every 5a column: **none.**

`executed / counterfactual` only:

| run | repeats | same config? | same protocol? | genuine re-test? |
|---|---|---|---|---|
| run_027 | run_024:run_024 | yes — 0 differing leaves of 30 | executed yes (`baseline_v1.json`); at 5a no (an unloadable 4h escalation path) | **yes** — `protocol_result.yaml` results identical to run_024's apart from `run_id` |

Only two config hashes are shared by more than one keyed run (`config_hash_collisions`):
run_024/run_027 and run_017/run_036 (same config, different protocol — NOVEL). So no
convention could produce more than these from this corpus.

## 4. Spot-checks (both configs opened, leaf-by-leaf diff)

1. **run_027 vs run_024 — genuine re-test; at 5a the gate raises.** Identical
   `candidate_strategy_config.json` (0 of 30 leaves differ), results identical apart
   from `run_id`. run_027's card is `TIMEFRAME_ESCALATION_4H`; its
   `pipeline_state.yaml: last_error` is an `[Errno 22] Invalid argument` on
   `protocols\escalation_solusdt_Backtest RSI momentum, … .json` — a protocol file name
   built from the escalation prose. That is the path the resolver produced, so at 5a
   `novelty.load_protocol` raises (FAIL_LOUD). The backtest later ran the 1h baseline,
   and `verdict_interpretation.yaml` still reads the result as a 4h finding. The old
   check filed run_024 as `unclassified:position_sizing_timeframe_coupling` and run_027
   as `keltner_channel` (4h), so it never linked them.
2. **run_012 vs run_011 — old `repeat`; not a re-test.** 16 differing leaves: detector
   `smooth_period` 5 → 2, `default_regime`, the regime rules (a `vr >= 1.1` condition
   added, a `gte` rule turned into `between 0.9–1.1`), the transforms (`identity` →
   `ratio_to_mean`, `scale 10`, `threshold_filter 15`), a `vol_normalize` history
   transform. The old fingerprint ignores rule contents and transforms.
3. **run_034 vs run_033 — old `repeat`; not a re-test.** 4 differing leaves: ER
   threshold 0.5 → 0.35, `default_regime` unknown → trending, `lookback: 50` added, the
   `unknown` regime removed.
4. **run_032 vs run_025 — old `repeat`; not a re-test.** 2 differing leaves (ER
   threshold 0.3 → 0.5, `lookback: 500` removed). run_032's records also disagree on
   its protocol: `run_context.yaml` (`replication_diagnostic`) and `pipeline_state.yaml`
   say `baseline_v1.json`, `protocol_result.yaml` says `escalation_avaxusdt_4h.json`.
   The 5a resolver follows `run_context.yaml` (baseline); the `executed` columns follow
   `protocol_result.yaml`. Both give NOVEL.
5. **run_036 vs run_017 — same config hash, NOVEL (near-miss by protocol).** Identical
   configs; run_017 ran `baseline_v1.json` (1h), run_036 `diagnostic_btceth_4h.json`
   (4h, same windows). run_036 has no card, so it never enters memory.

## 5. Every run by outcome (PRIMARY)

- **NOVEL (5):** run_036 (`diagnostic_btceth_4h.json`), run_054 and run_057
  (`ts_trend_daily_v1.json`), run_059 (`funding_mr_daily_retest_v1.json`), run_060
  (`funding_mr_4h_retest_v1.json`).
- **FAIL_LOUD — `promotion_unratified` (32):** `baseline_v1.json` 25 (run_011–run_026,
  run_032–run_035, run_037, run_039, run_043, run_044, run_047);
  `escalation_solusdt_4h.json` 2 (run_028, run_029); `escalation_avaxusdt_4h.json` 2
  (run_030, run_031); `run_048_generated.json`, `run_050_generated.json`,
  `run_053_generated.json` 1 each.
- **FAIL_LOUD — `novelty_error` (1):** run_027.
- **UNKEYED — `no_candidate_config` (18):** card readable, no config (run_002–run_007,
  run_058); card unparseable (run_0001, run_008); brief only (run_038, run_040, run_045,
  run_046, run_049, run_051, run_052, run_055, run_056).
- **UNKEYED — `b10_no_evidence` (4):** run_009, run_010 (config, never executed),
  run_041, run_042 (`prescreen_backfill` ledger rows, no protocol path recorded).

Runs whose 5a protocol differs from the executed one: run_027 (unloadable escalation
path vs `baseline_v1.json`) and run_032 (`baseline_v1.json` vs
`escalation_avaxusdt_4h.json`).

## 6. Other findings

- **The E-039 S1 reruns are invisible to the gate.** For all 7 prescreen-killed runs,
  `runs/<run>/e039_s1_rerun/config.snapshot.json` hashes equal to the run's
  `candidate_strategy_config.json` (7 of 7); a tracked `protocol_summary.json` exists for
  5 of them (run_043, run_044, run_047, run_048, run_053). None has a memory entry in
  either column.
- **The hashed file is not always `backtest_spec.yaml`'s config** (correction (b)). Of the
  40 runs with both files, 35 hash identically and 5 do not — see §7.
- **Escalation and diagnostic protocols share the baseline's windows.** `baseline_v1`,
  both `escalation_*_4h` and `diagnostic_btceth_4h` have the same windows hash; only the
  timeframe (and, for the escalations, the symbols) tells them apart in the key.

## 7. Corrections to S1_FINDINGS_SLICE8.md (dated 2026-09-27; also appended there)

- **(a) The key's fourth field is not the raw `protocol_ref`.** It is
  `"windows:" + sha256 of the protocol file's windows`, with the file's own timeframe as
  the third field (`novelty.novelty_key` / `protocol_spec`; decide_next used the same
  before the S2a extraction). The memory stores `protocol_ref`; the key resolves it.
- **(b) `backtest_spec.yaml`'s config is not written verbatim.** The trial row and the
  gate hash `candidate_strategy_config.json`. Of the 5 corpus runs where the two differ,
  **only 2 are F4d's `significance_methodology` injection** (run_048, run_060). The other
  3: run_024 (the file's `unknown` regime is `null` where the spec had a zero-weight
  `BuyAndHoldStrategy` component — the file was edited after the spec), and run_036,
  run_037 (forced diagnostics: `backtest_spec.yaml` has no `config` at all; the config
  was placed in `candidate_strategy_config.json` directly).

## 8. Reproduce

```
python strategy-research/tools/replay_repeat_gate.py
```

Writes `engineering/roadmap/E-036/s2b_replay_result.yaml` (refuses an `--out` under
`--runs-dir`; absolute paths in quoted error messages are rewritten relative to the
repo). Tests: `tests/test_e036_s2b_corpus_replay.py`.
