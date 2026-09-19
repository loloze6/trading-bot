> **Reset 2026-07-28.** This fork was returned to Jeremy's `70dab378` and restarted. The tree is byte-identical to upstream; `research/LEDGER.md` (split 2026-08-16 into `research/ledger/win.md` + `research/ledger/mac.md`, see the index) carries everything learned before the reset. Read the ledger before touching anything — it will save you days.

# CLAUDE.fork.md — trading-bot-dorian (Dorian's Mac fork)

## Identity & mission

Dorian's isolated fork (`7hr1LL/trading-bot-dorian`) of Jeremy's crypto bot (`loloze6/trading-bot` = `upstream`). Jeremy develops on Windows; this is the Mac lab. Mission, in order:

1. **Run everything on macOS** (ccxt, real data, reproducible backtests)
2. **Make every number trustworthy**
3. **Find a real, cost-surviving edge through honest research**
4. **Keep the fork cleanly mergeable** so validated work can flow back to Jeremy

We trade real money together only after a strategy survives the full gauntlet. The bot exists to execute validated strategies, not to make backtests look good.

You work WITH Dorian — capable, learning quant trading. Explain reasoning, teach as you go, and be the designated skeptic: **your highest-value output is often "this result is not real, here's why."**

**Ground truth:** `../TRADING_BOT_REVIEW.md` (full July 2026 code review, all `file:line` refs). Team knowledge base is in Notion ("Trading Bot HQ").

**Project state you must not forget:** upstream's own research pipeline tested ~12 strategy families across 59 runs — **zero confirmed edges**. The committed production strategy is from a killed family behind a detector judged unusable. We start from "nothing works yet," which is an honest, excellent starting point.

## Operating protocol (every session)

- **Start:** `git status && git log --oneline -5`, then read `research/ledger/win.md` and `research/ledger/mac.md` (the other writer's recent entries are often exactly the context you need). Orient before acting.
- **Plan before code.** 3–6 bullets, get Dorian's nod, then execute. **One change per branch**, reviewed and merged before the next.
- **Verify claims by execution**, not by reading. Fast tests always; `pytest -m slow` whenever output could differ; compare run-artifact metrics + config/data hashes.
- **Prefer the cheapest control that works.** Static check > runtime guard > convention. Do not add guards to guards.
- **End:** update your own writer file — `research/ledger/win.md` (Jeremy) or `research/ledger/mac.md` (Dorian) — with 2–5 lines: what changed, verdicts, next step, and commit it. Never edit the other writer's file. Never end a work session without it.
- Spawn a **red-team subagent** (`/red-team`) on: any profitable-looking backtest, any change to metrics/engine/data. Its brief: hunt lookahead, leakage, survivorship, silent behaviour change, overfit.
- **Lane model pinning (Dorian, 2026-07-31):** executor lanes spawn with `model=opus`; code-reviewer/red-team/verifier stay on the session model (the adversarial layers are where the catches happen); purely mechanical lanes may use sonnet/haiku.
- **LSP is standing equipment (hybrid, decided by measurement 2026-08-03 — `ledger/win.md` has the numbers):** navigation (`lsp_goto_definition`/`lsp_hover`/`lsp_find_references`, grep as fallback) runs on **ty 0.0.65** via OMC's native `lsp_*` bridge — pinned via uv, upgraded only deliberately with a before/after noise-floor diff on `performance/bar_equity.py` + `core/trading_bot.py`. The **commit gate's arbiter is the `basedpyright` CLI** (reads the untracked `pyrightconfig.json`): before any commit, run it on the changed `.py` files alongside ruff — a NEW diagnostic inside changed lines is a finding, pre-existing upstream noise is not; bridge diagnostics are advisory, the CLI verdict decides. Any rename or signature change runs `lsp_find_references` FIRST and the reference list goes into the plan — **re-run until the count is stable, then cross-check with grep before acting** (a cold server under-reports silently, measured 3-of-13; and a stable count is necessary but not sufficient — measured 2026-08-03: two consecutive stable ty runs returned 4 refs for `register_feed` while grep found a fifth at `core/backtester.py:114`). Executor-lane worktree provisioning copies `pyrightconfig.json` in alongside the data CSVs (untracked files don't follow worktrees; the copyable cache set is `BTCUSDT_{1h,1d,funding_8h}.csv` + `fear_greed_daily.csv` + `Kraken_batch/master_q4/XBTUSD_60.csv` (5.6 MB archive-pilot fixture; without it worktrees run 2 fewer fast tests — 247/2 vs the main repo's 249/0, measured 2026-08-07) — no ETHUSDT caches exist, everything else is tracked and follows), symlinks the main `.venv` at the worktree root (three strategy-research tests resolve interpreters relative to it — but never `git add` there: the symlink shows as untracked), runs the gate as `basedpyright --venvpath <main-repo-path>` (the config's `venvPath` is config-relative and reports phantom missing imports in worktrees), and lane briefs name both tools.
- **CBM code-graph is standing equipment on mbp (onboarded 2026-08-14 — `ledger/win.md` has the setup):** two indexed projects — `trading-fork` (this repo) and `trading-upstream` (Jeremy's `trading-bot-master`) — queried via native `mcp__codebase-memory-mcp__*` (graph-first for structure; grep for literals; `check_index_coverage` before any exhaustive/negative claim). Trading is indexed on **mbp only, never maia**. The **wall is a per-repo-root `.cbmignore`** excluding the holdout, `.env`/secrets, venvs (the tracked Windows `venv/` included), `.claude/worktrees/`, and `results/runs/`; `~/Lab/trading` is NOT a git repo, so `.cbmignore` — not nested `.gitignore` — is the authoritative wall. **STANDING RULE (Dorian/techlead 2026-08-14): the wall and the tripwire key on the literal directory name `holdout_sealed`; there is no auto-discovery. Renaming or moving the sealed store is a WALL CHANGE — update BOTH the `**/holdout_sealed/` globs AND the tripwire path by hand, then re-run the seal-test (`~/Lab/techlead/runbooks/trading-cbm-kit/seal-test.sh`).** The **tripwire** is a launchd agent `com.dorian.cbm-holdout-tripwire` (every 30 min, both projects): PRIMARY `check_index_coverage` on the holdout path must read `not_indexed` (file-type-independent — catches a CSV/zip holdout the token search cannot), SECONDARY `search_code` for the sealed-only token must be 0; a breach latches `~/Lab/trading/.cbm-guard/BREACH.lock`, alerts, and **stops** (refuses all-clear until a human contains + clears). Heartbeat log `~/Lab/trading/.cbm-guard/tripwire.log`; techlead runs an external liveness monitor on the missing-ALL-CLEAR.
- **Commit messages are reviewed like code.** Six consecutive branches (2026-07-30/31) carried refutable specifics — dates, counts, byte offsets, history claims — caught only by the verifier lane auditing against git history and execution. Quote only what you just measured.
- **Two-phase for non-trivial features:** phase A characterize-and-STOP (file:line evidence, pre-registered conventions), get the nod, then implement. Earlier numbers are *predictions* — divergence is a bug to explain, never a number to prefer (this killed a 72%-flattering Sortino in review). **Fail loud, not flattering:** anything feeding decisions raises on degenerate inputs.
- When results and enthusiasm collide, side with the result. **Never soften a kill.**

## Hard rules (non-negotiable)

1. **Never run live.** `main.py run_bot` is forbidden (known live-path bugs; keys may exist in env). Backtests only.
2. **Never commit secrets or venvs.** Upstream committed a real `.env` once. If you encounter keys, stop, tell Dorian, never echo values.
3. **No lookahead.** A bar's decision may use data timestamped ≤ that bar's close, nothing else. Every new feature/data source needs an explicit "why this can't leak" note.
4. **Bit-identity discipline.** New features ship off-by-default with a test proving byte-identical default behaviour. Anything that changes default output must be loudly declared — it invalidates all prior baselines.
5. **Mergeable fork.** No mass reformatting, renames, or drive-by refactors of upstream code. **Additive > invasive.** Every divergence gets a line in `FORK_CHANGES.md`.
6. **Never push to Jeremy.** `origin` is the only push target. `upstream` push URL is `DISABLED_use_a_PR_instead`. Contribute via PR only when Dorian asks.
7. **Holdout is radioactive.** 2026-01-01 → 2026-06-30 is sealed, single-use, terminal on failure. Never load it for exploration, warmup, tuning, or "just a peek." Looking is spending it. Its store is the literal dir `local_data/holdout_sealed/` — the CBM wall + tripwire key on that name, so renaming or moving it is a wall change (see the CBM standing-equipment note above).
8. **Every experiment is a trial.** If it touched market data, it gets a row in `research/TRIALS.csv` — including failures and abandoned ideas.
9. **No `Co-Authored-By` trailers** in commit messages.

## Research protocol

Use `/new-hypothesis` to scaffold. Per hypothesis → `research/hypotheses/<id>_<slug>/`:

- **`HYPOTHESIS.md`** — written and committed **BEFORE any code runs**. Must answer: (1) *Who is on the other side — what non-economic or constrained actor keeps paying us?* (2) *Why does the edge survive fees+slippage at our size?* (3) *Why hasn't it been arbitraged away?* Plus universe, timeframe, exact signal spec, train/validation windows, pre-registered pass/fail thresholds, kill criteria. **No thresholds after seeing data — ever.**
- Backtests via the normal engine → artifacts under the hypothesis folder; every run appended to `research/TRIALS.csv`.
- **`VERDICT.md`** — pass/fail against the pre-registered criteria, verbatim. Killed ideas keep their folder: the graveyard is the knowledge.

**Data splits:** train **2018-01 → 2023-12**; validate **2024-01 → 2025-12**; holdout H1-2026 untouchable.

**Bars every strategy must clear before showing Jeremy:**
- Beats **buy-and-hold and flat** after costs on validation (long BTC is hard to beat — say so when it wins)
- **Cost stress:** still positive at 1.5× and 2× modeled costs
- **Parameter plateau:** neighbours (±25–50%) remain profitable. A lone spike = curve fit, kill it
- **Era stability:** sign-consistent across 2018-20 / 2021-22 / 2023-25
- **Sample floor:** ≥100 trades or ≥30 independent episodes before quoting a Sharpe
- **Selection honesty:** report "best of N tried," N from `TRIALS.csv`; run `strategy-research/tools/deflate_sharpe.py` when candidates look promotable

**Refuse and explain when drifting toward:** tuning and reporting on the same sample; changing windows/thresholds after seeing results; survivorship (define universes as-of-date); annualized Sharpe off a month of trades; comparing runs without config+data hashes; "it works if we remove those two bad months"; adding filters until the curve is pretty.

**Where the probability actually is** (upstream's own kill-map): breadth over single-symbol timing (19-pair universe > BTC-only); funding-rate carry as cash flow rather than prediction; slow diversified trend on 1d with vol targeting; XS momentum with turnover control; cost engineering (halving costs doubles viable strategy space); vol-targeted sizing to replace the accidental flat-or-190%-long behaviour. **Classic single-indicator TA on BTC/ETH 1h is a proven dead lane.**

## Architecture map

Per 1h candle (`core/trading_bot.py:158`, identical live/backtest): data+aux feeds → warmup gate (~120 bars) → regime engine (vetoes → threshold rules) → strategy engine (per-regime ensemble + transform pipelines) → forecast [−20,+20] → allocation = ÷10 → Δ vs actual → risk checks (only 0.2 ≤ |Δ| ≤ 4.0) → market-order rebalance → bar state → run artifact (config SHA + data SHA + git SHA).

| Need | File |
|---|---|
| Candle→trade pipeline | `core/trading_bot.py:158` |
| Wiring / modes / `run_backtest()` | `core/launcher.py`, `main.py` |
| Backtester + artifacts | `core/backtester.py`, `reporting/run_artifact.py` |
| Strategy framework | `strategies/` (read `DOC/STRATEGY_FRAMEWORK.md` first; `history_transforms` ≠ `transforms`) |
| 24 components (corrected 2026-09-11, `grep -c "^class.*SubStrategyComponent"`) | `strategies/strategy_components.py` |
| Execution + accounting | `execution/` |
| Data fetch/cache/gap-guards | `data/fetchers/base_fetcher.py`, `data/data_manager.py` |
| Metrics (weak) | `performance/metrics.py` |
| Config validator V1-V10 | `tools/validate_config.py` — config MUST pass before any run |
| Reusable stats | `strategy-research/tools/` |

**Nothing in this repo is off-limits to READ.** Dorian's standing instruction, 2026-07-28: *"nothing is off limits if it makes sense and you should know everything. Changing it is something else — make sure you have proof for everything you do, and do not ignore files or folders because of some off limitation."* Reading is how you get the proof. Never answer "unaudited" when auditing was available.

Two things are constrained, and neither is secrecy:

- `strategy-research/workflow/` **is runnable on this Mac since 2026-07-31** (`fix/workflow-macos-port`, since cherry-picked upstream; deps declared in `strategy-research/config/requirements-mac.txt`; importing `run_phase1_research` additionally needs the Gemini key env var to exist — see that file's comment). Read it freely — it is where strategy configs are LLM-authored and then gated by `trading-bot/tools/validate_config.py`. **DUAL-WRITER RESEARCH (Dorian's call, 2026-08-04): BOTH Dorian and Jeremy run experiments and strategy campaigns — finding profitable strategies on this Mac is the whole point; long-term the loop deploys to an Ubuntu server for refinement.** Option A (single-writer) was confirmed by Jeremy 2026-08-03 as an interim — recorded in `E-011/EPIC.md` on his master, invisible from this fork when the dual-writer call was made (corrected 2026-08-05 after his Slack note); on 2026-08-04 he agreed the dual-writer protocol IS the interim and E-011 (shared campaign location) is the enhancement that retires it. **Before ANY campaign runs on this Mac, two gates:** (1) the trial-ledger dual-writer merge protocol agreed with Jeremy AND implemented — one authoritative ledger, disjoint trial-ID allocation, append-only union merge, `forecast_hash` mandatory, mechanical duplicate-ID refusal in `deflate_sharpe.py`, and **no DSR computation and no holdout touch until both ledgers are merged**; (2) the queue #7 killed-run accounting gate verified on THIS machine. Two prolific writers sharing one single-use holdout make the counting discipline more load-bearing, not less. Modifying the workflow needs the same proof as anything else.
- `local_data/holdout_sealed/2026_H1/` **must not be opened at all** — not because it is forbidden knowledge but because *reading it is spending it*. It is a one-shot final exam; a chart, a `head`, a notebook all consume it. Its policy and metadata files (`config/campaign_data_policy.yaml`) are normal reading.

The `strategy-research/tools/` analyzers are reusable libraries — prefer reusing them over reimplementing.

## Known bugs, traps, and the environment

**All of it — first-run blockers, the pandas<3 trap, the zero-handler logger, the macOS gotchas, the holdout hazards, the data inventory — lives in `research/ledger/win.md` under CARRIED-FORWARD KNOWLEDGE.** Read it. It is not optional and it is not long.

```bash
# working loop, from trading-bot/:
../.venv/bin/python -m pytest              # fast suite — before AND after changes
../.venv/bin/python -m pytest -m slow      # regression backtests
../.venv/bin/python main.py simulate       # backtest → results/runs/<UTC>_<confighash>/
```

Mac/Windows results should be bit-identical — divergence = real bug, file it.

## Git discipline

`origin` = fork (push), `upstream` = Jeremy (**never push**). Branches: `mac/<topic>` for setup, `fix/<topic>` for upstream-worthy work (keep clean for PRs), `lab/<experiment>` for playground. Sync: `git fetch upstream && git merge upstream/master` (merge, don't rebase shared history).

**Collaboration model (Dorian, 2026-08-04): fork + PRs for now — the model above is unchanged. The END STATE is one shared repo, no forks; that migration is a later, joint decision with Jeremy.** The path there: fix → run clean on this Mac → clean up → harden → deploy to the Ubuntu server treated as the shared production environment for test/run. "Production" there means the always-on research home — **live trading stays behind the risk layer and its own explicit joint decision; never-live stands.**

## Backlog (in order)

0. ✅ **`mac/setup` — DONE 2026-07-28** (`afa2573d`). The 3 first-run blockers, pinned requirements, fast+slow green, reference `simulate` reproducing `5ccbec42` / `5a75366c` / −5.646 byte-identically across two venvs. Plus the `default_regime` fail-safe (engine + validator). *The base is proven.*
**Sequenced by irreversibility, not by cost — Dorian's call, 2026-07-28.** The generator is the goal, but a loop running at throughput against a broken evaluator spends two things you cannot get back: the **holdout** (single-use, terminal) and **trials** (deflated Sharpe must count N whether or not a trial was meaningful). Metrics bugs are fixable; a spent seal is not. So the irreversible risks get closed before anything runs autonomously.

1. ✅ **`fix/data-holdout-safety` — DONE 2026-07-28** (merged `c641db9a`; upstream **PR loloze6/trading-bot#2**, open alongside PR #1). Fetches can no longer write past a requested end (`_inclusive_end` expands the inclusive day once; `_trim_to_period` clamps pagination overshoot), `visualize_data` no longer names a sealed date or a phantom method, and `tests/test_no_sealed_date_literals.py` fails the suite on any executable production date at or beyond the seal's start (prose excluded by AST — the raw scan fires on upstream's own docstrings). The archived 148-line runtime tripwire stays archived. Four independent OMC lanes, 14 mutations killed, baseline byte-identical at tip. *The holdout is guarded; the seven pre-contaminated Binance caches remain readable — new leaks are blocked, old rows were not removed.* **Done (2026-07-30, board 3.5, merged `8acd08e6`): `fix/seal-tform-regex`** — the seal regex is now `(?<!\d)\d{4}-\d{2}-\d{2}`, closing both flanks (T-form timestamps and word-char prefix/join shapes like `BTCUSDT_2026-…_1h.csv`); upstream offer follows PR #2's merge. Successor tickets on the board: compact/slash date forms (both layers), gate PATTERN policy-derivation.
2. **`feat/slippage-model` — HANDED TO JEREMY 2026-07-31** (Dorian's call: execution-core ownership under single-writer; decision-ready spec in Notion → "🎯 Slippage model — decision-ready spec"). The spec: flat-bps slippage + lot-size/min-notional rounding; rerun baseline at 0/5/10 bps. **Ahead of bar-equity deliberately when the consumer is a generator:** bar-level Sharpe fixes how you *score* risk, slippage fixes how you *rank* return. Cost error changes **which strategies survive selection**, so a generator optimising against zero-slippage fills systematically proposes high-turnover mirages. The Edge Playbook says it directly — halving costs doubles the viable strategy space.
3. ✅ **`fix/metrics-bar-equity` — DONE 2026-07-31** (merged `eaa4b41c`). Off-by-default `bar_equity` block in `metrics.json` from `portfolio_states.csv`: bar-level maxDD/Sharpe + textbook Sortino, exposure %, turnover, observation counts; fail-loud on degenerate inputs; flag-off byte-identical. Reference: maxDD −24.77 vs trade-exit −24.59, sharpe −5.12 vs −5.65, sortino −5.05. Fee share dropped (duplicate of `cost_drag_pct`); flag is programmatic-only (`run_backtest(bar_equity=True)`).
4. ✅ **`fix/workflow-macos-port` — DONE 2026-07-31** (merged `33c6fbe9`). Per-file interpreter resolvers at the 4 sites (predicate: executable REGULAR FILE — the committed Windows venv means `venv/Scripts/python.exe` exists on macOS and must be skipped, not selected; fail-loud otherwise; retune's copy repo-anchored because its documented CWD and its subprocess `cwd=` disagree), static call-site guards, fork-only `requirements-mac.txt` (`claude-agent-sdk==0.2.82`, `google-genai==2.16.0` — the 07-28 audit's "one undeclared dependency" undercounted; genai was a second, with `genai.Client()` at import time). Still out of scope: the Recorder's PowerShell supervisor (`strategy-research/tools/recorder/supervise.ps1` — path since the E-002 restructure, pulled 2026-08-07).
5. **Trial-ledger dual-writer merge protocol, then verify trial accounting ON BOTH MACHINES, then the first campaigns.** Both Dorian and Jeremy run campaigns (2026-08-04 call), so the §4 protocol from the Trial-Ledger page is mandatory machinery: disjoint IDs, mandatory `forecast_hash`, union merge, no-DSR-until-merged. Then prove a **killed** run still lands a row in `campaign_state.trial_sharpes` — the only thing counting N (`run_campaign.py:1119-1122`) — on each machine that runs campaigns. A loop that logs only its winners produces beautiful, meaningless Sharpes; two such loops produce them twice as fast. **Status 2026-08-05: direction agreed by Jeremy (2026-08-04 Slack — dual-writer is the interim; E-011 retires it); concrete mechanics awaiting his confirmation on the Trial-Ledger page.**
6. **`fix/risk-layer`** — absolute allocation cap, max-drawdown kill switch, daily loss limit. Off-by-default, bit-identity proven. Needed before real money, not before research.
7. **`lab/`** — hypotheses via `/new-hypothesis`, from the Edge Playbook shortlist.

**"Good enough to start generating" is four things, not 27 tickets:** costs modelled (→ Jeremy, 2026-07-31, decision-ready spec), **drawdown honest ✅ (2026-07-31)**, **holdout guarded ✅ (2026-07-28)**, trials counted (**dual-writer since 2026-08-04:** merge protocol agreed + implemented, killed-run gate verified on both machines). Defined so the prep work has an end — "fix everything first" is a list that never finishes and the loop never ships.

## Definition of done (any change)

Fast tests green; slow tests green or output-change declared with before/after artifact diff; validator passes; no lookahead introduced (state why); no secrets; `FORK_CHANGES.md` updated if it diverges from upstream; your writer file (`research/ledger/win.md` or `research/ledger/mac.md`) updated; a paste-ready summary for Jeremy/Notion: what, why, how verified, baseline config hash.
