# Deliberate divergences from upstream (loloze6/trading-bot)

One line each — keeps the eventual merge with Jeremy a checklist, not archaeology.

**Reset 2026-07-28.** This file was emptied when the fork was returned to Jeremy's `70dab378`. The tree is currently **byte-identical to upstream**; there are zero divergences. Every line added below from here on is a deliberate, reviewed decision.

Pre-reset divergences are recorded in the archive tags (`git show archive/2026-07-28/mac-bootstrap`), not here — they are history, not current state.

## Current divergences

All four below are from `mac/setup`, 2026-07-28, milestone 1 ("make Jeremy's bot run"). They are a single logical unit; the first three are the known first-run blockers and the fourth is forced by the first.

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 1 | `trading-bot/strategy_config.json` | `default_regime` `"mean_reversion"` → `"unknown"` | **Yes — this is a bug on every platform.** With non-empty `rules`, `"mean_reversion"` fails validator V9 and `AdvancedStrategy.__init__` raises `ValueError: invalid strategy_config` (`strategies/main_strategy.py:32`) before the first bar. Nothing runs, and the 4 slow regression tests error rather than execute. Already covered by open PR #1. |
| 2 | `trading-bot/config.json` | `trading.symbols` `["ETHUSDT"]` → `["BTCUSDT"]` | Probably not. Local-environment fit: no `ETHUSDT_*.csv` exists in `local_data/`, so the shipped default cannot run offline here. Jeremy may legitimately have ETH cached. |
| 3 | `trading-bot/requirements.txt` | pin all 11 existing to installed versions; add `ccxt`, `matplotlib`, `requests`, `PyYAML` | **Yes.** All four are imported by shipped code and absent from the file. The `pandas==2.3.3` pin is load-bearing beyond tidiness — pandas 3.x parses caches to `datetime64[us]`, which silently changes `run_artifact.data_sha256` with no error, making every artifact incomparable to prior baselines. Comment in-file explains it. |
| 4 | `trading-bot/tests/fixtures/reference_run.json` | `76 / −270.797424 / −4.364` → `24 / −231.758912 / −5.646` | **Yes, as a consequence of #1.** The old values were validly measured on 2026-06-27 (`0ca4666d`, config `2754e184`); V9 was added three days later (`d570ffcd`, 2026-06-30) and made that config illegal, so from then on the four tests errored instead of running. Rebaselined from measured run `20260728T132811Z_5ccbec42`. |

Verified: fast 99 passed; slow 9 passed / 1 skipped / **0 errors** (was 6 passed / 4 errors before the change); validator exit 0; reference run reproduces `config_sha256 5ccbec42` / `data_sha256 5a75366c` / net −23.021% / sharpe −5.646 / maxDD −24.592% / 24 trades / fees 68.897289, and is byte-identical across two independent invocations and two independent venvs.

**Control run — the evidence that this is not "changing the test to match the code".** Replaying the *old* config (`2754e184`) with only the V9 check suppressed still yields **76 trades / −270.797404 / sharpe −4.364**, and `mean_reversion` bar_count 794 vs 208 after the change — a difference of exactly the 586 bars that now resolve to `unknown`. The engine is unchanged; 100% of the delta is the declared config fix. Note the old `net_pnl` reproduces to 2.0e-5 rather than exactly (`−270.797404` vs the recorded `−270.797424`) — inside the fixture's own 0.01 tolerance, cause unidentified, presumed float accumulation order. Recorded rather than ignored because this fork's thesis is bit-identity.

**Correction, 2026-07-28:** an earlier draft of row #4 and of the fixture note claimed the old values were "unreachable, not merely stale." That is false and refutable with one `git log` — the config was legal when they were recorded. The same wording is currently on the Notion P2 issue page and underlies PR #1's framing to Jeremy. The accurate justification is the control run above, which is stronger.

### `fix/regime-default-fail-safe` — 2026-07-28

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 5 | `trading-bot/strategies/regime_engine.py:137` | default-regime fall-through `MarketRegime.MEAN_REVERSION` → `MarketRegime.UNKNOWN` | **Yes — platform-independent, one word.** |
| 6 | `trading-bot/tests/test_regime_default_fallback.py` | new file, 7 tests | Yes, ships with #5. |

`_classify_threshold_rules()` ended with `_REGIME_MAP.get(self._default_regime, MEAN_REVERSION)`. That fallback fires only for a value absent from `_REGIME_MAP` — an explicit `null`, or a name V7 would reject — and it resolved to the **one regime carrying components**, i.e. the only one that trades. An explicit `null` passes validator V9 with zero errors (V9 tests only the three literal names) and then traded every unmatched bar while all checks reported green.

**Why the engine and not V9:** it closes the whole class (any unmapped value, including a typo'd name reaching the engine unvalidated) rather than the one known instance, and it removes an internal inconsistency — the veto fallback (`:114`) and the rule-match fallback (`:136`) already return `UNKNOWN`. Two of three said fail-safe; one said fail-into-trading. Hardening V9 as well was considered and **deliberately declined** as a guard on a guard for an already-neutralised fault; kept as an optional Notion follow-up so the choice stays revisitable.

Note the asymmetry this closes: a *missing* `default_regime` key was always safe — `regime_engine.py:70` reads it as `config.get("default_regime", "unknown")`, and the *string* maps correctly. Only an *explicit* null was unsafe.

Verified: the 2 regression tests were **watched failing** before the fix (`MEAN_REVERSION is not UNKNOWN`) and pass after; further tests pin that all four valid names and the missing-key path are unaffected. Fast suite 99 → **108 passed**; slow **9 passed / 1 skipped / 0 errors**. Bit-identity proven, not assumed: `main.py simulate` after the change is **byte-identical** to the committed reference artifact on `bars.csv`, `portfolio_states.csv`, `trades.json`, `metrics.json`, `forecast_distribution.csv`, with `config_sha256 5ccbec42` / `data_sha256 5a75366c` and every metric unchanged.

**Why no config can reach the fallback — measured repo-wide, not sampled.** Parsing every JSON in the tree (3,288 files): **1,011 `default_regime` occurrences — `'unknown'` ×748, `'trending'` ×138, `'mean_reversion'` ×125, and zero nulls or unmapped values.** All four are in `_REGIME_MAP`, so `.get()` returns before the fallback is consulted. An earlier draft of this row justified the same conclusion with "both configs in the repo" — true of `trading-bot/` but a 0.2% sample of the real surface, since 999 of those occurrences live under `strategy-research/`. Conclusion unchanged; the basis is now the measurement.

*Caveat that no scan here can close:* `strategy-research/workflow/` is off-limits and unread, so if it **generates** configs at runtime rather than shipping committed JSON, its output is outside this count. Likewise Jeremy's own tree and unpushed branches. A `default_regime: null` config anywhere in those would change behaviour silently on merge — see the fail-silent note below.

**Public-path coverage, added after adversarial review.** The first version of the test file drove only the private `_classify_threshold_rules()`; a review proved that hollow by reintroducing the defect one level up inside `classify()`, where **0 of 7 tests failed**. Coverage now runs through `classify()` itself, with a control proving the fixture is not vacuously `UNKNOWN` (`classify()` short-circuits to `UNKNOWN` when not ready, so the control is load-bearing).

**This layer alone was not sufficient** — it traded fail-into-trading for fail-*silently*-flat. Completed in the validator by row 7 below.

### `fix/validator-rejects-null-default-regime` — 2026-07-28

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 7 | `trading-bot/tools/validate_config.py` | V7 and V9/V10 now read `rd.get("default_regime", "unknown")` instead of the raw value; V7's `is not None` skip becomes a plain membership test | **Yes — platform-independent, two lines.** |
| 8 | `trading-bot/tests/test_validate_config.py` | +8 tests | Yes, ships with #7. |

The root fault was **one mistake expressed in two dialects**: `validate_config.py` used `is not None` as a *skip*, where the engine used `.get(key, "unknown")` as a *substitute*. So `None` meant "don't check" to the validator and "unknown" to the engine. Both sites now use substitute-semantics, matching `regime_engine.py:70`.

Two distinct holes closed:

1. **Explicit `null` validated clean.** V7 skipped it (`is not None`), V9 tests a three-string tuple it isn't in, V10 skipped it too. Three rules blind to one value. Now V7 rejects it, so no such config can construct an `AdvancedStrategy` at all.
2. **An *omitted* key made V10 blind to a dead config.** A fully-ungated config with no `default_regime` resolves every bar to `unknown`; if `strategies.regimes.unknown` is null it forecasts 0.0 forever — verbatim what V10's own message describes — and V10 skipped it because it judged the raw value rather than the effective one. Pre-existing, unrelated to the null case, found by review.

**The absent-key case stays legal** — that is what makes this a fix rather than a tightening. `.get()` substitutes only for a *missing* key, so an explicit null still yields `None` and still trips V10's `is not None` guard at `:243`. That guard is kept deliberately: removing it (as an earlier draft of this file pre-registered) would emit a correct V7 *plus* a garbled `strategies.regimes.None` V10 for a single fault, since `validate()` collects violations without short-circuiting. Verified both ways.

Verified: 3 V7 tests and 1 V10 test **watched failing** before their respective fixes; mutating either line back fails tests the other does not cover. Fast suite 108 → **116 passed**; slow 9 passed / 1 skipped / 0 errors; validator exit 0; `simulate` byte-identical to the committed reference artifact.

**Reachability — audited, and it strengthens the case rather than qualifying it.** All **1,011** `regime_detector` dicts in committed JSON carry a valid `default_regime` (`'unknown'` ×748, `'trending'` ×138, `'mean_reversion'` ×125) — zero nulls, zero omissions, so no committed config changes verdict.

The runtime generators are no longer an unaudited caveat. `strategy-research/workflow/` was read in full (7 files):

- **Strategy configs are LLM-authored.** Stage `backtest_specification` (`workflow/stages.yaml:54`) has a `skill:` and no `tool:` — it is a model stage. `run_phase1_research.py:4885` writes its `backtest_spec.yaml → config` block **verbatim** to `candidate_strategy_config.json`.
- **`tools/validate_config.py` is the gate**, invoked immediately after at `:4888`; a non-zero exit routes the run to `failed_validation`. The validator hardened here is the only thing between an LLM-authored config and a backtest.
- **The model has demonstrably emitted an invalid regime name**: `runs/run_043/attempt_1_blocked/` invented `"active"`. V7 caught it then and still does (exit 1) — that fixture is already the non-regression test at the top of `tests/test_validate_config.py`.
- **The model has demonstrably dropped a mandatory field silently**: `run_phase1_research.py:4876-4883` force-injects `significance_methodology` because run_047's spec stage omitted it despite an explicit skill instruction. **A silently-omitted field is exactly the mechanism that produces an absent `default_regime`** — i.e. the V10 hole closed above is reachable by a documented failure mode of this pipeline, not a hypothetical one.
- The only other generator, `tools/retune_regime_detector.py:351`, hardcodes `"default_regime": "unknown"` and is safe.

`strategy-research/workflow/` cannot be *executed* here — it imports `claude_agent_sdk` and hardcodes Windows paths (`venv/Scripts/python.exe`). That is an executability limit, not a reason to leave it unread.

## Known-broken upstream, deliberately NOT fixed here

- **`tests/test_regression_backtest.py:39` — `test_config_actually_loaded` has never executed.** The `backtest_result` fixture returns from inside `with tempfile.TemporaryDirectory() as tmp:`, so the run dir is deleted the moment the fixture returns. The three sibling tests survive because `metrics` is already in memory; this one reads `manifest.json` from disk afterwards, finds nothing, and hits `pytest.skip` at line 114 — unconditionally, on every platform. The config-identity check that would catch "the backtest ran a different config than specified" is therefore dead code. Pre-existing upstream defect, unrelated to milestone 1, left for its own branch. Do not read `1 skipped` as benign.

## Decisions deferred to the first sessions

- **`.claude/commands/`** — the fork's 4 slash commands (`/red-team`, `/new-hypothesis`, `/run-baseline`, `/sync-upstream`) are restored on disk but Jeremy's `.gitignore` excludes `.claude/`, so they are currently untracked and would be lost on a clone. Tracking them requires a `.gitignore` divergence. Dorian's call.
- **`CLAUDE.md`** — Jeremy's version has no `@CLAUDE.fork.md` include, so the fork's guardrails do not auto-load into an agent session. Two lines would fix it, and it is arguably the highest-value divergence available. Dorian's call.
- **`venv/`** — upstream tracks 449 files of a Windows venv. The Mac venv lives at `.venv/`. Untracking upstream's is a separate, PR-worthy change; not done.
