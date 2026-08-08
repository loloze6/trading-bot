# Handoff → next Claude Code session (written 2026-08-08, end of the trust-gap batch session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a code block for clean copy-paste. If you change §1 here, change it there.

**LAUNCH COMMAND (Dorian's standing call, 1M context always):** `claude --model "claude-opus-4-8[1m]"` — the quotes are mandatory (zsh globs the `[1m]` brackets).

**1M CONTEXT IS THE RULE FOR EVERY MODEL (Dorian 2026-08-08)** — lead AND all lanes. Transcript-verify the resolved id every session: `grep -ho '"model":"[^"]*"' ~/.claude/projects/<proj>/<session>/subagents/agent-*.jsonl | sort | uniq -c`.

**Model governance (unchanged):** **fable = THE BRAIN** — plans (`/oh-my-claudecode:plan`, planner/critic `model:"fable"`), gates (a fable verifier before EVERY merge/PR), supervises. **PLANS + VERIFICATION are the two pillars.** **opus-4.8 = lead + adversarial lanes** (`redteam-48`/`reviewer-48` register from a fresh session — VERIFY on first spawn, fallback `general-purpose` inherits the 4.8 lead; both HELD this session — `redteam-48` spawns showed "(inherit)" and transcript-verified `claude-opus-4-8`). **sonnet-5 = implementation** (`model:"sonnet"`). The Agent enum has NO 4.8 value; 4.8 lanes come via frontmatter pins or lead inheritance. Transcript-verify EVERY lane.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -8
>
> WHERE WE ARE (written 2026-08-08, end of the trust-gap batch session): mac/setup @ `0ad66c43` or later — run git log for the actual HEAD. This session closed **THREE trust-gap branches**, each through the full pipeline (fable plan+critic → sonnet-5 impl → opus-4.8 red-team BLIND to the plan → fable verifier gate), every lane transcript-verified, byte-identity re-derived independently wherever production code was touched: **(3a) `fix/seal-test-hardening`** merged `d1ee2af0` (FORK_CHANGES Row 32) — the holdout-seal TEST now catches six date notations (dash/slash/dotted/underscore/compact-8/compact-datetime) and fails CLOSED on an unreadable `*.py`; **(3c) `fix/numpy-timedelta-deprecation`** merged `7e13bc81` (Row 33) — `pd.Timedelta`→stdlib `datetime.timedelta` at 8 constructions in `data/`, 5762→0 generic-unit warnings, simulate byte-identical (net −23.021/−5.646/24); **(3b) `fix/config-identity-test`** merged `3d957e81` (Row 34) — the config-identity check is now REAL: a non-default-config run asserts manifest sha == the declared config AND output changes vs default, both proven to bite by a 3-mutation matrix. **All three are upstream-offer CANDIDATES, none offered yet.** The rigor paid off: each adversarial pass caught a real defect a quick pass would have shipped into financial code (3a a trailing-guard fail-OPEN regression; 3c a `pd.to_timedelta` NaN→NaT fail-open on the anti-lookahead causality guard → switched to stdlib; 3b a `scaling_factor` inert false-lock). Baseline anchor unchanged: `5ccbec42`/`5a75366c`/−23.021%/−5.646/24 trades — REPRODUCIBILITY ANCHOR, NEVER A RESULT.
>
> **PR #14 (leg-6 A, content-aware cache guard) is STILL OPEN, unreviewed** — Jeremy was busy since ~noon 2026-08-08; no review, no reaction to the A/B-holdout note or the server-up news, and his SSH pubkey for the `loloze` server account has NOT arrived. upstream/master unchanged at `ebe42275`.
>
> FIRST ACTIONS, IN ORDER:
> 1. Slack (tradingbot, C0BLW7V6BC6): Jeremy's reactions to **PR #14**, the **A/B-holdout note**, the **server-up news**; did he send his SSH pubkey? Check PR #14: `gh pr view 14 --repo loloze6/trading-bot --json state,mergedAt,comments,reviews` (empty-output trap — use --json).
> 2. `git fetch upstream`. If Jeremy merged #14: sync merge per the standard protocol (merge-tree dry run FIRST; pre-registered blob-identical, zero conflicts; any textual conflict = STOP). FORK_CHANGES Row 31 closes on that merge.
> 3. THE TASK — keep closing the trust gap (Dorian: financial-ops software, thoroughness is the bar; the adversarial layers are where the catches happen). Plan-first (fable) + Dorian's nod, ONE change per branch. Proposed order (Dorian trusts your judgment — reorder if a better path shows):
>    **a. Branch 2 — holdout GATE + pre-commit wiring** 🟡 (the last big holdout-seal item; board ticket `…815e…` is In progress, test-layer half done). Two parts: (i) broaden `holdout_date_gate.sh`'s PATTERN to match the test layer's six notations AND policy-derive it (currently dash-only + hardcoded to 2026-0[1-6]); (ii) wire the gate into the installed `.git/hooks/pre-commit`. **BLOCKED ON A DESIGN DECISION first:** the gate is deny-by-default + whole-index and TODAY exits 1 (blocks commits) on our own LEDGER/FORK_CHANGES/CLAUDE.fork sealed-date PROSE (measured: only 3 files block; the registry `holdout_gate_exemptions.txt` already exempts 157/160). Wiring it in naively bricks our own ledger commits every session → `--no-verify` bypass, which the gate's own docstring calls worse than no gate. Options to bring Dorian: (A) scope blocking to data formats (.csv/.json/.yaml), exempt `.md` prose; (B) run the gate against the STAGED DELTA not the whole index (lead's lean — makes ledger edits safe by construction); (C) auto-manage the 3 doc exemptions. Also reconcile the TWO divergent hooks: installed `.git/hooks/pre-commit` = secret-scan only (cites a non-existent `scripts/pre-commit`); tracked `strategy-research/tools/hooks/pre-commit` = gate + Windows-python pytest, never installed here.
>    **b. E-012 two-bars off-by-one** 🟠 (engine, now PR-able) — the #1 backtest-correctness bug. Fork already MEASURED the fix (3 edits; LEDGER 2026-08-05 E-012 S1): `has_more_data` bound + end-of-replay flush + cursor-park-past-end. Delta is zero only on windows ending FLAT; position-holding windows force-close at a stale price. Rebaselines ALL baselines (46 of Jeremy's archived runs carry the truncation) → loud declaration + joint call with Jeremy. Either nudge him for his design nod OR build it + red-team + offer as a PR.
>    **c. Offer 3a / 3c / 3b upstream** (all clean candidates; each PR must handle its fork-only bits — 3b's offer must bundle/strip the `_cache_guard` import; the seal test's `FORK-ONLY` docstring header is now stale since it lives upstream via PR #2).
>    **d. Cheap follow-ups from 3b:** T2 (latent `NameError` `backtester.py:293`, Low, ~1 line) is trivial; T1 (manifest re-reads config from disk vs in-memory — anchor-risk, needs a deliberate rebaseline) is Medium.
>    QUEUED: risk layer (live, never-live — not the backtest-trust gap); 9.5 dual-writer mechanics (Jeremy-gated, gates campaigns); the strategy generator (the actual edge hunt, once the environment is fully trusted).
>
> SERVER (culi.to) IS LIVE: `ssh culi-bot` = `trading` (bot account), `ssh culi.to` = `thrill` (Dorian). Repo `~trading/trading-bot-dorian` @ mac/setup, py3.13.12 venv, 5-file caches (Option A). To run acceptance THERE: from `~trading/trading-bot-dorian/trading-bot`, `../.venv/bin/python -m pytest -m slow --timeout=600` (the box is ~6× slower — pytest.ini's `--timeout=30` is too tight; raise it). Update via `git fetch && git merge --ff-only origin/mac/setup` (server never pushes — read-only deploy key). NEVER put `holdout_sealed/` on the server; NEVER run a window past 2025-12-31. `loloze` (Jeremy) awaits his pubkey.
>
> HARD RULES (unchanged): never run live; holdout sealed (reading it spends it; never a window past 2025-12-31; never copy `holdout_sealed/` to the server); every market-data experiment gets a research/TRIALS.csv row; no secrets; `origin` only, PRs to Jeremy (don't touch PR branches except on his feedback); no Co-Authored-By trailers.
>
> HOW I WANT YOU TO WORK (Dorian 2026-08-08): OMC teams for everything non-trivial. fable plans + gates + supervises; opus-4.8 orchestrates + attacks (red-team BLIND to the plan / code-review); sonnet-5 codes; ALL at 1M. Transcript-verify every lane. visual todo list first; plan → my nod → execute per branch; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution; byte-identity is a HARD gate for any production change (re-derive it independently, don't trust a stored control); commit gate basedpyright + ruff on changed .py; message-only amend to fix a commit's refutable specifics (tree stays byte-identical); keep Notion current as findings land (boards/bugs/epics — Fork state/location; Decisions log for binding cross-boundary calls); update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md + its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second.
>
> Start with FIRST ACTIONS 1-2, tell me what you find, then propose the next trust-gap task and get my nod.

---

## 2. State as of 2026-08-08 (trust-gap batch close)

| | |
|---|---|
| Branch | `mac/setup` @ `0ad66c43` (3b bookkeeping) — run `git log` for actual HEAD |
| Upstream | `ebe42275`; **PR #14 (leg-6 A) OPEN, unreviewed**; #10–#13 merged + synced home |
| This session | **3a** `d1ee2af0` (Row 32, seal-test), **3c** `7e13bc81` (Row 33, numpy Timedelta), **3b** `3d957e81` (Row 34, config-identity) — all merged + pushed, full pipeline, all lanes transcript-verified |
| Server | culi.to LIVE — Ubuntu 24.04, `trading`/`loloze`/`thrill`, py3.13.12, 6B green; `loloze` awaits Jeremy's key |
| Baseline | `5ccbec42` / `5a75366c` / −23.021 / −5.646 / 24 trades (anchor, never a result) |
| Suites | fast **291/0** (was 249 pre-batch; +42 = +18 seal +8 timedelta +... actually: 260 base → +18(3a)=278 wait see note); slow **16/0** (was 14; +2 from 3b); validator 0 |
| Board | 3c/3b → Done (Fork only); 3a → In progress (test layer done, gate=Branch 2); T1 (Medium)/T2 (Low) filed; the three fixes are upstream-offer candidates |
| Governance | engine work + PR to Jeremy allowed (2026-08-08); fable plans/gates, 4.8 leads/attacks-blind, sonnet codes, all 1M |
| Blocked on Jeremy | PR #14 review; `loloze` SSH key; E-012 fix-design (or we PR it); 9.5 dual-writer mechanics; A/B holdout trim discussion |
| Next task | keep closing the trust gap — **Branch 2 (needs the prose-accrual design decision)** or **E-012 two-bars (PR-able)**; plan-first, Dorian's nod |

*(Fast-suite count note: base 260 → 3a +18 (278) → 3c +5 (283) → 3b +5 fast-collected but 3b's 2 are slow-marked so fast = 291 total with +16 deselected. Confirm by running it.)*

## 3. The queue (Fork-order top-first)

Branch 2 = holdout gate PATTERN (policy-derive + six-notation) + pre-commit wiring (needs prose-accrual decision) → E-012 two-bars (engine, PR-able, rebaselines everything) → offer 3a/3c/3b upstream → T2 (cheap NameError) / T1 (config re-read, anchor-risk) → then: trial-accounting + 9.5 dual-writer (Jeremy-gated), risk layer (live), strategy generator (the edge hunt).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | 2026-08-08 entries: 3b, 3c, 3a (newest first) + CARRIED-FORWARD |
| `FORK_CHANGES.md` | Rows 32 (3a), 33 (3c), 34 (3b) — all upstream-offer candidates |
| 🐛 board (Fork queue view) | 3c/3b Done, 3a In progress (Branch 2), T1/T2 filed |
