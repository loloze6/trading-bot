# E-062 S2b-3 — Partial-coverage normalisation (D-042/D-045): characterization (read-only)

Base: `origin/master` `25df7d5d` (S2b-2b merged). Scope: lift the M1 cap (E-061 C2 S2b) by
normalising the time-dependent bars for a partial-coverage asset variant (D-042), plus Linear
CUL-344 items 4 (repeat key) and 6 (`sign_consistent_by_era` on one era). Method: code, protocol
*definitions* and synthetic numbers only. No backtest, no run result, no ledger or memory write.
Line refs are to `25df7d5d`. `rpr` = `workflow/run_phase1_research.py`, `vce` =
`tools/verdict_criteria_evaluator.py`, `vc` = `tools/variant_coin.py`, `pwt` =
`tools/portfolio_whole_test.py`, `cm` = `tools/campaign_memory.py`.

---

## Contradictions and surprises (flagged, not resolved)

| # | Finding | Against |
|---|---|---|
| X1 | **`sign_consistent_by_era` passes trivially on one era, and not only for partial assets.** The reducer (`vce:1159-1206`) PASSes when every *represented* era has the same nonzero median sign; with one era that is just "the median window is positive". Measured on the 13 committed protocols with the reducer's own era rule: **7 of 13 are single-era for the full base variant** (the five 11-window 2024 protocols; both `funding_mr_*_retest_v1`). A 60% suffix of `h041c_v2_backext` (the train-split shape, 2018-02..2023-12) is also one era (`era_2019_2023_full_feed`). | D-045's premise: "robustness across eras stays covered by the `sign_consistent_by_era` criterion". For the case D-045 opened (a coin listed after 2019-09 on a train-split protocol), the criterion covers nothing. |
| X2 | **The absolute trade floor is inert at the current coverage minimum.** Required = max(100 × f, floor). With f ≥ 0.60 (`D042_MIN_WINDOW_COVERAGE`) the rate term is already ≥ 60, so any floor ≤ 60 never binds. | D-042's "plus an absolute floor" — it only matters above 60 or if the coverage minimum is lowered. |
| X3 | **Normalising the trade count alone does not open branch 3.** The v2 cost row keeps its own absolute floor `cost_edge_min_trades: 100` non-forced trades (`rpr:12110-12125`). A partial variant with 61–99 trades would pass the normalised trade row but read NOT_EVALUABLE on the cost row, which blocks. | D-042 names only the trade minimum and drawdown; the D-038/D-039 cost floor is a second count. |
| X4 | **The repeat-key fix alone wastes a look.** A wider-coverage retest (same config, same coin, same source) collapses in the DSR dedupe (key `(forecast_hash, sorted symbols, source)`, `tools/deflate_sharpe.py:125-195`, lockstep `rpr:10602`), so under S2b-2b its DSR row reads NOT_EVALUABLE `dedup_collapse` (`rpr:11934`, `:12039`) and it can never pass branch 3. | CUL-344 item 4 assumes letting the retest run is enough. |
| X5 | Two era-assignment rules: `vc.window_coverage` uses the window's test **midpoint** (information only, `coverage.eras`); the grid reducer uses the window **label** = first day of the month (`vce:1097-1113`). They can disagree for a window just past an era boundary. | Information only today; worth one rule if eras ever gate. |
| X6 | Side finding: `_bars_file_sha256` (`rpr:5348-5350`) hashes the checkout's bytes. On this Windows worktree (`core.autocrlf=true`, no `.gitattributes`) the file hashes `f96ce688...` while the committed LF blob is `4a75ed66...` (S2B2 quoted the latter). An evaluation graded on one machine refuses `bars_changed` at a spend on the other. Fails closed; not in S2b-3's scope — ticket. | — |

---

## Q1 — Which v2 bars depend on the period length

f = covered / full period length (Q3 defines it). "Easier" = a zero-edge strategy passes with
higher probability on the shorter period, or a real edge needs less evidence.

| bar (`_grade_profit_bars_v2`, `rpr:12190`) | statistic | shorter period makes it… | why | normalise? |
|---|---|---|---|---|
| `sharpe_min` 1.0 | mean/sd × √365 (intensive) | **same expectation, noisier** → easier by luck | SE of annualised SR ≈ 1/√years at SR 0: P(SR̂ ≥ 1 \| SR 0) = 0.0023 at 8.0 y, 0.0056 at 6.42 y, 0.0139 at 4.84 y (normal approx). | **No** — the luck term is the DSR's job, and it is T-aware (next row). Rescaling the threshold would change what Sharpe 1 means. |
| `deflated_sharpe_threshold` 0.95 | BLP DSR on T daily returns | **harder** | √(T−1) in the numerator and σ_null = 1/√(T−1) in SR0 (D-046). Measured in D-046: hurdle annualised Sharpe 1.22 at T = 2695, 1.69 at T = 1394. | No — already period-aware. |
| `avg_daily_return_min` 0.0005 | mean daily return (intensive) | same expectation, noisier | as Sharpe | No. |
| `buy_and_hold_excess_return_min` 0 (`>`) | total strategy − total B&H over the same days | neither in sign; noisier | threshold 0 is scale-free; both legs use the same days (`pwt.chained_buy_and_hold`). | No. |
| `cost_edge_ratio_min` 2.2 (`>`) | ratio of mean gross to mean cost (intensive) | ratio: neither | — | ratio no; **floor: see Q3/X3** |
| `cost_edge_min_trades` 100 (floor of the row above) | count | **harder** (fewer trades accumulate) | a count grows ~linearly with time | operator choice (G4) |
| `trade_count_min` 100 (D-035) | count per coin, non-forced | **harder** | same | **Yes** (D-042) |
| `max_drawdown_pct_max` 20 | max peak-to-trough (extensive) | **easier** | E[max DD] grows with T (∝ √T driftless; ~log T with positive drift; ~T with negative drift). Measured below (Q4). | **Yes** (D-042) |
| grid `sign_consistent_by_era` (branch 1, not a bar) | agreement of era median signs | **easier** — trivially at one era (X1) | fewer eras = fewer chances to disagree | Q6 |
| other grid criteria (per-window reducers) | median/mean/min/max/fraction of window values | neither; their `min_windows`/`min_trades` floors make it harder → INCONCLUSIVE | absolute floors | No (fail-safe) |

`vc.D042_TIME_DEPENDENT_BARS = ("trade_count_min", "max_drawdown_pct_max")` (`vc:92`) already
names exactly the two bars D-042 normalises; this table agrees and adds the cost floor.

---

## Q2 — Where M1 is enforced, and what lifting it changes

| # | site | enforces | lift under the flag (G8) |
|---|---|---|---|
| 1 | `rpr:1839-1841` `_partial_coverage_variants` (`rpr:13723-13740`) in protocol_execution | builds `{vid: reason}` for graded partial variants | reason text changes ("normalised: …"); still built (reports use it) |
| 2 | `rpr:1931-1932` → `vce.evaluate_grid(partial_coverage_variants=…)`: validation `vce:1900-1906`, rollup cap `vce:1954-1958`, reason `vce:1966-1969` | **grid** capped at inconclusive | kwarg not passed under the flag → a partial column can validate the idea. Flag off: unchanged. |
| 3 | `cm:577-582` `_check_validated_is_whole` belt | memory refuses a `validated` grid carrying the key | unchanged (a flag-on grid no longer carries the key; flag-off grids still refused) |
| 4 | `rpr:11495-11500` `_profit_bars_backtest_candidates` tags `partial_coverage` | branch-3 candidate marker | becomes a structured coverage record (f, covered/full days) |
| 5 | `rpr:12381-12385` `_cap_partial_coverage_bars` (`rpr:12303-12330`) in `_evaluate_profit_bars_every_backtest` | **branch 3**: the two bars NOT_EVALUABLE → never `passing`, never `profit_bars_reached` | under v2: replaced by normalised thresholds; the variant can be `passing` → the `profit_bars_reached` stop can fire on it. v1 (`every_backtest` without v2): cap stays (v1's trade bar is a per-window minimum; normalisation is not defined there). |
| 6 | spend (`_validate_holdout_decision` → `_dsr_on_current_ledger`) | **no M1 site** — it acts only on a passing variant, and none could pass | becomes reachable for a partial asset. Nothing re-checks the normalisation at spend; the thresholds are frozen in the evaluation, and `bars_changed` (sha) covers the new bars key. No `bars_definitions` bump needed: every earlier flag-on evaluation of a partial variant is non-passing, so unspendable. |
| 7 | `rpr:1994-2011` reports' `coverage` note | information only (D-003) | unchanged |
| 8 | legacy promote path `_evaluate_profit_bars` `rpr:11310-11317` via `_bridge_partial_coverage` (`rpr:12282-12300`) | caps the bridge file's partial variant | **keep the cap** — this path never uses v2 (S1 G8), so no normalisation exists there. Under v2 it is reached only when no every_backtest evaluation exists (`rpr:12926-12935`). |
| 9 | CUL-344 item 2: C7 `pass_rule_evaluation` on the representative `_rep_vid` (`rpr:1859`: base, else the first graded) — a partial asset when base and design both failed | not capped (M1 caps bars only) | leave as is: legacy routing, holdout steps 1–3 still gate and pause; removal is D-043's. Site 8's cap stays, so the promote-path bars still cannot pass it. |
| 10 | `vc` docstrings, `is_partial_coverage` (`vc:280-296`), `D042_TIME_DEPENDENT_BARS` (`vc:92`) | text | reword; constant kept (it names the normalised bars) |

Composition runs: no per-coin variants (C2 G4), so never partial — no site.

---

## Q3 — Trade count normalisation

**f (G1):** f = |union of nominal calendar days of the variant's windows| ÷ |union of the run
protocol's|, windows' `test.start..test.end` inclusive (the one-day junction overlap counted
once). From protocol files only (no market data, no engine edge days). Full coverage → f = 1.0
exactly. The variant's windows are already verified a subsequence (`vc.check_variant_protocol`).

**Rule (G2):** required = max(⌈100 × f⌉, floor). "Per-year rate × covered years" with rate =
100 / full years **is** 100 × f — the rate is protocol-relative. A campaign-wide fixed rate would
change D-035's 100 for full-coverage variants on protocols of other lengths (0.92 y to 8.0 y
below), so it is not proposed.

Measured full test lengths (nominal first start to last end, inclusive):

| protocol | windows | days | years | rate / year |
|---|---|---|---|---|
| baseline_v1 (+ diagnostic_btceth_4h, escalation_* ×3) | 11 | 336 | 0.92 | 108.7 |
| funding_mr_{4h,daily}_retest_v1 | 49 | 1493 | 4.09 | 24.5 |
| h041c_v2_backext | 71 | 2161 | 5.92 | 16.9 |
| run_050_generated | 76 | 2314 | 6.34 | 15.8 |
| ts_trend_daily_v1 | 15 | 2741 | 7.50 | 13.3 |
| run_048_generated | 95 | 2891 | 7.92 | 12.6 |
| run_053_generated | 96 | 2922 | 8.00 | 12.5 |
| baseline_v2 | 24 | 732 | 2.00 | (ends on the sealed range, refused by `run_protocol.py`) |

Required trades for a coin covering the last k windows (a late listing), three candidate floors:

| protocol | coverage (windows) | f (days) | ⌈100 f⌉ | floor 30 | floor 60 | floor 80 |
|---|---|---|---|---|---|---|
| run_053 | 58/96 (60%) | 0.6047 | 61 | 61 | 61 | 80 |
| run_053 | 68/96 (70%) | 0.7088 | 71 | 71 | 71 | 80 |
| run_053 | 77/96 (80%) | 0.8025 | 81 | 81 | 81 | 81 |
| h041c_v2_backext | 43/71 (60%) | 0.6062 | 61 | 61 | 61 | 80 |
| funding_mr_4h | 30/49 (60%) | 0.6129 | 62 | 62 | 62 | 80 |
| ts_trend_daily_v1 | 9/15 (60%) | 0.6001 | 61 | 61 | 61 | 80 |
| baseline_v1 | 7/11 (60%) | 0.6399 | 64 | 64 | 64 | 80 |

**Recommend floor 60** (G3): inert today (X2) but a belt if `D042_MIN_WINDOW_COVERAGE` is ever
lowered; 30 is inert too and weaker as a belt; 80 flattens 60–80% coverage to 80 and partly
undoes D-042. A signed bars key `trade_count_min_floor: 60`, required only under v2.

**Cost floor (G4, X3):** `cost_edge_min_trades` (100) is a count too. Options: (a) the same
function and floor → required max(⌈100 f⌉, 60); (b) keep 100 absolute → a partial variant needs
100 non-forced trades anyway, so D-042's trade normalisation is inert on branch 3. The floor
exists for the ratio's sample reliability, which a count scaled down weakens. Recommend (a),
because (b) silently nullifies D-042 — but D-042 did not name this floor, so it is the
operator's call. The grid's menu cost criterion (`floor.min_trades: 100`) stays absolute either
way (a shortfall there is INCONCLUSIVE, fail-safe).

---

## Q4 — Drawdown scaling

Direction (D-042): a shorter period has a lower expected max drawdown, so the **same** limit is
easier to meet → the limit must **tighten**: limit(f) = 20 × g(f), g ≤ 1.

Candidates: **unchanged** g = 1; **square root** g = √f (driftless random walk: max DD ∝ σ√T);
**linear** g = f.

| f | unchanged | √f | linear |
|---|---|---|---|
| 0.60 | 20.00 | 15.49 | 12.00 |
| 0.6047 (run_053, 58/96) | 20.00 | 15.55 | 12.09 |
| 0.80 | 20.00 | 17.89 | 16.00 |
| 0.8025 (run_053, 77/96) | 20.00 | 17.92 | 16.05 |

Synthetic check (no market data; i.i.d. normal daily log returns, 20 000 paths, full T = 2922
days; scratch script, not committed). Pass probability P(max DD ≤ limit):

| annual vol, Sharpe | full T | f 0.6: unchanged / √f / linear | f 0.8: unchanged / √f / linear |
|---|---|---|---|
| 4%, 0 | 0.907 | 0.980 / 0.898 / 0.728 | 0.950 / 0.905 / 0.843 |
| 6%, 0 | 0.637 | 0.831 / 0.625 / 0.373 | 0.735 / 0.633 / 0.523 |
| 4%, +1 | 1.000 | 1.000 / 0.999 / 0.991 | 1.000 / 1.000 / 0.999 |
| 6%, +1 | 0.994 | 0.998 / 0.978 / 0.902 | 0.996 / 0.990 / 0.976 |
| 6%, −0.5 | 0.187 | 0.494 / 0.261 / 0.110 | 0.310 / 0.222 / 0.153 |

Reading: **unchanged** is lenient everywhere (0.637 → 0.831) — it violates D-042. **√f** matches
the full-period pass rate for the zero-edge null (0.637 vs 0.625 / 0.633) and is slightly
stricter for a real edge (0.994 vs 0.978) — i.e. conservative where it matters. It is lenient
only for a losing strategy (0.187 vs 0.261), which the Sharpe, avg-return, B&H and DSR bars
fail anyway. **Linear** is stricter than the full period in every case (0.637 vs 0.373): it
makes a partial variant pass *less* easily than a full one, beyond D-042's requirement.
**Recommend √f** (G5); linear is the stricter fallback if the operator prefers margin.

---

## Q5 — CUL-344 item 4: the repeat key

Today: key = `(forecast_hash, sorted symbols, timeframe, window_set)` (`tools/novelty.py:155`),
window set = sha of the **memory entry's protocol_ref** windows (the run protocol), for the
candidate too (`rpr:7342-7362`: "timeframe/windows stay the run protocol's"). A partial asset
tested once keys on the full window set, so every later run of the same config on that coin and
protocol reads REPEAT, whatever its coverage.

Proposal (G11): a per-coin variant whose windows differ from the run protocol's keys its
window set on **its own** windows: `windows:<_canonical_sha(variant windows)>`
(`novelty.py:72`). Memory records `windows_sha256` on that variant's entry only when it differs
(`cm:331-337` builder; `workflow_artifacts/schemas/campaign_memory.schema.json:82-83` has
`additionalProperties: false`, so the schema gains an optional property); `novelty_key` uses it
when present. Result: same coverage → same sha → REPEAT (still blocked); wider coverage or
full coverage → different sha → NOVEL. Every full-coverage variant keeps the run protocol's sha,
so all other keys are unchanged. No real memory is affected: `campaign_record/` holds no
`campaign_memory.yaml` on this checkout, and `variant_loop` is off
(`config/campaign_config.yaml:554-555`).

Interaction with S2b-2b (X4): the retest then runs and collapses in the DSR dedupe. Options:
(a) **extend the dedupe key** with the same optional `windows_sha256` on the trial row, written
only for a partial variant — `(hash, symbols, windows_sha or None, source)`, both lockstep paths
and `select_same_basis_sample` (`deflate_sharpe.py:982`). A row without the field keys as today
(byte-identical, the G6 `symbols` precedent). The retest counts as a new trial (N + 1, the
conservative direction) and gets its own DSR. (b) keep the collapse → the retest can never pass
branch 3; only the grid gains. Recommend (a) (G12) — it changes trial accounting, so BIG.

---

## Q6 — CUL-344 item 6: `sign_consistent_by_era` on one era

Yes, it passes trivially (X1): `vce:1196-1206` — one represented era, nonzero median → `True`.
Its floor (`min_windows 5, min_trades 15`, `config/criterion_menu.yaml:75-90`) does not help.

Fix (G10): fewer than **2 represented eras** → the cell is INCONCLUSIVE with reason
`single_era: <era>` (the reducer's existing "not computable" path, `vce:1287-1290`), never PASS.
A genuine sign disagreement still FAILs. Scope choice: (a) every column under the flag — the
honest fix, but it also turns the criterion INCONCLUSIVE for base variants on the 7 single-era
protocols (an idea picking it there can then never validate); (b) partial-coverage columns only
— the minimum CUL-344 asks for, leaving X1 open for base variants. Recommend (a), BIG (it
changes a grid criterion's meaning beyond partial assets).

---

## Q7 — Flag and byte identity

- **Flag:** reuse `orchestrator.profit_bars_v2.enabled` (S2B2 G6 precedent); no new flag. It
  gates: the branch-3 normalisation (site 5), not passing the grid kwarg (site 2), the era rule
  (G10), writing `windows_sha256` on memory entries and trial rows (G11/G12). The dedupe and
  novelty **reads** key on the field whenever present, flag-independent (N must not change when
  a flag toggles).
- **Flag off:** byte-identical — M1 at every site, grid, memory, ledger, golden fixtures.
- **Flag on, full coverage:** every bar row byte-identical to S2b-2b (normalisation applies only
  when f < 1; G7).
- **Row shape (G13):** a normalised row's `threshold` is the effective value; `detail.normalisation
  = {bars_threshold, coverage_fraction, covered_days, full_days, formula, floor}`. Readers
  (`cm.profit_bars_block`, `decide_next`) read name/result/actual/threshold generically.
- **Bars file (declared):** new key `trade_count_min_floor: 60` (int ≥ 1, required only under
  v2, like the four S2b keys, loader `rpr:2983`). The sha changes again (LF blob `4a75ed66...` →
  new); any evaluation under the old sha is unspendable (`bars_changed`). By design: the file is
  unsigned and signed before C4. No key for the drawdown formula (code, documented in the file
  header), none for the cost floor under G4(a) (it reuses the same floor).

---

## Q8 — Split

| slice | content | tests | model |
|---|---|---|---|
| **S2b-3a** pure | `vc`: `coverage_fraction(run_protocol, variant_protocol)`, `normalised_trade_minimum(base, f, floor)`, `scaled_drawdown_limit(limit, f)`. Nothing calls them. | f = 1.0 exactly on full; the table values above (run_053 58/96 → 0.6047, 61, 15.55); one-day junction counted once; non-contiguous windows; not a subsequence raises; f ∉ (0, 1] raises; floor binds when 100 f < floor; ⌈⌉ not round | Opus |
| **S2b-3b** wiring (flag) | sites 1–5 and 10 under v2; the era rule; loader key + bars file; cost floor per G4; register text | flag off: every M1 test unchanged; flag on: partial variant just above each normalised threshold PASSes and raises `profit_bars_reached`, just below FAILs; full-coverage rows byte-identical to S2b-2b; grid validates with a partial column; v1 `every_backtest` still capped; legacy promote path still capped with v2 on; single-era cell INCONCLUSIVE; loader requires the key only under v2 | Opus |
| **S2b-3c** repeat + dedupe (item 4) | memory `windows_sha256`, schema, `novelty_key`, `_check_variant_repeat`, trial-row field, both dedupe paths + `select_same_basis_sample` | same coverage REPEAT, wider NOVEL, full-after-partial NOVEL; lockstep dedupe on committed + random legacy ledgers unchanged; partial + wider rows = 2 trials; the retest's DSR is no longer `dedup_collapse` | Opus + safety review |
| S2b-4 | docs (as planned) | — | Sonnet |

**Declared test changes:** `tests/test_e062_s2b1_profit_bars_v2.py:657`
(`test_partial_coverage_cap_still_applies_under_v2` — the cap under v2 becomes the
normalisation). The M1 tests in `tests/test_e061_c2_s2b_one_coin_per_variant.py:895-1013` run
flag-off and stay. 3c: the dedupe lockstep tests gain cases, no expected value changes.

---

## Q9 — Guesses for the operator

| # | Question | Recommendation | Size | Blocks build? |
|---|---|---|---|---|
| G1 | What is f? | nominal calendar days of the variant's windows ÷ the run protocol's (union, from protocol files) | SMALL | yes (3a) |
| G2 | Trade minimum formula | max(⌈100 × f⌉, floor); the "per-year rate" is protocol-relative (= 100 × f) | SMALL (D-042 decided) | yes (3a) |
| G3 | Absolute floor value | **60**, signed key `trade_count_min_floor` (inert at the 0.60 coverage minimum, X2) | **BIG** (new signed value) | no (key required, value signed) |
| G4 | Cost-ratio floor (100) | same function and floor (else D-042 is inert on branch 3, X3) | **BIG** (not named by D-042; loosens a D-039 floor for partial variants) | yes (3b) |
| G5 | Drawdown formula | 20 × √f (neutral on the zero-edge null, conservative for a real edge); linear is the stricter fallback | SMALL (direction fixed by D-042, measured) | yes (3a) |
| G6 | Sharpe, avg return, B&H, DSR, cost ratio value | unchanged (intensive or already T-aware) | SMALL | no |
| G7 | Who is normalised | only f < 1; full-coverage rows byte-identical | SMALL | yes (3b) |
| G8 | Grid lift | under v2 the grid kwarg is not passed; memory belt kept for flag-off grids | SMALL | yes (3b) |
| G9 | Legacy promote path / C7 on a partial asset (CUL-344 item 2) | keep M1's cap there; C7 left to D-043 | SMALL | no |
| G10 | Era rule | < 2 represented eras → INCONCLUSIVE, **every column** under v2 (X1) | **BIG** (base variants on 7/13 protocols affected); SMALL if partial-only | yes (3b) |
| G11 | Repeat key | per-variant window sha when it differs from the run protocol's | SMALL | yes (3c) |
| G12 | Dedupe key for the retest | add the same optional window sha (N + 1, own DSR) | **BIG** (trial accounting) | yes (3c) |
| G13 | Row shape | effective `threshold` + `detail.normalisation` | SMALL | yes (3b) |
| G14 | Flag | `profit_bars_v2` for every write; dedupe/novelty reads flag-independent | SMALL | yes |
| G15 | X6 (line-ending sha) | ticket, outside S2b-3 | SMALL | no |

## Decision (operator, 2026-09-29) — recorded as D-047

- **G3:** floor 60 (`trade_count_min_floor`, signed with the bars file). The operator asked for a time-based
  minimum ("a trade per day?"); that re-decides D-035 and 1/day would exclude slow strategies, so per the
  operator's own fallback it is **parked** (calendar-rate minimum, to choose after C4 real trade counts).
- **G4:** the cost-ratio trade floor scales the same way (100 x f, floor 60).
- **G5:** drawdown limit x sqrt(f), as recommended.
- **G10:** fewer than 2 eras -> INCONCLUSIVE on every variant (under profit_bars_v2).
- **G12:** wider-coverage retest = new trial (window fingerprint in the repeat key and the dedupe key).
- SMALL guesses as recommended. Split 3a (pure) -> 3b (wiring) -> 3c (repeat key + dedupe), each reviewed and merged.
- **X6** (bars-file sha depends on line endings: CRLF f96ce688... on this Windows checkout vs LF 4a75ed66...,
  verified by the orchestrator) -> separate ticket, before any cross-machine holdout spend.

### S2b-3a built

- `tools/variant_coin.py` (commit `2237c546`): `coverage_days` / `coverage_fraction` (G1; windows parsed by `pwt.window_bounds_from_protocol`; not-a-subsequence raises), `normalised_trade_minimum` (max(⌈base·f⌉, floor); a float f is read as its day ratio, so float noise cannot bump the ceil; floor > base raises), `scaled_drawdown_limit` (limit·√f), `era_count_shortfall` (< 2 eras → `single_era: <eras|none>`). Nothing calls them (3b wires them).
- Era rule: `era_count_shortfall` takes era ids already assigned by the grid reducer (`vce._reduce_sign_consistent_by_era`: window label → first day of its month, `era_unmapped` excluded); it assigns none itself, so X5's midpoint rule (`coverage.eras`) stays information only. 3b passes the reducer's `by_era` keys.
- `tests/test_e062_s2b3a_normalisation.py`: 70 tests; every Q3/Q4 table row reproduced from the committed protocols (run_053 58/96 → 1767/2922 days, f 0.6047, 61 trades, 15.55; 77/96 → 0.8025, 81, 17.92; the other five rows too).
