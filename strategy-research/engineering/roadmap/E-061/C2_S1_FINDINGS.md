# E-061 C2 — S1 findings: the five vision fixes (characterize-and-STOP)

**Scope.** `delivery_plan_v26_continuation.md` C2 (C2.1–C2.5). Read-only: no code, no config, no
backtest, no network. Base: master `9900dee3`. Every `file:line` below was read on that commit.
Paths are relative to `strategy-research/`. `rpr` = `workflow/run_phase1_research.py`,
`vce` = `tools/verdict_criteria_evaluator.py`, `dn` = `tools/decide_next.py`,
`cm` = `tools/campaign_memory.py`.

**Binding decisions used (not re-asked, rule 10):** D-003 (readers see all variants), D-004 (branch 3
passes iff any one variant clears every bar), D-014 (FAIL dominates INCONCLUSIVE, confirmed),
D-015 (a crashed variant can never validate), D-016 (one coin per variant; the coin is a backtest
input, not a config field), D-017 (distance per card I), D-020 + D-034..D-039 (profit-bar bases
and values), cards C, D, E, I, J, K.

**One measurement taken (read-only, in memory, `build_reports(..., write=False)` on three tracked
runs):** report sizes in characters, per run (each run backtests 2 coins, one config):

| run | profitability | trade_efficiency | forecast_power | regime_power | component_attribution |
|---|---|---|---|---|---|
| run_054 | 37,047 | 74,490 | 12,721 | 35,566 | **1,663,960** |
| run_057 | 35,764 | 27,508 | 12,720 | 35,062 | **1,656,827** |
| run_059 | 120,019 | **438,573** | 41,108 | 106,945 | **912,333** |

Every reader prompt inlines its report in full (`rpr:865-872`, `_build_stage_prompt`). This
matters for C2.2 (see Guess 7).

---

## Guesses for the operator

SMALL = taken on my recommendation tonight. BIG = parked for you (changes the roadmap's intent or
spends money/trials). Only one BIG, and it rarely bites.

| # | Guess | Size | Blocks the build? | Recommendation |
|---|---|---|---|---|
| G1 | **Where the coin lives.** Each `variant_patches.yaml` entry gains `kind: base\|design\|asset` and `symbol: <SYMBOL>`. Step 5a copies both into `artifacts/variants/index.yaml` and writes a per-variant protocol `artifacts/variants/<id>/protocol.json` = the run's protocol with `symbols: [<symbol>]` (and `exchange` set from that coin's `coin_universe.yaml` entry). The data gate, `run_protocol.py`, the repeat gate and the residual-IC composite all read that file. `run_protocol.py` and `data_availability_gate.py` are **not** changed. | SMALL | blocks the build | Yes. Alternative (a `--symbols` flag on both tools) touches two tool CLIs and the composite runner for the same effect. |
| G2 | **Which coin is the base.** Base coin = the run protocol's `symbols[0]`, set by code. `base` and every `design` variant must use it; other protocol symbols are unused under `variant_loop` (logged). | SMALL | blocks the build | Yes. Keeps decide_next's novelty/cost prediction (`dn:1322`, base symbols) deterministic. |
| G3 | **What an asset variant is.** Empty config patch + a different coin: "one field changed" (card D/K) is the coin. The coin must be in `coin_universe.yaml`, in a **different category** from the base coin, and pass the Layer-1 coverage precheck (`data_availability_gate.layer1_price_precheck`, no network) for every protocol window. Its venue follows its `coin_universe.yaml` `exchange` key (today every non-`store_of_value` coin is `exchange: kraken`). | SMALL | blocks the build | Yes. |
| G4 | **Cross-sectional ideas (variant = whole universe).** Not built in C2. A multi-coin variant is refused at the Step 2 check for forecast ideas: `run_protocol.py` backtests each coin independently (`tools/run_protocol.py:2108-2137`) — there is no cross-coin ranking in the engine — and the menu forbids overriding `symbol_reducer` (`config/criterion_menu.yaml:42-44, 75-81`). Contract reserved for a later ticket: `symbols: [...]` + card `cross_sectional: true` + a declared reducer. **Composition runs are exempt**: their variants are weighting schemes and keep the protocol's full symbol list (the instrument set stays C5.3's question). | SMALL | default is safe | Yes. |
| G5 | **Profit bars with one coin per variant.** A variant's "equal-weight portfolio of tested coins" (D-020, D-034..D-037) is that one coin. Branch 3 stops the loop if any single variant — including the asset coin — clears every bar (D-004). No branch-3 code change; C3's S1 is told. | SMALL | default is safe | Yes (this is the plan's own "likely" reading). |
| G6 | **DSR trial dedupe must see the coin.** The asset variant has the base's exact config, so the same `forecast_hash`. Both DSR paths dedupe on `(forecast_hash, source)` (`tools/deflate_sharpe.py:174-184`; `rpr:9689`, `_dedupe_trials`, lockstep-tested), so the asset variant's trial would **silently collapse onto the base's** and N would undercount — against card D ("every tested variant counts as one attempt"). Fix: trial rows written by the variant loop carry `symbols`; both dedupe paths key on `(forecast_hash, sorted symbols or None, source)`. Rows without the field key exactly as today (byte-identical DSR on the existing ledger). | SMALL | blocks the build | Yes. It preserves card D's intent; not fixing it is the change of intent. Flagged loudly because it touches the trial ledger. |
| G7 | **Reports must be compacted before they go per-variant.** Measured above: `component_attribution` is 0.9–1.7 MB and `trade_efficiency` up to 0.44 MB per run, because both copy every per-bar / per-trade record three times (per window, regime, symbol: `tools/build_reports.py:294-296, 623-634`). Inlined, that is up to roughly 400k tokens for one reader call — over the model's context. Today under the variant loop these reports are silently near-empty (wrong paths, A3 §3.4), which hides the problem; C2.2 fixing the paths would expose it. Replace raw record lists with per-slice aggregates (n, mean, median, p10, p90 per metric), add a size budget per report (test + a fail-loud guard, never silent truncation). This is new computation in `build_reports.py`, whose docstring promises re-projection only (`tools/build_reports.py:33-58`). | SMALL | blocks the build (C2.2) | Yes. Card step 7 says "code computes five focused reports". |
| G8 | **Per-variant report shape.** `schema_version: 2`; `variants: {<vid>: {kind, symbol, status, slices}}`; a failed or not-tested variant is `{unavailable: true, reason}`; no separate base-only top-level `slices` (saves tokens). | SMALL | default is safe | Yes. |
| G9 | **What a "block type" is (card I).** `(kind, sorted component classes in the block's config fragment, timeframe_category)`. Code writes `artifacts/registry_summary.yaml` before the readers: one row per registered block (id, kind, component classes, timeframe, category, symbols_tested, residual IC, correlation to composite), this run's own block type and whether it is already present, the registered blocks it neighbours, and this run's measured correlation to the composite per variant when `artifacts/residual_ic.yaml` exists. Grouped by type past 50 rows. | SMALL | blocks the build (C2.3) | Yes. |
| G10 | **Distance anchors (card I).** 3 = the block type is not in the registry AND (measured \|corr to composite\| < 0.3, or no composite exists yet). 2 = type not in the registry, correlation 0.3–0.6 or not measurable (a `new_block` sketch). 1 = same component classes as a registered block but a different timeframe category or kind, or \|corr\| ≥ 0.6. 0 = a patch on an idea that is itself a registered block, or the same block type as a registered one. 0.3 / 0.6 are rank-only placeholders (they never touch idea status or the holdout). `rubric_version` → `<category>-reader-v2`. `confidence_real` and `mechanism_plausibility` anchors unchanged (mechanism drift, A2 I.4, is a separate ticket). decide_next unchanged. | SMALL | blocks the build (C2.3) | Yes. |
| G11 | **Crashed-variant column.** The grid gets a column for every variant that was `validated` going into protocol_execution. A variant with no graded result gets, in every criterion row, `{result: INCONCLUSIVE, not_graded: true, reason: "backtest_failed: ..."}`; top-level `failed_variants: {<vid>: reason}`. With D-014: a genuine FAIL on another variant still refutes; otherwise the idea is at best `inconclusive`. Every consumer that reads "grid column = tested" switches to "column not in `failed_variants`". Trial rows unchanged. | SMALL | blocks the build (C2.4) | Yes. |
| G12 | **Variant shape and its failure path (C2.5).** Step 2 must write 3 or 4 variants: exactly one `base` (id `base`, empty patch), at least one `design` (non-empty patch, base coin), exactly one or two `asset` (empty patch, G3 rules); composition runs exempt. A violation re-runs Step 2 **once** with the error (the `_route_block_manifest_check` precedent, `rpr:11664-11683`); a second failure pauses with a new flag `variant_shape_invalid` (RUNBOOK row) — not a raise. A 5a failure on one variant that is not a missing class (patch does not apply, unresolved manifest path, another V-code) takes the same retry, then pauses `variant_config_error`. The data-gate floor of 3 then only ever sees data losses; its park/pause stays as today. | SMALL | blocks the build (C2.5) | Yes. |
| G13 | **Asset coin that cannot cover the windows.** If no coin of another category covers the protocol's whole window set, may the asset variant run on only the windows its coin covers? That changes card E ("the protocol owns the windows", same for every variant). **Default until you decide:** full coverage is required; the Step 2 check refuses such a coin; if no eligible coin exists the idea parks `waiting_for_data`. Rarely bites today: XRP (payment, Kraken, from 2017-05 per `config/coin_universe.yaml`) covers any window from 2018 for a BTC/ETH base. | **BIG** | default is safe | Park. |
| G14 | **Diagnostics without a validation protocol.** Under config-direct nothing writes `validation_protocol.yaml`, so `run_protocol.py` writes `hypothesis_verdict: null` (`tools/run_protocol.py:2288-2296`): the diagnostics block (cost drag, gross PnL, forecast/return correlation) is computed only inside `evaluate_against_decision_rules` (`:1593`). Then `profitability.yaml`/`forecast_power.yaml` `overall` slices read "unavailable", the profitability reader's Rules 1 and 5 have no inputs, and trial rows lose `expectancy_bps`. **Recommendation:** C1.3 takes the "teach `run_protocol.py` it is optional" branch and still computes the diagnostics block with an empty rule set. If C1.3 is already merged the other way, S2d does it. | SMALL | blocks C2.2's usefulness, not its build | Coordinate with the C1.3 owner. |
| G15 | **Tie-break citation.** Cite D-014 (`engineering/DECISION_LOG.md`) at `vce:1055`, `vce:1640-1641` and `tests/test_grid_evaluation.py:247`. | SMALL | default is safe | Yes. |

---

## C2.1 — One coin per variant (D-016; cards C, D, E)

### Today: how coins flow (file:line)

1. **Brief → protocol.** `machine_constraints.protocol.symbols` is copied verbatim into a generated
   protocol (`rpr:7660-7715`, `_ensure_protocol_from_constraints`; `symbols` at `:7678`,
   `protocol_obj` at `:7689-7697`), or `machine_constraints.protocol_ref` pins an existing file whose
   `symbols` are used as is (`rpr:7895-7957`). `_resolve_protocol_path` (`rpr:7960`) returns that one
   run-level file for every consumer, after `_assert_promotion_ratified` (`rpr:7742-7795`).
2. **Variants.** Step 2 writes `variant_patches.yaml`: `{variant_id, patch: [{path, value}],
   rationale}` (`workflow_artifacts/skills/innovation-expansion/SKILL.md:237-257`). No coin field.
   The skill asks for the asset variant as "a patch changing whatever config path encodes the traded
   symbol" (`SKILL.md:268-271`), yet no such path exists (`docs/STRATEGY_DESIGN_GUIDE.md:396`, §7a
   "PROPOSED, NOT BUILT"), and its own example "asset" patch edits
   `/regime_detector/components/0/params/period` (`SKILL.md:251-256`). IMPROVEMENT 06 asks for two
   candidate coins from another `coin_universe.yaml` category (`SKILL.md:124-170`) but only as prose
   in `innovation_notes.yaml` — nothing downstream reads them. Step 2 receives `coin_universe.yaml`
   through the closed-book inputs (`rpr:2313-2317`) but not the protocol's coins or windows.
3. **5a (tool).** `rpr:2029-2217` applies each patch to the base config, validates it
   (`validate_config.py`), checks manifest paths, writes `artifacts/variants/<id>/strategy_config.json`
   and `artifacts/variants/index.yaml` (`{status, config_path, reason, report}` per variant,
   `:2193-2203`). No coin anywhere.
4. **Repeat gate (5a).** `_repeat_gate_context` (`rpr:6765-6831`) takes `symbols` once, from the run
   protocol (`:6805`, `:6824`); `_check_variant_repeat` (`:6834-6848`) keys every variant on those same
   symbols.
5. **Data gate, per variant.** `rpr:1326-1455`: one run-level `protocol_path` (`:1356`) passed to every
   variant's `data_availability_gate.py` call (`:1372-1377`); the tool checks every `symbol × window`
   of that protocol (`tools/data_availability_gate.py:677-699`).
6. **protocol_execution, per variant.** `rpr:1493-1789`: same run-level `protocol_path` (`:1542`) for
   every variant (`cmd` `:1579-1584`); `run_protocol.py` then runs `for symbol in symbols: for window
   in windows` (`tools/run_protocol.py:1968, 2108-2137`). Trial id `f"{run_id}:{variant_id}"`
   (`rpr:1551`).
7. **Grid.** One column per surviving variant (`rpr:1743-1750`); `symbol_reducer: null` pools every
   coin in the column (`vce:1500-1536`; menu fixes `symbol_reducer: null`, not card-overridable,
   `config/criterion_menu.yaml:42-44, 75-81`).
8. **Residual IC (composition_runs).** `_residual_ic_grid_inputs` (`rpr:3862-3917`) →
   `composite_cache.residual_ic_by_variant` (`tools/composite_cache.py:370-420`), which **raises if the
   variants read different market data** (`:392-397`) and runs the composite once on the run protocol's
   coins (`composite_series`, `:283-367`, data-fingerprint check `:346-349`).
9. **Memory, novelty, registry.** Memory measures each tested variant's `symbols` back from its own
   `protocol_result.yaml` (`cm:174-189, 273-275`) — already per variant. The novelty key is
   `(forecast_hash, sorted symbols, timeframe, window_set)`, where timeframe and window set come from
   the protocol file's content, never its path (`tools/novelty.py:111-167`). The registry records
   `symbols_tested` as information only (`tools/block_registry.py:251-252, 262`; any-coin eligibility,
   card F).
10. **decide_next.** A patch candidate's coins are its source run's base-variant coins (`dn:1322`), used
    for its novelty key (`dn:1388`) and cost (`n_windows × N_VARIANTS × len(symbols)`, `dn:1411`). The
    candidate brief copies the source's `machine_constraints` minus `pass_rule` (`dn:1792-1794`), so it
    inherits the same protocol. Composition briefs take the pinned validating run's
    `machine_constraints` (`dn:1195-1270`).

### What the decisions already settle (no question)

- The coin is a backtest input, not a config field (D-016) → it lives on the variant entry, never in
  `strategy_config.json`.
- Asset variation = a coin from a different category (card D). Default one symbol per variant; a
  reducer only for cross-sectional ideas (card C).
- Every tested variant is one attempt (card D) → the DSR dedupe must not merge base and asset (G6).
- Branch 3 passes iff any one variant clears every bar (D-004) → per-variant single-coin grading (G5).

### Proposed contract (minimal)

**`variant_patches.yaml` entry** (Step 2 writes; code checks, G12):

```yaml
- variant_id: base            # required id for kind base
  kind: base                  # base | design | asset
  symbol: BTCUSDT             # base/design: must equal the run protocol's symbols[0] (G2)
  patch: []
  rationale: "..."
- variant_id: <design_name>
  kind: design
  symbol: BTCUSDT
  patch: [{path: ..., value: ...}]   # non-empty
  rationale: "..."
- variant_id: <asset_name>
  kind: asset
  symbol: XRPUSDT             # coin_universe.yaml, other category, covers every window (G3)
  patch: []                   # the coin is the one change
  rationale: "..."
```

**5a (`rpr:2029-2217`), only under `variant_loop`:** after a variant validates, write
`artifacts/variants/<id>/protocol.json` = the run protocol (from `_resolve_protocol_path`) with
`symbols: [symbol]` and, when the coin's `coin_universe.yaml` entry names an `exchange`, that
exchange; windows, timeframe, holdout and promotion byte-equal to the source. Add to the index entry:
`kind`, `symbol`, `protocol_path`. `cm:100-101` (`_INDEX_STATUSES`, `_INDEX_KEYS`) must accept the
three new keys, or `campaign_memory` raises "unknown key(s)" (`cm:227-229`).

**Consumers switch to the variant's protocol when the index entry has one:**
data gate loop (`rpr:1356, 1372-1377`), protocol_execution loop (`rpr:1542, 1579-1584`), repeat gate
(`_check_variant_repeat` gets the variant's `[symbol]`; the run-level `ctx["symbols"]` stays for
`variant_loop` off), residual IC (`residual_ic_by_variant` groups variants by symbol set and runs one
composite per group on that group's protocol file; the cache key already includes the protocol sha,
`tools/composite_cache.py:314`, so per-coin caches separate naturally).

**Trial rows (G6):** `_record_backtest_trial` / `_record_failed_backtest_trial` (`rpr:8973`, `:9075`)
add `symbols` when called from the variant loop; `deflate_sharpe.deduplicate_trials`
(`tools/deflate_sharpe.py:125-186`) and `rpr:_dedupe_trials` (`:9689`) key on
`(forecast_hash, tuple(sorted(symbols)) if present else None, source)`. The lockstep test pins both.
Review `tools/killed_run_gate.py:248` ("distinct hashes per G2") for the same assumption.

**Step 2 inputs:** `_CLOSED_BOOK_STAGE_INPUTS["innovation_expansion"]` (`rpr:2313-2317`) gains an
injected context block: base coin, its category, the protocol's timeframe and first/last window
dates, and the earliest data date per eligible coin (from `config/venue_data_capability.yaml` and
`coin_universe.yaml`). Skill: IMPROVEMENT 06/07 rewritten (the asset example becomes empty patch +
`symbol`; the "patch the symbol path" sentence removed).

**Composition runs:** `_composition_variant_patches` (`rpr:4128-4135`) writes no `symbol`; 5a writes
no per-variant protocol; every composite variant runs the run protocol's full symbol list (G4).

### Consequences (stated, not asked)

- **Profit bars (G5).** `_portfolio_profit_metrics` (`rpr:10544-10649`) builds the portfolio from the
  coins in the variant's own `protocol_result` → one coin. Sharpe (median of per-coin medians), trade
  floor (worst coin), DSR, drawdown and B&H (C3) all become that coin's. `_evaluate_profit_bars_every_backtest`
  (`rpr:10676-10743`) is unchanged. **Branch 3 can now stop on a single coin that is not in the
  campaign's target set** (the asset coin); `target_instrument_set` is still unread (C5.3). That is
  D-004 as decided; the operator sees the coin at the `profit_bars_reached` stop.
- **Grid sample floors.** A column now holds one coin's windows instead of two pooled coins, so
  per-cell floors are reached with half the data: expect more INCONCLUSIVE cells than a two-coin
  protocol gave. Correct under card C, but it will show in the first real runs.
- **Novelty.** Asset variant key = (base config hash, [asset coin], tf, windows) — novel unless that
  config already ran on that coin. decide_next's predicted key for a patch candidate uses the source
  base coin (`dn:1322`) = the new run's base coin under G2, so prediction and 5a agree.
- **decide_next cost** falls to `n_windows × 3 × 1` for a run on a two-coin protocol — now correct.
- **Composites / registry.** No change: any-coin eligibility (`tools/block_registry.py:40-43`);
  `symbols_tested` becomes base coin + asset coin.
- **Venue and cost.** The asset coin will usually be Kraken, USD-quoted. `run_protocol.py` resolves
  fees per symbol with a `default` fallback (`tools/run_protocol.py:259-295`), not per venue, so the
  asset variant is costed at the default fee. Noted, not fixed here.
- **Data.** Aux feeds are per symbol (`tools/data_availability_gate.py:601-627`); a funding-rate idea's
  asset variant may lose to data → the idea parks `waiting_for_data` (card J), as intended.

### What breaks (to fix inside the slice)

`cm._INDEX_KEYS` (new keys) · `residual_ic_by_variant`'s single-fingerprint raise ·
DSR dedupe (G6) · `innovation-expansion/SKILL.md` asset example · `_repeat_gate_context`'s run-level
symbols · tests that pin the index shape or the per-variant `cmd`
(`tests/test_e033_slice4a_variant_loop.py`, `tests/test_e033_slice4b_*`, `tests/test_e036_*`).

### Flags

No new flag. Everything above runs only under `orchestrator.variant_loop` (which requires
`config_direct_authoring`); `variant_loop` off keeps the run-level protocol and writes no
`protocol.json` (byte-identical). G6's dedupe key change is byte-identical for every existing ledger
row (no `symbols` field). The skill text change is prompt-only and is read only when
`artifacts/backtest_spec.yaml` is present (config-direct).

### Tests

- 5a writes `variants/<id>/protocol.json` with `symbols: [coin]`, `exchange` from `coin_universe.yaml`,
  and windows/timeframe/holdout/promotion byte-equal to the run protocol; index carries
  `kind/symbol/protocol_path`; `campaign_memory` accepts it.
- Data gate and `run_protocol.py` argv carry the per-variant protocol path (monkeypatched subprocess).
- Repeat gate: asset variant with the base's config hash is NOVEL against the base's memory entry;
  REPEAT when the same config already ran on that coin.
- DSR: base + asset rows with the same `forecast_hash` and different `symbols` both count; legacy rows
  without `symbols` dedupe exactly as today (lockstep test extended on both paths).
- Residual IC: two coin groups → two composites, no `CompositeError`.
- `variant_loop` off: no `protocol.json`, argv unchanged (byte-identity).
- Composition mode: variants keep the protocol's symbols.
- **C1.1 extension** (`tests/test_e061_end_to_end_wiring.py`): run 1 has base BTC, design BTC, asset
  XRP; the stubbed `run_protocol` asserts it received `variants/<id>/protocol.json` and writes results
  for exactly that coin; memory records one coin per variant; run 2's decide_next candidate has cost
  basis `windows × 3 × 1`.

---

## C2.2 — Experts see every variant (D-003)

### Today

- `build_reports.load_run_sources(run_dir)` reads only `artifacts/protocol_result.yaml` (the base copy,
  `rpr:1622-1624, 1685`), `RUN_DIR/trade_diagnostics.json` and `RUN_DIR/results/<window_run_id>/bars.csv`
  (`tools/build_reports.py:194-223`). Under the variant loop, `run_protocol.py` writes those under
  `--out-dir` = `RUN_DIR/variants/<id>/` (`rpr:1576-1583`; `tools/run_protocol.py:2096, 2207`), so the
  trade and bar slices come out "unavailable" without error (A3 §3.4). The call is
  `_br.build_reports(RUN_DIR, write=True)` at `rpr:1775` (variant loop) and `rpr:1955` (flag off).
- Each reader's handoff lists only `artifacts/reports/<category>.yaml` and `grid_evaluation.yaml`
  (`rpr:3240-3261`); both are inlined in full (`rpr:865-872`).
- The five SKILLs describe a single-run report shape (e.g. `readers/profitability-reader/SKILL.md:36-54`)
  and forbid reading anything else (`:190-208`).
- Size: see the measurement table at the top. The two raw-record builders are
  `build_trade_efficiency_report` (`tools/build_reports.py:279-307`, every trade × 3 groupings) and
  `build_component_attribution_report` (`:594-641`, every bar × component × 3 groupings).

### Proposed change

1. **Compaction first (G7).** trade_efficiency and component_attribution slices become aggregates per
   group (n, mean, median, p10, p90 of each numeric field; component attribution per component).
   profitability/forecast_power/regime_power keep their per-window rows (one coin per variant roughly
   halves them). A module constant `REPORT_CHAR_BUDGET` per report; `build_reports` raises if a built
   report exceeds it (fail loud; `_sr_errors` then fails protocol_execution after the trial rows, as
   today `rpr:1781-1789`).
2. **Variant-aware build (G8).** `build_reports(run_dir, write=True, variants=None)`. `variants=None`
   keeps today's single-run behaviour. The variant-loop call site passes
   `{vid: {kind, symbol, status, reason}}` from `index.yaml` plus the grid's `failed_variants` (C2.4);
   sources per tested variant come from `artifacts/variants/<vid>/protocol_result.yaml`,
   `variants/<vid>/trade_diagnostics.json`, `variants/<vid>/results/<wid>/bars.csv`. Output per report:
   `schema_version: 2`, `variants: {<vid>: {kind, symbol, status, slices}}`, not-tested and failed
   variants as `{unavailable: true, reason}`.
3. **Reader SKILLs (all five).** New "Report shape" section for `variants:`; evidence paths become
   `variants.<vid>.slices...`; one added rule: a result that holds on `base` and `design` but not on
   `asset` is coin-specific evidence (cite both); proposals still patch the **base** config (decide_next
   resolves patches against the source base config, `dn:1345-1362`). The "optional grid" wording stays.
4. **Diagnostics (G14)** — without them the `overall` slices are empty under config-direct.

### Prompt-size impact

Five readers, one call each, each reading one report covering all variants (not 5 × N calls). With
compaction and one coin per variant, a report is expected to be about 1.5× today's per-window size for
the profitability/forecast/regime reports (3 variants × 1 coin vs 1 run × 2 coins) and bounded by the
budget for the other two. Token budget unchanged (`_check_reader_budget`, `rpr:3330-3337`).

### Flags

Under `category_reports` + `variant_loop` (the variant-loop call site). Compaction also changes the
single-run reports produced under `category_reports` with `variant_loop` off; `category_reports` is
off by default and has never run for real, so default runs are byte-identical. Readers' SKILL text is
read only under `specialist_readers`.

### Tests

- `build_reports(run_059, write=False)` stays under the budget for every report (tracked fixture).
- Variant build: three variant dirs → `variants.{base,design,asset}` populated with the right symbol;
  a failed variant and a not-tested variant are `unavailable` with their reasons.
- `variants=None` output equals today's for the non-compacted reports (profitability, forecast_power,
  regime_power).
- Budget guard raises on an oversized synthetic report.
- `tests/test_e046a_slice5b_i_reader_skills.py` extended: every SKILL mentions `variants.` and keeps
  its scope rules.
- **C1.1 extension:** each reader prompt (captured at the stubbed `_invoke_reader_llm`) contains all
  three variant ids and is under the budget.

---

## C2.3 — "Distance to profitable" per card I (D-017)

### Today

- Card I: "3 = fills a missing block type with low correlation to the registry; 0 = neighbour of
  something already validated". The five reader rubrics score closeness to a rule threshold instead:
  `profitability-reader/SKILL.md:172-177`, `trade_efficiency-reader/SKILL.md:150`,
  `forecast_power-reader/SKILL.md:143`, `regime_power-reader/SKILL.md:165`,
  `component_attribution-reader/SKILL.md:177`. `rubric_version` is free text (`*-reader-v1`); nothing
  reads it except to copy it (`dn:1434`, `rpr:6181-6184`, `tools/reader_proposals.py:63-65`).
- Readers cannot see the registry: their handoff has two inputs (`rpr:3254-3257`).
- The registry holds per block `kind`, `config_fragment`, `symbols_tested`, and — only under
  `composition_runs` — `timeframe`, `timeframe_category`, `residual_ic`, `correlation_to_composite`
  (`tools/block_registry.py:72-79, 170-209, 253-271`). There is no "block type" field anywhere; the
  component classes can be read from a fragment the way `dn:467-478` (`_component_classes`) reads a
  config.
- Ranking: `rank_key` = confidence desc, distance desc, cost asc (`dn:1574-1580`).

### Proposed change

1. **Registry summary (G9)**, a small pure function (e.g. `block_registry.registry_summary(doc,
   run_dir)`) called by `_run_specialist_readers_stage` before the first reader, written to
   `artifacts/registry_summary.yaml`, and added to every reader handoff's `required_inputs`
   (`rpr:3254-3257`). It reads only `campaign_record/block_registry.yaml` (past runs' validated
   blocks), this run's `block_manifest.yaml` + base config, and `artifacts/residual_ic.yaml` if present.
2. **Rubric (G10)** in all five SKILLs: the distance column rewritten per card I; the scope rules add
   `registry_summary.yaml` as the one extra allowed input; `rubric_version` → `<category>-reader-v2`.
3. **decide_next unchanged.** It ranks the same keys; only the meaning of the number changes.

### No lookahead, no overload

The summary is built from blocks validated by earlier runs and from this run's own already-finished
backtest. Every registry number comes from protocol windows that `run_protocol.py` asserts end before
the holdout starts (`tools/run_protocol.py:2113-2128`); the composite cache also refuses the sealed
range (`tools/composite_cache.py:199-240`). No future data can enter. Size: one short row per block;
grouped by type beyond 50 rows, so it stays a few thousand tokens.

### Flags

Only under `specialist_readers` (the only path that calls readers). No flag-off effect.

### Tests

- `registry_summary` on an empty registry, one block, a neighbour case (same component classes), a
  different timeframe category; this run's own type flagged present/absent correctly.
- Reader handoff lists `artifacts/registry_summary.yaml`; the SKILL tests check the v2 anchors and the
  new input.
- `rubric_version` values `-v2` accepted by `reader_proposals` (free text, so a smoke test).
- **C1.1 extension:** run 1 validates a block (stubbed grid PASS) → run 2's reader prompts contain
  that block in `registry_summary.yaml` with this run marked as its neighbour.

---

## C2.4 — A crashed variant can never validate (D-015)

### Today

- The variant loop `continue`s past every failure after recording a `backtest_failed` trial:
  missing `config_path` (`rpr:1561-1572`), non-zero exit (`:1588-1603`), missing summary (`:1605-1616`),
  unparseable summary (`:1618-1636`), trial write failure (`:1638-1653`). Only survivors enter
  `per_variant_summaries` (`:1655`); all failing raises (`:1659-1664`).
- `evaluate_grid(per_variant_summaries, ...)` (`rpr:1743-1750`) grades the survivors only; with all of
  them passing the idea is `validated` (`vce:1695-1704`). Memory then marks the crashed variant
  `failed` (`cm:276-281`) and the registry registers the block (`tools/block_registry.py:336-350`),
  whose `variants_passed` = the surviving columns (`:260`).
- Test pinning the continue: `tests/test_e033_slice4a_variant_loop.py:397`.

### Proposed change (G11)

- `evaluate_grid(..., failed_variants=None)` (`vce:1598`): for each `vid` in `failed_variants`, add a
  column whose every cell is `{result: INCONCLUSIVE, not_graded: true, reason}` without calling any
  grader (so neither `_evaluate_grid_cell` nor the composition `profit_bars_grader` nor the residual-IC
  diagnostic runs for it); list it in `variants`; add top-level `failed_variants`. `None` →
  byte-identical output. The rollup (`vce:1695-1704`) is unchanged: FAIL anywhere → refuted (D-014);
  else the crashed column makes it `inconclusive`. The `sign_consistent_by_era` and every other menu
  criterion need no special case — the crashed cell is never evaluated.
- The variant loop collects `failed_variants` (the five `continue` branches) and passes it, also on the
  composition path (`rpr:1737-1747`).
- Consumers that read "column = tested":
  - `_profit_bars_backtest_candidates` (`rpr:10493-10516`): a column in `failed_variants` →
    `NOT_TESTED` with the reason (not `_tested`, which would load a missing or stale result).
  - `cm._variants_block` (`cm:259-295`): a column in `failed_variants` → status `failed`, never
    "tested" (which requires a `backtest` trial row, `cm:209-221`, and would raise).
  - `cm._compact_cell` (`cm:135-145`) keeps `not_graded` (add to `_CELL_KEYS`, `cm:94`).
  - `tools/near_miss_scoreboard.py:451-476` counts it as INCONCLUSIVE — already correct.
  - `tools/block_registry.py` is unreachable (the idea is not validated) — no change.
- `idea_status.yaml` reason names the crashed variants.
- Profit bars: a crashed variant is `NOT_TESTED`, never graded, never passing (already so for
  "validated, no column", `rpr:10507-10511`). Trial rows unchanged.
- Tie-break comment: cite D-014 (G15).

### Flags

Only in the variant-loop branch with `grid_evaluation` on. Flag off: one column, a crash raises
(`rpr:1807-1817`), nothing changes.

### Tests

- Grid: two passing survivors + one failed → `inconclusive`, column present with `not_graded`;
  one FAIL survivor + one failed → `refuted`; `failed_variants=None` byte-identical to today.
- Memory: the failed column is `failed`, not `tested`; no raise; profit-bars block consistent.
- Branch 3: the failed column is `NOT_TESTED`.
- Registry: nothing registered for that run.
- `test_e033_slice4a_variant_loop.py:397` updated (declared): still continues, and the grid now shows
  the failed column.
- **C1.1 extension:** the stubbed `run_protocol` exits non-zero for the asset variant → run ends
  `completed_inconclusive`, a `backtest_failed` row exists for `run:asset`, no registry entry.

---

## C2.5 — Variant shape (card D; review A5)

### Today

- No check on Step 2's output. `variant_patches.yaml` is not a checked deliverable (A3 §3.4); a
  missing file raises only at 5a (`rpr:2053-2060`). No count limit; the skill says "more are permitted"
  (`innovation-expansion/SKILL.md:272`).
- Only 5a checks each entry: unique safe id (`rpr:2107-2140`), patch applies (`:2142-2149`), manifest
  paths (`:2156-2167`), `validate_config.py` (`:2175-2191`). A failure marks that variant `not_tested`.
- After the data gate, `_min_needed = 3` (lowered only by repeat skips, `rpr:12537-12538`). With fewer
  validated variants left: park when every loss is a missing class or a fetchable data decline
  (`_variant_park_kind`, `rpr:4300-4331`), otherwise pause `variant_gate_insufficient`
  (`rpr:12561-12570`) — also when the real cause was a patch that did not apply or another V-code, so
  the label is wrong in that case. With the data gate switched off, the route goes straight to
  protocol_execution with ≥ 1 validated variant (`rpr:11867-11894`).
- Precedent for "retry, not raise": `_route_block_manifest_check` (`rpr:11664-11683`, one retry,
  context carried by `_apply_block_manifest_retry_context`, `:11686-11701`).

### Proposed change (G12)

- New `_route_variant_patches_check` after `innovation_expansion` under config-direct, non-composition
  (`rpr:12416-12425`): checks count 3–4, kinds (exactly one `base` with id `base` and an empty patch;
  ≥ 1 `design`, non-empty patch, base coin; 1–2 `asset`, empty patch, G3 rules incl. the Layer-1
  coverage precheck), and the G4 multi-coin refusal. Invalid → back to `innovation_expansion` once
  with the error in `injected_context`; second failure → `paused_for_human`, flag
  `variant_shape_invalid`.
- `_route_post_config_direct_backtest_specification` (`rpr:11823-11894`): if any variant is
  `not_tested` for a reason other than a missing class (V12 cannot-load stays the park-for-component
  path), send Step 2 back once with the 5a report; second time → pause `variant_config_error`. So a
  config error never reaches the data gate.
- The data-gate floor (`rpr:12537-12570`) is unchanged in shape; after the two checks above it can
  only be triggered by data losses (plus missing classes), so `variant_gate_insufficient` becomes
  honest. The same "≥ 3 validated" check also runs when the data gate is switched off.
- `run_campaign.py` `_classify_human_pause` / `_PAUSE_FLAG_TO_REASON` (`workflow/run_campaign.py:1029,
  1139-1140, 1402-1446`) and `docs/RUNBOOK.md` §3 get rows for the two new flags.
- `workflow_artifacts/templates/handoffs/hypothesis_to_innovation_expansion.yaml`: C1.2 makes
  `variant_patches.yaml` a checked deliverable — S2c relies on it (see conflicts below).

### Flags

Under `config_direct_authoring` (and `variant_loop` for the floor). Flag off: no change.

### Tests

- Shape violations each trigger exactly one retry, then the pause flag: 2 variants; 5; no `base`;
  asset in the base's category; asset with a non-empty patch; design on another coin; a coin failing
  the coverage precheck; a multi-coin forecast variant. Composition mode skips the check.
- 5a: a patch that does not apply → one Step 2 retry → `variant_config_error`, never
  `variant_gate_insufficient`; a V12 missing class still parks as component.
- Data loss of the asset variant → park `waiting_for_data` (fetchable) or `variant_gate_insufficient`
  (unfetchable), unchanged.
- **C1.1 extension:** stubbed Step 2 first returns 2 variants, then 3 → the run proceeds; the retry is
  visible in the audit log.

---

## Proposed S2 split

| slice | items | main files | depends on |
|---|---|---|---|
| **S2a** | C2.4 crashed-variant column + G15 comment | `tools/verdict_criteria_evaluator.py`, `rpr` variant loop (`1493-1789`) + `_profit_bars_backtest_candidates`, `tools/campaign_memory.py` (`_variants_block`, `_CELL_KEYS`), tests | C1 merged |
| **S2b** | C2.1 one coin per variant (G1–G6) | `rpr` 5a (`2029-2217`), data-gate loop (`1326-1455`), protocol_execution loop, `_repeat_gate_context`/`_check_variant_repeat`, `_residual_ic_grid_inputs`, trial recorders; `tools/composite_cache.py`; `tools/campaign_memory.py` (`_INDEX_KEYS`); `tools/deflate_sharpe.py` + `rpr:_dedupe_trials` (lockstep); `innovation-expansion/SKILL.md`; tests | S2a (same loop block) |
| **S2c** | C2.5 variant shape (G12) | `rpr` routing after `innovation_expansion` and after 5a, data-gate route; `workflow/run_campaign.py`; `docs/RUNBOOK.md`; tests | S2b (`kind`/`symbol` fields); C1.2 (deliverable) |
| **S2d** | C2.2 per-variant reports + compaction (G7, G8, G14 if C1.3 did not) | `tools/build_reports.py`, `rpr` call sites (`1767-1776`, `1947-1966`), five reader SKILLs (report-shape sections), tests | S2a (`failed_variants`); soft on S2b (symbol labels — reads them from the index when present) |
| **S2e** | C2.3 distance per card I (G9, G10) | `tools/block_registry.py` (summary fn), `rpr` readers stage + handoff (`3240-3261`, `3464-3486`), five reader SKILLs (rubric), tests | S2d (same five SKILL files) |

**Order:** S2a → S2b → S2c; S2d may start after S2a in parallel with S2b; S2e after S2d.

**File-conflict risks.**

- `rpr` is touched by all five. S2a and S2b both edit the protocol_execution variant loop
  (`rpr:1493-1789`) — strictly sequential. S2c and S2b both touch 5a (`rpr:2029-2217` vs the route at
  `11823-11894`) — sequential. S2d touches only the two `build_reports` call sites; S2e only the reader
  stage — low risk.
- `tools/campaign_memory.py`: S2a (`_variants_block`, `_CELL_KEYS`) and S2b (`_INDEX_KEYS`) — different
  lines of one area; sequential merge avoids it.
- The five reader SKILLs: S2d and S2e both rewrite them — sequential, or merge the two into one slice if
  the reviewer prefers one SKILL pass.
- `tests/test_e061_end_to_end_wiring.py` (C1.1, branch `test/e061-c1-1-end-to-end-wiring`, in
  progress): every S2 adds its own test function to it; each S2 rebases on the previous one's merge.
  Do not start an S2 before C1.1 is on master.
- C1.2 edits `hypothesis_to_innovation_expansion.yaml` and the config-direct handoffs; C1.3 decides
  whether `run_protocol.py` keeps diagnostics without a validation protocol (G14). Both land before S2c
  / S2d.
- C3 (profit bars v2) edits `_portfolio_profit_metrics` and the bars file; C2 does not touch them.
  C3's S1 must be told that a variant's portfolio is one coin (G5).

**Run budget:** none (C4 proves it, as the plan says).

## Out of scope, noted

- `mechanism_plausibility` anchors ≠ card I's "who is on the other side" (A2 I.4) — separate ticket.
- A real cross-sectional engine (cross-coin ranking) — nothing in `run_protocol.py` supports it (G4).
- Venue-aware costs for Kraken-sourced asset coins — the cost model is per symbol, not per venue.
- `target_instrument_set` for composites and for the profit-bars stop — C5.3.
