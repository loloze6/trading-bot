# Handoff → next Claude Code session (written 2026-07-28, after milestone 1)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a plain-text code block for clean copy-paste. If you change §1 here, change it there — that page is the one Dorian actually copies from.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: `CLAUDE.fork.md`, `research/LEDGER.md`, `research/NEXT_SESSION.md`. **`CLAUDE.fork.md` is NOT auto-loaded** — Jeremy's `CLAUDE.md` has no include for it, so you must read it explicitly. Then run `git status && git log --oneline -5`.
>
> **Where we are:** milestone 1 is done. Jeremy's bot runs on my Mac and the reference backtest reproduces the baseline exactly — `config_sha256 5ccbec42` / `data_sha256 5a75366c` / net −23.021% / sharpe −5.646 / 24 trades / fees 68.897289 — byte-identically across two independent venvs. Branch `mac/setup`. The last **code** change is the merge `3225a281`; everything after it is documentation, so check `git log` for the actual HEAD rather than trusting a hash written here. Fast suite 116 passed, slow 9 passed / 1 skipped / 0 errors. That number is a **reproducibility anchor, never a result**: the committed strategy is from a killed family and loses ~23%.
>
> **What I actually care about now, and it reorders the backlog:** the LLM research workflow is the product. I want a **self-improving loop** — the pipeline proposes strategies, we backtest them, the results feed back and improve the next proposal. Getting the research stack running on macOS is the priority, **ahead of** `fix/metrics-bar-equity`.
>
> **It is two ports, not one — know this before you scope it.**
>
> 1. **`strategy-research/workflow/` — audited 2026-07-28, small.** Four hardcoded Windows interpreter paths (`workflow/run_phase1_research.py:990,1462,4889` and `tools/retune_regime_detector.py:486`, all the same `Path("..")/"venv"/"Scripts"/"python.exe"` line) plus one undeclared dependency (`claude_agent_sdk`, imported at `:54`, pinned `0.2.82` in comments, in no requirements file, not installed here). No other OS hazards — zero `shell=True`, zero `os.name`/`platform` branches, zero backslash literals. The file already uses the correct idiom (`sys.executable`) at `:1587` and `:2777`, so the fix applies a pattern the code already contains. Keep Jeremy's tree working: **resolver, not a hard swap** — the fork must stay mergeable.
> 2. **The Recorder — unscoped.** `strategy-research/recorder/` is 26 Python modules plus one `supervise.ps1`. The library is portable; the *supervised launch path* is PowerShell, and its own RUNBOOK argues the supervisor is the valuable part because book gaps are permanently unrecoverable. Decide explicitly whether the loop needs live capture before committing to this one — it may not be on the critical path for backtest-only research.
>
> **Read anything you need.** Nothing in this repo is off-limits to read — that includes `strategy-research/workflow/`, which is only *unexecutable* here, not secret. Never tell me something is "unaudited" when you could have audited it. Changing things is what needs proof. The one exception is the sealed holdout **data** at `local_data/holdout_sealed/2026_H1/`: don't open it, because reading it spends it. Its policy files are normal reading.
>
> **How I want you to work:**
> - Propose a plan in 3–6 bullets and get my nod **before writing any code**.
> - One change per branch. Reviewed and green before you start the next.
> - Prefer the cheapest control that works. Do not add guards to guards.
> - Verify by execution, never by reading. `main.py simulate` prints **nothing** — read the newest dir under `results/runs/` via `stat -f '%m %N' results/runs/* | sort -rn | head -1`.
> - Mutation-test new tests: break the thing they guard, at the *public* entry point, and confirm they fail.
> - Never push to Jeremy. `origin` only. No `Co-Authored-By` trailers.
> - Update `research/LEDGER.md` before the session ends.
>
> Start by confirming the environment and telling me what you find.

---

## 2. State as of 2026-07-28

| | |
|---|---|
| Branch | `mac/setup` @ `afa2573d`, pushed to `origin` |
| Upstream | Jeremy still at `70dab378`, 0 commits ahead |
| Fast suite | 116 passed |
| Slow suite | 9 passed, 1 skipped, 0 errors *(the skip is a known dead test — see below)* |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades — byte-identical across two venvs |

**Merged this session** (each on its own branch, reviewed, merged `--no-ff`):

| Commit | What |
|---|---|
| `443a1b57` | Three first-run blockers: `default_regime`→`unknown`, `symbols`→`BTCUSDT`, `requirements.txt` pinned + 4 missing packages |
| `c37dd38e` / `c1257be4` | `regime_engine.py:137` fall-through `MEAN_REVERSION`→`UNKNOWN`; public-path tests |
| `4fc45f68` | `validate_config.py` judges the *effective* `default_regime` at V7 and V9/V10 |
| `afa2573d` | Audit of `strategy-research/workflow/`; read-policy corrected in `CLAUDE.fork.md` |

---

## 3. The priority: port `strategy-research/workflow/` to macOS

**Why it matters more than the old "off-limits" label implied.** The audit found strategy configs there are **LLM-authored**:

- `workflow/stages.yaml:54` — stage `backtest_specification` has a `skill:` and **no** `tool:`. It is a model stage.
- `workflow/run_phase1_research.py:4885` writes its `backtest_spec.yaml → config` block **verbatim** to `candidate_strategy_config.json`.
- `trading-bot/tools/validate_config.py` is the gate at `:4888`; non-zero exit → `failed_validation`.

The model has failed in both relevant ways, on record: it invented the regime name `"active"` (`runs/run_043/attempt_1_blocked/`, caught by V7, still exits 1), and it **silently dropped a mandatory field** (`run_phase1_research.py:4876-4883` force-injects `significance_methodology` after run_047 omitted it). That second one is exactly how an absent `default_regime` would arise — which is why the V7/V10 hardening shipped this session is load-bearing, not theoretical.

**Blocker 1 — four Windows interpreter paths.** All the same line:
```python
TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"
```
at `workflow/run_phase1_research.py:990`, `:1462`, `:4889` and `tools/retune_regime_detector.py:486`; plus `tools/hooks/pre-commit:40` (a git hook, not pipeline code). Mac equivalent from `strategy-research/` is `../.venv/bin/python`. Keep Jeremy's tree working — prefer a resolver (Windows path if present, else `.venv/bin/python`, else `sys.executable`) over a hard swap, since the fork must stay mergeable.

**Blocker 2 — `claude_agent_sdk` is undeclared.** Imported at `:54`, pinned to `0.2.82` in comments (`:498`, `:541`), **not installed and in no requirements file**. PyPI name `claude-agent-sdk`. Pin it in a requirements file so a fresh clone reproduces — same discipline as milestone 1's `trading-bot/requirements.txt`.

**Pipeline model:** `claude-haiku-4-5` (`:748`).

### The honesty problem the loop creates — raise this before it runs

A self-improving loop that proposes and tests strategies is mechanically a **selection-bias machine**. Every proposal backtested is a trial, and deflated Sharpe is only as honest as the trial count behind it. The machinery exists — `campaign_state.trial_sharpes` (`run_campaign.py:1053`), `tools/deflate_sharpe.py` — and `run_campaign.py:1119-1122` warns that trials are counted **only** via `trial_sharpes`, never `campaign_state.runs`, so a missed append silently understates N. **Verify that accounting works on Mac before trusting anything the loop produces, including the runs it kills.** A loop that logs only its winners produces beautiful, meaningless Sharpes.

---

## 4. Known-broken, deliberately not fixed

- **`test_config_actually_loaded` has never executed.** `tests/test_regression_backtest.py:39` — the `backtest_result` fixture returns from inside a `with tempfile.TemporaryDirectory()`, so the run dir is deleted before the test reads `manifest.json`; it hits `pytest.skip` at `:114` unconditionally, on every platform, since the file's first commit. **The `1 skipped` in the slow suite is this. Do not read it as green** — the check that would catch "the backtest ran a different config than specified" is dead code. Notion issue open, own branch.
- `main.py simulate` rewrites the **tracked** `results/trades.json` every run — restore with `git checkout --` after any reproducibility check.
- Backlog after the port: `fix/metrics-bar-equity` (bar-level equity → true maxDD/Sharpe; unblocks trusting every number), then `fix/risk-layer`, then `feat/slippage-model`.

---

## 5. Lessons this session paid for — do not re-learn them

1. **Verify inherited claims by execution.** The ledger, Notion and the handoff all stated the old fixture values were "unreachable, not stale." One `git log` refuted it — V9 arrived three days *after* the values were recorded. Carried-forward knowledge is the least-tested artifact in the repo.
2. **Never rebaseline without a control run.** Replay the *old* config and show it still produces the *old* numbers, or a rebaseline is indistinguishable from one hiding a regression.
3. **Mutation-test new tests.** A 7-test file here caught **0 of 7** mutations because every test drove a private helper instead of the public entry point. Watching a test fail proves only that it reaches the path you wrote it against.
4. **Reject the strongest form of an option, not the easiest.** I declined to harden V10 by refuting a version of the idea nobody should have chosen, and shipped half a fix my own `FORK_CHANGES.md` had pre-registered as two parts.
5. **Never hedge with "unaudited" when auditing is available.** Said three times; the audit took fifteen minutes and turned the caveat into the strongest evidence for the change.

---

## 6. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, read policy, backlog. **Not auto-loaded — read it.** |
| `research/LEDGER.md` | every trap, finding, correction, and the working agreement. **The important one.** |
| `FORK_CHANGES.md` | the 8 deliberate divergences from Jeremy, with the evidence behind each |
| `strategy-research/workflow/stages.yaml` | the pipeline's stage graph — start here for the port |
| `strategy-research/config/campaign_data_policy.yaml` | `holdout_range` — source of truth for the seal |
| `research/TRIALS.csv` | every experiment; T001/T002 are baseline reproductions, not results |

Notion — "Trading Bot HQ": the **🐛 Bugs & Tasks** DB. `Status` = Jeremy's master, **"Dorian's fork"** = this fork. The hub's top banner is current as of 2026-07-28.
