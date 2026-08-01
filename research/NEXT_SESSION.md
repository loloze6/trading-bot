# Handoff → next Claude Code session (written 2026-07-31, end of the big-merge day)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a plain-text code block for clean copy-paste. If you change §1 here, change it there — that page is the one Dorian actually copies from.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md now @-includes CLAUDE.fork.md (added 2026-07-31, first session start since) — if the fork guardrails already appear in your context, that is the include working and you should say so; if not, the include failed: read the file explicitly and report it. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (end of 2026-07-31, a two-part day): Jeremy MERGED PRs #1-#3 (upstream 63237b88); we synced (merge 290ed4fb) and opened FIVE offers on his repo: #4 seal-regex flanks, #5 fixture revival, #6 validator effective default_regime, #7 bar-equity, #8 end-of-backtest close fix. The fork queue #1-#6 is DONE: the research workflow is RUNNABLE on this Mac (fix/workflow-macos-port merged 33c6fbe9 — per-file interpreter resolvers with an executable-regular-file predicate against the COMMITTED Windows venv, static call-site guards, fork-only strategy-research/requirements-mac.txt pinning claude-agent-sdk==0.2.82 + google-genai==2.16.0; importing run_phase1_research needs the Gemini key env var to EXIST — see the requirements file's comment) and the end-of-backtest close records honestly on failure paths (fix/close-positions-nameerror merged 1c84ba0e). Suites: fast 195 passed / 0 SKIPPED, slow 14 passed / 0 skipped / 0 errors. Baseline anchor unchanged: config_sha 5ccbec42 / data_sha 5a75366c / net -23.021% / sharpe -5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT. Branch mac/setup @ 418272e5 or later — run git log for the actual HEAD.
>
> SESSION-START CHECKS (any may preempt the plan — tell me before proceeding):
> 1. gh pr view N --repo loloze6/trading-bot for N=4,5,6,7,8. If any merged, follow-ups unblock: after #4 — the compact/slash/dotted date-forms ticket (Medium) touches the same seal-test file and was deliberately held to avoid tangling his review; after all five — the workflow-resolver upstream offer (FORK_CHANGES row 22; its PR text must carry the latent wrong-CWD limitation and the POSIX scoping of the subprocess mechanism). Never push to his repo; PRs only.
> 2. git fetch upstream && git log --oneline mac/setup..upstream/master. W8→W15 were STILL UNPUSHED at 07-31 EOD, and Jeremy's local master is DIVERGED from his own GitHub (he merged our PRs server-side) — he must pull before pushing; we flagged it in PR #4, the HQ banner and Slack. If he pushed, a sync merge (git merge upstream/master — merge, never rebase) comes FIRST and any conflict resolution gets a pre-registered per-file map like 290ed4fb's.
> 3. Notion: Trading Bot HQ banner, Mac Fork — Home, and the Trial-Ledger page. If Jeremy confirmed Option A (single-writer), write the one-sentence rule into the Working Agreement page AND CLAUDE.fork.md — still-queued action. Also check for his claude-agent-sdk / google-genai versions (ours: 0.2.82 / 2.16.0, genai pinned-at-install — realign if his differ) and any reaction to the slippage spec.
>
> THE TASK — two candidates, recommended in this order; propose a 3-6 bullet plan and get my nod BEFORE code:
> A (small opener, high information): TRACE THE LAST-TWO-BARS TICKET — measured 07-31: every backtest's last PROCESSED bar is <end> 21:00; the last two FETCHED bars are never traded; systematic across all probed windows; fetch path exonerated (BaseFetcher._inclusive_end keeps the 23:00 bar); cause untraced in the candle-completion loop; may be intentional. Outcome is either "intentional, documented where" (close the ticket with the citation) or a real off-by-one/two (own fix branch — LOUDLY declare the bit-identity implications first: fixing it would change every backtest's output and invalidate all baselines, so the finding comes to me before any fix).
> B (main): QUEUE #9 — ingest Kraken daily bars, enabling the 1d slow-diversified-trend lane from the Edge Playbook. GATE FIRST: tools/ingest_kraken_archive.py OVERWRITES the cache instead of merging (measured 2026-07-28: 500 rows → 10; passes no existing=, so _assert_no_new_gap is dead there) — fix that on its own branch before ANY ingest run; candidate fixes exist in archive/2026-07-28/fix-fetch-end-bound (cherry-pick deliberately, one at a time, reviewed — never bulk-restore). Then ingest majors' 1d bars from the 26 GB local archive with per-file provenance checks like the 07-28 BTC reproduction. Never commit new CSVs.
>
> HARD RULES (unchanged): never run live; the holdout is sealed (local_data/holdout_sealed/2026_H1/ — reading it spends it; seven pre-contaminated Binance caches remain readable, so never run a window past 2025-12-31 — and remember the engine's own truncation: the last processed bar is <end> 21:00); every experiment touching market data gets a research/TRIALS.csv row; no secrets (the pre-commit scanner blocks even the Gemini env-var NAME in a diff — reword prose, never bypass the hook); origin only; no Co-Authored-By trailers.
> RUNNABLE ≠ RUN: strategy-research/workflow imports and resolves on this Mac now, but campaigns execute ONLY on Jeremy's machine under trial-ledger Option A, and the queue #7 killed-run accounting gate (run_campaign.py — a KILLED run must still land a row in campaign_state.trial_sharpes) is UNVERIFIED. Do not execute campaigns, ever, without Dorian's explicit direction.
>
> LESSONS THAT MUST SHAPE THIS SESSION (07-31 additions on top of the standing set — details in the ledger):
> 1. CONNECT KNOWN FACTS TO NEW DESIGNS: the committed 449-file Windows venv falsified a pre-registered resolver predicate; the falsifying fact was ALREADY IN THE LEDGER's environment traps. Phase A of any design must be checked against the ledger's traps explicitly.
> 2. ONE CONSOLIDATED REVIEW ROUND-TRIP: collect BOTH review lanes' findings before re-dispatching an executor, and lanes re-check their inbox before implementing — a crossed directive cost a full round.
> 3. CONTENT-BLIND TESTS ARE DECORATION: assert what a record CONTAINS (sign included) and pin conventions (the None sentinel) — a sign-flipping regression passed an existence-only suite 5/5.
> 4. ZERO SKIPS IS THE HEALTHY STATE, fast AND slow: two lanes independently shipped generated-then-skipped test cases and were made to remove them; an empty parametrize collects zero and reads green — assert your filters are non-empty.
> 5. Standing: commit messages reviewed like code (the verifier's audit hit ZERO refutations for the first time — keep it that way); two-phase characterize-and-STOP; earlier numbers are predictions; fail loud, not flattering; lane pattern with executor=opus, code-reviewer/red-team/verifier on the session model; worktrees in the scratchpad with gitignored caches COPIED never symlinked — and provision caches into ANY environment that runs the engine (a reviewer's self-built scratch clone quietly fetched from Binance's public endpoint when its cache was missing).
>
> HOW I WANT YOU TO WORK: plan in 3-6 bullets and get my nod BEFORE code; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution — main.py simulate prints NOTHING, read the newest results/runs/ dir via: stat -f '%m %N' results/runs/* | sort -rn | head -1; mutation-test new tests at the PUBLIC entry point and mutation-test the fix itself; keep Notion updated as findings land (board: "Dorian's fork" column + the Detail lead-note convention; the full lifecycle value is "Merged upstream"); update research/LEDGER.md before session end; post the wrap to Slack (tradingbot channel, C0BLW7V6BC6) in plain human language first, numbers second.
>
> Start by confirming the environment (git state; fast+slow suites — expect 195 / 14-0-0) and the three session-start checks, and tell me what you find.

---

## 1b. Separate add-on prompt — Python LSP setup + usage (paste on its own, any session)

> LSP SETUP + USAGE (one-off, ~30-45 min; independent of the main task — it changes HOW we work, not WHAT we build). If the fork guardrails didn't auto-load, read CLAUDE.fork.md first.
>
> GOAL: give this Mac a Python language server that OMC's LSP bridge (lsp_servers, lsp_diagnostics, lsp_hover, lsp_goto_definition, lsp_find_references, lsp_rename) can talk to, wire it to the REAL venv so imports resolve, and make LSP usage part of the standing development pattern for the main session AND every OMC lane — an installed-and-forgotten tool is a failure here. Installing basedpyright is pre-approved by this prompt; anything else still needs my explicit yes.
>
> STEPS:
> 1. Install: `uv tool install basedpyright` (uv is the house tool; `.venv` has no pip; basedpyright is self-contained — no npm needed). Verify it is on PATH.
> 2. Config at repo root, `pyrightconfig.json`: `{"venvPath": ".", "venv": ".venv", "pythonVersion": "3.13", "typeCheckingMode": "basic"}`. The venv wiring is the step that actually matters — without it every import of pandas/ccxt/claude_agent_sdk/google.genai reads as unresolved and diagnostics are noise. Basic mode is deliberate: upstream code is not typed to strict standards, and strict would invite exactly the drive-by "fixes" the mergeable-fork rule forbids. DECISION FOR ME BEFORE ACTING: leave the file untracked, or gitignore it with a FORK_CHANGES row (the `.omc/` row-9 precedent). Recommend gitignore + row, so a stray `git add -A` can never ride it toward Jeremy.
> 3. Tell me to restart Claude Code (the plugin re-detects servers at session start). After restart, verify BY EXECUTION: `lsp_servers` lists the server; `lsp_diagnostics` on `trading-bot/performance/bar_equity.py` returns with venv imports RESOLVING (if pandas shows unresolved, the venv wiring failed — fix before claiming anything); hover/goto_definition on a known symbol works.
> 4. ACCEPTANCE IS USAGE, NOT INSTALLATION — codify in CLAUDE.fork.md's operating protocol (3-4 lines, no more): (a) before any commit, `lsp_diagnostics` on the changed .py files alongside ruff — a NEW diagnostic inside changed lines is a finding, pre-existing upstream noise is not; (b) any rename or signature change runs `lsp_find_references` FIRST and the reference list goes into the plan; (c) Phase A characterization uses goto_definition/hover/references as the primary navigation, grep as the fallback; (d) executor-lane worktree provisioning COPIES `pyrightconfig.json` in alongside the data CSVs (untracked files don't follow worktrees), and lane briefs name the LSP tools so executors actually reach for them.
> 5. Sanity probe both directions, in the SCRATCHPAD never the tree: a scratch file importing a nonexistent name from `core.trading_bot` must produce a diagnostic; a clean file must not. Same discipline as every guard we ship — prove it fires AND prove it stays quiet.
> 6. Wrap: 2-3 line ledger entry; FORK_CHANGES row if the gitignore divergence was chosen; one line on Mac Fork — Home. No Slack needed for tooling.
>
> WORTH PROPOSING WHILE AT IT (propose, don't do — each needs my explicit yes; all three are the same spirit: cheap guards that make claims reproducible):
> (a) Pin dev tools — the venv has no ruff, so yesterday's verifier could not reproduce a ruff finding count because tool versions float; a pinned dev-tools section (ruff==X, basedpyright==Y) in `strategy-research/requirements-mac.txt` makes lint claims reproducible.
> (b) The unqueued CI ticket — a GitHub Actions fast-suite run on the FORK would have caught the seal guard being dead on Windows (cp1252) months earlier; fork-only workflow file, divergence row, Jeremy invited to adopt.
> (c) Wire `holdout_date_gate.sh` into pre-commit (existing unqueued ticket).
>
> HARD RULES apply unchanged: never run live; holdout sealed, no window past 2025-12-31; no secrets (the pre-commit scanner blocks even env-var NAMES in diffs — reword prose, never bypass); origin only; no Co-Authored-By.

---

## 2. State as of 2026-07-31 (end of day)

| | |
|---|---|
| Branch | `mac/setup` @ `418272e5`, pushed — run `git log` for the actual HEAD |
| Upstream | `63237b88` (= `70dab378` + our PRs #1-#3, merged by Jeremy server-side); his local W8→W15 still unpushed, his local master DIVERGED from his GitHub |
| Open PRs | **#4 #5 #6 #7 #8**, all ours, all against `63237b88` |
| Fast suite | 195 passed / **0 skipped** |
| Slow suite | 14 passed / 0 skipped |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades — byte-identical at the merge tip (`33c6fbe9` in the fresh manifest) |
| Workflow | RUNNABLE on this Mac (import + resolver smokes green); campaigns Jeremy-side only (Option A, his confirmation pending) |
| Deps | `.venv` + `strategy-research/requirements-mac.txt`: claude-agent-sdk==0.2.82, google-genai==2.16.0; trading-bot pins untouched |
| Venv | `trading-bot-dorian/.venv` → `../.venv/bin/python` from `trading-bot/`; no pip — use uv |

## 3. The queue after this day

- ✅ #1-#6 all done (holdout safety, seal regex, fixture, bar-equity, workflow port; slippage → Jeremy).
- **#7 verify trial accounting** — Jeremy's machine under Option A; blocked on him.
- **#9 Kraken daily ingest** — next fork-side main task (candidate B above), gated on the ingest-overwrite fix.
- **#10 risk layer** — before real money, not before research.
- New Medium tickets: **last-two-bars truncation** (candidate A above); compact/slash date forms (after PR #4 merges); config-identity wiring gap.
- **PR #8 candidate shipped** — it's a real PR now.

## 4. Known-broken / deferred (tracked on the board)

- Seven Binance caches carry sealed rows — never run a window past 2025-12-31.
- Backtests never trade the last two fetched bars (<end> 21:00; cause untraced — candidate A).
- The close fix leans on None-falsiness at three ternaries; dead `hasattr` tracker guard; the blanket per-symbol `except Exception` still converts future defects into silent artifact truncation; close row duplicates the final bar timestamp (all pre-existing, report-only, in the 07-31 evening ledger entry).
- `main.py simulate` rewrites tracked `results/trades.json` — restore with `git checkout --` after reproducibility checks.
- Recorder PowerShell supervisor port — still unscoped, out of every past scope.
- `holdout_date_gate.sh` PATTERN hardcoded; pre-commit wiring unwired (unqueued).

## 5. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, backlog with #1-#6 done; auto-included from CLAUDE.md since 2026-07-31 — verify it loaded |
| `research/LEDGER.md` | the 2026-07-31 entries (three that day) are the important ones: the merge day, the PR batch, the port + close fix |
| `FORK_CHANGES.md` | rows 22-23: what still diverges and what's offered upstream |
| `strategy-research/requirements-mac.txt` | the dependency story incl. the Gemini env-var note |
| `tools/ingest_kraken_archive.py` | candidate B's gate — the overwrite bug |

Notion — "Trading Bot HQ": 🐛 Bugs & Tasks → **🍎 Fork queue (in order)**; rows 1-6 read done, PRs #4-#8 read `Done + PR open`, merged PR #1-#3 rows read `Merged upstream`. The ✉️ response note, 🎯 slippage spec and 🔢 Trial-Ledger page are under Trading Bot HQ.
