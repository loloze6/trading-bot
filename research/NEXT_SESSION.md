# Handoff → next Claude Code session (written 2026-07-31, end of the finish-line session)

Paste §1 into a fresh session. Everything below it is the context that prompt refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home*, where §1 sits in a plain-text code block for clean copy-paste. If you change §1 here, change it there — that page is the one Dorian actually copies from.

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. CLAUDE.fork.md is NOT auto-loaded — Jeremy's CLAUDE.md has no include for it, so you must read it explicitly. Then run: git status && git log --oneline -5
>
> WHERE WE ARE (end of 2026-07-31): the fork's half of the finish line is COMPLETE — holdout guarded (queue #1), drawdown honest (board #5: off-by-default bar_equity block, merged eaa4b41c), the seal regex closes both flanks (board 3.5, 8acd08e6), and the never-executed manifest-integrity test lives (board 4.5, f3d85745 — slow suite fully green for the first time). Slippage is HANDED TO JEREMY with a decision-ready spec on Notion (execution-core is his under single-writer). Suites: fast 165 passed, slow 14 passed / 0 skipped / 0 errors. Branch mac/setup — run git log for the actual HEAD. Baseline anchor: config_sha 5ccbec42 / data_sha 5a75366c / net -23.021% / sharpe -5.646 / 24 trades — a REPRODUCIBILITY ANCHOR, NEVER A RESULT; honest bar-level numbers exist behind run_backtest(bar_equity=True): maxDD -24.77 / sharpe -5.12 / sortino -5.05.
>
> SESSION-START CHECKS (any may preempt the plan — tell me before proceeding):
> 1. gh pr view 1 --repo loloze6/trading-bot (same for 2 and 3). Jeremy verified #1/#2 on Windows and said MERGE BOTH. If any merged, the stacked follow-up offers unblock: seal-regex fix (after #2), fixture-revival (after #1), bar-equity + the validator PR #4 candidate (after all three). Never push to his repo; PRs only.
> 2. git fetch upstream && git log --oneline mac/setup..upstream/master. Jeremy's W8→W15 (7 commits, incl. a BREAKING register_feed(window_seconds=...) change and a Linux recorder port) were UNPUSHED as of 07-31. If he has pushed, a sync merge (git merge upstream/master — merge, never rebase) comes BEFORE the port task, and the port-surface line numbers below must be RE-VERIFIED after the merge.
> 3. Check Notion for new Jeremy notes (his last pass rewrote a session plan): Trading Bot HQ banner, Mac Fork — Home, and the Trial-Ledger page. If he confirmed Option A (single-writer), write the one-sentence rule into the Working Agreement page AND CLAUDE.fork.md — a queued action from our ✉️ response note.
>
> THE TASK — fix/workflow-macos-port (queue #4; board #6): make strategy-research/workflow/ RUNNABLE on this Mac. Port surface, audited 2026-07-28 (re-verify line numbers if upstream moved): 4 hardcoded Windows interpreter paths — strategy-research/workflow/run_phase1_research.py:990, :1462, :4889 and strategy-research/tools/retune_regime_detector.py:486 (all point at venv/Scripts/python.exe) — plus ONE undeclared dependency: claude_agent_sdk, imported at run_phase1_research.py:54, pinned 0.2.82 in comments, in no requirements file. The fix is a RESOLVER, not a hard swap: sys.executable is already used correctly at :1587/:2777, so apply the file's own idiom; Jeremy's Windows tree must keep working unchanged. The 2026-07-28 audit found zero other OS hazards (no shell=True, no os.name branches, no backslash literals). Pipeline model: claude-haiku-4-5.
>
> SCOPE BOUNDARIES: (1) runnable ≠ run — do NOT execute campaigns. Under trial-ledger Option A campaigns run on Jeremy's machine, and the trial-accounting gate (run_campaign.py:1119-1122 — a KILLED run must still land a row in campaign_state.trial_sharpes) is unverified. (2) The Recorder's PowerShell supervisor (strategy-research/recorder/supervise.ps1) is a SECOND, UNSCOPED port — explicitly out of scope. (3) Adding the claude_agent_sdk dependency needs my explicit approval first (no new deps without approval) and lives in a fork-only requirements file or documented install step — NOT in upstream's requirements.txt without discussion. ACCEPTANCE: a dry smoke check proving the resolver finds the right interpreter on BOTH path styles (mock the Windows case), imports resolve on the Mac, and NOTHING fetches or runs against market data — no window past 2025-12-31, ever. Propose the design in 3-6 bullets and get my nod BEFORE code.
>
> HARD RULES (unchanged): never run live; the holdout is sealed (local_data/holdout_sealed/2026_H1/ — reading it spends it; seven pre-contaminated Binance caches remain readable, so never run a window past 2025-12-31); every experiment touching market data gets a research/TRIALS.csv row; no secrets; origin only; no Co-Authored-By trailers.
>
> LESSONS THAT MUST SHAPE THIS SESSION (paid for 07-30/31 — details in the ledger):
> 1. COMMIT MESSAGES ARE REVIEWED LIKE CODE: six branches in a row carried refutable specifics (dates, counts, byte offsets, history claims) caught only by the verifier lane. Never write a number or claim you didn't just measure.
> 2. TWO-PHASE FOR ANYTHING NON-TRIVIAL: phase A characterize-and-STOP (schemas/derivations/insertion points with file:line evidence, conventions pre-registered), get the go, then phase B implement. Phase A caught the warmup-boundary trap before it shipped.
> 3. EARLIER NUMBERS ARE PREDICTIONS: divergence is a bug to explain, never a number to prefer. That is how a 72%-flattering Sortino died in review instead of in production.
> 4. FAIL LOUD, NOT FLATTERING: anything feeding decisions raises on degenerate inputs (an all-NaN allocation column used to read as 100% exposed, silently).
> 5. LANE PATTERN + MODEL PINNING (Dorian's cost policy): executor lanes spawn with model=opus; code-reviewer + red-team + verifier stay on the session model; purely mechanical lanes may use sonnet/haiku. Executor implements from a surgical spec → code-reviewer + red-team in parallel on the diff → separate verifier → team-lead merges. Commit BEFORE mutation rounds. Worktrees live in the scratchpad with the gitignored local_data CSVs COPIED in (never symlinked — a stray fetcher write must not poison the real cache).
>
> HOW I WANT YOU TO WORK: plan in 3-6 bullets and get my nod BEFORE code; one change per branch, reviewed and green before the next; cheapest control that works; verify by execution — main.py simulate prints NOTHING, read the newest results/runs/ dir via: stat -f '%m %N' results/runs/* | sort -rn | head -1; mutation-test new tests at the PUBLIC entry point and mutation-test the fix itself; keep Notion updated as findings land (board tickets: "Dorian's fork" column + the Detail lead-note convention); update research/LEDGER.md before session end; post the wrap to Slack (tradingbot channel, C0BLW7V6BC6).
>
> Start by confirming the environment (git state; fast+slow suites — expect 165 / 14-0-0) and the three session-start checks, and tell me what you find.

---

## 2. State as of 2026-07-31 (end of day)

| | |
|---|---|
| Branch | `mac/setup` @ `e0848424`, pushed to `origin` — run `git log` for the actual HEAD |
| Upstream | Jeremy's GitHub still `70dab378` (his local +7, W8→W15, unpushed); **PRs #1, #2, #3 open**, his findings fixed on all branches |
| Fast suite | 165 passed |
| Slow suite | 14 passed, 0 skipped |
| Baseline | `5ccbec42` / `5a75366c` / −5.646 / 24 trades, byte-identical at tip (re-certified during board #5) |
| bar_equity (flag-on) | maxDD −24.7684 / sharpe −5.1217 / sortino −5.0479 / exposure 3.79% / turnover 84.67 |
| Finish line | costs modelled → Jeremy (spec ready) · **drawdown honest ✅** · **holdout guarded ✅** · trials counted → Jeremy's machine (Option A, pending his confirmation) |
| Venv | `trading-bot-dorian/.venv` → run as `../.venv/bin/python` from `trading-bot/` |

## 3. The task: `fix/workflow-macos-port` — notes

- **Port surface** (4 lines + 1 dep) audited 2026-07-28; the ledger's "PRIORITY CHANGE + workflow audit" entry has the full detail. Re-verify line numbers if upstream moved.
- **Resolver design intent:** find the venv interpreter relative to the repo (Mac `.venv/bin/python`, Windows `venv/Scripts/python.exe`), falling back sensibly — Jeremy's tree must work unchanged; prefer the file's own `sys.executable` idiom where the subprocess should reuse the running interpreter.
- **Why now:** inert until a campaign runs; under Option A it is portability insurance and the groundwork for the agreed Linux deploy target.
- **Out of scope:** the Recorder supervisor port (`supervise.ps1`), executing any campaign, verifying trial accounting (Jeremy's machine).

## 4. Known-broken / deferred (tracked on the board)

- **Seven Binance caches carry sealed rows** — new leaks blocked (queue #1); never run a window past 2025-12-31.
- Config-identity check cannot catch config_path wiring (Medium) — needs a non-default-config run; TOCTOU defense-in-depth noted.
- Compact/slash/non-padded date forms slip BOTH seal-guard layers (Medium — compact-T is the run-dir naming style).
- `holdout_date_gate.sh` PATTERN hardcoded, not policy-derived (Low); pre-commit wiring still unwired (unqueued).
- Seal scan aborts wholesale on the first undecodable file (Low, fail-closed).
- `main.py simulate` rewrites tracked `results/trades.json` — restore with `git checkout --` after reproducibility checks.
- `visualize_data` cache dir in tracked `trading-bot/data/`; whale's duplicate midnight rule — cosmetic, deferred.
- Latent NameError `trading_bot.py:374` (`previous_allocation` out of scope in `_close_all_positions_at_end`) — confirmed real 2026-07-31, dormant on windows ending flat.

## 5. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, backlog with #5 done and the finish line updated. **Not auto-loaded.** |
| `research/LEDGER.md` | every trap and lesson; the 2026-07-30/31 entries are the important ones |
| `FORK_CHANGES.md` | rows 17–20: exactly what this session changed and why |
| `strategy-research/workflow/run_phase1_research.py` | the task's home — read the interpreter-path sites and the `sys.executable` idiom first |
| `strategy-research/tools/retune_regime_detector.py` | the fourth path site |

Notion — "Trading Bot HQ": 🐛 Bugs & Tasks → **🍎 Fork queue (in order)**. Rows 1–5 (incl. 3.5/4.5) read done; row 6 is ⬅️ next. The ✉️ response note and the 🎯 slippage spec are under Trading Bot HQ.
