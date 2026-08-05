# Handoff → next Claude Code session (written 2026-08-05 afternoon, end of the decisions + E-012 S1 + leg-1 session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a code block for clean copy-paste. If you change §1 here, change it there.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, that is the include working and you should say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (start of the leg-2 session; written 2026-08-05 afternoon): mac/setup @ 5724a3f9 or later — run git log for the actual HEAD. The 08-05 session did, in order: sync-merged Jeremy's 4 docs-only commits (0962f4e9 — E-010/E-011 epics, E-003 provisional, PROCESS amendments; zero conflicts pre-registered; acceptance green: fast 213/0, slow 14-0-0, validator 0, simulate byte-identical); ast-grep MCP probe PASSED (napi pin 0.33.1 live — tool usable again, CLI stays primary); Dorian's decisions recorded and shipped (commit a233030c + two Slack messages): E-010 slippage spec RATIFIED AS-IS (S0 cleared — S1 is Jeremy's), two-bars FIX-FORWARD agreed (manifest fix separable; loop fix gated on the measurement), Option-A record CORRECTED everywhere (Jeremy HAD confirmed it 2026-08-03 as interim, recorded in E-011/EPIC.md, invisible fork-side; dual-writer is the agreed interim per his 08-04 Slack note, E-011 retires it later; MECHANICS still awaiting Jeremy on the Trial-Ledger page — ID scheme + authoritative-ledger host), four-rules process proposal parked for Dorian's separate reply; all pushed epics (E-001..E-011) mirrored VERBATIM into Notion 🧱 Engineering Epics behind "git is authoritative" banners (E-011 card was missing — created; Dorian's standing preference: epics fully readable in Notion like the bugs); E-012 S1 delta MEASURED AND TRIPLE-VERIFIED (probe 23aa31e6 on lab/e012-s1-probe, NEVER merged; evidence worktree in the prior session's scratchpad; full record = ledger 2026-08-05 (afternoon) entry + TRIALS T003/T004 + commit 5724a3f9; headline: the fix is THREE edits not two — advance() must park the cursor past the end; the delta is ZERO only on windows ending flat — a position-ending window moved sharpe −7.585→−7.018 because the dropped bars carried a genuine exit signal; no lookahead — causality guard + funding-boundary discriminating test; blast radius 10 tests incl. a vacuous-pass hazard on the close-positions guards; Jeremy has all numbers via Slack, fix design + threshold call are HIS); task C leg 1 (rider 8.7) CLEAN — cache-less fresh clone fast suite 196 passed / 17 skipped / 0 failures, all skips the designed guards, offline-safety proven under a known-answer-tested socket blocker. THREE new board tickets from the day: slow suite NOT offline-safe on a cache-less clone (9 tests fetch live Binance; fix folds into leg 5 — do NOT scope-creep it into leg 2); run-artifact git_sha has NO dirty detection (a manifest certifies a commit label, never the tree — demonstrated); get_historical_klines one-bar-lookahead compat shim (zero callers today). Baseline anchor unchanged: config 5ccbec42 / data 5a75366c / net −23.021% / sharpe −5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT (still carries the uniform last-two-bars truncation; the fix waits on Jeremy's design, E-012).
>
> FIRST ACTIONS, IN ORDER:
> 1. git fetch upstream && git log --oneline mac/setup..upstream/master. Jeremy is ACTIVE (E-013–E-019 Notion cards created 08-05 09:58Z; his local carries unpushed E-012–E-019 EPIC.md files, an evolved E-010, and the four-rules PROCESS.md amendment — his push was requested twice). If he pushed docs-only: light merge — merge never rebase, pre-register BOTH the conflict set AND the auto-merge set from a merge-tree dry run, full acceptance at the tip (fast+slow, validator, simulate byte-identity vs 5ccbec42/5a75366c). If CODE landed: full four-lane pattern, and every ledger file:line becomes a prediction to re-verify on the merged tree. After any merge that lands new EPIC.md files: mirror them into the Notion epics DB (same verbatim-behind-banner pattern as E-001..E-011).
> 2. Slack (tradingbot, C0BLW7V6BC6) AND the Notion 🐛 board: Jeremy's reaction to the two 08-05 messages (the decisions bundle; the E-012 S1 numbers). He communicates via Claude-sent Slack messages — READ THE CHANNEL, not just Notion (the 08-04 session missed two substantive answers by checking Notion only). Any answer on E-012 fix design, 9.5 mechanics, or A14 may re-sequence — report before proceeding.
> 3. No tool probes needed this session: ast-grep pin verified 08-05; LSP hybrid standing (ty 0.0.65 bridge for navigation, basedpyright 1.39.5 CLI as commit-gate arbiter; grep PRIMARY for enumeration; a stable lsp_find_references count is necessary, not sufficient).
>
> THE TASK — task C leg 2: fix/kraken-ingest-merge. PLAN APPROVED BY DORIAN 2026-08-05 (this exact scope — deviations need a fresh nod):
> 1. Branch fix/kraken-ingest-merge off mac/setup. Read `git show archive/2026-07-28/fix-fetch-end-bound` (the tag MESSAGE) FIRST — its own instruction — then identify the ingest-merge commit and cherry-pick ONLY that one. No bulk restore.
> 2. The defect (measured 2026-07-28, still present): tools/ingest_kraken_archive.py OVERWRITES the cache instead of merging — re-ingesting a 500-row cache left 10 rows; it passes no existing= so _assert_no_new_gap is dead on that path; _merge_and_store's comment claiming union is FALSE. Acceptance: re-ingest UNIONS with the existing cache and the gap guard is live on the ingest path.
> 3. Regression test WATCHED FAILING FIRST (the 500→10 reproduction as a test), then mutation-test at the PUBLIC entry point (run the actual tool, not internals) and mutation-test the fix's own direction (break union back toward overwrite — the test must die).
> 4. Lanes: opus executor in a provisioned scratchpad worktree; code-reviewer + red-team (data-path change → mandatory) on the session model; separate verifier before merge. Lane briefs name the LSP tools and the gate command.
> 5. Gates: fast+slow green, validator 0, simulate byte-identity on all five artifact files (the tool is off the simulate path — identity expected, prove it anyway), basedpyright CLI + .venv/bin/ruff on the changed .py files (a NEW diagnostic inside changed lines is a finding), a research/TRIALS.csv row for ANY run touching archive/market data, never commit new CSVs. Upstream-worthy → keep the branch clean for a PR; Dorian decides when it goes to Jeremy.
> QUEUED AFTER (per-branch plan → nod → execute): leg 3 = binance cache-dir hardcode (pre-merge prediction data_manager.py:768 — RE-DERIVE on the current tree before quoting; it makes Kraken caches unreachable); leg 4 = majors' 1d ingest from the 26 GB archive with per-file provenance (the 07-28 BTC pattern: re-ingest, compare to committed, explain every delta; TRIALS rows); leg 5 = ubuntu+windows fast-suite CI (fork-only file + FORK_CHANGES row; fold the slow-suite offline-safety fix here).
>
> WORKTREE PROVISIONING (inventory corrected 2026-08-05): copy BTCUSDT_{1h,1d,funding_8h}.csv + fear_greed_daily.csv into <wt>/trading-bot/local_data/ (the 19 kraken_*USD_1h.csv AND the 6 USDT-quoted AVAX/SOL caches are TRACKED and follow automatically); the 26 GB Kraken_batch/ archive does NOT follow and exists only on this machine — anything needing it runs in the MAIN repo or copies the specific file; symlink the main .venv at the worktree ROOT (never git add it); copy pyrightconfig.json; gate from worktrees = `basedpyright --venvpath <main-repo-path>`.
>
> HARD RULES (unchanged): never run live; the holdout is sealed (reading it spends it; never run a window past 2025-12-31; seven pre-contaminated Binance caches remain readable); every experiment touching market data gets a research/TRIALS.csv row; no secrets (the pre-commit scanner blocks even env-var NAMES in prose — reword, never bypass); origin only, never push to Jeremy; no Co-Authored-By trailers. Campaigns stay gated by the 9.5 mechanics + queue #7 verified on both machines — leg 2 is data groundwork, NOT campaign work.
>
> LESSONS THAT MUST SHAPE THIS SESSION (08-05 additions on top of the standing set): 1. Evidence must outlive the lane — persist artifacts BEFORE reporting; a lane still writing after it reports races its auditors. 2. `timeout` does not exist on macOS — exit 127 with no output reads exactly like a clean pass; never wrap commands in it. 3. Manifest git_sha has NO dirty detection — never cite a manifest as provenance for a tree that could have been dirty; re-run instead. 4. Window choice is part of measurement design — the reference window understated a real defect to ZERO; pick windows that exercise the failure mode. 5. Verify counts you relay — "26 kraken caches" was a miscount that survived a week (fresh clone measured 19 kraken + 6 USDT-quoted + README). Standing set: pre-register auto-merge sets, not just conflict sets; verbatim means verbatim; blind the enumeration lanes; the lead audits the auditor; results before decisions (present, END TURN, decide later); issue-first + red-team anything external; measure before arguing; mutation-test at the public entry point AND the fix's direction; content-blind tests are decoration; zero skips is the healthy state; commit messages reviewed like code; two-phase characterize-and-STOP; earlier numbers are predictions; fail loud, not flattering; provision caches into ANY environment that runs the engine.
>
> HOW I WANT YOU TO WORK: visual todo list first; plan → my nod → execute per branch (leg 2's plan is pre-approved above; legs 3-5 each need a fresh plan + nod); one change per branch, reviewed and green before the next; OMC lanes for anything non-trivial (executor lanes model=opus; code-reviewer/red-team/verifier on the session model; separate verifier before any merge); cheapest control that works; verify by execution — main.py simulate prints NOTHING, read the newest results/runs dir via stat -f '%m %N' results/runs/* | sort -rn | head -1, and restore the tracked results/trades.json after any reproducibility check; gate every commit with the basedpyright CLI + .venv/bin/ruff on the changed .py files; keep Notion current as findings land; update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md and its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second (the 08-05 morning/afternoon content is already on Slack in two messages; the wrap covers leg 2 onward).
>
> Start with FIRST ACTIONS 1-2 in order and tell me what you find — especially anything from Jeremy — before touching leg 2.

---

## 2. State as of 2026-08-05 (afternoon)

| | |
|---|---|
| Branch | `mac/setup` @ `5724a3f9`, pushed — run `git log` for the actual HEAD |
| Upstream | synced through `10b46a63` (docs-only); Jeremy's local is AHEAD again (E-012–E-019 epics, evolved E-010, four-rules PROCESS amendment — push requested) |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades (uniform 2-bar truncation stands; fix = Jeremy's E-012 design, fork measurement done) |
| Suites | fast 213/0, slow 14-0-0 at the merge tip; cache-less fresh clone 196/17/0 (leg 1 verified) |
| E-012 S1 | DONE fork-side: probe `23aa31e6` (never merged), triple-verified, TRIALS T003/T004, all numbers with Jeremy |
| Decisions | E-010 ratified as-is (S1 = Jeremy); two-bars fix-forward agreed; dual-writer = agreed interim (mechanics open); four rules = Dorian's separate reply pending |
| LSP / tools | hybrid unchanged (ty 0.0.65 bridge / bp 1.39.5 CLI gate); ast-grep MCP verified live (napi 0.33.1); ruff 0.15.10 in .venv; repo-wide bp floor 737/23 measured at 3fdb5b2c — re-measure before quoting |
| Venv | `../.venv/bin/python` from trading-bot/; no pip — use uv |

## 3. The queue

- ✅ #1–#6, 8.5/8.6 (characterized/done), leg 1 of task C. **Next: leg 2 `fix/kraken-ingest-merge` (plan pre-approved) → leg 3 binance hardcode → leg 4 majors' 1d ingest → leg 5 ubuntu+windows CI (+ slow-suite offline fix).**
- **9.5 dual-writer mechanics** — direction agreed by Jeremy; concrete mechanics (ID scheme, authoritative-ledger host) awaiting him; gates ALL campaigns with queue #7 (both machines). Not gating task C.
- **Blocked on Jeremy:** E-012 fix design (fork measurement delivered); A14 remedy; his push; 9.5 mechanics; venv untrack (E-006 — Dorian's yes is on record).
- **Blocked on Dorian:** four-rules reply (his separate review).
- New tickets 2026-08-05: slow-suite offline safety (→ leg 5), git_sha dirty detection, get_historical_klines shim. Parked by design: cleanup umbrella, compact/slash date forms, config-identity wiring, pre-commit holdout-gate wiring, record taxonomy (E-004, joint).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | the two 2026-08-05 entries (decisions + S1/leg-1 record) and CARRIED-FORWARD |
| `research/TRIALS.csv` | T003/T004 = the S1 measurement rows |
| 🐛 board + 🧱 epics DB | all tickets current as of 08-05; epics mirrored verbatim |
