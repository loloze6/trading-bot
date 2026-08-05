# Handoff → next Claude Code session (written 2026-08-05 evening, end of the leg-2 session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a code block for clean copy-paste. If you change §1 here, change it there.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, that is the include working and you should say so; if not, read the file explicitly and report it. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (start of the leg-3 session; written 2026-08-05 evening): mac/setup @ 4c82a826 or later — run git log for the actual HEAD. The leg-2 session did: FIRST ACTIONS clean (Jeremy silent everywhere — no push, no reaction to the two 08-05 messages; E-012–E-019 EPIC.md files STILL unpushed, requested twice); leg 2 `fix/kraken-ingest-merge` DONE — merged `4c82a826` (single commit `a9f56317`), **upstream PR loloze6/trading-bot#9 OPEN** (branch fix/kraken-ingest-merge-upstream, blob-identical, fast 221/2 on Jeremy's base). The fix: re-ingest UNIONS (archive wins duplicates, 500→10 data-loss repro is a regression test), gap guard live on the ingest path, byte-idempotent re-ingest (close_time normalized — without it a re-ingest rewrites ~998k tracked rows of formatting), exists-but-unreadable cache refused loudly, `verify_boundary_values` closes the top-up blind spot of the timestamp-only post-write check (proven inert in 3-of-5 geometries under an injected +1h write shift), strict duplicate/out-of-order source rejection. Full lane pattern ran: opus executor (two watched-failing rounds), code-reviewer (0 blockers), red-team (3 measured MAJORs → all fixed on Dorian's calls), separate verifier (MERGE-READY; its one MINOR fixed by message amend, tree unchanged). 12/12 mutations killed bytecode-purged. Merged-tip acceptance: fast **223/0** (the 2 archive-gated tests ran for real — zero skips is the healthy state), slow **14-0-0**, validator 0, simulate **byte-identical ×5** (5ccbec42/5a75366c), manifest git_sha certifying the clean tip. New board tickets: "Ingest path has no holdout seal guard" (Medium, unqueued — the archived guard is a PORT not a cherry-pick; tools/fetch_data.py doesn't exist on this tree). Record correction: the "false union comment" defect leg never existed on this tree (archive-branch artifact). Baseline anchor unchanged: config 5ccbec42 / data 5a75366c / net −23.021% / sharpe −5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT (still carries the uniform last-two-bars truncation; E-012 fix design is Jeremy's).
>
> FIRST ACTIONS, IN ORDER:
> 1. git fetch upstream && git log --oneline mac/setup..upstream/master. Jeremy owes: his push (E-012–E-019 epics, evolved E-010, four-rules PROCESS amendment), reactions to the 08-05 decisions + E-012 numbers, and now PR #9. Docs-only push → light merge (merge never rebase; pre-register BOTH the conflict set AND the auto-merge set via merge-tree dry run; full acceptance at the tip incl. simulate byte-identity vs 5ccbec42/5a75366c). Code → full four-lane pattern, every ledger file:line becomes a prediction. New EPIC.md files → mirror into the Notion epics DB (verbatim-behind-banner). If he MERGES PR #9: the FORK_CHANGES row 25 closes; sync-merge his master back per the standard pattern.
> 2. Slack (tradingbot, C0BLW7V6BC6) AND the Notion 🐛 board AND `gh pr view 9 --repo loloze6/trading-bot --comments` — he communicates via Claude-sent Slack messages; READ THE CHANNEL. Any answer on E-012 fix design, 9.5 mechanics, A14, or PR #9 review comments may re-sequence — report before proceeding.
> 3. No tool probes needed: ast-grep pin verified 08-05; LSP hybrid standing (ty 0.0.65 bridge navigation, basedpyright 1.39.5 CLI commit-gate arbiter, grep PRIMARY for enumeration; stable lsp_find_references count = necessary, not sufficient).
>
> THE TASK — task C leg 3: the binance cache-dir/exchange hardcode in data_manager. **NO PRE-APPROVED PLAN — this leg needs characterize → plan (3-6 bullets) → Dorian's nod BEFORE any code.** Critical: the old prediction "data_manager.py:768 hardcodes binance, making Kraken caches unreachable" is STALE — the current tree has `fetch_historical_data(self, symbol, start_date, end_date, exchange: str = "binance")` at `data_manager.py:876-889` (Jeremy's W-series added an exchange param with a binance default; "defaults to binance so existing call sites are unaffected"). RE-DERIVE the actual defect surface first: What can and cannot reach a `kraken_*` cache today? Which call sites pass exchange? Is the remaining gap the default, a missing prefix in cache_key resolution, or nothing at all? Measure by execution (a config pointing at a kraken cache), then characterize-and-STOP for the nod. Scope discipline: leg 3 is reachability only — no engine multi-symbol work, no leg-4 ingest.
> QUEUED AFTER (each needs fresh plan + nod): leg 4 = majors' 1d ingest from the 26 GB archive with per-file provenance (the 07-28 BTC pattern: re-ingest, compare to committed, explain every delta; TRIALS rows; hypothesis-adjacent per the board ticket — pre-registration discipline; NOTE: main() has no per-asset isolation — one gap refusal aborts the remaining assets, decide handling in the plan; summary dict rows/first/last/gaps are WHOLE-CACHE semantics since leg 2). leg 5 = ubuntu+windows fast-suite CI (fork-only file + FORK_CHANGES row; fold the slow-suite offline-safety fix here — 9 slow tests fetch live Binance on cache-less clones).
>
> WORKTREE PROVISIONING (unchanged, verified twice on 08-05): copy BTCUSDT_{1h,1d,funding_8h}.csv + fear_greed_daily.csv into <wt>/trading-bot/local_data/ (19 kraken + 6 USDT-quoted caches are TRACKED and follow); the 26 GB Kraken_batch/ does NOT follow (main repo only); symlink the main .venv at the worktree ROOT (never git add); copy pyrightconfig.json; gate from worktrees = `basedpyright --venvpath <main-repo-path>`. Two leg-2 worktrees still registered in scratchpad (wt-kraken-ingest, wt-kraken-pr) — `git worktree list` before adding new ones; prune when convenient.
>
> HARD RULES (unchanged): never run live; the holdout is sealed (reading it spends it; never run a window past 2025-12-31; seven pre-contaminated Binance caches remain readable); every experiment touching market data gets a research/TRIALS.csv row (leg 2 needed none — synthetic tmp data only; leg 4 WILL need them); no secrets; origin only, never push to Jeremy (PRs only, and PR #9 is already open — don't touch its branch except on Jeremy's feedback); no Co-Authored-By trailers. Campaigns stay gated by the 9.5 mechanics + queue #7 on both machines.
>
> LESSONS (two NEW from leg 2, on top of the standing set): 1. **Mutation loops must purge `__pycache__` and set PYTHONDONTWRITEBYTECODE=1** — a stale .pyc executed M4's code under M5's label and produced a wrong kill-set that looked plausible. 2. **Never trust a piped command's exit code** — `cmd | tail` returns tail's 0; a cwd-broken slow-suite run read as a clean pass until the output file was checked. Verify the OUTPUT, not the exit code. Standing set: evidence outlives the lane (persist BEFORE reporting — all three lanes idled without narratives this session and the evidence files were the recovery path); no macOS `timeout`; manifest git_sha is a commit label, not tree provenance (but a CLEAN tree's manifest at the tip is real provenance — leg 2's certifies 4c82a826); window/geometry choice is measurement design (red-team's 5-geometry probe found what the reference case couldn't); verify counts you relay; pre-register auto-merge sets; verbatim means verbatim; blind enumeration lanes; the lead audits the auditor; results before decisions (present, END TURN); issue-first + red-team anything external; measure before arguing; mutation-test at the public entry point AND the fix's direction; content-blind tests are decoration; zero skips is the healthy state; commit messages reviewed like code (the verifier's undercount catch keeps the streak alive); two-phase characterize-and-STOP (leg 2's conflict/fold characterization earned the fresh nod BEFORE the executor ran); earlier numbers are predictions (the :768 → :876-889 drift proves it again); fail loud, not flattering; provision caches into ANY environment that runs the engine.
>
> HOW I WANT YOU TO WORK: visual todo list first; plan → my nod → execute per branch (leg 3 has NO pre-approval — characterize first, STOP for the nod); one change per branch, reviewed and green before the next; OMC lanes for anything non-trivial (executor=opus; code-reviewer/red-team/verifier on the session model; separate verifier before any merge); cheapest control that works; verify by execution — `main.py simulate` prints NOTHING, read the newest results/runs via stat -f '%m %N' results/runs/* | sort -rn | head -1, restore tracked results/trades.json after any reproducibility check; gate every commit with the basedpyright CLI + .venv/bin/ruff on changed .py files; keep Notion current as findings land; update research/LEDGER.md + commit before session end; rewrite research/NEXT_SESSION.md + its Mac Fork — Home mirror at session end; post the day's Slack wrap (tradingbot, C0BLW7V6BC6) at session end — plain human language first, numbers second.
>
> Start with FIRST ACTIONS 1-2 in order and tell me what you find — especially anything from Jeremy — before touching leg 3.

---

## 2. State as of 2026-08-05 (evening)

| | |
|---|---|
| Branch | `mac/setup` @ `4c82a826`, pushed — run `git log` for the actual HEAD |
| Upstream | synced through `10b46a63`; **PR #9 OPEN** (Kraken ingest fix); Jeremy's local still AHEAD (E-012–E-019 etc., push requested twice) |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades (uniform 2-bar truncation stands; E-012 design = Jeremy) |
| Suites | fast **223/0** (main repo, archive tests live), slow 14-0-0, validator 0, simulate byte-identical ×5 at `4c82a826` |
| Leg 2 | DONE + PR #9; evidence in the 08-05 session scratchpad `evidence-leg2/` (00–17 + rt_*); evidentiary runs `20260805T165635Z` (branch tip) + `20260805T204440Z` (merged tip) preserved untracked |
| Blocked on Jeremy | E-012 fix design; A14 remedy; 9.5 mechanics; his push; venv untrack (E-006); now PR #9 review |
| Blocked on Dorian | four-rules reply (his separate review) |
| LSP / tools | hybrid unchanged (ty 0.0.65 bridge / bp 1.39.5 CLI gate); ruff 0.15.10 in .venv; ast-grep napi 0.33.1 |
| Venv | `../.venv/bin/python` from trading-bot/; no pip — use uv |

## 3. The queue

- ✅ #1–#6, 8.5/8.6, leg 1, **leg 2 (`fix/kraken-ingest-merge`, PR #9)**. **Next: leg 3 binance-hardcode RE-DERIVATION (no pre-approval — plan + nod) → leg 4 majors' 1d ingest → leg 5 ubuntu+windows CI (+ slow-suite offline fix).**
- **9.5 dual-writer mechanics** — awaiting Jeremy; gates ALL campaigns with queue #7 (both machines). Not gating task C.
- New tickets 2026-08-05 (evening): ingest-path seal guard (Medium, unqueued — a PORT of the archived guard, not a cherry-pick). Recorded latents: number_of_trades NaN int→float promotion (armed by first live Kraken top-up); pandas-3 FutureWarning via C3; main() no per-asset isolation (leg-4 planning input); truncated-mid-file caches indistinguishable from truth.
- Parked by design: cleanup umbrella, compact/slash date forms, config-identity wiring, pre-commit holdout-gate wiring, record taxonomy (E-004, joint).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | the 2026-08-05 (evening) leg-2 entry + CARRIED-FORWARD |
| `FORK_CHANGES.md` | row 25 = the leg-2 divergence, closes when PR #9 merges |
| 🐛 board | "Ingest Kraken daily bars" ticket (gate cleared, leg-4 scope) + the new seal-guard ticket |
