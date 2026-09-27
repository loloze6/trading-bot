# E-062 S1 — Profit bars v2: characterization (read-only)

Delivery plan: `engineering/delivery_plan_v26_continuation.md` C3 (C3.1–C3.6). Decisions in
force (binding, not re-asked): D-004, D-020, D-021, D-034..D-039. D-016 (one coin per variant,
C2.1, parallel) is accounted for in every section. Base: `origin/master` `9900dee3`.

Method: code and protocol *definitions* only. No run results, trial Sharpes, campaign state or
anything under the sealed store were opened. No thresholds are proposed here — the values are
D-039's. Every line reference is to `9900dee3`.

---

## Guesses for the operator

SMALL = taken on the recommendation tonight. BIG = parked (changes roadmap intent, spends
money/trials, or changes a ratified value).

| # | Question | Recommendation | Blocks the build? | Size |
|---|---|---|---|---|
| G1 | How do windows chain into one whole-test curve? | **Earliest window owns a day; the next window joins at the shared junction day.** Every protocol in the repo (13 JSON files + the generator) has consecutive windows that share exactly **one day** (`end` is inclusive by day and equals the next `start`), so this rule is exactly what today's pooled daily returns already do — only the drawdown changes. A gap (none exist today) is linked flat and its days are not counted; an overlap of more than one day keeps the earliest window's days; a junction day that the later window lacks is treated as a gap. | yes (the S2 needs a rule) | SMALL — default is safe |
| G2 | Coverage over the whole test? | Keep the 0.9 per-window floor **and** apply the same 0.9 constant to the chained span (counted days ÷ calendar days from the first anchor to the last day). Below it → NOT_EVALUABLE. | no | SMALL — default is safe |
| G3 | Sharpe formula (D-036) | mean ÷ sample stdev (ddof 1) × √365, risk-free 0, on the chained daily returns — same convention as `core.sharpe` and `bar_equity`. NOT_EVALUABLE below **30 daily returns** or at zero stdev. | yes | SMALL — default is safe |
| G4 | Does the DSR bar move to the new Sharpe basis too? | **No.** The trial ledger stores the median of per-coin median window Sharpes (`run_phase1_research.py:9017-9020, 9052`); the DSR compares the candidate with that distribution, so its candidate must stay on the same basis. Only `sharpe_min` moves. | yes | SMALL — default is safe |
| G5 | What is a "trade" for the ≥100-per-coin count (D-035)? | Count per coin over the whole test, **excluding trades closed by the end-of-window forced close** (`exit_reason: end_of_window`). Each window restarts flat and force-closes at its end, so a strategy that is always long gets one "trade" per window: 96 on a 96-window protocol, almost 100 without ever trading. Stricter than the raw count, never looser. Both numbers are recorded on the row. | yes | SMALL — default is safe (stricter) |
| G6 | Buy-and-hold bar (D-037): what is compared? | **Total compounded return** of the chained portfolio vs. equal-weight buy-and-hold over the **same counted days**, B&H charged one round trip per coin (fee from `config/cost_model.yaml` + the engine slippage in effect). PASS iff strategy − B&H **> 0**. Total return, not Sharpe, because the fork bar reads "beats buy-and-hold **and flat**" — the same measure for both. | yes | SMALL (stricter for low-volatility strategies in a bull market — say so when B&H wins) |
| G7 | Where does "survives 2× costs" (D-038) live, per coin or pooled? | A **profit bar** in `profitability_bars.yaml` (branch 3 grades every backtest of every idea = "for every idea"), using the existing `realized_edge_to_cost_ratio` **pooled** over the variant's trades, `> 2.2`, floor **100 pooled trades** with a measured cost, NOT_EVALUABLE below it or when any trade lacks a cost. The idea-grid menu criterion gets the new values (2.2 / 100) but stays one that 1a picks: making it a code-added **grid** criterion for every idea would fail regime blocks (D-025: judged on regime quality) and composition blocks (judged on residual IC). With one coin per variant, pooled = per coin. | yes | SMALL — default is safe |
| G8 | Flag design | New flag `orchestrator.profit_bars_v2.enabled` (strict bool, default false, requires `profit_bars_every_backtest`). The legacy promote path never uses v2. The evaluation records `bars_definitions: v2`; a spend refuses (existing code `bars_changed`) when the evaluation's definitions differ from the current flag. | yes | SMALL — default is safe |
| G9 | Ratification fields | **Already answered by C3.6** ("`ratified_by`/`ratified_at` filled by the operator"): the build writes the D-039 values and leaves both null; the menu's `residual_ic.ratified` also stays `false` for the operator to flip. Add one fix: the loader accepts an unquoted YAML date for `ratified_at` (today an unquoted `ratified_at: 2026-09-30` loads as a `date` and the loader refuses it — `run_phase1_research.py:2607`). | no | SMALL — answered, not a question |
| G10 | Slow strategies can never pass the DSR bar | Recorded, **not built**. A variant with more than 50% of windows under 5 trades is "sparse": the DSR is not computed (`run_phase1_research.py:9887-9918`), so the DSR bar reads NOT_EVALUABLE and blocks. D-035's whole-test trade count therefore does not open branch 3 to strategies that trade under 5 times a month. Fixing it needs a whole-test Sharpe in the trial ledger, which changes trial accounting. | no | **BIG — parked** |
| G11 | Junction cost artifact | No correction. The chained curve pays one forced-exit fee per window junction while a position is held (the re-entry fee falls before the next window's anchor). About 8.5 bps per junction per held coin. Conservative. | no | SMALL — default is safe |

---

## Q1 — Window chaining (C3.1, C3.3)

### Current state

**Window layouts** (definitions only, `protocols/*.json`, measured with a script over the
`windows` lists; the two `prereg_whale_footprint_*.yaml` files are pre-registrations with a
forward-recorder span, not tile lists):

| protocol | windows | tf | tile length | next.start − prev.end |
|---|---|---|---|---|
| baseline_v1, diagnostic_btceth_4h, escalation_{avax,sol}usdt_4h, escalation_tf_15m | 11 | 1h/4h/15m | 1 month | 0 days (all) |
| baseline_v2 | 24 | 1h | 1 month | 0 days (its last tile ends on the first day of the sealed range: refused by `run_protocol.py:2113-2128`, and unratified) |
| funding_mr_{4h,daily}_retest_v1 | 49 | 4h/1d | 1 month | 0 days |
| h041c_v2_backext | 71 | 1h | 1 month | 0 days |
| run_048/050/053_generated | 95/76/96 | 1h | 1 month (last tile ends on the 31st) | 0 days |
| ts_trend_daily_v1 | 15 | 1d | 6 months | 0 days |

Generated protocols come from `_generate_monthly_windows` (`run_phase1_research.py:7627-7657`):
`end` = the first day of the next month = the next window's `start`.

**`end` is inclusive by day** at the engine (`trading-bot/data/fetchers/base_fetcher.py:336`
`_inclusive_end`; spelled out at `run_phase1_research.py:7590-7607` and
`run_protocol.py:2114-2121`). So **every protocol overlaps by exactly one UTC day**: window k
holds bars through 23:00 of day d*, and window k+1 starts at 00:00 of the same day d*. None is
gapped, and none overlaps by more than one day.

**Each window is a separate backtest** (`run_protocol.py:2108-2137`): fresh
`DEFAULT_INITIAL_BALANCE`, flat position. `warmup_prefetch=True` feeds 2 × `required_bars`
before `start` through the strategy **without recording anything**
(`trading-bot/core/trading_bot.py:384-390`, `core/launcher.py:908-925, 971-985`), so recorded
bars begin at the window start. The open position at the end is force-closed and folded into
the final bar's row (`trading_bot.py:602-687`, `replace_if_same_bar`,
`execution/portfolio_info.py:429-490`), so the last `postRebalance_total_value` includes the exit
fee.

**Portfolio today** (`tools/portfolio_daily.py`; `_portfolio_profit_metrics`,
`run_phase1_research.py:10544-10649`):
- per window: common UTC days, coverage ≥ `PORTFOLIO_MIN_COMMON_DAY_COVERAGE = 0.9`
  (`portfolio_daily.py:38, 139-157`), each coin normalized at the window's first common day
  (the **anchor**), portfolio = mean of the normalized coins;
- daily returns only between consecutive common days (`:160-169`); the anchor day adds no
  return; returns **pooled** across windows → `avg_daily_return`;
- drawdown: bar-level, per window, from the anchor close; the **largest window** is the actual
  (`run_phase1_research.py:10614-10631`, basis `portfolio_equal_weight_worst_window`).

Consequence of the one-day overlap: window k's returns cover days (s_k, d*], window k+1's cover
(d*, e_{k+1}] — the pooled list is already a contiguous, non-duplicated chain. **The avg daily
return bar does not change under v2.** Only drawdown (per window → chained) and Sharpe (per
window, per coin → chained portfolio) change.

Sharpe today: `core.sharpe` per window (trade-exit P&L by exit day, ×√365,
`trading-bot/performance/metrics.py:1464-1499`), nulled below 5 trades
(`run_protocol.py:2142-2145`), median per coin (`:2231`), median over coins
(`run_phase1_research.py:9861-9862`), graded at `:10251-10252`.

### Proposed change

A pure function `chain_windows(windows, coins)` in `tools/portfolio_daily.py` (one definition,
also usable later by the composition):

1. Build each window's common curve exactly as today (`window_common_curve`), then **sort the
   windows by anchor date** (not by results order); two windows with the same anchor →
   NOT_EVALUABLE.
2. Chain level L = 1.0 at the first window's anchor close. For each next window w, with
   `last_day` = the last day already chained:
   - anchor == `last_day` (the one-day overlap, every protocol today): scale window w by
     L ÷ v_w(anchor) = L; count its returns for days after the anchor;
   - anchor < `last_day` (overlap of more than one day): the earliest window keeps its days;
     window w joins at `last_day` if `last_day` is one of its common days (scale L ÷ v_w(last_day)),
     otherwise → NOT_EVALUABLE ("overlap without a common junction day");
   - anchor > `last_day` (gap): join at the anchor with scale L (flat across the gap); the gap
     days get no return; count them in `n_gap_days`.
3. Daily returns: the chained consecutive-day returns (identical list to today's pooled
   returns on every current protocol). Avg daily return = mean (unchanged definition).
4. **Sharpe** = mean ÷ stdev(ddof=1) × √365 of that list (G3). NOT_EVALUABLE if fewer than 30
   returns or stdev == 0.
5. **Drawdown**: the chained **bar-level** curve (each window's common bars after its junction
   timestamp, times its scale); actual = 100 × max(1 − V_t ÷ max_{s≤t} V_s) over the whole test.
   Basis `portfolio_equal_weight_whole_test_chained`.
6. Whole-test coverage (G2): counted return days + 1 ≥ 0.9 × calendar days from the first
   anchor to the last chained day, else NOT_EVALUABLE.

Warm-up bars stay excluded (the NOT_READY filter, `portfolio_daily.py:77-78`; with the prefetch
it only removes rows after a large-gap reset). The common-day rule and the 0.9 floor are kept
per window.

**NOT_EVALUABLE (v2)** = every current case (empty results, missing equity file, coin set
differs, < 2 common days, below coverage, no common bar) + duplicate anchor, overlap without a
junction day, whole-test coverage below 0.9, < 30 daily returns / zero stdev (Sharpe only).

**One coin (D-016) vs. several coins.** One coin: common days = that coin's days, the portfolio
is the coin's own equity, the chain is its whole-test equity curve. Several coins (a
cross-sectional variant = a universe): the portfolio is reset to 1/N at every window start (each
coin's backtest restarts its own balance), i.e. an equal-weight book **rebalanced at every
window junction** — same as today inside each window, now chained.

Caveat (G11): the chain pays one forced-exit fee per junction while held, never a re-entry fee
(it falls before the next anchor). Conservative, left as is.

### Tests (S2a)
- contiguous one-day overlap (the real layout): chained returns == today's
  `portfolio_daily_returns` list; drawdown spanning two windows is found (a loss that starts in
  window 1 and continues in window 2 — today's per-window value is smaller);
- a gap: flat link, `n_gap_days`, no return across it; coverage floor triggered by a long gap;
- overlap of several days: earliest window's days kept; a missing junction day → NOT_EVALUABLE;
- results listed out of chronological order → same answer as sorted;
- one coin; two coins with a common-day drop; duplicate anchor → NOT_EVALUABLE;
- Sharpe: known series against a hand-computed value; < 30 returns and zero stdev → NOT_EVALUABLE.

---

## Q2 — Trades per coin over the whole test (C3.2)

### Current state
- Per window: `results[i].core.trade_count` (`run_protocol.py:2147-2151`, from `metrics.json`).
- `per_symbol_summary[s].min_trade_count` = min over windows (`run_protocol.py:2223, 2233`); the
  bar grades the min over coins of that (`run_phase1_research.py:10273-10280`, basis
  `worst_coin`).
- Per-trade records with `symbol`, `window`, `exit_reason` are in `trade_diagnostics.json`
  (`run_protocol.py:604-716, 2193-2211`) in the variant's out dir, next to `results/`
  (`portfolio_daily.py:48-51`). `exit_reason: end_of_window` is detected by timestamp at the
  final bar (`run_protocol.py:540-586`).
- The cost criterion's floor counts **total** trades of all (coin, window) entries in scope
  (`verdict_criteria_evaluator.py:1327-1330`).

### Proposed change
- actual per coin = Σ over windows of that coin's trades whose `exit_reason != end_of_window`
  (G5). The row's actual = the **worst coin** (min); the note carries per-coin raw totals
  (Σ `core.trade_count`) and the excluded count. Threshold `trade_count_min: 100`, `>=`. Basis
  `per_coin_total_whole_test_excl_window_closes`.
- Source check: per (coin, window), the number of records in `trade_diagnostics.json` must equal
  `core.trade_count`, else NOT_EVALUABLE (a broken artifact pair). All `core.trade_count == 0`
  → actual 0 (FAIL), with no file needed. File missing while trades > 0 → NOT_EVALUABLE.
- One coin: the coin's own count. Several coins: every coin must reach 100 (D-035 "per coin").
- Interplay with the cost bar (Q4): its floor is 100 **pooled** trades with a measured cost,
  counted over all records (forced closes included, since they are in the ratio). With one coin,
  raw pooled ≥ the excluded per-coin count, so when the trade-count bar passes the cost floor is
  met; the floor only matters as a guard when records lack a cost.

### Tests
- a synthetic always-long strategy: 1 `end_of_window` trade per window → actual 0, raw = n
  windows; a real signal trade crossing a junction counted once;
- two coins, one below 100 → FAIL on the worst coin; record/core count mismatch → NOT_EVALUABLE;
  no trades anywhere → 0 → FAIL.

---

## Q3 — Buy-and-hold bar (C3.4)

### Current state
Not checked anywhere (D-037). The price series the backtest saw is already in every window's
`portfolio_states.csv`: `record_state` copies the bar's OHLCV into every row
(`execution/portfolio_info.py:467-480`), so a `close` column sits next to
`postRebalance_total_value`. No new data and no cache read are needed.

Costs the engine charged: commission = `config/cost_model.yaml` `fee_rate_bps[symbol]` (spot,
7.5 bps; the pipeline never passes `--cost-product`/`--commission-bps`), slippage =
`trading-bot/config/cost_model.json` per-symbol table (1 bp BTC, 1.5 ETH per side), recorded in
each window's `manifest.json` `config.cost_model.slippage_bps` (`core/launcher.py:863-868`).
Caveat: the same manifest's `fee_bps` is the table value (10), **not** the commission actually
charged, so the fee must come from `cost_model.yaml`, not the manifest.

### Proposed change
- Reader `window_close_bars(path)` next to `window_equity_bars` (same NOT_READY filter, fail
  loud on a missing/non-positive close).
- B&H curve = the **same** `chain_windows` machinery with `close` in place of equity: same
  common days, same anchors, same junctions, same counted days. One coin: exactly buy-and-hold.
  Several coins: equal weight reset at each junction, like the strategy portfolio (no
  rebalancing cost charged to B&H — which favours B&H, so conservative).
- Costs: one round trip per coin for the whole test, c_s = (fee_rate_bps[s] + slippage_bps[s])
  ÷ 10⁴ per side; B&H total = Π(1 + r_bh,d) × mean_s[(1 − c_s)²] − 1.
- Strategy total = final chained level − 1 (its costs are already in the equity).
- **Bar** (G6): actual = strategy total − B&H total (a fraction); threshold
  `buy_and_hold_excess_return_min: 0.0`, comparator `>`. The note shows both totals and the day
  count. Basis `portfolio_equal_weight_vs_buy_and_hold`.
- NOT_EVALUABLE whenever the chain is NOT_EVALUABLE.

### Tests
- synthetic rising prices, strategy flat → FAIL; strategy = the same exposure as B&H → FAIL by
  exactly the cost gap; falling prices, strategy flat → PASS;
- two coins with different paths: equal-weight rebalanced per window, checked by hand;
- missing `close` column → raises; B&H cost uses `fee_rate_bps`, not the manifest's `fee_bps`.

---

## Q4 — 2× cost bar (C3.5)

### Current state
- `realized_edge_to_cost_ratio` (`run_protocol.py:1110-1121`) = mean gross bps ÷ mean
  `cost_paid` bps, pooled over every trade record that has `cost_paid`; gross = the trade's
  `profit_loss_percent` (after slippage, before commission); `cost_paid` = 2 ×
  `fee_rate_bps[symbol]` (`:589-601`). `cost_components_measured.fees` is true only when every
  record has a cost (`:957-997`). Stored in `trade_diagnostics_summary`, which reaches each
  variant's `protocol_result.yaml`.
- Graded today only when 1a picks the menu criterion (`criterion_menu.yaml:24-60`, `> 0.3`,
  floor `min_windows 5, min_trades 15`).
- Not a profit bar; `_bar` knows only `>=` and `<=` (`run_phase1_research.py:10231-10240`).

### Proposed change
- New profit bar `cost_edge_ratio_min: 2.2`, comparator **`>`** (add `>` to `_bar`), plus
  `cost_edge_min_trades: 100`. Actual = `trade_diagnostics_summary.realized_edge_to_cost_ratio`
  of the variant (one definition, shared with the menu), **pooled** over its trades (G7). Basis
  `pooled_trades_realized_edge_to_cost`.
- NOT_EVALUABLE when: no `trade_diagnostics_summary`, ratio None (zero cost), `fees` not true,
  or the number of records < 100 (`per_trade_expectancy_bps.n`; equal to the ratio's record
  count once `fees` is true).
- 2.2 = 2 + slippage round trip ÷ fee round trip (ETH 3 ÷ 15 = 0.2; BTC 2 ÷ 15 ≈ 0.13), so doubled
  slippage is covered too (PLACEHOLDER_VALUES_PROPOSAL §3).
- The menu entry gets the D-039 values (threshold 2.2, `min_trades` 100), still 1a-optional.

### Tests
ratio 2.3 PASS, 2.2 FAIL (strict `>`), negative FAIL; 99 trades NOT_EVALUABLE; zero cost /
missing summary / `fees: false` NOT_EVALUABLE; one coin vs two coins pooled.

---

## Q5 — Values (C3.6)

### Exact edits (in the same PR as the definitions — D-039)

`strategy-research/config/profitability_bars.yaml`:
- Header: remove the "DRAFT -- NOT RATIFIED ... PLACEHOLDER" block (lines 1-11); state "values
  D-039 (2026-09-27); `ratified_by`/`ratified_at` are the operator's signature"; document the v1
  and v2 definitions and the new `basis` strings.
- `sharpe_min: 1.0` (was 0.5) · `max_drawdown_pct_max: 20.0` (was 25.0) ·
  `avg_daily_return_min: 0.0005` (kept) · `trade_count_min: 100` (was 30) ·
  `deflated_sharpe_threshold: 0.95` (kept).
- New keys: `buy_and_hold_excess_return_min: 0.0`, `cost_edge_ratio_min: 2.2`,
  `cost_edge_min_trades: 100`.
- `target_instrument_set` unchanged; `ratified_by: null`, `ratified_at: null` (G9).

Loader (`run_phase1_research.py:2599-2657`): the three new keys become **required only under
`profit_bars_v2`** (a v2 schema = v1 + 3); v1 already ignores extra keys, so the flag-off loader
is unchanged. `ratified_at` also accepts a YAML date (G9).

`strategy-research/config/criterion_menu.yaml`:
- `realized_edge_to_cost_ratio`: `threshold: 2.2` (was 0.3), `floor.min_trades: 100` (was 15);
  rewrite the `basis` text (D-038/D-039).
- `code_added_criteria.residual_ic`: `threshold: 0.02` (was 0.01), `max_p_value: 0.05` (kept;
  one-sided already, `tools/residual_ic.py:22, 296`), `floor.min_n_eff: 30` (kept); replace the
  "PLACEHOLDER, UNRATIFIED" comments with "D-039"; `ratified: false` left for the operator (G9;
  a meta key the code strips, `run_phase1_research.py:3745`).

`config/cost_model.yaml`: no change.

### sha256 consequences (by design)
The evaluation records the whole bars file's sha256 (`BARS_FILE_SHA_FIELD`,
`run_phase1_research.py:4872, 4921-4923, 10697-10737`); a spend refuses `bars_changed` when it
differs (`:4979-4994`). The C3.6 PR changes the file, and the operator's signature changes it
**again** — so any evaluation graded between the merge and the signature is not spendable. The
operator must sign before C4 (C4.1 already says so). Note also: with `profit_bars_file` on and
v2 off, the new values are graded under the old definitions (e.g. 100 as a per-window minimum)
— legacy/test-only paths, acceptable, stated in the header.

---

## Q6 — Branch 3's "PASS iff any one variant clears every bar" (D-004)

- Per variant: `_grade_profit_bars` → PASS only when every row is PASS
  (`run_phase1_research.py:10299-10300`); a NOT_EVALUABLE row blocks.
- Per run: `passing = [variants with PASS]`, result PASS iff non-empty (`:10718-10719`); the stop
  (`_profit_bars_stop_route`, `:10759-10795`) and the spend (`variant_not_passing`,
  `_dsr_on_current_ledger` `:4997-5024`) act on one named passing variant.
- `_write_promotion_audit`'s own DSR OR across variants (`:10093-10132`) is separate, unchanged.
- The composition grid's `profit_bars` cell calls the same `_grade_profit_bars_protocol_result`
  (`:10652-10673`), so it gets v2 too under the flag.
- `campaign_memory.profit_bars_block` (`tools/campaign_memory.py:328-390`) reads bars
  generically by name; `decide_next`'s only re-firable bar is the DSR (`tools/decide_next.py:1001-1006`),
  and every new bar is a fixed-data property — correct as is.

**The new bars do not change the quantifier.** They add rows to each variant's AND. With one
coin per variant (D-016), "any variant" = "any coin", each compared with its own coin's
buy-and-hold; the selection over coins is paid in the DSR's N (one trial row per variant).

---

## Q7 — Flag design and flag-off byte-identity

- New `orchestrator.profit_bars_v2.enabled` in `config/campaign_config.yaml` (next to
  `profit_bars_every_backtest`, `:379`), default false, strict bool (same reader shape as
  `_profit_bars_every_backtest_enabled`, `run_phase1_research.py:2545-2593`), raises if on without
  `profit_bars_every_backtest`; resolved in run_loop's pre-flight (`:12019-12029`, and C1.5's
  launch pre-flight); a `feature_flag_register.yaml` entry.
- On: `_grade_profit_bars` receives a `v2` block from `chain_windows` + trade counts + cost
  ratio; rows keep their names; new `basis` strings; the evaluation gains
  `bars_definitions: v2`. `_evaluation_under_current_bars` also refuses `bars_changed` when the
  evaluation's `bars_definitions` differ from the current flag (no new refusal code, so no new
  RUNBOOK row).
- Off: no code path changes. The golden fixtures (`tests/fixtures/profit_bars_golden/`, five
  cases) and `tests/test_profit_bars_every_backtest.py` / `test_profit_bars_stop.py` stay
  byte-identical — pinned with the fixture bars files they already use, **not** the committed
  values.
- C4.2's target flag set gains `profit_bars_v2: true`.

---

## Q8 — Tests

Unit (S2a, pure): Q1–Q4 lists above. Wiring (S2b): flag reader (quoted `"false"` refused,
dependency raise); loader v2 schema (missing new key raises only under v2; date `ratified_at`
accepted); one row per bar with the v2 basis; `>` comparator; spend refused on a
`bars_definitions` mismatch; flag-off golden fixtures unchanged. **C1.1 extension**
(`tests/test_e061_end_to_end_wiring.py`, rule 8): add `profit_bars_v2: true` to the flag set;
the stubbed `run_protocol` writes per-window `portfolio_states.csv` with `close`, a
`trade_diagnostics.json` with `exit_reason` and `trade_diagnostics_summary` with the ratio; one
variant built to pass every v2 bar (stop → `holdout_decision: continue` → resume, as today) and
one failing only buy-and-hold; assert `bars_definitions: v2` and the seven rows.

---

## Proposed S2 split

| slice | content | depends on |
|---|---|---|
| **S2a** | `tools/portfolio_daily.py`: `chain_windows`, `window_close_bars`, whole-test drawdown/Sharpe, chained buy-and-hold; unit tests (Q1, Q3). Pure, nothing calls it, no flag, no output change. | — (parallel with C2) |
| **S2b** | Definitions **and** values in one PR (D-039): flag + pre-flight + register; loader v2 schema + date fix; `_grade_profit_bars` v2 rows (drawdown, Sharpe, trade count per coin, buy-and-hold, cost ratio, `>`); `bars_definitions` + spend check; `profitability_bars.yaml` and `criterion_menu.yaml` edits (Q5); flag-off golden byte-identity; C1.1 extension. | S2a; C1.1 merged; C2.1 ideally merged first (the per-coin variant shape the e2e test should use) |
| **S2c** | Docs: bars header wording checks, RUNBOOK/USER_GUIDE profit-bar sections, `DECISION_LOG.md` (the accepted guesses as new D-numbers; D-034..D-039 → built-flag-off), Linear E-062. | S2b |

After S2b: the operator signs `ratified_by`/`ratified_at` (and `residual_ic.ratified`) before C4.

---

## Decision (operator's standing instruction, 2026-09-28 night)

The operator is away with a standing instruction: SMALL questions are taken on the S1
recommendation, BIG ones are parked. Recorded by the orchestrator:

- **Accepted as recommended (SMALL):** G1 window chaining (earliest window owns a day, gaps
  linked flat and not counted, a missing junction day treated as a gap); G2 0.9 coverage per
  window and on the whole chained span; G3 Sharpe = mean / sample stdev (ddof 1) x sqrt(365),
  rf 0, NOT_EVALUABLE below 30 daily returns or zero stdev; G4 the DSR bar keeps its
  ledger-consistent basis, only `sharpe_min` moves; G5 trade count excludes
  `exit_reason: end_of_window` forced closes, both counts recorded; G6 buy-and-hold = total
  compounded return over the same counted days, one round trip per coin (fee from
  `cost_model.yaml` + the engine's slippage), PASS iff strategy minus buy-and-hold > 0;
  G7 "survives 2x costs" is a profit bar (branch 3) on the pooled `realized_edge_to_cost_ratio`
  > 2.2 with a 100-trade floor (NOT_EVALUABLE below), the menu entry gets 2.2 / 100 but stays
  optional for 1a; G8 new flag `orchestrator.profit_bars_v2.enabled` requiring
  `profit_bars_every_backtest`, evaluations record `bars_definitions: v2`, a spend under other
  definitions is refused via `bars_changed`; G9 ratification fields stay null for the operator,
  plus the unquoted-date loader fix; G11 no correction for junction fees (conservative).
- **Parked for the operator (BIG):** G10 — slow strategies take the sparse path where no DSR is
  computed, so branch 3 can never pass for them even with D-035's whole-test trade count.
  Fixing it changes trial accounting. Not blocking S2; to be decided with the operator.
- **Sequencing:** S2a (pure functions) may run now in parallel with C1; S2b after C1.1 lands
  (and ideally after C2.1); the operator must sign the bars file before C4 (sha changes at merge
  and at signature).
