# Handoff → next Claude Code session (written 2026-08-03, end of the LSP + type-sweep day)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a plain-text code block for clean copy-paste. If you change §1 here, change it there — that page is the one Dorian actually copies from.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, that is the include working and you should say so; if not, the include failed: read the file explicitly and report it. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (end of 2026-08-03): mac/setup @ 069d0331 or later — run git log for the actual HEAD. Fork queue #1-#6 DONE; five PRs (#4-#8) open on Jeremy's repo, all against 63237b88. Suites: fast 195 passed / 0 skipped, slow 14 passed / 0 skipped / 0 errors. Baseline anchor unchanged: config_sha 5ccbec42 / data_sha 5a75366c / net -23.021% / sharpe -5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT.
>
> NEW SINCE 07-31 (the 2026-08-03 LSP + type-sweep day; full numbers in the ledger's three 08-03 entries):
> 1. LSP IS STANDING EQUIPMENT AND MUST BE USED, hybrid decided by measurement. NAVIGATION = ty 0.0.65 (pinned via uv) on OMC's native lsp_* bridge — lsp_goto_definition / lsp_hover / lsp_find_references are the PRIMARY navigation in any Phase A; grep is the fallback. COMMIT GATE ARBITER = basedpyright 1.39.5 CLI, reading the untracked pyrightconfig.json (venv .venv, basic mode, extraPaths [strategy-research, strategy-research/tools]) — run it with ruff on the changed .py files before EVERY commit; a NEW diagnostic inside changed lines is a finding, pre-existing noise is not; bridge diagnostics are advisory. Any rename or signature change runs lsp_find_references FIRST and the list goes into the plan — RE-RUN UNTIL THE COUNT IS STABLE (a cold index under-reports silently; measured 3-of-13). Known floors, always quoted with tool+version: basedpyright — bar_equity.py 1, trading_bot.py 33, repo-wide 408; ty — 0, 32, 289.
> 2. OMC IS STOCK — the temporary registry patch is REVERTED (verified byte-identical to stock). The basedpyright PR to OMC was closed by its owner (ty-only is intentional; their issue 3624 stays open as a design question); 7hr1LL/oh-my-claudecode is archive-only. If lsp_* ever reports no Python server, ty fell off PATH — reinstall ty; do NOT patch OMC.
> 3. ORCHESTRATION PER THE STANDING AGREEMENT — non-trivial work runs through OMC lanes, not inline: executor lanes spawn with model=opus; code-reviewer / red-team / verifier stay on the session model (the adversarial layers are where the catches happen); a separate verifier passes before any merge; worktrees live in the scratchpad with gitignored caches AND pyrightconfig.json COPIED in (untracked files don't follow worktrees); lane briefs name the LSP tools and the gate command so executors actually use them.
> 4. THE TYPE SWEEP IS TRIAGED — do not re-derive it: the one real defect found is queue 8.5 (task A below). Benign verdicts are recorded on the parked cleanup ticket (quoted CompletedTrade annotations — runtime-safe BECAUSE quoted; metrics comma-chain extends — execute fine; main_strategy.py:81 override smell; NaT floor/ceil stub noise). The ~370 possibly-None findings (backtester 62, portfolio_info 55, trading_bot 33) are fix/live-wiring triage material, later.
>
> SESSION-START CHECKS (any may preempt the plan — tell me before proceeding):
> 1. gh pr view N --repo loloze6/trading-bot for N=4,5,6,7,8. If any merged: after #4 the compact/slash date-forms ticket unblocks; after all five, the workflow-resolver offer (FORK_CHANGES row 22 — its PR text must carry the wrong-CWD limitation and the POSIX scoping). Never push to his repo; PRs only.
> 2. git fetch upstream && git log --oneline mac/setup..upstream/master. W8-W15 were still unpushed at 08-03 and Jeremy's local master is DIVERGED from his own GitHub. If he pushed, a sync merge comes FIRST (merge, never rebase) with a pre-registered per-file conflict map like 290ed4fb's.
> 3. Notion: HQ banner, Mac Fork — Home, and the Trial-Ledger page. If Jeremy confirmed Option A, write the single-writer sentence into the Working Agreement page AND CLAUDE.fork.md — still queued. Check his claude-agent-sdk / google-genai versions (ours 0.2.82 / 2.16.0) and any slippage-spec reaction.
>
> THE TASK — in order, one branch each; plan in 3-6 bullets and get my nod BEFORE code:
> A (queue 8.5, opener): CHARACTERIZE THE CANDLE-CALLBACK CHAIN — the board ticket carries fully validated evidence (2026-08-03): CandleBuilder calls callback(symbol) — ONE arg — at data_manager.py:267, but the default wiring installs the TWO-arg _enrich_and_notify (:436/:493), so the default chain TypeErrors on every candle close, swallowed by the blanket except; _strategy_callback is NEVER set (neither launcher ctor passes the kwarg — verified :145-149 and :204-209); shipped paths work only because launcher.py:230 / backtester.py:159 clobber the builder callback with the 1-arg bot method; aux enrichment actually happens at READ time (get_data_history → _attach_aux_columns; backtest premerge at initialize) so the :21/:432/:497 docs describe a design the code doesn't implement; test_funding_rate_component.py:165 already bypasses the broken default. Phase A: characterize, choose between deleting the dead layer (cheapest control) vs implementing the documented design, then STOP for my nod. Bit-identity mandatory either way — this is per-bar hot-path code. ISSUE-FIRST with Jeremy before any upstream offer: his unpushed W8-W15 touched register_feed and may rework this area.
> B: TRACE THE LAST-TWO-BARS TICKET — last processed bar is <end> 21:00, systematic across all probed windows; fetch path exonerated; cause untraced in the candle-completion loop; may be intentional. Outcome: "intentional, documented where" (close with the citation) or a real off-by-one/two — the finding comes to me BEFORE any fix, because a fix invalidates every baseline.
> C (main, queue #9): KRAKEN DAILY INGEST — GATE FIRST: tools/ingest_kraken_archive.py OVERWRITES the cache instead of merging (measured 2026-07-28: 500 rows → 10; passes no existing=, so _assert_no_new_gap is dead there) — fix on its own branch first (candidates in archive/2026-07-28/fix-fetch-end-bound; cherry-pick one at a time, reviewed). Absorb data_manager.py:768's hardcoded binance cache dir into this work (it makes Kraken caches unreachable). Then ingest majors' 1d bars from the 26 GB archive with per-file provenance checks (the 07-28 BTC reproduction pattern). Never commit new CSVs; every run touching market data gets a research/TRIALS.csv row.
> Opportunistic riders, already approved via the board: 8.6 dev-tool pins (ruff==0.15.10 into .venv — .venv has NO ruff today, homebrew's copy was the 07-31 verifier's non-repro cause; record the uv pins basedpyright 1.39.5 / ty 0.0.65 and the deliberate-upgrade rule). 8.7 fork CI — FIRST verify the fast suite is green on a cache-less fresh clone (currently UNVERIFIED), then the ubuntu+windows fast-suite workflow (fork-only file + FORK_CHANGES row; ubuntu continuously proves the agreed Linux deploy target).
>
> HARD RULES (unchanged): never run live; the holdout is sealed (reading it spends it; seven pre-contaminated Binance caches remain readable — never run a window past 2025-12-31; and remember the engine's own truncation: last processed bar is <end> 21:00); every experiment touching market data gets a research/TRIALS.csv row; no secrets (the pre-commit scanner blocks even env-var NAMES in diffs — reword prose, never bypass the hook); origin only, never push to Jeremy; no Co-Authored-By trailers.
> RUNNABLE does NOT mean RUN: campaigns execute ONLY on Jeremy's machine under trial-ledger Option A, and the queue #7 killed-run accounting gate is UNVERIFIED. Never execute campaigns without Dorian's explicit direction.
>
> LESSONS THAT MUST SHAPE THIS SESSION (08-03 additions on top of the 07-31 standing set — details in the ledger):
> 1. RESULTS BEFORE DECISIONS: when work produces results Dorian asked to see, present them and END THE TURN — the decision prompt comes in a LATER turn, never in the same message (his explicit instruction, 2026-08-03).
> 2. ISSUE-FIRST + RED-TEAM ANYTHING EXTERNAL: adversarially pre-review every external-facing PR before opening it, and ask one question first when the change might touch an intentional design decision — the OMC PR died on a deliberate design choice one issue-question would have surfaced, and both bot review findings were foreseeable by our own standing lessons.
> 3. MEASURE BEFORE ARGUING: two of three stated concerns against ty died on contact with measurement; when a comparison is cheap, run it instead of defending the recommendation.
> 4. Standing (07-31): connect known facts to new designs; one consolidated review round-trip; content-blind tests are decoration; zero skips is the healthy state; commit messages reviewed like code; two-phase characterize-and-STOP; earlier numbers are predictions; fail loud, not flattering; provision caches into ANY environment that runs the engine.
>
> HOW I WANT YOU TO WORK: visual todo list first; plan → my nod → execute; one change per branch, reviewed and green before the next; OMC lanes per NEW-SINCE item 3 for anything non-trivial; cheapest control that works; verify by execution — main.py simulate prints NOTHING, read the newest results/runs/ dir via stat -f '%m %N' results/runs/* | sort -rn | head -1; gate every commit with the basedpyright CLI + ruff on the changed files; lsp_find_references before any rename, re-run until stable; mutation-test new tests at the PUBLIC entry point and mutation-test the fix itself; keep Notion current as findings land (board Detail lead-note convention); update research/LEDGER.md before session end; post the wrap to Slack (tradingbot channel, C0BLW7V6BC6) in plain human language first, numbers second.
>
> Start by confirming the environment (git state; fast+slow suites — expect 195 / 14-0-0; lsp_servers lists ty for .py; basedpyright floors bar_equity 1 / trading_bot 33) and the three session-start checks, and tell me what you find.

---

## 1b. LSP add-on prompt — COMPLETED 2026-08-03, superseded

The former §1b (basedpyright setup) ran on 2026-08-03 and evolved past its own plan: OMC's bridge turned out to hardcode ty, a head-to-head measurement (ledger, 08-03 entries) decided a HYBRID — ty 0.0.65 on the bridge for navigation, basedpyright 1.39.5 CLI as the commit-gate arbiter via pyrightconfig.json. The usage protocol lives in CLAUDE.fork.md's operating protocol; the upstream basedpyright offer was closed by the OMC owner (archive: 7hr1LL/oh-my-claudecode). Nothing left to run from here.

---

## 2. State as of 2026-08-03 (end of day)

| | |
|---|---|
| Branch | `mac/setup` @ `069d0331`, pushed — run `git log` for the actual HEAD |
| Upstream | `63237b88`; his local W8-W15 still unpushed, his local master DIVERGED from his GitHub |
| Open PRs | **#4 #5 #6 #7 #8**, all ours, all against `63237b88` — status unchecked since 07-31 |
| Fast suite | 195 passed / 0 skipped |
| Slow suite | 14 passed / 0 skipped |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades |
| LSP | HYBRID: ty 0.0.65 (uv) on OMC's stock lsp_* bridge; basedpyright 1.39.5 (uv) = commit-gate arbiter via untracked `pyrightconfig.json` (extraPaths added 08-03). Floors: bp 1/33/408, ty 0/32/289 |
| OMC | STOCK, zero divergence; `7hr1LL/oh-my-claudecode` archive-only |
| Workflow | RUNNABLE on this Mac; campaigns Jeremy-side only (Option A, confirmation pending) |
| Venv | `trading-bot-dorian/.venv` → `../.venv/bin/python` from `trading-bot/`; no pip — use uv; **no ruff in .venv** (ticket 8.6) |

## 3. The queue

- ✅ #1-#6 done. **8.5** candle-callback characterization (task A) → **8.6** dev-tool pins → **8.7** fork CI leg → last-two-bars trace (task B) → **#9** Kraken daily ingest (task C).
- **#7 verify trial accounting** — Jeremy's machine under Option A; blocked on him.
- **#10 risk layer** — before real money, not before research.
- Parked by design (blank Fork order): cleanup umbrella ticket (type-hygiene batch with recorded verdicts), compact/slash date forms (after PR #4), config-identity wiring gap, pre-commit holdout-gate wiring.

## 4. Known-broken / deferred (tracked on the board)

- Seven Binance caches carry sealed rows — never run a window past 2025-12-31.
- Backtests never trade the last two fetched bars (task B; cause untraced).
- Candle-callback default chain arity-broken/dead (task A; shipped paths unaffected — verified).
- `main.py simulate` rewrites tracked `results/trades.json` — restore with `git checkout --` after reproducibility checks.
- Close-fix report-only flags (07-31 evening ledger entry); Recorder PowerShell supervisor port unscoped; `holdout_date_gate.sh` PATTERN hardcoded + pre-commit unwired.

## 5. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, LSP+lane protocol (updated 08-03); auto-included from CLAUDE.md — verify it loaded |
| `research/LEDGER.md` | the three 08-03 entries (LSP setup, hybrid decision, type sweep) + the 07-31 entries |
| `FORK_CHANGES.md` | rows 22-24: current divergences incl. the pyrightconfig gitignore |
| `pyrightconfig.json` (untracked) | the gate's config — copy into any worktree that runs the gate |
| 🐛 board tickets 8.5 / 8.6 / 8.7 | full validated evidence + scopes for the next tasks |

Notion — "Trading Bot HQ": 🐛 Bugs & Tasks → **🍎 Fork queue (in order)**. The ✉️ response note, 🎯 slippage spec and 🔢 Trial-Ledger page are under Trading Bot HQ.
