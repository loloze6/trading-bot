# Handoff → next Claude Code session (written 2026-08-08 evening, after the upstream-offers + board-reconcile session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (sync §1 there if you change it here).

**LAUNCH COMMAND (Dorian's standing call, 1M context always):** `claude --model "claude-opus-4-8[1m]"` — the quotes are mandatory (zsh globs the `[1m]` brackets).

**1M CONTEXT IS THE RULE FOR EVERY MODEL** — lead AND all lanes. Transcript-verify the resolved id every session: `grep -ho '"model":"[^"]*"' ~/.claude/projects/<proj>/<session>/subagents/agent-*.jsonl | sort | uniq -c`.

**Model governance (unchanged):** **fable = THE BRAIN** — plans, gates (a fable verifier before EVERY merge/PR), supervises. **opus-4.8 = lead + adversarial lanes** — `redteam-48`/`reviewer-48` register from a fresh session (VERIFY on first spawn; both HELD this session, spawned as `(inherit)` and transcript-verified `claude-opus-4-8`); fallback `general-purpose` inherits the 4.8 lead. **sonnet-5 = implementation** (`model:"sonnet"`). Transcript-verify EVERY lane.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -8
>
> WHERE WE ARE (written 2026-08-08 evening): mac/setup @ `08d2ec67` or later — run git log for the actual HEAD. Last session: **(1) fixed the fork-CI red streak** — one POSIX-only assertion in the seal test (`.startswith("IsADirectoryError")`; Windows raises `PermissionError` opening a directory, both `OSError`), `fix/seal-test-windows-portability` merged `2ab6f2fe`; fork CI green on ubuntu AND windows. **(2) Offered the three trust-gap fixes upstream** as cross-fork PRs, each built on Jeremy's `ebe42275`, verified there by execution, opus-4.8 red-teamed BLIND (all SHIP, transcript-verified `claude-opus-4-8`): **PR #15** (3c numpy Timedelta — simulate 5-artifact byte-identical `5ccbec42`/`5a75366c`), **PR #16** (3a seal test + the Windows fix, FORK-ONLY docstring stripped), **PR #17** (3b config-identity — REBASED onto upstream's bare-`.exists()` guard so PURELY ADDITIVE and INDEPENDENT of #14). Merge-tree `--write-tree` (exit 0): PRs **#14/#15/#16/#17 merge in ANY order, zero conflicts**; Slack merge playbook posted to Jeremy. **(3) Reconciled the 🐛 Bugs & Tasks board:** the new `Upstream?` column is populated across all 73 rows (49 Candidate / 22 N/A / 2 Permanent fork-only — only pyrightconfig + dev-tool-pins are permanently fork-only); fixed one stale status (seal-resilience ticket was done by 3a); split repo-hygiene (CI = its own Done/fork-only row; remove-venv/ = open Candidate); closed culi.to; filed a Jeremy-SSH-key task assigned to him. Baseline anchor: `5ccbec42`/`5a75366c`/−23.021%/−5.646/24 — REPRODUCIBILITY ANCHOR, NEVER A RESULT.
>
> upstream/master was `ebe42275` at session end; Jeremy had been quiet since ~noon 2026-08-08 and may not have merged #14–#17 yet.
>
> FIRST ACTIONS, IN ORDER:
> 1. Slack (tradingbot, C0BLW7V6BC6): Jeremy's reactions to PRs #14/#15/#16/#17 — did he merge any, in what order? — and did he send his SSH pubkey for the `loloze` account? Check: `gh pr list --repo loloze6/trading-bot --state all --json number,state,mergedAt` (empty-output trap — use --json).
> 2. `git fetch upstream`. For any of #14–#17 Jeremy merged: sync merge per the standard protocol (merge-tree dry run FIRST; the four were pre-registered blob-identical/zero-conflict; any textual conflict = STOP). Close the matching FORK_CHANGES rows (#14→31, #15→33, #16→32+35, #17→34) and flip the board's `Fork location` to Merged upstream.
> 3. THE TASK — **E-012: backtests never trade the last two fetched bars** (the #1 backtest-correctness bug; engine; PR-able). The joint FIX-FORWARD decision is ALREADY MADE (2026-08-05, per Jeremy's 08-04 Slack). Plan-first (fable) + Dorian's nod, ONE change per branch. **Characterize by EXECUTION before planning** — the numbers below are the fork's own prior measurement (probe `23aa31e6`, NEVER MERGED); re-derive them from scratch, don't trust them (the ledger's "int()-wrap" prediction for 3c was refuted by execution).
>    **The bug (two independent, additive off-by-ones):** Drop 1 — `has_more_data` (`data_manager.py:816`) is `cursor < len(historical_data) - 1`, so the final loaded row is never fed. Drop 2 — a candle completes only when a LATER row arrives (`_ingest`, `data_manager.py:355`/`:364`), so the last fed row opens a candle that never closes; `get_final_candle` (`:794`) exists to retrieve exactly that leftover but has ZERO callers (abandoned fix-in-progress). Last PROCESSED bar = `<end> 21:00`, not 23:00.
>    **The fix is THREE edits, not two** (proven by bounded simulation): (i) relax the `has_more_data` bound; (ii) end-of-replay flush — fire the final still-open candle, making the flush callback-visibility symmetric with `_ingest`; (iii) park the cursor PAST the end — `advance()` parks it ON the last row, so relaxing has_more_data alone re-feeds the final row forever.
>    **Delta (measured, re-derive):** on windows ending FLAT it's bookkeeping-only — reference window (2024-04-01→05-30): bars 1438→1440, first 1438 rows byte-identical, **trades.json byte-identical, both config+data hashes UNCHANGED**, 4 of 91 default metrics keys move, manifest bar_count finally agrees with bars.csv, off-by-default bar_equity exposure_pct 3.7908→3.785. On a position-HOLDING window (2024-09-15→10-05) the dropped bars carry a real EXIT signal — unpatched force-closes at a stale 21:00 price (61857.64), patched self-exits at 22:00 (62039.52): net −8.446→−7.907, **sharpe −7.585→−7.018**, win 41.18→47.06%, maxDD −9.83 / 17 trades both legs. **Delta is ZERO only on flat-ending windows** — "2-in-1440 ≈ noise" does NOT hold for position-holding windows.
>    **Four fix-design constraints (all must be handled):** (a) re-anchor `test_close_positions_at_end` to a NEW position-ending window — post-fix its premise dissolves (9 tests fail; its 2 survive-tests pass VACUOUSLY, disarming the ONLY coverage for the two `_close_all_positions_at_end` NameErrors); (b) rebaseline the bar_equity fixtures; (c) make the flush callback-visibility symmetric with `_ingest`; (d) add a still-forming-final-candle check for windows ending at the cache tip.
>    **This rebaselines baselines → LOUD declaration.** 41 of 46 archived upstream runs show delta exactly 2; ALL 46 end at 21:00; the committed reference artifact carries it (manifest 1440 vs bars.csv 1438). The reference fixture's manifest bar_count + the 4 moved metrics keys must be rebaselined WITH a control run proving 100% of the delta is the fix (not an engine regression) — never change an expected value without replaying the old path. Byte-identity is NOT preserved for position-holding windows; that is the point and must be declared, not hidden. Manifest fix is separable/metadata-only; pre-fix results stay comparable among themselves with a dated boundary line; NO cross-boundary comparisons; thresholds stay Jeremy's (P4 vs run_054: BTCUSDT ≥ 0.5791, ETHUSDT ≥ 0.0318 median Sharpe).
>    **Approach:** full pipeline (fable plan+critic → sonnet-5 impl → opus-4.8 red-team BLIND → fable verifier), re-derive the fix + every number by execution, rebaseline the reference fixture with the control run, LOUD declaration in FORK_CHANGES + a new baseline anchor, then — since fix-forward is decided — build + red-team + **offer as a PR to Jeremy** (the shared reference-fixture rebaseline is his to accept on merge; the PR body declares the manifest+metrics delta and the position-holding-window sign change explicitly). Nudge him on Slack if you want his design nod before opening. Full prior record: fork `research/LEDGER.md` 2026-08-03 (late) + 2026-08-05 (afternoon), TRIALS T003/T004, ledger commit `5724a3f9`, probe `23aa31e6`.
>    QUEUED after E-012: offer T1/T2 + the other Candidate engine bugs; Branch 2 (holdout gate + pre-commit, needs the prose-accrual design decision A/B/C); risk layer (live, never-live); 9.5 dual-writer mechanics (Jeremy-gated); the strategy generator (the edge hunt, once the environment is fully trusted).
>
> SERVER (culi.to) IS LIVE: `ssh culi-bot` = `trading` (bot account), `ssh culi.to` = `thrill` (Dorian). Repo `~trading/trading-bot-dorian` @ mac/setup, py3.13.12 venv, 5-file caches (Option A). Acceptance THERE: from `~trading/trading-bot-dorian/trading-bot`, `../.venv/bin/python -m pytest -m slow --timeout=600` (box ~6× slower). Update via `git fetch && git merge --ff-only origin/mac/setup` (read-only deploy key). NEVER put `holdout_sealed/` on the server; NEVER run a window past 2025-12-31. `loloze` (Jeremy) awaits his pubkey.
>
> HARD RULES (unchanged): never run live; holdout sealed (reading it spends it; never a window past 2025-12-31; never copy `holdout_sealed/` to the server); every market-data experiment gets a research/TRIALS.csv row; no secrets; `origin` only, PRs to Jeremy (don't touch PR branches except on his feedback); no Co-Authored-By trailers.
>
> HOW I WANT YOU TO WORK (Dorian, standing): OMC teams for everything non-trivial. fable plans + gates + supervises; opus-4.8 orchestrates + attacks (red-team BLIND to the plan / code-review); sonnet-5 codes; ALL at 1M. Transcript-verify every lane. visual todo list first; plan → my nod → execute per branch; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution; byte-identity is a HARD gate for any production change (re-derive it independently — and where E-012 deliberately BREAKS it, declare the delta loudly with a control run); commit gate basedpyright + ruff on changed .py (delta, not total — pre-existing upstream noise is not a finding); message-only amend to fix a commit's refutable specifics (tree stays byte-identical); watch the zsh traps (unquoted `$var` doesn't word-split; heredoc + `&&` mangles commit messages — use `git commit -F <file>`); keep Notion current as findings land (boards/bugs/epics; Decisions log for binding cross-boundary calls); update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md + its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second.
>
> Start with FIRST ACTIONS 1–2, tell me what you find, then plan E-012 (fable) and get my nod before building.

---

## 2. State as of 2026-08-08 (evening)

| | |
|---|---|
| Branch | `mac/setup` @ `08d2ec67` (board bookkeeping) — run `git log` for actual HEAD |
| Upstream | `ebe42275`; **four PRs OPEN: #14 (leg-6A cache guard), #15 (3c numpy Timedelta), #16 (3a seal test + Windows fix), #17 (3b config-identity)** — merge-tree clean, any order; none merged yet at session end |
| This session | `2ab6f2fe` seal-test Windows fix (green CI); PRs #15/#16/#17 opened + red-teamed (all SHIP); board `Upstream?` column reconciled; `08d2ec67` bookkeeping |
| Server | culi.to LIVE (ticket closed Done); `loloze` awaits Jeremy's SSH key (own ticket) |
| Baseline | `5ccbec42` / `5a75366c` / −23.021 / −5.646 / 24 trades (anchor) — **E-012 will rebaseline the reference manifest bar_count 1438→1440 + 4 metrics keys; trades + hashes hold on the flat reference** |
| Board | `Upstream?` column: 49 Candidate / 22 N/A / 2 Permanent fork-only (pyrightconfig, dev-tool pins). Live In-progress fork code: E-012 (order 10), seal-gate/Branch-2 (order 1), remove-venv/ (order 22) |
| Blocked on Jeremy | PRs #14–#17 review/merge; `loloze` SSH key; E-012 design nod (or we PR it); 9.5 dual-writer mechanics |
| Next task | **E-012 two-bars** — plan-first (fable), Dorian's nod, build + red-team + offer as PR (fix-forward decided) |

## 3. The queue (Fork-order top-first)

E-012 two-bars (engine, PR-able, rebaselines everything) → sync/close #14–#17 as Jeremy merges → offer remaining Candidate engine bugs (T1/T2 + the exchange/aux/lookahead set) → Branch 2 (holdout gate + pre-commit, needs the prose-accrual decision) → risk layer (live) → 9.5 dual-writer (Jeremy-gated) → strategy generator (the edge hunt).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | newest entry (this session) + 2026-08-05/08-03 E-012 entries + CARRIED-FORWARD |
| `FORK_CHANGES.md` | Rows 31–35 (the four open PRs + the Windows fix) |
| E-012 bug page (🐛 board) | full trace + the 08-05 fix-forward joint decision callout |
