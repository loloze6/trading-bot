# E-036 S2b — read-only corpus replay of the exact-match repeat gate (slice 8)

Measured 2026-09-27 on `feat/e036-s2b-corpus-replay` (branched from `origin/master` at
`b27e6ce9`, PR #226 merged). Script: `tools/replay_repeat_gate.py`. Machine-readable result:
`engineering/roadmap/E-036/s2b_replay_result.yaml` (one row per run, plus the totals below).
Read-only: no backtest, no market data, no API call, the holdout not opened; a file
listing with sizes and mtimes of `runs/` (8,791 entries) was identical before and after
every replay. `orchestrator.variant_anti_adjacency_gate` stays **off**; nothing here
recommends switching it on — that is the operator's call.

---

## What switching it on would have changed (read this first)

Across all 60 past runs, the new exact-match gate would have refused **one** run:
**run_027**. It was a true re-test: the same strategy config as run_024, on the same
1h protocol, with backtest results identical to run_024's line for line. run_027 was
meant to try that idea on 4h, but its 4h protocol could not be loaded (the protocol
file name was built from prose), so it quietly ran the 1h baseline instead, and its
verdict was then written up as a finding about 4h. The gate would have stopped it
before the backtest, as a repeat of run_024.

The three runs the old family check refused (run_012, run_032, run_034) are all
admitted by the new gate. Each one really differs from the run it was flagged
against: changed regime-detector thresholds or rules, changed transforms, and in one
case (run_032) a different coin and timeframe from what its card said. The old check
compared only a coarse outline of the config and the coins/timeframe written on the
card, so it saw repeats that were not there, and it missed run_027 because it filed
run_024 and run_027 under different families although their configs are identical.

Two limits matter for the decision. First, 22 of the 60 runs cannot be checked at
all (18 never got a strategy config, 4 have one but no record of which protocol they
would run), and only 29 runs could ever be in the gate's memory. The 7 runs the old
prescreen stopped are never in memory, so their configs — all 7 of which were later
re-run outside the pipeline (E-039 S1 reruns) — would not stop a future exact repeat. Second, this replay shows what the gate *would have* done had campaign
memory existed. It does not exist today: `regroup_record` has been off for this whole
corpus and old runs are never backfilled. Switched on now, the gate would start from
empty memory and compare only against runs recorded from then on.

---

## 1. Method

- **Order.** Runs in run-number order (`run_0001` … `run_060`), taken as chronological.
  Not independently checked against timestamps: `pipeline_state.yaml` carries only an
  `updated_at` (last change), not a start time. Each run is checked against the memory of **earlier** runs only
  (what the gate would have seen then), and — as live — with its own run id excluded
  (`novelty.match_index(..., exclude_run_id=run_id)`). Its own memory entry is added
  after its check.
- **One variant per run.** No run in this corpus has `artifacts/variants/index.yaml`,
  so each run has exactly one tested variant, named after the run (the memory's
  single-column shape). Runs = variants = 60.
- **New gate, candidate side** — exactly `run_phase1_research._repeat_gate_context` /
  `_check_variant_repeat`: `novelty.forecast_hash_of_config` of
  `artifacts/candidate_strategy_config.json` (the file `_compute_forecast_hash` and the
  trial row hash), the protocol file's `symbols` (read strictly),
  `anti_adjacency_gate.candidate_key`, then `anti_adjacency_gate.layer2_digest_check`.
  The protocol is the one the run executed (`protocol_result.yaml: protocol_file`); for
  a prescreen-killed run, the one it had resolved (`prescreen_result.yaml:
  protocol_version`) — the 5a gate sits before both.
- **New gate, memory side.** `campaign_memory.yaml` does not exist for this corpus, and
  `campaign_memory.build_memory_entry` cannot run on it: no run has
  `idea_status.yaml` / `grid_evaluation.yaml` (later machinery). The entry is therefore
  assembled in memory (never written) from the same helpers `build_memory_entry` uses
  for every field the key reads: `campaign_memory._variants_block` (symbols measured
  from `protocol_result.yaml` results, `forecast_hash` copied from the trial ledger's
  `backtest` row), `campaign_memory.protocol_ref_of`, and the card timeframe (fallback
  only). The key itself is `novelty.novelty_key` / `novelty.match_index` — no second key.
- **Declared deviation — the ledger hash is backfilled.** No `backtest` row in
  `campaign_state.yaml: trial_sharpes` carries a `forecast_hash` (the ledger holds 15
  rows: 3 `backtest`, 10 `prescreen`, 2 `prescreen_backfill`; only one row of all 15
  carries a hash). The missing hash is filled with
  `novelty.forecast_hash_of_config` of the run's `candidate_strategy_config.json` — the
  function and file `_record_backtest_trial` hashes. Evidence this is the same number:
  the ledger's only hashed row (run_060, a prescreen row) carries `4aa5c775…`, equal to
  the replay's file hash for run_060 (1 of 1). A test pins both paths to the same key
  (`test_replay_key_equals_the_live_gate_key_on_both_sides`).
- **Protocol content is today's file.** The key reads the protocol file's current
  `timeframe` and `windows`, as the live gate does. Measured: every parseable revision in
  git of the protocols this corpus ran (`baseline_v1.json`, `escalation_solusdt_4h.json`,
  `escalation_avaxusdt_4h.json`, `diagnostic_btceth_4h.json`, `ts_trend_daily_v1.json`,
  `funding_mr_daily_retest_v1.json`) has the same windows hash, symbols and timeframe as
  today, so reading today's file changes nothing here. `protocol_warnings` is empty: every
  memory entry's protocol resolved.
- **Self-consistency.** For all 29 memory entries, the key a later run would find the
  entry by equals the key the run itself was checked with (`self_inconsistent_runs: []`).
  So measured symbols always equalled the protocol's symbols — no blind spot of that kind
  in this corpus.
- **Old layer 2** (information only) — the retired family-grain check as its last 5a
  caller used it: `build_exclusion_digest.legacy_family_lookup` with the run's hypothesis
  card, `backtest_spec.yaml`'s `config` for the composition fingerprint (what the old
  call site read), every (instrument, timeframe) the card names, and the old
  multi-instrument precedence repeat > neighbour > novel. The digest is
  `scan_run_triples` over the corpus restricted to earlier runs. **"Old refuse" counts
  `repeat` only** — the one outcome that REFUSEd. `neighbour` ADMITted with a note and is
  shown separately.
- **Not replayed:** Layer 1 (the KB check) on either side. It is advisory in the new
  gate, and the KB is today's, not what each run saw.
- **Unkeyed runs** are reported with their reason and never dropped. A run with no
  (matchable) memory entry can never be matched — the safe direction, as live.

## 2. Counts

| | count |
|---|---:|
| Runs (run dirs) | 60 |
| Variants | 60 (one per run) |
| Keyed (new gate could check it) | 38 |
| Unkeyed — no `candidate_strategy_config.json` | 18 |
| Unkeyed — config, but no protocol recorded | 4 |
| **New REPEAT (refuse)** | **1** |
| **New NOVEL (admit)** | **37** |
| **Old refuse (`repeat`)** | **3** |
| Old admit — `neighbour` | 26 |
| Old admit — `novel` | 18 |
| Old not evaluable — no card | 11 |
| Old not evaluable — card unparseable (run_0001, run_008) | 2 |
| Memory entries (runs a later run could match) | 29 |
| Distinct config hashes among the 38 keyed runs | 36 |

**Agreement matrix, old (rows) × new (columns):**

| old \ new | REPEAT | NOVEL | UNKEYED | total |
|---|---:|---:|---:|---:|
| repeat (refuse) | 0 | 3 | 0 | 3 |
| neighbour (admit) | 1 | 21 | 4 | 26 |
| novel (admit) | 0 | 11 | 7 | 18 |
| not evaluable | 0 | 2 | 11 | 13 |
| **total** | **1** | **37** | **22** | **60** |

The two checks agree on **no** refusal: the old one refused 3 runs the new one admits,
and the new one refuses 1 run the old one admitted as a `neighbour`.

## 3. Every new REPEAT

| run | repeats | same config? | same protocol? | genuine re-test? |
|---|---|---|---|---|
| run_027 | run_024:run_024 | yes — 0 differing leaves of 30 | yes — `baseline_v1.json` (1h, BTCUSDT+ETHUSDT) | **yes** — `protocol_result.yaml` results identical to run_024's apart from `run_id` |

Only two config hashes are shared by more than one keyed run at all
(`config_hash_collisions`): run_024/run_027 (above) and run_017/run_036 (same config,
different protocol — NOVEL, see spot-check 5). So no protocol or memory convention
could have produced more than these two REPEATs from this corpus; in particular,
counting the 7 prescreen-only runs as tested would add none.

## 4. Spot-checks (both configs opened, leaf-by-leaf diff)

1. **run_027 vs run_024 — new REPEAT, genuine.** Identical `candidate_strategy_config.json`
   (0 of 30 leaves differ), both ran `protocols\baseline_v1.json`, results identical
   apart from `run_id`. run_027's card is `TIMEFRAME_ESCALATION_4H` (timeframe 4h); its
   `pipeline_state.yaml: last_error` shows the 4h protocol path failed (`[Errno 22]
   Invalid argument` on a protocol file name built from the escalation prose), and the run
   executed the 1h baseline. Its `verdict_interpretation.yaml` then reads the result as
   "Regime is uninformative at 4h timeframe" — a 4h conclusion drawn from a 1h re-run.
   The old check filed run_024 as `unclassified:position_sizing_timeframe_coupling` and
   run_027 as `keltner_channel`, so it never linked them (`neighbour` of run_021/022).
2. **run_012 vs run_011 — old `repeat`, new NOVEL; not a re-test.** 16 differing leaves:
   detector `smooth_period` 5 → 2, `default_regime`, the regime rules (a `vr >= 1.1`
   condition added, a `gte` rule turned into `between 0.9–1.1`), the component's
   transforms (`identity` → `ratio_to_mean`, `scale 10`, `threshold_filter 15`) and a
   `vol_normalize` history transform. The old fingerprint ignores rule contents and
   transforms.
3. **run_034 vs run_033 — old `repeat`, new NOVEL; not a re-test.** 4 differing leaves:
   ER threshold 0.5 → 0.35, `default_regime` unknown → trending, `lookback: 50` added,
   the `unknown` regime removed. A refinement, correctly new.
4. **run_032 vs run_025 — old `repeat`, new NOVEL; not a re-test.** 2 differing leaves
   (ER threshold 0.3 → 0.5, `lookback: 500` removed) **and** a different protocol:
   run_032 ran `escalation_avaxusdt_4h.json` (AVAXUSDT, 4h), while its card says
   BTCUSDT/ETHUSDT 1h — the old check matched on the card's triple, not on what ran.
5. **run_036 vs run_017 — same config hash, NOVEL (near-miss by protocol).** Identical
   configs (0 of 30 leaves differ); run_017 ran `baseline_v1.json` (1h), run_036
   `diagnostic_btceth_4h.json` (4h, same windows). A different test, correctly admitted.
   run_036 also has no hypothesis card, so it never enters memory.

## 5. Unkeyed and unmatched runs, by reason

**Unkeyed as candidates (22):**

- `no_candidate_config` (18):
  - card readable, no config — the idea never reached `backtest_specification` (7):
    run_002, run_003, run_004, run_005, run_006, run_007, run_058;
  - card unparseable YAML, no config (2): run_0001, run_008;
  - no card and no config — the run stopped at or before the brief (9): run_038,
    run_040, run_045, run_046, run_049, run_051, run_052, run_055, run_056.
- `no_protocol_recorded` (4) — a config exists but neither `protocol_result.yaml` nor
  `prescreen_result.yaml` names a protocol: run_009, run_010 (never reached execution),
  run_041, run_042 (their ledger rows are `prescreen_backfill`, rebuilt from
  `verdict_interpretation.yaml`; no protocol path was recorded).

**Keyed as candidates but never in memory (9)** — later runs can never match them:

- prescreen stubs, `not_backtested (prescreen_stub)` (7): run_043, run_044, run_047,
  run_048, run_050, run_053, run_060;
- no hypothesis card, which `build_memory_entry` requires (2): run_036, run_037.

**No memory entry, by reason (all 31):** no card 11, unparseable card 2, no
`protocol_result.yaml` 11, not backtested 7. The other 29 runs (run_011–run_035,
run_039, run_054, run_057, run_059) are the gate's whole memory.

## 6. Other findings

- **The E-039 S1 reruns are invisible to the gate.** For all 7 prescreen-killed runs,
  `runs/<run>/e039_s1_rerun/config.snapshot.json` hashes equal to the run's
  `candidate_strategy_config.json` (7 of 7 measured) — those exact configs were re-run
  later, outside the pipeline (a tracked `protocol_summary.json` exists for 5 of them:
  run_043, run_044, run_047, run_048, run_053). None has a memory entry, so a new
  pipeline run of any of those configs would be admitted as NOVEL.
- **The hashed file is not always `backtest_spec.yaml`'s config** (correction (b) below).
  Of the 40 runs with both files, 35 hash identically and 5 do not: run_048 and run_060
  (F4d added `significance_methodology`), run_024 (the file's `unknown` regime is `null`
  where the spec had a zero-weight `BuyAndHoldStrategy` component — edited after the
  spec), run_036 and run_037 (`backtest_spec.yaml`'s `config` is not a mapping).
- **Escalation and diagnostic protocols share the baseline's windows.** `baseline_v1`,
  both `escalation_*_4h`, and `diagnostic_btceth_4h` have the same windows hash; only the
  timeframe (and for the escalations, the symbols) tells them apart in the key.

## 7. Corrections to S1_FINDINGS_SLICE8.md (dated 2026-09-27, found in S2a, measured here)

Also recorded at the end of `S1_FINDINGS_SLICE8.md`.

- **(a) The key is not the raw `protocol_ref`.** S1 (§2 "Key", guess 2, Decision 2) gives
  the key as `(forecast_hash, sorted(symbols), timeframe, protocol_ref)` with
  `protocol_ref` = `protocol_result.yaml`'s `protocol_file`. The key actually used — by
  decide_next before the S2a extraction as well — is
  `(forecast_hash, sorted(symbols), <protocol file's timeframe>, "windows:" + sha256 of the protocol file's windows)`
  (`tools/novelty.py::novelty_key`, `protocol_spec`). The memory *stores* `protocol_ref`;
  the key resolves it to what the file tests, so two runs on differently-named generated
  protocols with the same windows and timeframe match, and the card timeframe is only the
  fallback when the file cannot be read (then the key is `unresolved:<ref>` and never
  matches).
- **(b) `backtest_spec.yaml`'s config is not written verbatim.** S1 (§1 "Readers") says
  the 5a call site reads `backtest_spec.yaml`'s own `config` as the candidate config. Before
  `candidate_strategy_config.json` is written, `run_loop` (F4d) injects
  `machine_constraints.significance_methodology` into it; the trial row's `forecast_hash`
  and the S2a gate both hash `candidate_strategy_config.json`, not the spec's config.
  Measured: 5 of 40 corpus runs differ between the two (§6).

## 8. Reproduce

```
python strategy-research/tools/replay_repeat_gate.py
```

Writes `engineering/roadmap/E-036/s2b_replay_result.yaml` (refuses an `--out` under
`--runs-dir`). Tests: `tests/test_e036_s2b_corpus_replay.py` (synthetic corpus: known
repeats, a one-parameter near-miss, a different-protocol near-miss, every unkeyable
reason, run-number ordering, prescreen stubs never in memory, the old side, a corpus
listing + mtimes unchanged by the CLI, and the replay key equal to the live gate's
recorded key and to a memory entry written by the real writers).
