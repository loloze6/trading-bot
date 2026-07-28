# Research & Engineering Ledger

**Update this every session. It is the agent's only memory across sessions.**

---

## RESET — 2026-07-28

The fork was reset to Jeremy's tree and restarted from scratch. Dorian's call, and the reason matters more than the mechanics:

> "we have done lots of changes recently and i am not aligned with it anymore as i cant trust the basis anymore."

**What was measured before the reset** (so nobody re-litigates it later): the old tree was objectively intact — engine files 0 changed, committed market data 0 bytes changed, holdout seal intact, baseline byte-identical, git history unbroken. **The problem was not the repository.** It was that the agent proposed a heavy runtime guard where a static check would have done, batched seven commits into a session scoped as a cleanup, and needed three adversarial review rounds to stabilise its own work. Trust in the *process* went, and a base you cannot trust is worthless regardless of what the diff says.

**A code reset does not fix a process problem.** The working agreement below is the actual remedy; the clean base is what makes it possible to start applying it.

### Where the old work went — nothing was deleted

| Tag | What is in it |
|---|---|
| `archive/2026-07-28/mac-bootstrap` | env bootstrap, the 3 first-run blockers, Kraken archive acquisition, baseline proof |
| `archive/2026-07-28/fix-first-run-blockers` | the 4 upstream-worthy files behind **PR #1** (still open, still correct — do not close) |
| `archive/2026-07-28/fix-fetch-end-bound` | holdout-enforcement work; read its tag message before reusing anything from it |

All three are pushed to `origin`. `git show <tag>` reads the rationale. Branches `mac-bootstrap`, `fix/first-run-blockers`, `fix/fetch-end-bound` also still exist on `origin`.

---

## Current state

- **Branch:** `mac/setup`, cut from `upstream/master` = `70dab378`. Byte-identical to Jeremy at reset time.
- **`origin/master`** fast-forwarded to `70dab378` (was 1 commit behind; nothing orphaned, no force-push).
- **Jeremy has not moved** since `70dab378` — confirmed 2026-07-28, 0 commits ahead.
- **Milestone 1 is done (2026-07-28).** The three first-run blockers are fixed on `mac/setup` and the baseline reproduces exactly. `main.py simulate` no longer fails. See the session log at the bottom for the measured evidence.

---

## CARRIED-FORWARD KNOWLEDGE

Everything below was paid for once. Do not re-derive it.

### The three first-run blockers (nothing runs until these are fixed)

1. **`strategy_config.json` fails validator V9** — `default_regime: "mean_reversion"` with non-empty `rules`. `AdvancedStrategy` runs the same check at construction (`strategies/main_strategy.py:31`) and raises before the first bar, so this is a hard blocker on **every** platform, not a Mac issue. Fix is one word: `"unknown"`.
   *Consequence when fixed:* the reference run moves **76 trades → 24**, net −270.797424 → −231.758912, Sharpe −4.364 → −5.646. The old numbers are **unreachable**, not merely stale, so `tests/fixtures/reference_run.json` must be rebaselined with the fix.
2. **`config.json` trades `ETHUSDT`** but only `BTCUSDT` is cached → cannot run offline.
3. **`requirements.txt`** is unpinned and missing `ccxt`, `matplotlib`, `requests` (imported by shipped code) and `PyYAML` (reached via `strategy-research/tools/prescreen_signal.py`; its absence fails `test_funding_rate_component`).

### Baseline target — the number that proves a base is sound

Window 2024-04-01 → 2024-05-30, BTCUSDT, 1h, 1,440 bars:

| | |
|---|---|
| `config_sha256` | `5ccbec42…` |
| `data_sha256` | `5a75366c…` |
| net / sharpe / maxDD | −23.021% / **−5.646** / −24.592% |
| trades / win | 24 / 41.67% |
| fees / cost drag | 68.897289 / 42.30% |

Reproduced on Linux+py3.10+pandas2 **and** macOS+py3.13+pandas2 — both hashes, every metric. **This is a reproducibility anchor, never a result.** The committed strategy is from a killed family and loses ~23%; the Sharpe is also computed off the *trade-exit* equity curve, so it understates drawdown. Never quote it as performance.

### Environment traps (each cost real time)

1. **`venv/` is a committed Windows venv** — 449 tracked files, `home = C:\Users\alauz\...`. The Mac venv lives at **`.venv/`**. Run everything as `../.venv/bin/python` from `trading-bot/`.
2. **pandas must stay `<3`.** 3.x parses caches to `datetime64[us]` instead of `[ns]`; `run_artifact.data_sha256` hashes the timestamp column, so **the data hash changes with no visible symptom** and every artifact silently stops being comparable. Nothing errors. This is not in the July review — it was found here.
3. **The `trading_bot` logger has zero handlers.** `main.py simulate` prints *nothing* on success or failure — including "No data in DataManager cannot run backtest". Read the newest dir under `results/runs/` for results; add a `StreamHandler` when debugging or you will read silence as success.
4. **macOS:** BSD `find -newermt` silently returns nothing, and `ls` is aliased to `eza` and mis-sorts. Use `stat -f '%m %N' | sort -rn`. This made a working run look like a no-op.
5. **A failed test run can poison the data cache.** With `fear_greed_daily.csv` absent, `FearGreedFetcher` writes a 13-row stub from its rolling-window endpoint, and every later fetch then trips `FetchGapError` forever. Delete the stub, restore the real file.
6. **`git config user.email`** is the GitHub noreply address (`20472984+7hr1LL@users.noreply.github.com`). Keep it — pushes were blocked otherwise.
7. **`pytest` skips the slow end-to-end tests** by default (`-m "not slow"`). Run `pytest -m slow` before any "unchanged" claim.

### Data on disk — 28 GB, almost none of it on GitHub

| Path | What |
|---|---|
| `trading-bot/local_data/` root | **26 tracked** `kraken_*USD_1h.csv` (2013→2025) — safe to clone |
| `trading-bot/local_data/` (6 files) | **gitignored, holdout-carrying**: `BTCUSDT_{1h,1d}`, `BTCUSDT_funding_8h`, `ETHUSDT_*`, `fear_greed_daily` |
| `trading-bot/local_data/Kraken_batch/master_q4/` | **12,027 files, 26 GB**, all pairs × 8 intervals, 2013-10-06 → 2025-12-31 23:59 UTC |
| `trading-bot/local_data/holdout_sealed/2026_H1/` | ⛔ **SEALED, 2.4 GB, read-only, never opened** |

**A fresh clone does NOT get 28 GB of this.** That is why the reset reused this working directory instead of cloning.

- **Kraken archive provenance is PROVEN, not assumed:** re-ingesting BTC reproduces the committed `kraken_BTCUSD_1h.csv` at 96,381 rows over an identical span, with 5 rows differing in `volume` only, all within 1 ULP (decimal serialisation, not data).
- **Full-archive holdout sweep: 0 contaminated files of 12,027.** Latest bar anywhere = 2025-12-31 23:59 UTC.
- **Acquisition note if this is ever repeated:** Kraken's quarterly ZIPs are **incremental, not cumulative** (Q1-2023 holds only Jan–Mar 2023); only the complete-history bundle reaches back to 2013. The Drive link hits a per-file quota — the workaround is to copy the file into your own Drive, then download your own copy.

### Holdout — the expensive rule

`holdout_range` = **2026-01-01 → 2026-06-30**, from `strategy-research/config/campaign_data_policy.yaml`. Sealed, single-use, `holdout_failure_is_terminal: true`. **Looking is spending it** — a chart, a `head`, a notebook all count.

Known, measured holdout hazards **still present on this clean tree**:

- **`CcxtFetcher` overshoots its own `end_date`.** `ccxt_fetcher.py:149-174` loops `while current_since < until`, so the bound governs where a page *starts*, never where data *ends*; the frame is never trimmed. A fetch bounded at 2025-12-31 wrote daily bars through **2026-03-19**. Measured, not theoretical.
- **`launcher.py:357` (`visualize_data`) hardcodes `end_date='2026-04-23'`** — inside the seal — with `localStorage=True` and a 60s interval: **~500k sealed 1m bars per run**. It then dies on `validate_quality_data_continuity`, a method that exists on no fetcher, so the damage lands *before* it reports failure. No `BTCUSDT_1m.csv` exists here, so it has never actually been run.
- **Seven Binance caches already contain sealed rows** (4,344 in `BTCUSDT_1h.csv`). They are gitignored, but they are readable, and a backtest window reaching into 2026 will happily read them — measured: **1,440 sealed rows handed to a caller** with nothing complaining.
- **A cheap control that would catch most of this:** a static test asserting no date literal anywhere in the repo falls inside `holdout_range`. ~15 lines, zero divergence from Jeremy. This was *not* what the old branch built, and should have been.

### Rescued from the archived Notion bootstrap report, 2026-07-28 — re-verified on this tree

The Notion bootstrap report was archived on this date. Three of its findings were **not** recorded anywhere else. Each was re-measured here before being carried over, rather than copied on trust:

1. **A second Windows dependency for the porting effort: the Recorder.** `strategy-research/recorder/` is **26 Python modules and one `supervise.ps1`** — the library is portable, but the *supervised launch path* is PowerShell. Its own `RUNBOOK.md` argues the supervisor is the valuable part, because book gaps are permanently unrecoverable. So "run the research stack on macOS" is really **two** ports: `workflow/` (scoped, small) and the Recorder supervisor (unscoped). Do not discover this halfway through backlog #1.
2. **`base_fetcher.py:220` widens every requested end by a day** — `df["timestamp"] < self.end_date + datetime.timedelta(days=1)`. An `end_date` of `2025-12-31 23:00` admits bars through `2026-01-01 22:00`, i.e. **past an explicitly stated bound and into the seal**. Still present, verified by reading the line on this tree.
3. **`base_fetcher.py:391` derives period ends as `ts − 1ms`**, so a cached row at exactly `00:00:00.001` yields a period end of exactly midnight, which day-expansion then widens by 24h. **`BTCUSDT_funding_8h.csv` carries exactly 244 such rows** — the archived figure re-measured and confirmed to the row. Latent today; arms on any adjacent gap. (Note 3,229 of its 7,468 rows carry *some* sub-second component — a broader and different measurement, not the hazard.)

Fixes for 2 and 3 exist in `archive/2026-07-28/fix-fetch-end-bound`. Cherry-pick deliberately, one at a time, reviewed — do not bulk-restore.

### Other bugs found and verified (all still present on this tree)

- `tools/ingest_kraken_archive.py` **overwrites** the cache instead of merging (measured 500 rows → 10) and passes no `existing=`, so `_assert_no_new_gap` is dead there.
- `tests/test_regression_backtest.py` — the config-identity check **never executes**: the fixture holds its temp dir in a `with tempfile.TemporaryDirectory()` block that exits when the fixture *returns*, deleting the run dir before any test reads it.
- `main.py simulate` rewrites the **tracked** `results/trades.json` on every run, so the tree is dirty after any reproducibility check.
- `_merge_and_store` **overwrites rather than unions** — `ingest_kraken_archive.py`'s comment claiming otherwise is false.
- Fixes for all of these exist in `archive/2026-07-28/fix-fetch-end-bound`. Cherry-pick deliberately, one at a time, reviewed — do not bulk-restore.

---

## WORKING AGREEMENT (the actual remedy)

1. **One change per branch.** Reviewed and merged before the next begins.
2. **Dorian approves the plan before any code is written.** 3–6 bullets, then wait.
3. **Prefer the cheapest control that works.** A static check beats a runtime guard; a runtime guard beats a convention. The old branch got this backwards and paid for it.
4. **Do not add guards to guards.** Most of the pre-reset churn came from new guards interacting with existing ones.
5. **Verify by execution, never by reading.** Fast tests always; `pytest -m slow` before any "unchanged" claim; baseline hashes quoted with every result.
6. **Never push to Jeremy.** `origin` is the only push target; `upstream` push URL is `DISABLED_use_a_PR_instead`. Standing instruction, 2026-07-28.
7. **No `Co-Authored-By` trailers** in commit messages. Global rule.
8. **Never run live.** `main.py run_bot` is forbidden. Backtests only.

---

## Session log (newest first)

- **2026-07-28 — PRIORITY CHANGE + workflow audit.** Dorian: *"the important part will be to work on the workflow designer and to leverage the LLM workflow to get new proposed strategies that we can test and improve. It should be a self-improving loop."* **`fix/workflow-macos-port` now sits ahead of `fix/metrics-bar-equity`.** Audited `strategy-research/workflow/` (7 files): port surface is **4 hardcoded Windows interpreter paths** (`run_phase1_research.py:990,1462,4889`; `tools/retune_regime_detector.py:486`) plus **`claude_agent_sdk` undeclared** (imported `:54`, pinned `0.2.82` in comments, in no requirements file, not installed). Zero other OS hazards — no `shell=True`, no `os.name`/`platform` branches, no backslash literals — and `sys.executable` is already used correctly at `:1587`/`:2777`, so the fix applies an idiom the file already contains. Pipeline model: `claude-haiku-4-5`. Notion issue created; `NEXT_SESSION.md` rewritten around this.

  **The skeptic's note, to be raised before the loop runs:** a self-improving strategy loop is mechanically a selection-bias machine. Every proposal backtested is a trial, and deflated Sharpe is only as honest as N. `run_campaign.py:1119-1122` states trials are counted **only** via `campaign_state.trial_sharpes`, never `campaign_state.runs` — so a missed append silently understates N and inflates every downstream significance claim. Verify that accounting works on Mac **before** trusting anything the loop emits, including the runs it kills.

- **2026-07-28 — `fix/regime-default-fail-safe`.** One word: `regime_engine.py:137` default-regime fall-through `MEAN_REVERSION` → `UNKNOWN`, closing the null-bypass found during the milestone 1 review (learning #2 below). Shipped with `tests/test_regime_default_fallback.py` (7 tests); the 2 regression cases were **watched failing first**. Fast 99 → **108 passed**; slow 9 passed / 1 skipped / 0 errors; `simulate` **byte-identical** to the committed reference artifact on all five data files, hashes `5ccbec42` / `5a75366c` unchanged. Unreachability measured repo-wide rather than sampled: parsing all 3,288 JSON files gives **1,011 `default_regime` occurrences, all four mapped names, zero nulls or unmapped** (999 of them under `strategy-research/`). Chose the engine over hardening V9 deliberately: it closes the whole class (incl. typo'd names reaching `strategy-research/tools/validate_regime_detector.py:116`, which constructs the engine with no validation at all) and makes the file self-consistent — the veto (`:114`) and rule-match (`:136`) fallbacks already returned `UNKNOWN`. Next: backlog #2, `fix/metrics-bar-equity`.

  **Red-teamed before merge; two findings acted on, and both are lessons rather than one-offs:**
  1. **The first test file was hollow.** All 7 tests drove the private `_classify_threshold_rules()` with hand-stuffed `_history`, bypassing `update()`/`is_ready()`/`classify()` — the only path production uses. The reviewer reintroduced the exact defect one level up inside `classify()` and **0 of 7 failed.** Fixed by adding an end-to-end test through `AdvancedStrategy` (now catches it, 31 of 31 bars trading) plus a control so all-zero can't be confused with a broken fixture. **Rule: a regression test that never touches the production entry point is decoration.** Mutation-test new tests by breaking the thing they guard.
  2. **I re-committed the same shape of overclaim I had retracted two rows earlier in the same file.** "Both configs in the repo set `default_regime` explicitly" was true of `trading-bot/` and a 0.2% sample of the 1,011 real occurrences. The conclusion survived the full scan, but the *basis* was asserted from convenience. Reach for the measurement even when you're confident — especially then. See also the milestone 1 "unreachable" retraction below; this is the identical failure mode, one branch later.

  **Known limitation at the time — since closed** by `fix/validator-rejects-null-default-regime` (entry above). The engine layer alone swapped fail-into-trading for **fail-silently-flat**: harmless but invisible.

- **2026-07-28 — `fix/validator-rejects-null-default-regime`.** The validator half. `validate_config.py` now reads `rd.get("default_regime", "unknown")` at both V7 and V9/V10 instead of the raw value, and V7's `is not None` skip becomes a plain membership test. Root fault was **one mistake in two dialects**: the validator used `is not None` as a *skip* where the engine used `.get(key, "unknown")` as a *substitute*, so `None` meant "don't check" to one and "unknown" to the other. Closed two holes — explicit `null` validating clean (V7/V9/V10 all blind to it), and an *omitted* key making V10 blind to a genuinely dead fully-ungated config. Absent-key configs stay legal, which is what makes it a fix rather than a tightening. Fast 108 → **116 passed**; slow 9 / 1 skipped / 0 errors; validator exit 0; `simulate` byte-identical. Run through `/autopilot` with parallel architect + code-reviewer validation.

  **I was wrong about the scope, and both reviewers caught it independently.** I argued V10 should be left alone because removing its `is not None` guard would double-report one fault (a correct V7 plus a garbled `strategies.regimes.None` V10). **That claim is true but answers the wrong question** — it evaluates deleting the guard, which nobody should do. The right move was applying my own V7 technique 34 lines lower: give `.get()` the engine's default *and keep the guard*. Both goals hold at once, because `.get()` substitutes only for a **missing** key, so an explicit null still yields `None` and still trips the guard. **Lesson: when you reject an option, check you rejected the strongest version of it, not the easiest one to argue against.** I had also baked the strawman into a test name, which would have made the gap harder to revisit later.

  **Reachability — I said "unaudited" three times when auditing was available. Then I audited it.** All 1,011 `regime_detector` dicts in committed JSON carry a valid `default_regime` (748 `unknown`, 138 `trending`, 125 `mean_reversion`). And `strategy-research/workflow/` — 7 files, previously treated as off-limits — turns out to **invert** the caveat rather than qualify it:

  - Strategy configs are **LLM-authored**. `workflow/stages.yaml:54` gives `backtest_specification` a `skill:` and no `tool:`; `run_phase1_research.py:4885` writes its output block **verbatim** to `candidate_strategy_config.json`.
  - `trading-bot/tools/validate_config.py` is the gate at `:4888`, non-zero exit → `failed_validation`. **The validator hardened today is the only thing between a model-written config and a backtest.**
  - The model **has** emitted an invalid regime name — `run_043/attempt_1_blocked/` invented `"active"`, caught by V7 then and now (that fixture is already the first test in `test_validate_config.py`).
  - The model **has** silently dropped a mandatory field — `run_phase1_research.py:4876-4883` force-injects `significance_methodology` after run_047's spec stage omitted it. A silently-dropped field is *precisely* how an absent `default_regime` arises, so **the V10 absent-key hole closed today is reachable by a documented failure mode**, not a hypothetical.
  - Only other generator, `tools/retune_regime_detector.py:351`, hardcodes `"unknown"`. Safe.

  **The lesson is bigger than the phrasing rule I wrote earlier.** Twice I hedged a claim with "unaudited" and moved on; the audit took fifteen minutes and turned a qualifier into the strongest evidence for the change. Per Dorian, 2026-07-28: *nothing is off-limits to read; changing is what needs proof.* `strategy-research/workflow/` is unexecutable here (Agent SDK + Windows paths), not unreadable. `CLAUDE.fork.md` updated accordingly. The one genuine exception is the sealed holdout **data**, and for a different reason — reading it spends it.

- **2026-07-28 — MILESTONE 1 DONE. The base is sound, by measurement.** Three blockers fixed on `mac/setup` (`default_regime`→`"unknown"`; `symbols`→`BTCUSDT`; `requirements.txt` pinned + `ccxt`/`matplotlib`/`requests`/`PyYAML` added). Reference run `20260728T132811Z_5ccbec42` reproduces the target **exactly**: `config_sha256 5ccbec42`, `data_sha256 5a75366c`, net −23.021%, sharpe −5.646, maxDD −24.592%, 24 trades, fees 68.897289. Fast 99 passed; slow **6 passed/4 errors → 9 passed/1 skipped/0 errors**; validator exit 0. `requirements.txt` proven by building a throwaway venv from scratch: it resolved to the identical pinned set and produced a run **byte-identical** to the main venv's on `bars.csv`, `portfolio_states.csv`, `trades.json`, `metrics.json`, `forecast_distribution.csv`. Reference artifact committed so future bit-identity checks can `cmp` instead of re-derive. Next: backlog #2, `fix/metrics-bar-equity`.

  **Control run — do not skip this when rebaselining anything, ever again.** Replaying the *old* config (`2754e184`) with only the V9 check suppressed still gives **76 trades / −270.797404 / −4.364**, `mean_reversion` bar_count 794 (vs 208 after), difference exactly the 586 bars now resolving to `unknown`. This is what proves a rebaseline is not masking an engine regression. It was missing from the first draft of this work and an adversarial review had to supply it — a rebaseline without its control is indistinguishable from a cover-up, which is the exact failure this fork exists to prevent. Side observation worth keeping: the old `net_pnl` reproduces to 2.0e-5, not exactly (`−270.797404` vs recorded `−270.797424`) — inside the fixture's 0.01 tolerance, cause unidentified, presumed float accumulation order.

  **Notion synced 2026-07-28 (after the commit):** P2, P9, P10 and the pandas ticket all rewritten to say milestone 1 landed as `443a1b57` on `mac/setup` — previously they said the fixes existed only on the PR #1 branch, which was the exact ambiguity that misled earlier sessions. P2 carries an explicit correction of the "unreachable, not stale" overclaim plus the control-run evidence and the `default_regime: null` bypass; P9 carries the measured pandas hash table and the corrected in-tree PyYAML citation. **PR #1 itself was left untouched — Dorian's call what reaches Jeremy.**

  **Four things learned this session, all worth keeping:**
  1. **The slow suite was already red on Jeremy's clean tree** — the same 4 tests errored before any change, so rebaselining `reference_run.json` repaired a broken test rather than overwriting a passing one. **But the framing first used for this was wrong and must not be repeated:** "the old values were unreachable, not stale" is false. `reference_run.json` was created 2026-06-27 (`0ca4666d`); `strategy_config.json` was last touched 2026-06-12; **V9 was added 2026-06-30 (`d570ffcd`), three days after.** The numbers were validly measured against a then-legal config and remain exactly reproducible. Jeremy can refute the overclaim with one `git log`. The true statement — "blocked by a rule added after they were recorded, and here is the control run proving the engine still yields them" — is both accurate and stronger. **The same false wording is on the Notion P2 issue page and underlies PR #1's framing to Jeremy; it needs correcting there.**
  2. **`"default_regime": null` passes the validator and does exactly what V9 exists to prevent.** Measured on a synthetic bar matching no rule: `"unknown"` → `UNKNOWN` (validator passes); `"mean_reversion"`/`"trending"`/`"chop"` → those regimes (V9 **blocks**); **`None` → `MEAN_REVERSION` with validator errors 0**. `validate_config.py:183` guards V7 with `if default_regime is not None`, V9 (line ~221) only tests the three literal names, and `regime_engine.py:137` is `_REGIME_MAP.get(self._default_regime, MarketRegime.MEAN_REVERSION)` — so an explicit null silently lands on the one regime that trades. A *missing* key is safe (defaults to `"unknown"`); an explicit null is not. This also settles that `"unknown"` was the right choice: it is the only value that both passes V9 and makes an unmatched bar genuinely flat. Pre-existing upstream defect, not introduced here. **Cheapest fix is one word:** change that fallback to `MarketRegime.UNKNOWN` so it fails safe. Own branch.
  3. **The pandas<3 trap is now proven, not inferred.** Measured on `local_data/BTCUSDT_1h.csv`: pandas 2.3.3 → `datetime64[ns]`, `hash_pandas_object` head `0x2e4d238f18634b07`; pandas 3.0.5 → `datetime64[us]`, head `0xbc4d8b3a3dd41a6e`. Same instants, different digest, and `reporting/run_artifact.py:40-44` feeds that column straight into `data_sha256`. `requirements.txt` now says **exact pin required**, not "below 3" — a reader relaxing to `>=2,<3` would honour the old wording and still corrupt the hash.
  4. **`1 skipped` in the slow suite is not benign — do not read it as green.** `test_config_actually_loaded` has *never executed*, on any platform. The `backtest_result` fixture returns from inside `with tempfile.TemporaryDirectory() as tmp:` (`tests/test_regression_backtest.py:39`), so the run dir is deleted the instant the fixture returns; the three sibling tests survive only because `metrics` is already in memory, while this one reads `manifest.json` from disk afterwards and hits `pytest.skip` at line 114. Mechanism proven by execution, not inferred. **The check that would catch "the backtest ran a different config than specified" is dead code** — which is uncomfortable given config identity is what the whole artifact-hash discipline rests on. Pre-existing upstream defect; left for its own branch to keep this one single-purpose. A fix exists in `archive/2026-07-28/fix-fetch-end-bound` — not restored, per standing instruction.

- **2026-07-28 — RESET.** Fork returned to Jeremy's `70dab378`; three archive tags pushed; knowledge carried forward, code not. `origin/master` fast-forwarded to Jeremy. New branch `mac/setup`. Next: milestone 1 below.
