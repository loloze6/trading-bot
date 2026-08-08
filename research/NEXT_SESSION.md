# Handoff → next Claude Code session (written 2026-08-08, end of the server + leg-6 session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a code block for clean copy-paste. If you change §1 here, change it there.

**LAUNCH COMMAND (Dorian's standing call, 1M context always):** `claude --model "claude-opus-4-8[1m]"` — the quotes are mandatory (zsh globs the `[1m]` brackets).

**1M CONTEXT IS THE RULE FOR EVERY MODEL (Dorian 2026-08-08)** — lead AND all lanes. Transcript-verify the resolved id every session: `grep -ho '"model":"[^"]*"' ~/.claude/projects/<proj>/<session>/subagents/agent-*.jsonl | sort | uniq -c`.

**Model governance (unchanged):** **fable = THE BRAIN** — plans (`/oh-my-claudecode:plan`, planner/critic `model:"fable"`), gates (a fable verifier before EVERY merge/PR), supervises. **PLANS + VERIFICATION are the two pillars.** **opus-4.8 = lead + adversarial lanes** (`redteam-48`/`reviewer-48` register from a fresh session — VERIFY on first spawn, fallback `general-purpose` inherits the 4.8 lead). **sonnet-5 = implementation** (`model:"sonnet"`). The Agent enum has NO 4.8 value; 4.8 lanes come via frontmatter pins or lead inheritance. Transcript-verify EVERY lane.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -8
>
> WHERE WE ARE (written 2026-08-08, end of a big session): mac/setup @ `2b91e9c9` or later — run git log for the actual HEAD. This session, in order: **(1) SYNC-MERGED upstream `ebe42275`** — Jeremy merged all three fork PRs (#11 daily ingest, #12 slow-suite guards, #13 engine plumbing); pulled home byte-identically (merge `da4f1e0d`, tree-OID-identical to pre-merge; one pre-registered leg-6A/#12 conflict resolved take-ours; FORK_CHANGES rows 26/28/29 closed). **(2) OFFERED leg-6 A upstream = PR loloze6/trading-bot#14 (OPEN)** — content-aware cache guard, blob-identical to fork HEAD, verified on Jeremy's base (fast 249→260/0, slow 14, simulate byte-identical, degenerate demo 9F/5P→14-skipped), opus-4.8 red-team SHIP + fable verifier MERGE-READY, Slack posted; FORK_CHANGES Row 31. **(3) STOOD UP culi.to AS THE SHARED PRODUCTION/RUN SERVER + LEG 6 B GREEN** — Ubuntu 24.04, `trading` service account (key-only), read-only deploy key, python 3.13.12 via uv; **6B acceptance byte-identical on Linux: validator 0, fast 260/0, slow 14/0, simulate == reference (`5ccbec42`/`5a75366c`/−23.021/−5.646/24 trades) + deterministic, zero new listeners. python-build parity HOLDS.** Caches = Option A (Dorian's call, in-file 2026 rows unread via the window rule; A/B trim/decontamination deferred, flagged to Jeremy — now a filed board ticket at Fork queue 7.5). **(4) Board reordered (actionable to top, Done down); workflow brainstorm posted to Notion for Dorian+Jeremy alignment.** Baseline anchor unchanged: `5ccbec42`/`5a75366c`/−23.021%/−5.646/24 trades — REPRODUCIBILITY ANCHOR, NEVER A RESULT.
>
> **NEW GOVERNANCE (Dorian 2026-08-08): ENGINE WORK ON THE FORK + PR TO JEREMY IS NOW GREEN-LIT.** We understand the codebase and trust is there both ways. Additive is still preferred and mergeability still matters, but correctness fixes to the engine (E-012, config-identity, G1, aux-feeds) can now be BUILT on the fork and OFFERED as PRs — no longer issue-first-only. Same rigor: fable plan → Dorian's nod → per-branch → red-team + verifier → PR.
>
> FIRST ACTIONS, IN ORDER:
> 1. Slack (tradingbot, C0BLW7V6BC6): Jeremy's reactions to **PR #14**, the **A/B-holdout note**, and the **server-up news**; did he send his SSH pubkey (to finish the `loloze` account)? Check PR #14 with `gh pr view 14 --repo loloze6/trading-bot --json state,mergedAt,comments,reviews` (empty-output trap — use --json).
> 2. `git fetch upstream`. If Jeremy merged #14: sync merge per the standard protocol (merge-tree dry run FIRST; pre-registered blob-identical, zero conflicts; any textual conflict = STOP). FORK_CHANGES Row 31 closes on that merge.
> 3. THE TASK — **close the trust gap** (Dorian: "i still cant fully trust the bot, too many open things"). Plan-first (fable) + Dorian's nod, ONE change per branch. Proposed order (Dorian trusts your judgment — reorder if a better path shows):
>    **a. Harden the holdout seal** 🟢 — one branch: compact/slash/non-padded date forms (`test_no_sealed_date_literals.py` + `holdout_date_gate.sh` PATTERN, both layers), seal-scan resilience (aborts on first undecodable file today), wire `holdout_date_gate.sh` into the installed pre-commit. Cheap, high-value, fully fork-owned; protects the one-shot exam.
>    **b. Make the config-identity check real** 🟡 — `test_config_actually_loaded` is vacuous; a non-default-config run must prove the config you declared is the one that ran. Foundational trust.
>    **c. numpy Timedelta deprecation on the default bar path** 🟢🟡 — `data_manager.py:209,217,772`; kills the ~50k-warning flood + the latent numpy-bump break; MUST prove byte-identity (default path).
>    **d. ENGINE (now allowed via PR):** E-012 two-bars off-by-one is the #1 backtest-correctness bug — fork already measured the fix (3 edits); either nudge Jeremy for his design nod OR build it + red-team + offer as a PR. Then G1 kraken read-path cache-mutation guard and aux-feeds-follow-exchange (both disclosed in merged PRs).
>    QUEUED: risk layer (live, never-live — not the backtest-trust gap); 9.5 dual-writer mechanics (Jeremy-gated, gates campaigns); the strategy generator (the actual edge hunt, once the environment is fully trusted).
>
> SERVER (culi.to) IS LIVE: `ssh culi-bot` = `trading` (bot account), `ssh culi.to` = `thrill` (Dorian). Repo `~trading/trading-bot-dorian` @ mac/setup, py3.13.12 venv, 5-file caches (Option A). To run acceptance THERE: from `~trading/trading-bot-dorian/trading-bot`, `../.venv/bin/python -m pytest -m slow --timeout=600` (the box is ~6× slower — pytest.ini's `--timeout=30` is too tight; raise it). Update via `git fetch && git merge --ff-only origin/mac/setup` (server never pushes — read-only deploy key). NEVER put `holdout_sealed/` on the server; NEVER run a window past 2025-12-31. `loloze` (Jeremy) awaits his pubkey.
>
> HARD RULES (unchanged): never run live; holdout sealed (reading it spends it; never a window past 2025-12-31; never copy `holdout_sealed/` to the server); every market-data experiment gets a research/TRIALS.csv row; no secrets; `origin` only, PRs to Jeremy (don't touch PR branches except on his feedback); no Co-Authored-By trailers.
>
> LESSONS (standing set, most recent first): 6B proved python-build parity holds (Clang/python-build-standalone 3.13.12 == byte-identical engine) — a slow-suite "failure" was pytest-timeout (30s) on the ~6× slower box, NOT a divergence; simulate's config+data+metrics match is the cleanest parity diagnostic (data_sha first splits parse-level vs engine-level); an over-broad `find *holdout*` false-alarms on tracked source/doc files — gate on `holdout_sealed` specifically; a read-only deploy key mechanically enforces "server never pushes"; `gh repo deploy-key add` (no `--allow-write`) lets the lead add it without the owner; allowlist rsync (never blocklist) for cache transfer; the fable planner/critic CORRECT the lead's ground truth (verify BOTH ways); blob-gate == fork-HEAD is the upstream-offer honesty proof; the fable verifier catches refutable commit-message specifics (message-only amend keeps the tree byte-identical); transcript-verify EVERY lane's model; results before decisions (present, END TURN); never trust a piped exit code; simulate prints NOTHING (read results/runs; restore trades.json); no macOS `timeout` (ssh `-o ConnectTimeout`, remote `nice`); provision caches into ANY engine environment; commit messages reviewed like code; two-phase characterize-and-STOP; earlier numbers are predictions; fail loud not flattering.
>
> HOW I WANT YOU TO WORK (Dorian 2026-08-08): OMC teams for everything non-trivial. fable plans + gates + supervises; opus-4.8 orchestrates + attacks (red-team/code-review); sonnet-5 codes; ALL at 1M. Transcript-verify every lane. visual todo list first; plan → my nod → execute per branch; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution; commit gate basedpyright + ruff on changed .py; keep Notion current as findings land (boards/bugs/epics — Fork state/location; Decisions log for binding cross-boundary calls); update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md + its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second.
>
> Start with FIRST ACTIONS 1-2, tell me what you find, then plan task 3a and get my nod.

---

## 2. State as of 2026-08-08 (server + leg-6 close)

| | |
|---|---|
| Branch | `mac/setup` @ `2b91e9c9` (LEDGER 6B) — run `git log` for actual HEAD |
| Upstream | `ebe42275`; **PR #14 (leg-6 A) OPEN**, unreviewed; #10-#13 merged + synced home |
| Server | **culi.to LIVE** — Ubuntu 24.04, `trading`/`loloze`/`thrill` accounts, py3.13.12, 6B GREEN, baseline byte-identical on Linux |
| Baseline | `5ccbec42` / `5a75366c` / −23.021 / −5.646 / 24 trades (anchor, never a result) |
| Suites | fast **260/0**, slow **14/0** (server: `--timeout=600`), validator 0 |
| Board | reordered: actionable to top (holdout-seal → config-identity → numpy → engine), Done pushed down |
| Governance | **engine work + PR to Jeremy now allowed** (2026-08-08); fable plans/gates, 4.8 leads/attacks, sonnet codes, all 1M |
| Blocked on Jeremy | PR #14 review; `loloze` SSH key; E-012 fix-design (or we PR it); 9.5 dual-writer mechanics; A/B holdout trim discussion |
| Next task | close the trust gap — start **3a holdout-seal hardening**, plan-first, Dorian's nod |

## 3. The queue (post-reorder, Fork-order top-first)

Holdout-seal hardening (a: compact-dates, scan-resilience, pre-commit wiring, PATTERN-from-policy, scan-scope, merge-enforcement, ingest-seal-guard) → config-identity (b) → numpy-deprecation (c) → **engine via PR:** E-012 two-bars, G1 cache-mutation, aux-feeds-follow-exchange, campaign-path exchange validation, measure_bar_sigma, get_historical_klines lookahead, funding_rate follow-on → then: trial-accounting + 9.5 dual-writer (Jeremy-gated), risk layer (live), strategy generator (the edge hunt).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | 2026-08-08 leg-6B + sync-merge + leg-6A entries + CARRIED-FORWARD |
| `FORK_CHANGES.md` | rows 26/28/29 closed (merged), Row 31 (leg-6 A → PR #14) |
| `.omc/plans/server-provisioning.md` + `.omc/artifacts/leg6B/RESULT.md` | how culi.to was set up + the 6B evidence |
| `.omc/plans/collaboration-workflow-brainstorm.md` | the workflow ideas (also in Notion) — for Dorian+Jeremy alignment, NOT execution |
| 🐛 board (Fork queue view) | reordered; the trust-gap items are the top rows |
