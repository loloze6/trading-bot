# Handoff → next Claude Code session (written 2026-07-28, after the reset)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: `CLAUDE.fork.md`, `research/LEDGER.md`, `research/NEXT_SESSION.md`. **`CLAUDE.fork.md` is NOT auto-loaded** — Jeremy's `CLAUDE.md` has no include for it, so you must read it explicitly. Then run `git status && git log --oneline -5`.
>
> **Context:** this fork was reset to Jeremy's `70dab378` on 2026-07-28 and restarted from scratch. The tree is byte-identical to upstream. All prior work is preserved in three `archive/2026-07-28/*` tags — nothing was deleted, and nothing from them is to be restored without my say-so. `research/LEDGER.md` carries the knowledge that was expensive to get; read it properly, it will save you days and it is where the traps live.
>
> The reason for the reset is in the ledger and I want you to take it seriously: the previous agent proposed heavy runtime guards where a static check would have done, batched large changes into sessions I'd scoped small, and needed three adversarial review rounds to stabilise its own work. I lost trust in the process, not the code. **The working agreement in the ledger is the remedy. Follow it.**
>
> **Goal for this session: milestone 1 — make Jeremy's bot run on my Mac and prove the base is sound.**
>
> Right now `../.venv/bin/python main.py simulate` exits `FATAL ERROR: invalid strategy_config`. Three known first-run blockers are described in the ledger. The definition of success is not "it runs" — it is:
>
> ```
> config_sha256 5ccbec42…   data_sha256 5a75366c…
> net −23.021%   sharpe −5.646   maxDD −24.592%   24 trades   fees 68.897289
> ```
>
> If a clean Jeremy base plus those three fixes reproduces that exactly, we know the foundation is sound by measurement rather than assertion. That is the whole point of the milestone.
>
> **How I want you to work:**
> - Propose a plan in 3–6 bullets and get my nod **before writing any code**.
> - One change per branch. Reviewed and green before you start the next.
> - Prefer the cheapest control that works. Do not add guards to guards.
> - Verify by execution, never by reading. `main.py simulate` prints **nothing** — read the newest dir under `results/runs/`.
> - Never push to Jeremy. `origin` only.
> - No `Co-Authored-By` trailers.
> - Update `research/LEDGER.md` before the session ends.
>
> Start by confirming the environment and telling me what you find.

---

## 2. What happened (2026-07-28)

The fork was reset at Dorian's request. He could no longer trust the basis after a session in which the agent injected nine defects that three adversarial review rounds had to catch.

**Measured before the reset, so it is not re-litigated:** the old tree was objectively intact — engine files 0 changed, committed market data 0 bytes changed, holdout seal intact, baseline byte-identical, git history unbroken. The repository was fine. The *process* was not.

What was done:

1. Three `archive/2026-07-28/*` tags created and pushed, each with a message explaining what is inside and what is worth cherry-picking.
2. `origin/master` fast-forwarded to `upstream/master` = `70dab378`. It was 1 commit behind and 0 ahead, so this was a plain fast-forward — **no force-push, nothing orphaned**.
3. New branch `mac/setup` cut from `upstream/master`.
4. Knowledge carried forward (`CLAUDE.fork.md`, `research/LEDGER.md`, `research/TRIALS.csv`, `FORK_CHANGES.md`, `.claude/commands/`). **Code was not.**

**Jeremy has not moved** since `70dab378` — verified, 0 commits ahead. There was no newer upstream code to pull.

---

## 3. Expected state — verify, don't assume

| Check | Expected |
|---|---|
| branch | `mac/setup`, cut from `70dab378` |
| `git diff upstream/master..HEAD -- trading-bot/` | **empty** (tree is Jeremy's) |
| `main.py simulate` | `FATAL ERROR: invalid strategy_config`, no run produced |
| `.venv/bin/python --version` | Python 3.13.12 |
| installed deps | pandas 2.3.3, ccxt 4.5.68, matplotlib 3.11.1, requests 2.34.2, PyYAML 6.0.3, pytest 9.1.1, numpy 2.5.1 |
| `trading-bot/local_data` | 28 GB present |
| `git remote -v` | `upstream` push URL = `DISABLED_use_a_PR_instead` |

**The venv already exists and already has ccxt.** It survived the reset because it is gitignored. So "make it run on the Mac" is *not* an environment problem — the environment works. It is a config problem (blocker #1) plus a `requirements.txt` that does not yet describe what is actually installed (blocker #3).

That distinction matters for milestone 1: fixing `requirements.txt` is about making a *fresh clone on another machine* work. Consider proving it with a throwaway venv rather than assuming.

---

## 4. Milestone 1 — the plan to propose

Not prescriptive; the next agent should think and propose. But the shape is known:

1. **Blocker #1** — `strategy_config.json`: `default_regime` `"mean_reversion"` → `"unknown"`. Declare the behaviour change loudly: 76 trades → 24, and `tests/fixtures/reference_run.json` must be rebaselined because the old values are **unreachable**, not stale.
2. **Blocker #2** — `config.json`: `trading.symbols` `ETHUSDT` → `BTCUSDT`.
3. **Blocker #3** — `requirements.txt`: pin versions, add `ccxt`, `matplotlib`, `requests`, `PyYAML`, and **cap `pandas<3`**. The cap is not cosmetic — read the ledger entry on it.
4. **Prove it:** fast suite, `pytest -m slow`, `tools/validate_config.py`, then `main.py simulate` reproducing `5ccbec42` / `5a75366c` / −5.646 / 24 trades.
5. **Record it:** `research/LEDGER.md`, `FORK_CHANGES.md` (these are the first real divergences), a `TRIALS.csv` row for the baseline reproduction.

Do these as **one branch, one review** — they are a single logical unit ("make it run"), not four separate concerns.

---

## 5. Deliberately NOT restored — decide before reusing

All in `archive/2026-07-28/fix-fetch-end-bound`. Read the tag message first.

| Item | Assessment |
|---|---|
| **`BaseFetcher` end-bound fix** | **Worth cherry-picking.** CcxtFetcher wrote 259 sealed bars past an explicit `end_date` — measured. ~30 lines, upstream-worthy, no dependency on `strategy-research/`. |
| **`visualize_data` fix** | **Worth cherry-picking.** `end_date='2026-04-23'` is inside the seal with `localStorage=True` (~500k sealed 1m bars per run), and it calls a method that exists on no fetcher. |
| **Holdout write tripwire** | **Reconsider.** +148 lines inside Jeremy's `base_fetcher.py` with a hard dependency on `strategy-research/config/`. Measured to guard the *write* path only — it handed 1,440 sealed rows to a caller on the *read* path without firing. A static check that no date literal in the repo falls inside `holdout_range` would catch more, for ~15 lines and zero divergence. |
| **`tools/fetch_data.py`** | Fork-only new file, cannot conflict. Provisions the gitignored caches without crossing the seal. Useful if a fresh clone ever needs provisioning. |
| **Kraken ingest merge fix** | Real bug (overwrites instead of merging, 500 rows → 10) but only matters if you re-run the ingest. Not urgent. |

**PR #1 to Jeremy is still open and still correct.** Do not close it.

---

## 6. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, research protocol, backlog. **Not auto-loaded — read it.** |
| `research/LEDGER.md` | every trap, finding, and the working agreement. **The important one.** |
| `../TRADING_BOT_REVIEW.md` | full July 2026 code review, all `file:line` refs |
| `research/TRIALS.csv` | every experiment; T001 is the pre-reset baseline reproduction |
| `strategy-research/config/campaign_data_policy.yaml` | `holdout_range` — source of truth for the seal |
| `DOC/STRATEGY_FRAMEWORK.md` | read before touching strategies |

Notion — "Trading Bot HQ": the **🐛 Bugs & Tasks** DB, where `Status` = Jeremy's master and **"Dorian's fork"** = this fork.

---

## 7. Open decisions for Dorian

- **`.claude/commands/`** (4 fork slash commands) are on disk but untracked — Jeremy's `.gitignore` excludes `.claude/`. Tracking them needs a `.gitignore` divergence.
- **`CLAUDE.md`** no longer includes `@CLAUDE.fork.md`, so fork guardrails do not auto-load. Two lines would fix it; that is divergence #1 and his call.
- **`venv/`** — upstream tracks 449 files of a Windows venv. Untracking is PR-worthy, separate.
