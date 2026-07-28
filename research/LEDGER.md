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

- **2026-07-28 — MILESTONE 1 DONE. The base is sound, by measurement.** Three blockers fixed on `mac/setup` (`default_regime`→`"unknown"`; `symbols`→`BTCUSDT`; `requirements.txt` pinned + `ccxt`/`matplotlib`/`requests`/`PyYAML` added). Reference run `20260728T132811Z_5ccbec42` reproduces the target **exactly**: `config_sha256 5ccbec42`, `data_sha256 5a75366c`, net −23.021%, sharpe −5.646, maxDD −24.592%, 24 trades, fees 68.897289. Fast 99 passed; slow **6 passed/4 errors → 9 passed/1 skipped/0 errors**; validator exit 0. `requirements.txt` proven by building a throwaway venv from scratch: it resolved to the identical pinned set and produced a run **byte-identical** to the main venv's on `bars.csv`, `portfolio_states.csv`, `trades.json`, `metrics.json`, `forecast_distribution.csv`. Reference artifact committed so future bit-identity checks can `cmp` instead of re-derive. Next: backlog #2, `fix/metrics-bar-equity`.

  **Control run — do not skip this when rebaselining anything, ever again.** Replaying the *old* config (`2754e184`) with only the V9 check suppressed still gives **76 trades / −270.797404 / −4.364**, `mean_reversion` bar_count 794 (vs 208 after), difference exactly the 586 bars now resolving to `unknown`. This is what proves a rebaseline is not masking an engine regression. It was missing from the first draft of this work and an adversarial review had to supply it — a rebaseline without its control is indistinguishable from a cover-up, which is the exact failure this fork exists to prevent. Side observation worth keeping: the old `net_pnl` reproduces to 2.0e-5, not exactly (`−270.797404` vs recorded `−270.797424`) — inside the fixture's 0.01 tolerance, cause unidentified, presumed float accumulation order.

  **Notion synced 2026-07-28 (after the commit):** P2, P9, P10 and the pandas ticket all rewritten to say milestone 1 landed as `443a1b57` on `mac/setup` — previously they said the fixes existed only on the PR #1 branch, which was the exact ambiguity that misled earlier sessions. P2 carries an explicit correction of the "unreachable, not stale" overclaim plus the control-run evidence and the `default_regime: null` bypass; P9 carries the measured pandas hash table and the corrected in-tree PyYAML citation. **PR #1 itself was left untouched — Dorian's call what reaches Jeremy.**

  **Four things learned this session, all worth keeping:**
  1. **The slow suite was already red on Jeremy's clean tree** — the same 4 tests errored before any change, so rebaselining `reference_run.json` repaired a broken test rather than overwriting a passing one. **But the framing first used for this was wrong and must not be repeated:** "the old values were unreachable, not stale" is false. `reference_run.json` was created 2026-06-27 (`0ca4666d`); `strategy_config.json` was last touched 2026-06-12; **V9 was added 2026-06-30 (`d570ffcd`), three days after.** The numbers were validly measured against a then-legal config and remain exactly reproducible. Jeremy can refute the overclaim with one `git log`. The true statement — "blocked by a rule added after they were recorded, and here is the control run proving the engine still yields them" — is both accurate and stronger. **The same false wording is on the Notion P2 issue page and underlies PR #1's framing to Jeremy; it needs correcting there.**
  2. **`"default_regime": null` passes the validator and does exactly what V9 exists to prevent.** Measured on a synthetic bar matching no rule: `"unknown"` → `UNKNOWN` (validator passes); `"mean_reversion"`/`"trending"`/`"chop"` → those regimes (V9 **blocks**); **`None` → `MEAN_REVERSION` with validator errors 0**. `validate_config.py:183` guards V7 with `if default_regime is not None`, V9 (line ~221) only tests the three literal names, and `regime_engine.py:137` is `_REGIME_MAP.get(self._default_regime, MarketRegime.MEAN_REVERSION)` — so an explicit null silently lands on the one regime that trades. A *missing* key is safe (defaults to `"unknown"`); an explicit null is not. This also settles that `"unknown"` was the right choice: it is the only value that both passes V9 and makes an unmatched bar genuinely flat. Pre-existing upstream defect, not introduced here. **Cheapest fix is one word:** change that fallback to `MarketRegime.UNKNOWN` so it fails safe. Own branch.
  3. **The pandas<3 trap is now proven, not inferred.** Measured on `local_data/BTCUSDT_1h.csv`: pandas 2.3.3 → `datetime64[ns]`, `hash_pandas_object` head `0x2e4d238f18634b07`; pandas 3.0.5 → `datetime64[us]`, head `0xbc4d8b3a3dd41a6e`. Same instants, different digest, and `reporting/run_artifact.py:40-44` feeds that column straight into `data_sha256`. `requirements.txt` now says **exact pin required**, not "below 3" — a reader relaxing to `>=2,<3` would honour the old wording and still corrupt the hash.
  4. **`1 skipped` in the slow suite is not benign — do not read it as green.** `test_config_actually_loaded` has *never executed*, on any platform. The `backtest_result` fixture returns from inside `with tempfile.TemporaryDirectory() as tmp:` (`tests/test_regression_backtest.py:39`), so the run dir is deleted the instant the fixture returns; the three sibling tests survive only because `metrics` is already in memory, while this one reads `manifest.json` from disk afterwards and hits `pytest.skip` at line 114. Mechanism proven by execution, not inferred. **The check that would catch "the backtest ran a different config than specified" is dead code** — which is uncomfortable given config identity is what the whole artifact-hash discipline rests on. Pre-existing upstream defect; left for its own branch to keep this one single-purpose. A fix exists in `archive/2026-07-28/fix-fetch-end-bound` — not restored, per standing instruction.

- **2026-07-28 — RESET.** Fork returned to Jeremy's `70dab378`; three archive tags pushed; knowledge carried forward, code not. `origin/master` fast-forwarded to Jeremy. New branch `mac/setup`. Next: milestone 1 below.
