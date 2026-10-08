# E-075 phase A: the analyst, a reader that explores the raw data (pilot)

**Status:** characterisation only (design, no code). Written 2026-10-08, autonomously; the
operator reviews and merges. Nothing here changes behaviour.

**Ids used below:**
- E-075 = this epic (Linear project P-CUL-83).
- E-072 = ideas are confirmed on windows the proposer never saw (P-CUL-80; PR #340, branch
  `feat/e072-explore-confirm`, `engineering/roadmap/E-072/PHASE_A.md`, `tools/explore_confirm.py`).
- E-073 = observable backtest; its step 1 is the data dictionary (P-CUL-81; PR #342, branch
  `feat/e073-data-dictionary`, `docs/DATA_DICTIONARY.md`). Its audit findings are named A1..A15.
- E-074 = the exploration digest (P-CUL-82). Its phase A is being written in parallel on branch
  `docs/e074-phase-a` (`engineering/roadmap/E-074/PHASE_A.md`); this file does not repeat it.
- CUL-336 = stage agents run closed-book (no tools, no settings, no memory).
- D-079 = the operator's approval of the readers plan (`engineering/delivery_plan_readers.md`,
  PR #339, item 4 and "Decisions taken").

**Line references** are on master `4d585c33` unless a branch is named. SDK references are to the
installed package under `venv/Lib/site-packages/claude_agent_sdk/` (read, never called).

**Verdict in one line:** feasible with the installed SDK and the existing claim engine; the pilot
as specified has two problems that must be fixed before any money is spent: (1) only 6 of the
10 saved runs have backtests, and they share 4 price series, and (2) the go rule "at least 2 of
10 more than placebo" passes on pure noise about 1 time in 4.

---

## 1. The SDK and the minimal change for one tool-using stage

### 1.1 What is installed

- `claude-agent-sdk` 0.2.82 is installed in the Windows venv (`_version.py:3`), bundling CLI
  2.1.142 (`_cli_version.py:3`).
- It is pinned only in `strategy-research/config/requirements-mac.txt:25` (`claude-agent-sdk==0.2.82`).
  There is no Windows requirements pin. The pin should be added to whatever file installs the
  Windows venv in slice 2 (or noted as mac-only on purpose).
- `tool(name, description, input_schema, annotations=None)` exists (`__init__.py:166`).
- `create_sdk_mcp_server(name, version="1.0.0", tools=None)` exists (`__init__.py:307`) and
  returns `McpSdkServerConfig {type: "sdk", name, instance}` (`types.py:627-632`).
- The options the epic needs all exist on `ClaudeAgentOptions` (`types.py:1579`):
  `tools` (1582), `allowed_tools` (1593), `mcp_servers` (1615), `strict_mcp_config` (1622),
  `permission_mode` (1629, includes `"dontAsk"`, `types.py:24-26`), `max_turns` (1653),
  `max_budget_usd` (1659), `disallowed_tools` (1666), `hooks` (1760), `effort` (1874).
- An in-process server works with a plain string prompt, which is how readers call today:
  `query()` collects the `sdk` servers' instances (`_internal/client.py:136-142`), writes the
  string prompt after `initialize` (`client.py:207-217`), and keeps stdin open until the first
  result when SDK servers or hooks exist (`_internal/query.py:810-826`). Tool calls are routed
  to our Python handlers in this process (`query.py:548`, `tools/list` at 602, `tools/call` at 634).
- `can_use_tool` (a per-call permission callback) is NOT usable with a string prompt: it raises
  "can_use_tool callback requires streaming mode" (`client.py:101-105`). So the code-level
  guard must be a `PreToolUse` hook (`types.py:308-314` input, `412-417` deny output), which
  does work with a string prompt (the hooks keep stdin open, `query.py:819`).

### 1.2 How readers are called today

- One options helper, `_stage_agent_options()` (`workflow/run_phase1_research.py:1118-1175`):
  `model=_CLAUDE_WORKER_MODEL` ("claude-haiku-4-5", `:1111`), `tools=[]`, `setting_sources=[]`,
  `strict_mcp_config=True`, auto-memory off through `env`, a neutral `cwd` outside the repo;
  `max_turns` left unset on purpose (one turn by construction, docstring `:1158-1161`).
- Two call sites, both `query(prompt=..., options=_stage_agent_options())`: `run_claude_worker`
  (`:1370`, query at `:1395`) and `_invoke_reader_llm` (`:4498-4519`, query at `:4506`).
- A reader is `run_reader_worker` (`:4806`): handoff -> prompt -> one `_invoke_reader_llm`
  call -> validate -> at most one retry with the error -> write `artifacts/proposals/<cat>.yaml`.
- The CUL-336 test (`tests/test_cul336_closed_book_stages.py`) pins:
  - the helper's fields, `max_turns is None` included (`:61-73`);
  - the CLI command it produces: `--tools ""`, `--setting-sources=`, `--strict-mcp-config`,
    no `--allowedTools`, no `--max-turns` (`:101-117`);
  - exactly one `ClaudeAgentOptions(...)` call, inside `_stage_agent_options` (`:169-176`);
  - exactly two `query(...)` calls, both passing `options=_stage_agent_options()`, in
    `run_claude_worker` and `_invoke_reader_llm` (`:178-186`);
  - no production file other than `run_phase1_research.py` imports the SDK (`:191-218`).

### 1.3 The minimal change (slice 2)

- Keep ONE construction site: `_stage_agent_options(*, analyst=None)`. With `analyst=None` it
  returns exactly today's object (every existing CUL-336 assertion still holds unchanged).
  With an analyst spec it adds, on the same closed-book base:
  - `model` = the analyst model (pilot: "claude-sonnet-5-5"), not the Haiku constant;
  - `mcp_servers={"analyst": <create_sdk_mcp_server(...)>}` and nothing else;
  - `allowed_tools` = exactly the six analyst tool names (so they run without a prompt);
  - `permission_mode="dontAsk"` (anything not pre-approved is denied, `types.py:1629-1637`);
  - `hooks={"PreToolUse": [deny any tool_name not in the six]}`;
  - `max_turns` (pilot 40) and `max_budget_usd` (pilot 1.50).
- Add ONE new call site, `_invoke_analyst_llm(prompt, server, caps)`, in
  `run_phase1_research.py` next to `_invoke_reader_llm`, passing
  `options=_stage_agent_options(analyst=...)`. It returns the text, the cost/usage/num_turns,
  the `ResultMessage.subtype` (so `error_max_turns` / `error_max_budget_usd` are recorded),
  and every tool_use the hook saw.
- The query functions themselves live in a new pure module `tools/analyst_queries.py` that does
  NOT import the SDK. Only the thin wrapper (the six `@tool` functions calling into that module,
  and `create_sdk_mcp_server`) sits in `run_phase1_research.py`. This keeps the CUL-336
  "single importer" test true without editing it.
- Deliberate CUL-336 test changes (the only ones):
  - `:178` "exactly two query calls" becomes three, and the expected set of enclosing
    functions adds `_invoke_analyst_llm`; every call must still pass a `_stage_agent_options(...)` call;
  - a new test builds the analyst options and reads the CLI command off the installed SDK's
    builder (same technique as `:101-117`): `--tools ""`, `--strict-mcp-config`,
    `--setting-sources=`, `--mcp-config` holding only the `analyst` server,
    `--allowedTools` equal to the six names, `--permission-mode dontAsk`, `--max-turns 40`,
    `--max-budget-usd 1.5`;
  - a new test calls the hook with `tool_name="Read"` and `"Bash"` and asserts a deny.

### 1.4 Can the allow-list guarantee that no built-in tool (Read, Bash, ...) is reachable?

- **No, not the allow-list by itself.** `allowed_tools` only lists tools that run without
  asking; it does not limit which tools exist (`types.py:1593-1603`: "To restrict which tools
  are available at all, use `tools`"). It becomes `--allowedTools` (`_internal/transport/subprocess_cli.py:252-257`).
- **What removes built-in tools is `tools=[]`**, sent as `--tools ""` (`types.py:1582-1589`,
  `subprocess_cli.py:240-247`). The analyst keeps `tools=[]`, exactly like every stage since CUL-336.
- **Our tools survive `tools=[]`** because they are MCP tools, not built-in tools (CUL-336's own
  note, `run_phase1_research.py:1137-1140`); `strict_mcp_config` removes every other MCP server
  (`types.py:1622-1627`, `subprocess_cli.py:340-341`).
- **Defence in depth, each one checkable without a model call:**
  1. `tools=[]` (no built-in tool exists);
  2. `strict_mcp_config=True` + only our server in `mcp_servers` (no other MCP tool exists);
  3. `setting_sources=[]` (no settings file can add allow rules);
  4. `permission_mode="dontAsk"` (anything not pre-approved is denied);
  5. a `PreToolUse` hook that denies any `tool_name` outside the six, and logs it;
  6. the handlers take only typed parameters (no path, no code string; section 2.1).
- **Not verifiable from the Python source (CLI behaviour, checked in the slice-2 smoke
  session):** (a) the exact tool-name form the CLI gives MCP tools (expected
  `mcp__analyst__<name>`; the SDK docstring example uses bare names, `__init__.py:352`),
  which the allow-list and the hook must match; (b) that the `system/init` message lists only
  the six tools (the smoke session fails closed if any other name appears, or if the list is
  absent); (c) that the bundled CLI accepts the model id "claude-sonnet-5-5".

---

## 2. The query functions

### 2.1 Rules common to all six

- **Data is loaded before the session, exploration windows only.** The tool server is built
  from (a) the variants' `bars.csv` rows whose window label is in E-072's exploration list and
  (b) `trade_diagnostics.json` trades whose `window` field is in that list. Confirmation rows
  are never loaded into the server's memory. The split is E-072's own function on the saved
  protocol files (`explore_confirm.protocol_windows` + `split_windows`, branch
  `feat/e072-explore-confirm` `tools/explore_confirm.py:213-251`). On every saved run below
  that gives exploration 2022-01 / 2022-05 / 2022-09 and confirmation 2023-01 / 2023-05 / 2023-09
  (measured from `run_065/artifacts/variants/run_protocol.json`).
- **Bars are loaded with the claim engine's own reader** (`claim_tests.load_variant_bars`,
  `tools/claim_tests.py:407-437`) with `cache_path_for=None`: no warm-up rows, so no file under
  `trading-bot/local_data/` is ever opened. Then `claim_measure.check_before_holdout`
  (`tools/claim_measure.py:113`) with the configured holdout start
  (`_load_holdout_range`, `run_phase1_research.py:9878`) refuses any bar at or after it.
- **No lookahead, by code:**
  - a condition may read only bar-t values: the claim engine's selector vocabulary
    (`claim_tests.py:146-147`, `:443-530`: `forecast`, `close`, `past_return` with `bars`,
    `regime`, `regime_change`, `calendar`, `quantile` over TRAILING bars);
  - an outcome is matched by timestamp inside one window (`Window.index_at`, `claim_tests.py:284-296`),
    so an exploration outcome can never reach into a confirmation window;
  - every other column is classed by the data dictionary's "When known" column (branch
    `feat/e073-data-dictionary`, `docs/DATA_DICTIONARY.md` section "How to read it" and
    section 1 / 2 tables). The server parses those two tables once and allows:
    `close` and `fill` columns as features; `exit` and `after` fields only as outcomes
    (`trade_slice` agg, `event_study` after-path); `meta` as labels only; `end` and `run`
    never. This removes `balances.*` (A1: end-of-run values on every row, a real lookahead)
    and the all-window `summary` block;
  - trade filters accept only entry-time fields (`close`/`fill`/`meta`): never
    `profitable_net`, `realized_return`, `holding_bars`, `exit_*`, `mae`, `mfe`, `post_exit_*`.
- **No free code, no strings that execute.** Parameters are JSON with closed vocabularies:
  column names checked against the allowed list; filters are lists of `{field, op, value}`
  with `op` in the claim engine's `_OPS` (`claim_tests.py:180`); never `DataFrame.query`,
  `eval`, a path or a regex. A bad parameter returns an error message (logged, 0 comparisons).
- **Outcome layer (needed by the placebo, section 3).** Every function that returns anything
  about bars after t gets those bars from one `outcome_window(w)`: the real window in the real
  arm, the placebo window in the placebo arm. Features (conditions, filters, `describe`,
  `distribution`, the before-path of `event_study`) always read the real window.
- **Trade outcome fields are recomputed by our code in both arms** (realized return net of the
  run's cost model, MAE/MFE from the bar AFTER the fill, post-exit returns), from the outcome
  window. Two reasons: the placebo needs it, and the engine's fields carry A4 (entry efficiency
  measures slippage), A5 (exit_reason 99% `signal_flip`), A6 (MAE/MFE include the entry bar's
  own high/low) and A7 (`cost_paid` is fee only). The analyst never sees `entry_efficiency`,
  `exit_reason` or `cost_paid`.
- **Every call is logged** to `analyst_queries.yaml` (in the campaign: `artifacts/analyst_queries.yaml`;
  in the pilot: the session folder, section 7): id, function, parameters, result, result hash,
  `n_comparisons`, cumulative comparisons. Written by the handler before it returns, so a
  crash cannot lose a look.
- **Comparisons, not calls.** One comparison = one returned number that relates a condition
  or a group to an outcome. Feature-only results (`list_columns`, `describe`, `distribution`,
  a `trade_slice` agg of entry fields) count 0 comparisons but are logged.
- **Caps per call:** at most 12 groups, at most 6 horizons, result text at most 4,000
  characters (about 1,000 tokens); a call over a cap is refused with the reason.
  **Per session:** at most 150 comparisons; after that every outcome call returns "comparison
  budget spent: write your proposal".

### 2.2 The six functions

| Function | Exact parameters | Reads | Returns | Comparisons |
|---|---|---|---|---|
| `list_columns()` | none | the dictionary tables + the loaded columns | per column: name, meaning, unit, when known, role (feature / outcome / label), and whether a condition on it compiles into a claim test | 0 |
| `describe(column, by=None)` | `column`: a feature column; `by`: one of `null`, `window`, `coin`, `regime`, `weekday`, `hour` (hourly runs only) | real bars, exploration windows | per group: n, NaN share, mean, std, p10, p50, p90 | 0 |
| `distribution(column, by=None, bins=10)` | as `describe`; `bins` 2..20 | real bars | per group: bin edges and counts | 0 |
| `conditional_effect(variant, condition, horizons, outcome="fwd_return", baseline={"kind": "complement"}, statistic="mean_diff", direction="greater", by=None)` | `condition`: one claim-engine selector; `horizons`: 1..6 ints; `outcome`/`baseline`/`statistic`/`direction`: the claim engine's names (`claim_tests.py:28-32`); `by`: `null`, `window` or `coin` | selector on real bars, outcome on `outcome_window` | per horizon (and per group): effect, oriented effect, n_events, windows with events; plus the exact `test` block ready to paste into a claim | horizons x groups |
| `trade_slice(variant, filter, agg, by=None)` | `filter`: list of `{field, op, value}` on entry-time fields; `agg`: list of `{field, stat}` with `stat` in `mean`, `median`, `share_positive`, `count`; `by`: `null`, `window`, `direction`, `regime_at_entry`, `weekday`, `hour` | trades (entry fields real, outcome fields from `outcome_window`) | per group: n trades and each agg | groups x outcome aggs |
| `event_study(variant, trade_filter, bars_before, bars_after)` | `trade_filter` as above; `bars_before` 1..24 (hourly) / 1..10 (daily); `bars_after` same bounds | before-path on real bars, after-path on `outcome_window` | mean cumulative return from the entry close at fixed checkpoints (1, 2, 3, 6, 12, 24 bars hourly; 1, 2, 3, 5, 10 daily) before and after | after-checkpoints returned |

- `variant` must be one of the run's variants with bars; default `base`.
- `conditional_effect` with `by=window` reuses the engine's `per_window`; `by=coin` reuses
  `claim_measure`'s `per_coin`. `by=regime/weekday/hour` is NOT offered there on purpose: a
  claim test has one selector and no AND, so a "only in regime X" finding could not compile.
  To test a regime or an hour, the analyst uses it AS the condition.

### 2.3 How `conditional_effect` compiles into a claim test

- Each call builds a `claim_tests.TestSpec` (`claim_tests.py:707-730`) from
  `selector=condition`, `outcome={kind, horizons}`, `baseline`, `statistic`, `direction` and a
  placeholder `floor={"min_events": 1}`, and runs `check_spec` (`:798-855`) first. A spec it
  refuses is refused here with the same message (0 comparisons).
- The numbers come from the engine's own pieces: `SELECTORS`, `BASELINES`, `OUTCOMES`,
  `STATISTICS` (`claim_tests.py:530`, `:633`, `:582`, `:699`), composed exactly as `_prepare` /
  `effect_sizes` do (`:899-911`, `:1022-1060`), with one difference: outcomes read
  `outcome_window(w)`. In the real arm `outcome_window(w)` is `w`, so the numbers must equal
  `claim_tests.effect_sizes` on the same windows exactly (slice 1 test).
- The result carries `test: {name, selector, outcome, baseline, statistic, direction, floor}`,
  which is exactly `claim_card.TEST_KEYS` (`tools/claim_card.py:65-66`; `alpha` and
  `significance` stay fixed by code, `:67`). The proposal's claim block is then checked by
  `claim_card.check_claim` (`:156-216`) unchanged, and measured on the confirmation windows by
  E-072's `measure_on_windows` (`explore_confirm.py:403-423`) with E-072's strict sign rule
  (`test_sign` / `finding_sign`, `:697-731`).
- **Limit of the vocabulary:** conditions on `volume`, `fear_greed`, a component's value or the
  allocation are visible in `describe` / `distribution` / `trade_slice` but cannot be a claim
  selector today (`BAR_T_FIELDS = ("forecast", "close", "past_return")`, `claim_tests.py:146`).
  A proposal built on them becomes `tests: none` with `missing_block` (a test request,
  `claim_card.py:184-194`). Decision 5 asks whether to widen the vocabulary.

### 2.4 What one session produces (`proposal.yaml`, validated by code)

- `claim`: a full claim block (`statement`, `kind`, `tests` 1..3, `pass_if`, `fail_if`,
  `rationale`), checked by `check_claim`.
- `variant`: the variant whose bars the claim is about.
- `falsifier`: in plain words, what result on the confirmation windows would show the claim is
  wrong. The mechanical rule is E-072's sign rule; the text must at least name the horizon(s)
  and the sign. Written in the session, so before any confirmation number exists (the
  confirmation step runs after the session has ended and the file is hashed).
- `citations`: list of `{query_id, path, value}`. Each resolves only if the id is in this
  session's log, the path exists in that call's result and the value equals the logged value.
  This is the generic "citations checked against their values" rule of E-073 step 2, applied to
  the query log.
- Written by code, never by the model: `looks` (calls, comparisons), `candidates_examined`
  (the distinct condition specs tried, by `spec_hash`), `exploration_effect` (the claim's tests
  measured on the exploration windows through the outcome layer) and, after the session,
  `confirmation_effect` (measured on the real confirmation windows) side by side.

---

## 3. The placebo, and what the saved runs contain

### 3.1 What is scrambled

- **Only the future, never the features.** Every value known at bar t (close, forecast, regime,
  components, allocation, entry fields) stays real in both arms. Only what the query functions
  return about bars after t goes through `outcome_window(w)`, which in the placebo arm is a
  rebuilt path.
- **Proposed method: block sign-flip.** For each exploration window: the one-bar log returns,
  cut into blocks of `claim_tests.BLOCK_BARS` (24 bars hourly, 5 daily, `claim_tests.py:177`)
  after a random rotation, each block's returns multiplied by a random +1 or -1; the outcome
  path is rebuilt from the window's first real close; a flipped bar's high and low are mirrored
  (log(high'/close') = -log(low/close)). Seed per session, written in the pilot file before the
  pilot starts.
- **Why sign-flip and not a full block shuffle** (the claim engine's null, `fake_window`,
  `claim_tests.py:868-886`):
  - sign-flip keeps the size of every move at its real time, so volatility clustering and
    "big moves follow big moves" stay true in both arms; a full shuffle would remove them in
    the placebo only, handing the real arm a free win for re-finding a known, non-directional
    fact;
  - it removes any directional link between a bar-t feature and the future (a random sign per
    block, independent of the features);
  - within a block the autocorrelation of returns is kept, so the placebo path looks like a
    real path.
- **Trades in the placebo:** entries, sides and holding periods are the real ones (they come
  from the real forecast); their outcome fields are recomputed on the flipped path (section 2.1).
- **Everything else that carries a real exploration outcome must be removed or rebuilt in both
  arms**, or the placebo analyst reads the real answer elsewhere:
  - the E-074 digest: given only if it is computed through the same `outcome_window` (a
    requirement on E-074, to agree with its author); otherwise withheld in both arms (decision 6);
  - the category reports, the grid, the registry summary, `claim_result_digest`: not given in
    either arm (they are not in the epic's input list anyway);
  - the claim card: E-072's whitelist copy with numbers masked (`reader_card`,
    `explore_confirm.py:544`), identical in both arms.
- **What the placebo analyst cannot tell:** the prompt, the tools, the context and the column
  list are byte-identical across arms; only numbers differ, and real 2022 numbers are mostly
  near zero too (no edge found in 59+ runs). Residual tell: the unconditional drift implied by
  outcomes differs from the drift implied by `past_return`; no function returns either
  directly, but a determined analyst could approximate it. Accepted and stated.
- **Confirmation treats both arms the same:** every proposal, real or placebo, is measured on
  the REAL confirmation windows, same code, same rule. The placebo arm measures how often a
  proposal from this model, with this context and these tools, holds on 2023 when its 2022
  evidence was noise: its priors plus chance.
- **The pilot's looks are real looks on the shared confirmation set** (2023 windows used by
  every run since run_065). Both arms' measurements are recorded in E-072's ledger
  (`campaign_record/confirmations.yaml`) with `basis: analyst_pilot` (decision 10).

### 3.2 What runs 065-074 contain (measured, main checkout, read-only)

| Run | State | Timeframe | Variants with bars (coin) | Claim block |
|---|---|---|---|---|
| run_065 | backtested | 1d | base (BTC), donchian_period_14_reactive (BTC), donchian_solusdt_crossasset (SOL) | no |
| run_066 | backtested | 1h | base (BTC), keltner_extended_momentum (BTC), sol_infra (SOL); xrp_payment has no bars | no |
| run_067 | stopped at hypothesis_generation (brief exhausted) | - | none | - |
| run_068 | same as run_067 | - | none | - |
| run_069 | same as run_067 | - | none | - |
| run_070 | backtested | 1h | base (BTC), shock_lookback_250 (BTC), sol_generalization (SOL), uni_defi (UNI) | yes |
| run_071 | backtested | 1h | base (BTC), donchian_faster_10bar (BTC), solana_smart_contract (SOL); xrp_payment_category has no bars | yes |
| run_072 | failed at backtest_specification (`ORPHANED_README.md`) | - | none | yes |
| run_073 | backtested | 1h | base (BTC), design_period_3 (BTC); asset_xrp has no bars | yes |
| run_074 | backtested | 1h | base (BTC), design_longer_smoothing (BTC); asset_xrp_generalization has no bars | yes |

- Every backtested variant has all 6 windows' `bars.csv` (2022-01 .. 2023-09), every window's
  `trades.json`, and one `trade_diagnostics.json` whose trades carry a `window` label. Every run
  has `artifacts/variants/run_protocol.json` and a `protocol_result.yaml` per variant, so
  E-072's split and the claim engine's loader work as they are.
- All six are Kraken perpetual futures, fee 5 bps a side (each base `manifest.json`).
- Exploration size per variant: about 8,760 bars hourly (2,880 + 2,952 + 2,928) and 4,400 to
  7,500 trades; 365 bars daily and about 260 trades (run_065).
- XRP never has bars (all four XRP variants), so no XRP unit exists.

**Consequences:**
- **Only 6 runs, not 10, can host a session**, and they hold 17 (run, variant) units.
- **Those units share 4 price series**: BTC hourly (11 units), SOL hourly (3), UNI hourly (1),
  BTC daily (2) and SOL daily (1) -- 5 series counting the daily SOL. A price-only claim (on
  `close`, `past_return`, `calendar`) explored on any BTC hourly unit is explored on the same
  2022 BTC path and confirmed on the same 2023 BTC path. Two sessions that propose the same
  price-only test get the same confirmation result. Sessions are clustered, not independent.
- **Only forecast- or regime-based claims differ between units of the same coin**, because the
  forecast column differs per variant.
- **Mixed 1h / 1d:** a horizon of 1 is one hour in run_065's neighbours and one day in run_065;
  the placebo block is 24 vs 5 bars; run_065 has about 365 exploration bars per coin, so most
  conditions will have few events there. Two pre-1a-claim runs (065, 066) have no claim block to
  give. Default: include one daily unit for diversity, report it on its own line (decision 4).
- **Config-change claims cannot be confirmed offline** (no new backtests). A proposal whose
  claim needs a new forecast or regime block (E-072 `finding_route` -> `pending`,
  `explore_confirm.py:677-695`) counts as "not held" in both arms (decision 11).

---

## 4. The go / no-go statistics

### 4.1 What the operator's rule does

- Rule: GO if real proposals keep their sign on the confirmation windows in at least 2 more
  sessions out of 10 than placebo proposals, and they pass `check_claim` with every citation
  resolving.
- Simulated (200,000 draws, independent sessions, the scratch script is not committed):

| Placebo hold rate | Real hold rate | P(GO), ">= 2 more of 10" | P(GO), ">= 4 more of 10" |
|---|---|---|---|
| 0.30 | 0.30 (no skill) | 0.23 | 0.04 |
| 0.30 | 0.50 (+20 points) | 0.60 | 0.25 |
| 0.30 | 0.60 (+30 points) | 0.76 | 0.42 |
| 0.45 | 0.45 (no skill) | 0.25 | 0.06 |
| 0.45 | 0.65 (+20 points) | 0.60 | 0.25 |
| 0.45 | 0.75 (+30 points) | 0.77 | 0.42 |

- **The operator's rule is too weak: with no skill at all it says GO about 1 time in 4.**
  Exact one-sided Fisher tests agree: 4 vs 2 of 10 gives p = 0.31; 6 vs 4 gives p = 0.33.
- These numbers are the OPTIMISTIC case. The sessions share 4 price series and one
  confirmation set (section 3.2), so the effective sample is smaller and noise passes more often.
- **The base hold rate is not 50% and not known in advance.** E-072's rule is strict (every
  horizon with a value must keep the sign), which lowers it; a `rank_ic` claim keeps market
  drift, which can raise it in an up year. That is why the placebo arm exists: it measures the
  base rate with the same model, context and tools.

### 4.2 What 10 vs 10 can detect

- With any rule that keeps false GO near 5% (">= 4 more of 10", about Fisher p <= 0.09:
  6 vs 2, 7 vs 3, 5 vs 1), a true +20-point advantage is found 1 time in 4 and a +30-point
  advantage about 2 times in 5.
- 20 vs 20 with ">= 6 more" keeps false GO near 3-4% and finds +30 points about 57% of the time.
- So 10 vs 10 is a **screen for a large effect only**. A NO-GO does not show the analyst is
  useless; it shows the advantage, if any, is not huge.

### 4.3 Proposed honest rule (pre-registered in the pilot file before any session)

- **Design: paired.** Each of the 10 pre-registered (run, variant) units gets one real and one
  placebo session (same context, same caps, different arm). Pairing removes the unit as a
  source of difference.
- **Counting:** a session "holds" when its proposal compiles (`check_claim` without errors,
  not `tests: none`), is measurable on the saved bars, and `finding_sign` returns true on the
  confirmation windows. Anything else counts as not held, in both arms.
- **Duplicates count once:** two sessions of the same arm whose tests have the same
  `spec_hash` on the same coin and timeframe give one result, not two (the confirmation data
  is the same). The report gives both the raw and the de-duplicated counts.
- **GO only if all three hold:**
  1. real holds - placebo holds >= 4 (de-duplicated counts; about one-sided Fisher p <= 0.09);
  2. at least 8 of the 10 real proposals compile, and every citation of every real proposal
     resolves;
  3. at least 3 of the real holds are directional claims (`fwd_return` or `trend_ends`
     outcomes), so a GO cannot rest on volatility claims alone.
- **Alternative if the operator wants more power:** 20 vs 20 (repeat 3 units with new seeds),
  GO at ">= 6 more", same other gates, about twice the cost (section 5).

### 4.4 What a GO would and would not show

- **Would show:** on these 4 price series, this model reading exploration windows through these
  six functions proposes claims that keep their sign on 2023 more often than the same model
  reading noise. Its reading of the data adds something to its priors.
- **Would not show:**
  - an edge, a profit, or survival after costs (no claim here is a strategy);
  - significance after best-of-N: each session examined many candidates; the report shows the
    comparisons, it does not correct for them;
  - that the effect generalises beyond BTC/SOL/UNI, 2022 to 2023, Kraken perps;
  - that the 2023 hold is not a regime coincidence (2022 bear, 2023 recovery);
  - that the confirmation set is still fresh: the pilot spends looks on it (section 3.1).
- **What GO buys:** the right to build the campaign integration (a sixth reader behind the
  flag) and to keep counting its proposals through E-072's ledger. Proof still needs more years
  (E-066).

---

## 5. Cost (estimate, not measured)

**Assumed prices (claude-api skill table, cached 2026-09-25):** Claude Sonnet 5.5
(`claude-sonnet-5-5`) $2.00 per million input tokens, $10.00 per million output tokens, cache
reads $0.20 per million; cache writes assumed at 1.25 x input = $2.50 per million (5-minute
cache). The SDK sends an empty system prompt by default (`subprocess_cli.py:227-228`), so the
CLI adds little of its own.

| Item | Low case | High case |
|---|---|---|
| Starting context (skill, run context, card, dictionary analyst subset, digest, tool schemas) | 25k tokens | 25k tokens |
| Tool calls | 25 | 35 |
| Growth per call (call + capped result) | 2k tokens | 2k tokens |
| Output per call (thinking + call), plus the final proposal | 0.8k + 3k | 1.5k + 3k |
| Cache reads (context resent each turn) | 1.23M -> $0.25 | 2.07M -> $0.41 |
| Cache writes | 75k -> $0.19 | 95k -> $0.24 |
| Output | 23k -> $0.23 | 55k -> $0.55 |
| **Per session** | **about $0.67** | **about $1.20** |

- 10 vs 10: about $13-24; plus 2-3 smoke sessions in slice 2, about $3. **Pilot total about
  $16-27**, above the plan's $10-15 (whose $0.5-0.7 per session is the low edge of this range).
- 20 vs 20: about $30-50.
- If prompt caching does not engage (cache reads billed as input), a session would cost about
  $2.5-3; the per-session cap below stops it at $1.50 and the session is recorded as
  `error_max_budget_usd`. The smoke session checks `cache_read_input_tokens > 0`.
- The confirmation measurement is code only: $0.

---

## 6. Safety

- **Holdout:** the server reads only `strategy-research/runs/<run>/variants/*/results/*/bars.csv`
  and `trade_diagnostics.json` of saved runs whose windows end 2023-12; `cache_path_for=None`
  means no `trading-bot/local_data/` file is opened (a slice-1 test patches `open` to fail on
  any path under `local_data`); `check_before_holdout` refuses any bar at or after the
  configured holdout start; the CLI has no file tool to open anything itself.
- **Sealed dates in outputs:** every number shown comes from 2022 (exploration) or 2023
  (confirmation) bars. The proposal text is model-written: code scans it with the existing seal
  pattern (`trading-bot/tests/test_no_sealed_date_literals.py`'s date regex) and refuses a proposal naming
  a date at or after the holdout start (one retry, then "not held").
- **Environment keys:** the CLI subprocess inherits the environment as today's readers do (it
  needs it to authenticate), but has no Bash, Read or any built-in tool (section 1.4). Our
  handlers take only typed values, never a path or an expression, and never read `os.environ`.
- **Network:** the only traffic is the CLI's own API calls. No WebFetch / WebSearch (built-ins
  removed), no other MCP server (strict). The in-process server opens no socket.
- **Runaway cost:** per session `max_turns=40` and `max_budget_usd=1.50` (CLI-enforced,
  `types.py:1653-1664`), the 150-comparison cap, the 4,000-character result cap, and a
  wall-clock timeout (15 minutes) around the session; per pilot a total cap ($30) checked
  before each session from the recorded `total_cost_usd`. A cap hit is recorded, never retried
  silently.
- **Saved runs are read-only:** the pilot writes only under its own folder (section 7), never
  into `strategy-research/runs/`, matching the claim engine's own CLI rule ("it never writes
  into a run directory", `claim_tests.py:13-14`).
- **Never live:** nothing here touches execution or `main.py run_bot`.

---

## 7. Slices

One umbrella flag: **`orchestrator.analyst.enabled`, off by default** (same style as
`orchestrator.explore_confirm.enabled` on PR #340). The pilot runner is an offline tool and
does not need the flag; the flag guards anything that later wires the analyst into a run.

**Dependencies:** slice 1 needs E-072 (PR #340: the split, `measure_on_windows`, the sign rule)
and E-073 step 1 (PR #342: the dictionary tables). Slice 3 needs E-074's digest only if
decision 6 includes it. Nothing here needs E-029 / E-027.

### Slice 1: the query engine (`tools/analyst_queries.py`, no SDK, no model)

- The six functions, the column roles parsed from the dictionary, the exploration-only loader,
  the outcome layer (real and sign-flip placebo), the trade outcome recomputation, the
  comparison counter, the caps, the query log writer.
- **Done when / tests:**
  - real-arm `conditional_effect` equals `claim_tests.effect_sizes` exactly on the same windows
    and spec, for every selector, outcome, baseline and statistic in the engine;
  - no confirmation-window row is ever loaded; an outcome at the last exploration bar is NaN,
    not a 2023 value;
  - no `local_data` path is opened; a bar at or after the holdout start is refused;
  - `end` / `run` columns and exit-time trade filters are refused;
  - placebo: features are byte-identical to the real arm; sign-flip keeps every |return| at its
    time; the forecast-to-future link is gone on a synthetic window with a planted effect;
  - comparisons counted as horizons x groups / groups x outcome aggs / checkpoints;
  - every call (including refused ones) is in the log before the function returns.
- No behaviour change: nothing calls the module.

### Slice 2: the tool wiring and the session (in `run_phase1_research.py`, behind the flag)

- `_stage_agent_options(analyst=...)`, the six `@tool` wrappers, `create_sdk_mcp_server`,
  the PreToolUse deny hook, `_invoke_analyst_llm`, the analyst SKILL text, the proposal
  validator (`check_claim`, citations, falsifier present, seal-date scan), the Windows pin.
- **Done when / tests** (stubbed `query`, no API key):
  - the CUL-336 changes of section 1.3, and every other CUL-336 assertion unchanged;
  - the analyst CLI command read off the installed SDK (section 1.3);
  - the hook denies `Read`, `Bash`, `WebFetch` and any unknown name;
  - a stubbed session writes `proposal.yaml` and `analyst_queries.yaml`; a bad proposal gets
    one retry with the error, then "not held".
- **One live smoke session** (operator-approved, about $1-3): checks the tool-name form, the
  init tool list (only the six), the model id, cache reads > 0, and the cost record.

### Slice 3: the pilot runner and report (`tools/analyst_pilot.py`)

- A pilot file committed BEFORE any session: the units, arms, seeds, model, caps, the GO rule
  of section 4.3. The runner refuses to start if it is missing or changed after the first session.
- Runs the sessions (real and placebo, alternating), then the confirmation of every proposal
  with E-072's code on the real confirmation windows, then writes `pilot_report.yaml` and a
  short `PILOT_REPORT.md`: per session the claim, falsifier, looks, candidates, exploration
  effect next to confirmation effect; the counts raw and de-duplicated; the GO / NO-GO with its
  numbers; and the E-072 ledger rows.
- **Done when / tests:** a dry run with a stubbed model on one saved run produces the full
  report; a changed pilot file stops the runner; looks land in the ledger.
- Then the operator runs the pilot (about $16-27, section 5). The epic is done when the report
  states the GO / NO-GO with its numbers.

### Not in this epic

- Wiring the analyst as a sixth reader in the campaign (only after a GO; a new decision).

---

## 8. Decisions for the operator

Each has the default this design assumes and the alternative.

1. **Placebo method.** Default: block sign-flip of future returns (keeps volatility structure in
   both arms). Alternative: full block shuffle (the claim engine's null); then volatility claims
   must be excluded from the count.
2. **GO rule.** Default: paired, de-duplicated, real - placebo >= 4 of 10, plus 8/10 compile
   with every citation resolving, plus at least 3 directional holds. Alternative: the plan's
   ">= 2 more", knowing it says GO on pure noise about 1 time in 4.
3. **Pilot size.** Default: 10 vs 10 (a screen for a large effect, about $16-27).
   Alternative: 20 vs 20 at ">= 6 more" (about $30-50, still clustered on 4 price series).
4. **Units.** Default: a pre-registered list of 10 (run, variant) units chosen for diversity:
   the 4 SOL/UNI hourly units (066 sol_infra, 070 sol_generalization, 070 uni_defi,
   071 solana_smart_contract), the 5 BTC hourly base variants (066, 070, 071, 073, 074) and
   run_065 base (BTC daily), reported on its own line. Alternative: hourly only (drop run_065).
5. **Condition vocabulary.** Default: the claim engine's selectors only (`forecast`, `close`,
   `past_return`, regime, calendar); other columns visible but a proposal on them becomes a test
   request. Alternative: add `volume`, `fear_greed` and component values to `BAR_T_FIELDS`
   (an E-068 claim-engine change with its own no-lookahead note; 1a would gain them too).
6. **The E-074 digest in the pilot.** Default: given only if computed through the same outcome
   layer, else withheld in both arms. Alternative: give the real digest in both arms (breaks the
   placebo: the placebo analyst would read the real answers).
7. **Trade outcome fields.** Default: recomputed by our code in both arms (fixes A6/A7 for the
   analyst, drops A4/A5 fields). Alternative: the engine's fields in the real arm (the placebo
   could then be told apart).
8. **Model and effort.** Default: Claude Sonnet 5.5, the CLI's default effort, as the plan says.
   Alternative: set effort explicitly (lower cost, possibly fewer, cruder queries); the model
   choice beyond the pilot stays parked (E-069).
9. **Caps.** Default: 40 turns, $1.50 and 150 comparisons per session, $30 per pilot.
   Alternative: tighter caps (cheaper, fewer looks) or looser.
10. **Looks on the shared confirmation set.** Default: both arms' confirmation measurements are
    recorded in E-072's ledger with `basis: analyst_pilot`. Alternative: keep them in the pilot
    report only (the ledger then undercounts the looks on the 2023 windows).
11. **Proposals that cannot be confirmed offline** (needs a new block or config, or `tests: none`).
    Default: count as not held, in both arms. Alternative: exclude them and report the excluded
    count (raises both rates, hides an analyst that proposes unconfirmable ideas).
12. **CUL-336 test changes.** Default: exactly the deliberate changes of section 1.3 (three
    query sites; a new analyst-options test). Alternative: a separate analyst test file and a
    second options helper (two construction sites, against CUL-336's "cannot drift" intent).
