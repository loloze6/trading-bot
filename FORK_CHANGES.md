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

### `mac/setup` — housekeeping, 2026-07-28

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 9 | `.gitignore` | ignore `.omc/` | **No — fork-only.** Jeremy's tree has no `.omc/`; the directory only exists because this lab runs oh-my-claudecode. Offering it upstream would ask him to carry a rule for tooling he does not use. |

`.omc/` is machine-local runtime state — session files, HUD caches, subagent tracking, mission/PRD scratch — regenerated on demand and never source. Three exist (repo root, `trading-bot/`, `strategy-research/`) and the single pattern covers all three; verified with `git check-ignore` on each.

Nothing under `.omc/` was ever tracked (`git ls-files | grep .omc/` → 0), so a plain ignore is sufficient — no `git rm --cached` needed. Before this, a `git add -A` would have committed OMC operational state into the fork.

**Cheapest-control note:** `.git/info/exclude` would have achieved the same with *zero* divergence from Jeremy. `.gitignore` was chosen anyway because it survives a fresh clone and is discoverable by the next session, and because a `.gitignore` line is about the least merge-conflict-prone divergence available. If minimising divergence ever matters more, this is a safe one to drop.

### `fix/data-holdout-safety` — 2026-07-28 (fork queue #1)

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 10 | `trading-bot/data/fetchers/base_fetcher.py` | `_load_all` expands the caller's inclusive day exactly once (`_inclusive_end`), passes it to `_identify_missing_periods`, clamps every fetched chunk (`_trim_to_period`), filters `<= window_end` | **Yes — the primary fetch path writes sealed data today.** Measured: a fetch bounded 2025-12-31 wrote daily bars through 2026-03-19. Also closes the `+1 day` end-widening and the −1ms midnight period-end re-widening (244 live trigger rows in `BTCUSDT_funding_8h.csv`). |
| 11 | `trading-bot/data/fetchers/whale_footprint_fetcher.py` | `_end_of_day_if_midnight` docstring re-anchored to `_inclusive_end` | Yes, ships with #10 — the old text cites the replaced trim line. |
| 12 | `trading-bot/tests/test_fetch_end_bound.py` | new file, 10 tests | Yes, ships with #10. |
| 13 | `trading-bot/core/launcher.py` | `visualize_data`: `end_date` `'2026-04-23'` → `'2025-12-31'`; `validate_quality_data_continuity` → `validate_data_continuity` | **Yes — both are plain bugs.** The old date sits inside the sealed holdout with `localStorage=True` at 60s interval (~500k sealed 1m bars per run); the old method exists on no fetcher, and the AttributeError landed *after* the cache write. |
| 14 | `trading-bot/tests/test_visualize_data_window.py` | new file, 3 tests (reads `holdout_range` from `campaign_data_policy.yaml`) | Yes, ships with #13. |
| 15 | `trading-bot/tests/test_no_sealed_date_literals.py` | new file, 1 test — static scan: no executable string date at or beyond the seal's start | Yes — upstream ships `strategy-research/` too, so the policy read resolves there. |
| 16 | `trading-bot/data/fetchers/fear_greed_fetcher.py` | `_fetch_remote` window filter `< end + 1 day` → `<= end` | Yes, ships with #10 — the same widening the orchestrator fix removed, left in a subclass; it received already-literal period ends and expanded them again. |
| 17 | `trading-bot/tests/test_no_sealed_date_literals.py`, `trading-bot/tests/test_visualize_data_window.py` | four reads pinned to `encoding="utf-8"` (2026-07-30) — on Windows cp1252 the seal test crashed with UnicodeDecodeError before scanning a single date (Jeremy's measurement); the policy-YAML sites are determinism hardening, not crash fixes | Yes — pushed to the PR #2 branch (`7f0ad3a5`); on `mac/setup` as `35b48736`. |
| 18 | `trading-bot/tests/test_no_sealed_date_literals.py` | `ISO_DATE` → `(?<!\d)\d{4}-\d{2}-\d{2}` + 8 extraction tests (2026-07-30, board 3.5, merged `8acd08e6`) — `\b` on either flank let T-form timestamps and word-char joins (`BTCUSDT_2026-…_1h.csv`) slip the seal scan; scan output on the clean tree identical (10 extractions, 0 violations) | Yes — after PR #2 merges (the file doesn't exist upstream yet). |
| 19 | `trading-bot/tests/test_regression_backtest.py` | fixture `return`→`yield` + skip→fail + honest docstring/failure text (2026-07-31, board 4.5, merged `f3d85745`) — revives `test_config_actually_loaded`, never executed on any platform; scope corrected to manifest integrity | Yes — after PR #1 merges (only demonstrable with its config fix). |
| 20 | `trading-bot/performance/bar_equity.py` (new), `reporting/run_artifact.py`, `core/backtester.py`, `core/launcher.py`, 3 test files + fixture | off-by-default `bar_equity` block in `metrics.json` (2026-07-31, board #5, merged `eaa4b41c`) — bar-level maxDD/Sharpe/textbook-Sortino + exposure/turnover/counts from `portfolio_states.csv`; fail-loud on degenerate inputs; flag-off byte-identical (independently reproduced) | Yes — after PRs #1–#3 merge; addresses review P7 (partially, off-by-default). |

Extracted from `archive/2026-07-28/fix-fetch-end-bound` at its reviewed **tip** (four review rounds after the original commit), per the ledger's cherry-pick-deliberately instruction. The archive's 148-line runtime write-tripwire was **deliberately not restored** — its own tag message rates it "reconsider": it guarded only the write path while measurably handing 1,440 sealed rows to a read-path caller.

**The static check is prose-aware, and the reason was found by execution, not design taste.** The archive tag recommended "no date literal anywhere in the repo inside `holdout_range`, ~15 lines." That version was built first and immediately failed on the clean tree: upstream's own `FetchGapError` docstring (`base_fetcher.py:49`) names `2026-01-01` while documenting an incident, as do the ported fix docstrings. A control that fires on the tree it protects is broken as designed, and rewording Jeremy's prose to appease a fork test would be a drive-by divergence. The shipped scanner tokenizes production `.py` files, scans **string tokens only** (a date can reach a fetcher only through a string, never bare code), excludes docstrings by AST position, and raw-scans the two committed config JSONs.

**Launcher bound is a literal, not a policy read — deliberately.** The archived fix imported a fork-only policy module into production `launcher.py`. The literal `'2025-12-31'` plus the static scan gives the same protection (a seal that moves over the constant fails the suite on the commit that moves it) with zero new production imports, keeping #13 mergeable upstream as-is.

**Adversarial review round (same day), two independent opus lanes — one must-fix found and fixed.** Both lanes independently proved the first cut regressed idempotency: the inclusive `window_end` made the type-2 completeness check see the sub-bar remainder after every complete cache's last bar — a phantom top-up fetch, a network call and a cache rewrite per run, with the top-up's first page opening past the requested end (the red-team measured it printing sealed-span rows to stdout via CcxtFetcher's fetch log before the trim). The reference-run byte-identity could not see it because `simulate`'s window ends mid-cache. Fixed by requiring a whole interval to fit before `end_date` (a bar can only exist on the grid); regression test pins the complete-cache case to zero fetches and a byte-untouched file. The review also hardened the scanner (relative-path exclusions — absolute-path matching let a checkout under any dir named `venv`/`tests` scan zero files and pass vacuously; a `core/launcher.py` sentinel assertion; and the rule widened from "inside the seal" to "at or beyond its start", since the straddle shape — both window literals outside the seal, the span crossing it — is what actually contaminated the seven Binance caches). Deferred with tracking: wiring `strategy-research/tools/holdout_date_gate.sh` into the installed pre-commit; the Kraken ingest path's direct `_merge_and_store` bypass (pre-existing, queue #9); `visualize_data`'s cache landing in tracked `trading-bot/data/` (pre-existing hygiene); whale's duplicate midnight rule.

**Verifier round (independent third lane) — approved, and two coverage gaps it proved by mutation were closed.** Disabling type-2 gap detection outright (or doubling its threshold) had survived the entire suite — a fetcher silently stopping cache top-ups while logging "complete". A companion under-fetch test now pins that direction (cache one bar short → exactly one trailing period, missing bar lands on disk). The fear&greed `<= end` fix was likewise untested — reverting it passed everything; a stub-API test across a seal-spanning payload now fails on the revert. The verifier also re-proved bit-identity **at the branch tip** (the committed baseline artifact predated the review-fix commits) and flagged that the scanner's at-or-beyond-seal-start rule is deliberately broader than its straddle rationale — the docstring now says so explicitly.

Verified at the branch tip: fast **130 passed** (116 + 14 new); slow **9 passed / 1 skipped / 0 errors**; validator exit 0; `simulate` **byte-identical** to the committed reference `20260728T132811Z_5ccbec42` on all five artifact files (`config_sha256 5ccbec42` / `data_sha256 5a75366c` / net −23.021% / sharpe −5.646 / 24 trades / fees 68.897289). **Fourteen distinct mutations across the lanes, all killed** at public entry points: chunk clamp removed (5 tests fail); window filter reverted (exactly the red-team B1 test); type-2 whole-bar condition reverted (idempotency + C1); type-2 disabled outright and threshold doubled (under-fetch companion); `'2026-04-23'` restored (behavioral test and static scan independently); launcher method name reverted; fear&greed widening restored; in-seal and straddle string literals planted (each caught with `file:line`); `core/` excluded from the scan (sentinel fails loudly); `window_end` swap in `_identify_missing_periods`; `_inclusive_end` made literal for date-only ends. Negative control: a sealed date in a *comment* correctly does not fire.

## Known-broken upstream, deliberately NOT fixed here

- **`tests/test_regression_backtest.py:39` — `test_config_actually_loaded` has never executed.** The `backtest_result` fixture returns from inside `with tempfile.TemporaryDirectory() as tmp:`, so the run dir is deleted the moment the fixture returns. The three sibling tests survive because `metrics` is already in memory; this one reads `manifest.json` from disk afterwards, finds nothing, and hits `pytest.skip` at line 114 — unconditionally, on every platform. The config-identity check that would catch "the backtest ran a different config than specified" is therefore dead code. Pre-existing upstream defect, unrelated to milestone 1, left for its own branch at the time. **FIXED 2026-07-31** (`fix/regression-test-fixture`, merged `f3d85745`, row 19): the fixture yields, the test executes, and a missing manifest is now a hard FAIL. Mutation-proven scope correction: the revived check guards **manifest integrity**, not config_path wiring — the reference config IS the hardcoded fallback's file, so a silent fallback reads as a pass; the wiring guard is tracked on the board (Medium). Slow suite: 10 passed / 0 skipped.

## Decisions deferred to the first sessions

- **`.claude/commands/`** — the fork's 4 slash commands (`/red-team`, `/new-hypothesis`, `/run-baseline`, `/sync-upstream`) are restored on disk but Jeremy's `.gitignore` excludes `.claude/`, so they are currently untracked and would be lost on a clone. Tracking them requires a `.gitignore` divergence. Dorian's call.
- **`CLAUDE.md`** — ~~Jeremy's version has no `@CLAUDE.fork.md` include, so the fork's guardrails do not auto-load into an agent session. Two lines would fix it, and it is arguably the highest-value divergence available. Dorian's call.~~ **DONE 2026-07-31, Dorian approved — see row 21.**
- **`venv/`** — upstream tracks 449 files of a Windows venv. The Mac venv lives at `.venv/`. Untracking upstream's is a separate, PR-worthy change; not done.

## Upstream merged PRs #1-#3 — sync merge, 2026-07-31 (`290ed4fb`)

Jeremy merged PRs #1, #2, #3 into `loloze6/trading-bot` master (`63237b88`, true
merges — our commit SHAs are upstream history; W8-W15 still unpushed, so his
local master is now diverged from his own GitHub). Synced back with
`git merge upstream/master`; four conflicts resolved by pre-registered map
(3x fork's version kept; `reference_run.json` took UPSTREAM's — the corrected
`3e00f895` provenance was never cherry-picked back to `mac/setup`, so the fork's
copy still carried the refuted "three days" claim). Post-merge verified: fast
165, slow 14-0-0, validator 0, `simulate` byte-identical to the committed
reference on all five files.

Status changes to the rows above:

- **Rows 1-6, 10-17: no longer divergences.** Upstream now carries the same
  content (rows 1-4 via PR #1, 5-6 via PR #3, 10-17 via PR #2).
- **Rows 7-8 (validator half), 18 (seal regex), 19 (regression fixture),
  20 (bar_equity): offered upstream 2026-07-31** as PRs #6, #4, #5, #7
  respectively — branches `0e51bdb7`, `8ab938b1`, `6941b0aa`, `11bcac06`, each
  cut from `63237b88`, suites verified on that base (control fast 120 passed /
  2 skipped, slow 9 passed / 1 skipped; the 2 fast skips are the Kraken-archive
  tests, archive absent in the verification worktrees).
- **Row 9 (`.omc/` ignore): unchanged, fork-only.**
- Residual `mac/setup` vs `upstream/master` delta beyond the four open PRs:
  fork docs (`CLAUDE.fork.md`, `research/`, this file), the committed reference
  artifact `results/runs/20260728T132811Z_5ccbec42/`, `.gitignore` (.omc), and
  `requirements.txt` comment wording (fork's EXACT-pin note is newer than the
  PR #1 text upstream took; pins identical).

### `CLAUDE.md` include — 2026-07-31, Dorian approved

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 21 | `CLAUDE.md` | added a fork-only section with `@CLAUDE.fork.md` so the fork's guardrails auto-load into every agent session | **No — fork-only by definition.** Jeremy has no `CLAUDE.fork.md`. Previously listed under "Decisions deferred"; decided 2026-07-31. On merge/PR days, keep this section out of anything offered upstream. |

### `fix/workflow-macos-port` + `fix/close-positions-nameerror` — merged 2026-07-31 (`33c6fbe9`, `1c84ba0e`)

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 22 | `strategy-research/workflow/run_phase1_research.py`, `strategy-research/tools/retune_regime_detector.py`, `trading-bot/tests/test_tbot_python_resolver.py` (new), `strategy-research/requirements-mac.txt` (new) | per-file `_resolve_tbot_python()` replaces 4 hardcoded Windows interpreter paths; predicate = executable regular file (the committed Windows venv exists on every checkout and must be skipped); retune's copy repo-anchored; fail-loud, no fallback; static AST call-site guards; fork-only dependency declaration (claude-agent-sdk==0.2.82, google-genai==2.16.0) | Resolver half: **yes, candidate offer after PRs #4–#7** (groundwork for the agreed Linux deploy; PR text must carry the latent wrong-CWD limitation and the POSIX scoping of the subprocess mechanism). requirements-mac.txt: **fork-only** — versions need a discussion with Jeremy first. |
| 23 | `trading-bot/core/trading_bot.py` (3 lines), `trading-bot/tests/test_close_positions_at_end.py` (new) | two dormant unbound-name defects in `_close_all_positions_at_end` fixed; the forced-close bar now reaches `portfolio_states.csv` on failed and exact-zero closes, recorded with the engine's own per-bar `(None, {})` skipped-call convention | **Yes — PR #8 candidate.** Dorian decides timing. |

### LSP setup — 2026-08-03

| # | File | Change | Upstream-worthy? |
|---|---|---|---|
| 24 | `.gitignore` | ignore `/pyrightconfig.json` (repo-root basedpyright config: `venvPath "."` / `venv ".venv"` / py 3.13 / basic mode) | **No — fork-only.** Machine-local tool wiring, same class as row 9's `.omc/`: the file names the Mac-only `.venv` layout and Jeremy runs no basedpyright. Gitignored rather than left loose so a stray `git add -A` can never carry it upstream. |

The config itself stays untracked (`git check-ignore` verified). Verified by execution 2026-08-03: venv imports resolve (`performance/bar_equity.py` — pandas clean, 1 pre-existing type finding; `core/trading_bot.py` — 0 unresolved imports, 33 pre-existing type findings = the basic-mode noise floor on untyped upstream code); scratchpad probe fires exactly one error on a nonexistent import symbol and stays silent on a clean file. Basic mode is deliberate — strict would invite the drive-by "fixes" the mergeable-fork rule forbids.

**Worktree caveat (measured 2026-08-03):** `venvPath "."` is config-relative, so in a git worktree without its own `.venv` the CLI reports phantom `reportMissingImports`. Run it as `basedpyright --venvpath /Users/lala/Lab/trading/dorian-fork/trading-bot-dorian <files>` from worktrees, or symlink the main `.venv` in.

## Upstream merged PRs #4–#8 + the port — sync merge, 2026-08-03 (`8b9a5f72`, follow-up `3f6d8bf1`)

Jeremy merged all five remaining PRs (#4–#8) into `loloze6/trading-bot` master on
2026-07-31 (server-side, our commit SHAs intact), cherry-picked the macOS port
himself (`c4feaf56`, squashed from the fork's five commits), deleted `main`, and
pushed — his master moved `63237b88` → `33ac7ec4` (~50 commits: W16–W22, the
CLEAN-* docs triage, the E-001 epic process, `deploy/kraken_recorder/`, and the
fork-PR merges). Synced back with `git merge upstream/master`; **3 conflicts,
all pre-registered** in the dry-run map before merging (`.gitignore` = union of
disjoint tail blocks; both test files = take upstream, verified strictly
additive over ours — upstream's versions are the fork's files plus his
cache-presence skip and his Windows `skipif`, so his "mirror the skipif" ask is
satisfied by construction). Follow-up commit removes the fork's
`strategy-research/requirements-mac.txt` after Jeremy relocated it to
`strategy-research/config/` (one-line header diff, verified).

Verified at the landed tip (`3f6d8bf1`, four lanes: opus executor →
code-reviewer + red-team → independent verifier, zero refuted claims): fast
**213 passed / 0 skipped** on the main repo (211/2 in the archive-less
worktree), slow **14 / 0 / 0**, validator exit 0, `simulate` **byte-identical**
to the committed reference on all five files (`5ccbec42` / `5a75366c`,
sharpe −5.646, 24 trades) — measured independently by executor AND verifier, so
upstream's new aux-feed causality layer is proven inert on the default path.
First-ever Mac run of the strategy-research suite: **708 passed / 2 failed /
11 skipped**; both failures attributed by control-run on the pre-merge tree
(`test_d3` census 8-vs-9 = upstream's own known failure, caused by his
`71573062` deletion; `test_r2_bypass_1_path_traversal` = pre-existing
macOS/Windows `path.exists()` semantics divergence, no security impact — the
ownership guard works on both platforms, the test's vector short-circuits on
POSIX).

Status changes to the rows above:

- **Rows 7–8, 18, 19, 20, 23: no longer divergences** — merged upstream via
  PRs #6, #4, #5, #7, #8 respectively.
- **Row 22: no longer a divergence** — resolver half cherry-picked by Jeremy
  as `c4feaf56` (the planned upstream offer is moot); `requirements-mac.txt`
  now lives upstream at `strategy-research/config/`, fork's old-path copy
  removed in `3f6d8bf1`.
- **Rows 9 (`.omc/`), 21 (`CLAUDE.md` include), 24 (`pyrightconfig` ignore):
  unchanged, fork-only** — Jeremy's cherry-pick deliberately excluded the
  fork-doc surface (his stated taxonomy question).
- Residual `mac/setup` vs `upstream/master` delta: fork docs (`CLAUDE.md`
  include, `CLAUDE.fork.md`, `research/**`, this file), the committed reference
  artifact `results/runs/20260728T132811Z_5ccbec42/`, the two fork-only
  `.gitignore` blocks, and `requirements.txt` comment wording (fork's EXACT-pin
  note; pins identical).

## 2026-08-05 — Row 25: Kraken ingest merge fix (leg 2) — divergence until upstream PR #9 merges

`trading-bot/tools/ingest_kraken_archive.py` + `trading-bot/tests/test_kraken_archive_ingest.py`
diverge from `upstream/master` by one commit (`a9f56317`, merged to `mac/setup`
as `4c82a826`): re-ingest UNIONS with the existing cache (archive wins duplicate
timestamps), the gap guard is live on the ingest path (`existing=` now passed),
re-ingest is byte-idempotent (`close_time` normalized before the merge), an
existing-but-unreadable cache is refused rather than treated as a fresh slot,
`verify_boundary_values` closes the top-up blind spot of the timestamp-only
post-write check, and the source guard rejects duplicate/out-of-order
timestamps by name. Offered upstream as **loloze6/trading-bot#9** (branch
`fix/kraken-ingest-merge-upstream`, blob-identical files, fast suite
221 passed / 2 skipped on Jeremy's base). Row closes when the PR merges.
Acceptance at the fork's merged tip: fast **223 / 0 skipped** (the two
archive-gated tests ran for real), slow **14-0-0**, validator 0, `simulate`
byte-identical on all five files (`5ccbec42` / `5a75366c`).

## 2026-08-06 — Row 26: trading.exchange engine plumbing (leg 3) — divergence until offered/merged upstream

`fix/kraken-cache-engine-reachability`, merged `d2759f80` (single commit
`205c4e1d` on base `29374252`). Optional `trading.exchange` key in
`config.json` flows `TradingParams` → `Launcher` → `BacktestEngine` →
`DataManager.fetch_historical_data(..., exchange=...)`, making the 19
`kraken_*_1h.csv` caches reachable from a plain backtest config. Absent key
resolves to `"binance"` — byte-identical default proven; no tracked config
declares the key, so no config hash moves. Bogus values fail loud at launch
(`ccxt.exchanges` membership, `logger.error` + `sys.exit(1)`). All three
`Launcher`-class engine sites forward it; module-level `run_backtest()` is
deliberately unchanged (campaign-path ticket, High, filed). 9 new tests
(8 watched failing first; the 9th — an AST forwarding invariant — verified
failing on the pre-fix tree post-hoc), 8 mutations killed across executor +
review lanes (one survivor was the then-dead dataclass default, folded into
the campaign ticket), sha256-unchanged assertion guards the reachability
test's no-rewrite premise. Full lane pattern: opus executor, code-review
(FIX ROUND NEEDED → 5 doc-level items delivered), red-team (NO BLOCKER;
gap-exposure measurements moved to the G1 ticket), independent verifier
(MERGE-READY, message audited claim-by-claim). Acceptance at the merged tip:
fast **232 / 0 skipped**, slow **14-0-0**, validator 0, `simulate`
byte-identical on all five files (`5ccbec42` / `5a75366c`), manifest
`git_sha d2759f80` from a clean tree. Upstream offer: Dorian's call.

## 2026-08-06 — Row 27: manifest git_sha dirty detection — divergence until upstream PR #10 merges

`fix/manifest-gitsha-dirty`, merged `87f2b762` (single commit `63fbcf85` on
`d2759f80`). `_get_git_sha()` appends `-dirty` when
`git status --porcelain --untracked-files=no` is non-empty; either git call
failing degrades to `"unknown"` as before. Tracked-only is a design decision
(untracked `results/runs/` dirs would make the marker permanent) pinned by a
dedicated test. 5 probes (1 watched-failing, 4 pins incl. the production
subdirectory-cwd geometry), 5 mutations killed with sha256-proven restores,
dirty-shape matrix verified by the adversarial lane (staged/deleted/renamed/
mode-change/detached-HEAD/zero-commit/stale-lock), E2E both directions.
Known boundaries, disclosed in the PR: `assume-unchanged`/`skip-worktree`
false-clean (shared with `git diff HEAD`); a clean tree with a failing
`git status` now reports `"unknown"` (safe direction). Acceptance at the
merged tip: fast **237/0**, slow **14-0-0**, validator 0, simulate
byte-identical ×5 — that run's manifest stamped `87f2b762-dirty`, correctly:
this row's own uncommitted edit was the dirt (first live catch). Offered
upstream as **loloze6/trading-bot#10** (blob-identical, fast 216/2 on
Jeremy's base). Row closes when the PR merges.

**CLOSED 2026-08-07.** Jeremy merged PR #10 on 2026-08-06 22:09Z (his merge
commit `63bad12c` = master tip, verified via the GitHub API; his suite
226/0/2). Pulled back in sync merge `c3c370ee`: `run_artifact.py` and
`test_gitsha_dirty.py` blob-identical both sides, diff pre-verified empty.
The dirty-marker is now shared history on both machines.

## 2026-08-07 — Row 28: daily (1440m) ingest + 19 kraken 1d caches — divergence until offered/merged upstream

`fix/kraken-ingest-1d`, merged `5af84961` (single amended commit `6b14522f` on
`f2fd2203`). Re-diverges the PR-#9 file pair: `tools/ingest_kraken_archive.py`
gains a `resolution_minutes` parameter on `to_binance_schema` (close_time was
hardcoded to the 1h `TIMEFRAME_MS` — a daily ingest silently wrote 1-hour
close_times), a `--resolution` CLI (default 60), an ingest()-level exact-ccxt-
timeframe guard (CcxtFetcher snaps to the NEAREST timeframe, so 720m would
land in and MERGE INTO a legitimate 4h cache — refused before any read or
write, all seven exactly-mapped resolutions measured passing), and per-asset
isolation in `run_all()` (one raising asset no longer aborts the rest; [FAIL]
and the failures table on stderr; non-zero exit if any failed).
`tests/test_kraken_archive_ingest.py` +12 tests. Full lane pattern
(opus-4.8 executor / opus-5 review + red-team / fable verifier, all
transcript-verified); 11 mutations killed incl. 4 that survived round 1's
whole suite. Worktree 247/2; main repo fast 249/0, slow 14-0-0, validator 0,
reference simulate byte-identical with bare-sha manifest `5af84961`.
Plus commit `45035402`: the 19 `kraken_<BASE>USD_1d.csv` caches (43,504 rows,
5.0 MB, tips 2025-12-31 00:00 = last pre-seal daily bar), per-source-file
sha256 provenance in the commit message, ingest run twice byte-identical.
Unblocks Jeremy's P4 (blocked_on_daily_bar_ingest). Upstream offer: Dorian's
call. Residues ticketed, not fixed: typo'd-and-absent resolution exits 0
(guard closes the dangerous present-sources case); post-write verify ordering
(pre-existing, leg-2 design); `verify_utc_roundtrip` failures name no dest.

## 2026-08-07 — Row 29: slow-suite offline-safety guards — divergence until upstream PR merges

`fix/slow-suite-offline-safety`, merged `fe9d7061` (single message-amended
commit `e481bccf` on `2de1302d`). Diverges 4 upstream-shared test files
(test_warmup_prefetch_bit_identical, test_regression_backtest,
test_bar_equity_bit_identical, test_commission_rate_param): each module's
`pytestmark = pytest.mark.slow` becomes `[slow, skipif]` on the
BTCUSDT_1h / BTCUSDT_funding_8h / fear_greed_daily triple, reason
"local_data fixtures not present" — the 0fd9a3e4 sibling convention
(predicate, `_NEEDED_CACHES` line and reason text character-identical).
Why: all 14 slow tests route through run_backtest over gitignored caches;
on a cache-less clone that path live-fetches Binance (networked) or
silently backtests empty data (measured offline: 9 fail — 7 AssertionError
+ 2 KeyError — and 4 of the 5 passes carry no signal; only
test_config_actually_loaded passes legitimately). Byte-inert with caches
present: merged-tip fast 249/0, slow 14-0-0, validator 0; cache-less
socket-blocked slow 14 skipped exit 0, fast 232/17/0 unchanged. Upstream
offer: YES (Dorian 2026-08-07), PR after this merge. Ticketed, not fixed:
`exists()` satisfied by a degenerate cache — measured EQUAL to the sibling
convention's own property, Medium, applies to the whole convention.
