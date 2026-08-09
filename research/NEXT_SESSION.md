# Handoff → next Claude Code session (written 2026-08-09, after E-012 shipped)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (sync §1 there if you change it here).

**LAUNCH COMMAND (Dorian's standing call, 1M context always):** `claude --model "claude-opus-4-8[1m]"` — the quotes are mandatory (zsh globs the `[1m]` brackets).

**1M CONTEXT IS THE RULE FOR EVERY MODEL** — lead AND all lanes. Transcript-verify the resolved id every session: `find ~/.claude/projects/<proj> -name 'agent-*.jsonl' -mmin -N | while read f; do grep -ho '"model":"[^"]*"' "$f" | sort -u; done`.

**Model governance (unchanged, and fully exercised this session):** **fable = THE BRAIN** — plans, gates (a fable verifier before EVERY merge/PR), 2nd-opinion. **opus-4.8 = lead + adversarial lanes** — `redteam-48`/`reviewer-48` (or `oh-my-claudecode:architect`/`critic` with model override; VERIFY they resolve to `claude-opus-4-8`). **sonnet-5 = implementation** (`model:"sonnet"`). E-012 ran 8 lanes through this — all transcript-verified: planner `fable-5`, architect/critic `opus-4-8`, 2nd-opinion `fable-5`, Phase-A executor `opus-4-8`, impl `sonnet-5`, red-team `opus-4-8`, verifier `fable-5`.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -8
>
> WHERE WE ARE (written 2026-08-09): mac/setup @ `d9c7d637` or later — run git log for the actual HEAD. **Last session SHIPPED E-012** — the #1 backtest-correctness bug: backtests silently never processed the last TWO fetched bars of any window (last processed bar landed at `<end> 21:00`, not 23:00; two additive off-by-ones). Fixed via the full OMC pipeline, ALL lanes transcript-verified to governance: fable plan → opus-4.8 deliberate consensus (architect killed a nondeterministic wall-clock guard; critic caught an F1 surprise-rebaseline + an F2 KILL criterion that would've aborted a correct fix) → fresh fable 2nd-opinion (found the basedpyright gate-staller) → Phase A characterize-by-execution (opus, Dorian signed off on the numbers) → sonnet-5 impl → opus-4.8 **BLIND** red-team (SHIP — reconstructed the pre-fix engine, proved only the last 2 bars move) → fable verifier (MERGE-READY; caught a false commit-message number → message-only amend). **Merged to mac/setup** (fix `7ad1c42d`, merge `3059b196`, loud declaration `d9c7d637`) and **offered to Jeremy as PR #18** (cherry-picked onto his `acfa5b63`, delta byte-identical to the verified fix, re-verified on his base: fast 302 / slow 16 green). **Baseline:** the TRADE-LEVEL anchor HOLDS byte-identical (`5ccbec42` / `5a75366c` / 24 / −23.021% / −5.646 — flat-window trades.json + prefix unchanged); BAR-LEVEL baselines + `bar_equity_reference.json` (n_bars_total 1438→1440, exposure_pct 3.7908→3.785) rebaselined at the 2026-08-09 boundary; position-holding windows change P&L (the fix working — stale 21:00 force-close → real 22:00 self-exit). No cross-boundary comparison of bar-level/bar_equity/position-holding results. Full plan + all lane evidence: `.omc/plans/e012-two-bars-fix.md` + `.omc/plans/e012-evidence/`.
>
> upstream/master was `acfa5b63` at session end; **PR #18 OPEN, not yet merged** (posted to Jeremy on Slack with the rebaseline warning). culi.to server: `loloze` still awaits Jeremy's SSH key. The parallel ingest-holdout-guard lane (board order 7) was NOT run — no `fix/ingest-holdout-seal-guard` branch exists; that ticket is still open.
>
> FIRST ACTIONS, IN ORDER:
> 1. Slack (tradingbot, C0BLW7V6BC6): Jeremy's reaction to **PR #18** — merged? in what state? — and did he send his SSH pubkey for the `loloze` account? Check: `gh pr list --repo loloze6/trading-bot --state all --json number,state,mergedAt` (empty-output trap — use --json).
> 2. `git fetch upstream`. If PR #18 merged: sync merge per the standard protocol (merge-tree dry run FIRST; the offer delta was pre-verified byte-identical to the merged fix, so expect a clean/near-empty engine delta — any textual conflict = STOP). Flip the E-012 board row's `Fork location` → Merged upstream and note it on the FORK_CHANGES 2026-08-09 row.
> 3. THE TASK — Dorian's pick from the queue (§3). Leading candidates, all PR-able and same-discipline as E-012 (plan-first fable → Dorian's nod → full pipeline, one change per branch, byte-identity gate): **(a)** the Candidate engine bugs that GATE multi-symbol/kraken campaigns — aux feeds don't follow `trading.exchange` (board order 12, Medium) + campaign path ignores/never-validates `trading.exchange` (order 13, HIGH, "must close before any kraken campaign"); these open the door to breadth (19-pair universe > BTC-only), where the edge probability actually is. **(b)** Branch 2 (holdout gate + pre-commit) — but it needs Dorian's **prose-accrual DESIGN DECISION first** (scope the deny-by-default gate to data-formats / staged-delta only / auto-manage the 3 doc exemptions — currently it blocks commits on our own LEDGER/FORK_CHANGES sealed-date PROSE). **(c)** the ingest holdout seal guard (order 7, Medium) — `tools/ingest_kraken_archive.py` write path has no seal check; a post-2025 tranche would write sealed rows into a tracked cache. Self-contained, PR-able, mission-aligned.
>
> SERVER (culi.to) IS LIVE: `ssh culi-bot` = `trading` (bot account), `ssh culi.to` = `thrill` (Dorian). Repo `~trading/trading-bot-dorian` @ mac/setup, py3.13.12 venv, 5-file caches (Option A). Acceptance THERE: from `~trading/trading-bot-dorian/trading-bot`, `../.venv/bin/python -m pytest -m slow --timeout=600` (box ~6× slower). Update via `git fetch && git merge --ff-only origin/mac/setup` (read-only deploy key). NEVER put `holdout_sealed/` on the server; NEVER run a window past 2025-12-31. `loloze` (Jeremy) awaits his pubkey.
>
> HARD RULES (unchanged): never run live; holdout sealed (reading it spends it; never a window past 2025-12-31; never copy `holdout_sealed/` to the server); every market-data experiment gets a research/TRIALS.csv row; no secrets; `origin` only, PRs to Jeremy (don't touch PR branches except on his feedback); no Co-Authored-By trailers.
>
> HOW I WANT YOU TO WORK (Dorian, standing): OMC teams for everything non-trivial. fable plans + gates + supervises; opus-4.8 orchestrates + attacks (red-team BLIND to the plan / code-review); sonnet-5 codes; ALL at 1M. Transcript-verify every lane. visual todo list first; plan → my nod → execute per branch; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution; byte-identity is a HARD gate for any production change (re-derive it independently — and where a change deliberately BREAKS it, declare the delta loudly with a control run); commit gate basedpyright + ruff on changed .py (delta, not total — pre-existing upstream noise is not a finding); message-only amend to fix a commit's refutable specifics (tree stays byte-identical); watch the zsh traps (unquoted `$var` doesn't word-split; heredoc + `&&` mangles commit messages — use `git commit -F <file>`; double `cd` fails — use absolute paths); keep Notion current as findings land (boards/bugs/epics; Decisions log for binding cross-boundary calls); update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md + its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second.
>
> Start with FIRST ACTIONS 1–2, tell me what you find, then plan the chosen task (fable) and get my nod before building.

---

## 2. State as of 2026-08-09

| | |
|---|---|
| Branch | `mac/setup` @ `d9c7d637` — run `git log` for actual HEAD |
| Upstream | `acfa5b63`; **PR #18 (E-012) OPEN, not merged** — verified on his base 302/16 green |
| This session | Synced #14–#17 (all merged by Jeremy) → `79bf2796`; E-012 built + verified (8 lanes) → merged `3059b196` + declaration `d9c7d637`; PR #18 opened + Slack-announced |
| Baseline | Trade-level anchor HOLDS `5ccbec42`/`5a75366c`/24/−23.021/−5.646; bar-level + `bar_equity_reference.json` rebaselined at 2026-08-09; **NO cross-boundary comparisons** of bar-level results |
| Server | culi.to LIVE; `loloze` awaits Jeremy's SSH key |
| Blocked on Jeremy | PR #18 review/merge; `loloze` SSH key; 9.5 dual-writer mechanics |
| Open fork tickets | ingest holdout guard (order 7), aux-feeds/campaign-exchange (orders 12/13), Branch 2 gate (needs prose-accrual decision), remove-venv/ (order 22), risk layer (order 23) |
| Next task | Dorian's pick — see §1 action 3 / §3 |

## 3. The queue (Fork-order top-first)

sync/close PR #18 as Jeremy merges → the exchange-plumbing Candidate bugs (aux-feeds order 12 + campaign-exchange order 13, gate kraken campaigns) → ingest holdout guard (order 7) → Branch 2 (holdout gate + pre-commit, needs the prose-accrual decision) → risk layer (order 23, live, never-live) → 9.5 dual-writer (Jeremy-gated) → the strategy generator (the edge hunt, once the environment is fully trusted — breadth/kraken campaigns are where the probability is).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | newest entry (E-012 ship) + CARRIED-FORWARD + the E-012 baseline-anchor update note |
| `FORK_CHANGES.md` | the 2026-08-09 E-012 loud declaration row |
| `.omc/plans/e012-two-bars-fix.md` + `.omc/plans/e012-evidence/` | the full E-012 plan + all lane evidence (Phase A / B-C / red-team / verifier) |
| E-012 board page (🐛) | Done / PR open |
