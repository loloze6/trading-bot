# Handoff → next Claude Code session (written 2026-08-03 late, end of the unification + double-characterization day)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a code block for clean copy-paste. If you change §1 here, change it there.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, that is the include working and you should say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (end of 2026-08-03, the unification + double-characterization day): mac/setup @ dab115ca or later — run git log for the actual HEAD. THE FORKS ARE UNIFIED: Jeremy merged all 8 fork PRs and cherry-picked the macOS port; we sync-merged his 33ac7ec4 back (8b9a5f72 + 3f6d8bf1; 3 conflicts, all pre-registered; byte-identity proven twice independently; four-lane pattern, zero refuted claims). Suites at tip: fast 213 passed / 0 skipped, slow 14 / 0 / 0. Baseline anchor unchanged: config 5ccbec42 / data 5a75366c / net −23.021% / sharpe −5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT. Know one new thing about it: EVERY artifact (this one included) carries the uniform last-two-bars truncation — bars.csv 1438 rows vs manifest 1440; internally comparable, individually overstated (finding 2 below).
>
> TWO CHARACTERIZATIONS COMPLETED 08-03 EVENING, BOTH VERDICTS DELIVERED, NEITHER FIXED (deliberate — fixes rebaseline everything and remedy ownership is Jeremy's; tickets assigned to Jeremy+Dorian for decision):
> 1. CANDLE-CALLBACK (queue 8.5, Phase A, ralplan consensus + 4 blinded lanes, ledger 08-03 night entry): the enrichment layer is INERT SINCE BIRTH (_strategy_callback never settable, _enrich_and_notify's body does no enrichment, 14,509-close census with 0 default fires) and the arity trap is a REGRESSION — at ac277917^ the builder called callback(symbol, completed_candle), 2-arg WORKING code; the restructure commit narrowed it to (symbol). Jeremy's own A14 triage has a false justification but true conclusion. Board ticket "A14 revisited" carries evidence, his 3 verification commands, and the recommendation (R4 as RESTORATION of his own pre-restructure design). DECISIONS PENDING: Jeremy's remedy choice, Dorian's stance.
> 2. LAST-TWO-BARS (task B, ledger 08-03 late entry): REAL, UNDOCUMENTED DEFECT — two additive off-by-ones: has_more_data's `- 1` (data_manager.py:816) never feeds the final loaded row; completion-requires-a-later-row (:355/:364) orphans the last fed candle (get_final_candle, built for exactly that leftover, has zero callers). AND the manifest over-reports BY CONSTRUCTION (run_artifact reads the LOADED frame — bar_count/data.end describe loaded rows, never replayed bars). 41/46 of Jeremy's archived runs show delta exactly 2; 46/46 end at 21:00. DECISION PENDING: joint fix conversation. NO fix branch until Dorian + Jeremy agree — any fix invalidates every baseline on both sides.
>
> STANDING EQUIPMENT (LSP hybrid unchanged + three updates):
> - LSP hybrid: ty 0.0.65 on OMC's lsp_* bridge for navigation; basedpyright 1.39.5 CLI is the commit-gate arbiter (untracked pyrightconfig.json; from worktrees run `basedpyright --venvpath <main repo>` or symlink .venv, else phantom missing-imports). PROTOCOL UPGRADE, measured 3×: a STABLE lsp_find_references count is NECESSARY, NOT SUFFICIENT — grep cross-check before acting on any reference list; for ENUMERATION tasks grep is PRIMARY and LSP the cross-check (architect-adjudicated inversion, navigation ≠ enumeration — not protocol drift).
> - ast_grep MCP tool: FIXED ON DISK — @ast-grep/napi installed at ~/.claude/node_modules (the bridge resolves createRequire-anchored from its own path; `npm install -g` does NOT work despite the tool's own error message). The previous session's server had the failure cached — VERIFY THE TOOL WORKS early this session and note the result.
> - ruff==0.15.10 now IN .venv (queue 8.6 done); uv pins basedpyright 1.39.5 / ty 0.0.65; deliberate-upgrade rule stands.
> - Worktree provisioning (corrected): copyable caches are BTCUSDT_{1h,1d,funding_8h}.csv + fear_greed_daily.csv ONLY (no ETHUSDT caches exist; the rest is tracked and follows); symlink the main .venv at the worktree root (3 strategy-research tests resolve interpreters through it); never `git add` there.
>
> SESSION-START CHECKS (any may preempt the plan — tell me before proceeding):
> 1. git fetch upstream && git log --oneline mac/setup..upstream/master. Jeremy is ACTIVE. Expected pushes: his `git rm -r --cached venv/` (Dorian said yes on the HQ banner — after it lands, our resolver-test docstring premise needs a wording touch), possibly the parked ~190-file strategy-research restructure (he will send NOTICE first — if it landed, PULL BEFORE ANY AGENT WORK, every path breaks otherwise). If he pushed anything: sync merge FIRST (merge, never rebase) and pre-register BOTH the conflict set AND the auto-merge set of fork-footprint files (the 08-03 process lesson — silent loss lives in auto-merges).
> 2. Notion 🐛 board: did Jeremy answer the two DECISION tickets (A14-revisited; last-two-bars — both assigned to him + Dorian), or measure_bar_sigma / r2-test-vector / numpy-deprecation / the two hazard tickets (all assigned to him)? And: his reaction to the DUAL-WRITER change + the merge-protocol ticket (Fork order 9.5, assigned to him + Dorian — this REPLACES the old Option A confirmation ask), and the slippage-spec reaction. Any answer re-sequences the session.
> 3. HQ banner + Mac Fork — Home for anything Jeremy posted.
>
> THE TASK (default if nothing preempts) — task C, queue #9: KRAKEN DAILY INGEST. GATE FIRST: tools/ingest_kraken_archive.py OVERWRITES the cache instead of merging (measured 2026-07-28: 500 rows → 10; passes no existing=, so _assert_no_new_gap is dead there) — fix on its own branch first (candidates in archive/2026-07-28/fix-fetch-end-bound; cherry-pick one at a time, reviewed). Absorb data_manager.py:768's hardcoded binance cache dir into this work (it makes Kraken caches unreachable — re-verify the line number on the merged tree before quoting it). Then ingest majors' 1d bars from the 26 GB archive with per-file provenance checks (the 07-28 BTC reproduction pattern: re-ingest, compare to committed, explain every delta). Never commit new CSVs; every run touching market data gets a research/TRIALS.csv row. RIDER 8.7 (approved): FIRST verify the fast suite is green on a cache-less fresh clone (Jeremy's 0fd9a3e4 made the close-regression tests SKIP without caches, so the unverified surface shrank but is still unverified), then the ubuntu+windows fast-suite workflow (fork-only file + FORK_CHANGES row).
>
> HARD RULES (unchanged): never run live; the holdout is sealed (reading it spends it; seven pre-contaminated Binance caches remain readable — never run a window past 2025-12-31; the engine's own truncation is now EXPLAINED, not mysterious: last processed bar = <end> 21:00, two off-by-ones, ticket has the mechanism); every experiment touching market data gets a research/TRIALS.csv row; no secrets (the pre-commit scanner blocks even env-var NAMES in diffs — reword prose, never bypass); origin only, never push to Jeremy; no Co-Authored-By trailers.
> DUAL-WRITER RESEARCH (Dorian's call, 2026-08-04 — supersedes Option A, which Jeremy never confirmed, nothing to unwind): BOTH Dorian and Jeremy run experiments and strategy campaigns — finding profitable strategies on this Mac is the whole point; long-term the loop deploys to an Ubuntu server for refinement. TWO GATES before ANY campaign runs on this Mac: (1) the trial-ledger dual-writer merge protocol agreed with Jeremy AND implemented (board ticket, Fork order 9.5: disjoint trial IDs, mandatory forecast_hash, append-only union merge, mechanical duplicate-ID refusal in deflate_sharpe.py, and NO DSR / NO holdout touch until both ledgers are merged); (2) the queue #7 killed-run accounting gate verified ON THIS MACHINE (and on Jeremy's). Two prolific writers on one single-use holdout make the counting discipline MORE load-bearing, not less.
>
> LESSONS THAT MUST SHAPE THIS SESSION (08-03-evening additions on top of the standing set — details in the ledger's three 08-03 evening/night/late entries):
> 1. For any sync merge, pre-register the AUTO-MERGE set (fork-footprint files upstream also touched), not just the conflict set.
> 2. VERBATIM MEANS VERBATIM: a condensed "verbatim" evidence file broke audit traceability twice in one session — hand verifier lanes the actual text, never a summary labeled verbatim.
> 3. A known-answer anchor must itself be verified before seeding it (round-2's anchor was measured EMPTY and would have failed a correct lane); and a lane reporting "the anchor's premise is false" is CORRECT, not failing.
> 4. Blind the enumeration lanes; give the pre-recon only to the verifier as reconciliation material — a wrong count anchors an honest lane into confirming it (measured: "five sites" would have capped a ten-site enumeration).
> 5. Verifier lanes can overclaim too (T3 framed a regression as breaking live mode; the shipped live path is clobber-protected) — the lead audits the auditor against the record before anything reaches a document.
> 6. Standing (07-31/08-03): results before decisions (present, END TURN, decide later); issue-first + red-team anything external; measure before arguing; one consolidated review round-trip; content-blind tests are decoration; zero skips is the healthy state; commit messages reviewed like code; two-phase characterize-and-STOP; earlier numbers are predictions; fail loud, not flattering; provision caches into ANY environment that runs the engine.
>
> HOW I WANT YOU TO WORK: visual todo list first; plan → my nod → execute; one change per branch, reviewed and green before the next; OMC lanes for anything non-trivial (executor lanes model=opus; code-reviewer/red-team/verifier on the session model; separate verifier before any merge; lane briefs name the LSP tools and the gate command); cheapest control that works; verify by execution — main.py simulate prints NOTHING, read the newest results/runs/ dir via stat -f '%m %N' results/runs/* | sort -rn | head -1; gate every commit with the basedpyright CLI + .venv/bin/ruff on the changed .py files; lsp_find_references before any rename, re-run until stable THEN grep cross-check; mutation-test new tests at the PUBLIC entry point and mutation-test the fix itself; keep Notion current as findings land (board Detail lead-note convention); update research/LEDGER.md before session end; post the wrap to Slack (tradingbot channel, C0BLW7V6BC6) in plain human language first, numbers second.
>
> Start by confirming the environment (git state; fast+slow suites — expect 213 / 14-0-0; lsp_servers lists ty for .py; basedpyright floors bar_equity 1 / trading_bot 33 — the repo-wide floor changed with the merge, re-measure before quoting it; ast_grep MCP tool now resolves) and the three session-start checks, and tell me what you find.

---

## 2. State as of 2026-08-03 (late)

| | |
|---|---|
| Branch | `mac/setup` @ `dab115ca`, pushed — run `git log` for the actual HEAD |
| Upstream | UNIFIED at `33ac7ec4` + our sync merge; his local venv-untrack + parked restructure may land next |
| PRs | ALL 8 merged; port cherry-picked (`c4feaf56`); no open PRs either direction |
| Fast suite | 213 passed / 0 skipped (main repo; 211/2 in archive-less worktrees) |
| Slow suite | 14 / 0 / 0 |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades (carries the uniform 2-bar truncation: bars.csv 1438 vs manifest 1440) |
| LSP | HYBRID unchanged: ty 0.0.65 bridge / bp 1.39.5 gate; floors bar_equity 1, trading_bot 33 (repo-wide: re-measure, changed with merge) |
| Tools | ruff 0.15.10 in .venv; ast_grep napi fixed at ~/.claude/node_modules (verify live this session) |
| Workflow | runnable on Mac AND merged upstream; DUAL-WRITER since 2026-08-04 — campaigns on BOTH machines once protocol 9.5 + gate #7 clear; Ubuntu server is the long-term home |
| Venv | `../.venv/bin/python` from trading-bot/; no pip — use uv |

## 3. The queue

- ✅ #1–#6, 8.5 (characterized), 8.6 done. **Next: task C (#9 Kraken ingest, gate-first) + rider 8.7 (CI leg — ubuntu is now the DEPLOY TARGET leg, fresh-clone verification first).**
- **NEW 9.5 — trial-ledger dual-writer merge protocol** (Dorian's 2026-08-04 call: both run campaigns): needs Jeremy's agreement on the mechanics, then implementation. Gates ALL campaigns on either machine, but not task C (data groundwork proceeds regardless).
- **Blocked on Jeremy+Dorian decisions:** A14 remedy (R1–R4; R4 = restoration, recommended), last-two-bars fix (joint, rebaselines everything), merge-protocol mechanics (9.5), venv untrack execution, restructure landing.
- **#7 trial accounting** — now BOTH machines, after 9.5. **#10 risk layer** — before real money, not before research. Unqueued new: Ubuntu server readiness (env, caches, recorder — W15's port has never run on a Linux host).
- Parked by design: cleanup umbrella (type-hygiene, verdicts recorded), compact/slash date forms (unblocked, unqueued), config-identity wiring gap, pre-commit holdout-gate wiring, record-taxonomy question (own session), ty upstream issue for the find_references instance-attribute blind spot (optional).

## 4. Known-broken / deferred (tracked on the board, all with lead notes)

- Last-two-bars: MECHANISM KNOWN (two off-by-ones + manifest over-report), fix pending joint decision.
- Candle-callback: INERT layer + arity REGRESSION, remedy pending Jeremy (A14-revisited ticket).
- Seven Binance caches carry sealed rows — never run a window past 2025-12-31.
- measure_bar_sigma latent seal overshoot (Medium/Security, Jeremy); seal-scan scope shrinkage; r2 test vector (POSIX); numpy Timedelta deprecation on the default path; live-warmup ordering hazard; optimize_strategy stale-callback hazard.
- `main.py simulate` rewrites tracked results/trades.json — restore after reproducibility checks.
- DST delta-3 hypothesis on 4 archived March runs — unverified, in the task-B record.

## 5. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, LSP+lane protocol (updated 08-03 evening: grep cross-check, worktree provisioning) |
| `research/LEDGER.md` | the three 08-03 evening/night/late entries (sync merge; Phase A; task B) — the day's full record |
| `FORK_CHANGES.md` | sync-merge section: which rows closed as merged upstream; residual divergence list |
| 🐛 board | two DECISION tickets (Jeremy+Dorian) + five Jeremy-assigned finding tickets, all with evidence lead-notes |

Notion — "Trading Bot HQ": the 🍎 evening banner answers Jeremy's four asks; 🐛 Bugs & Tasks → 🍎 Fork queue view; Trial-Ledger page still awaiting his Option A confirmation.
