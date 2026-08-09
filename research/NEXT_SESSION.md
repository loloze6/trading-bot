# Handoff → next Claude Code session (written 2026-08-09, afternoon — exchange-plumbing PLANNED + PHASE-A signed off; BUILD pending)

Paste §1 into a fresh session. Everything below it is context §1 refers to.

**Mirrored in Notion** at *Trading Bot HQ → 🍎 Mac Fork — Home* (keep the two in sync).

**LAUNCH COMMAND (Dorian's standing call, 1M context always):** `claude --model "claude-opus-4-8[1m]"` — quotes mandatory (zsh globs `[1m]`).

**1M CONTEXT IS THE RULE FOR EVERY MODEL** — lead AND all lanes. Transcript-verify the resolved id per lane: `find ~/.claude/projects/<proj> -name 'agent-*.jsonl' -mmin -N | while read f; do grep -ho '"model":"[^"]*"' "$f" | sort -u; done`.

**Model governance:** **fable = THE BRAIN** — plans + gates (a fable verifier before EVERY merge/PR). **opus-4.8 = lead + adversarial** — `redteam-48`/`reviewer-48` (BLIND red-team + code review). **sonnet-5 = implementation** (`model:"sonnet"`).

---

## 1. The prompt — paste this

> Read these three files in full before doing anything, in this order: CLAUDE.fork.md, research/LEDGER.md, research/NEXT_SESSION.md. NOTE: CLAUDE.md @-includes CLAUDE.fork.md — if the fork guardrails already appear in your context, say so; if not, read the file explicitly. Then run: git status && git log --oneline -8
>
> WHERE WE ARE (2026-08-09 afternoon): mac/setup — run git log for HEAD. PR #18 (E-012) is MERGED upstream (`d7a3710a`) and synced back. The exchange-plumbing fix (tickets 12+13, branch `fix/exchange-plumbing-campaign-aux`) is FULLY PLANNED (Rev 4; opus-4.8 red-team PLAN-SOUND + critic PASS) and PHASE-A VERIFIED + SIGNED OFF by Dorian. Decisions are LOCKED. **Your job THIS session: IMPLEMENT it end-to-end through the pipeline. No re-planning, no re-deciding — the plan is authoritative.**
>
> THE PLAN (authoritative spec — READ IT FIRST): `.omc/plans/exchange-plumbing-aux-and-campaign.md` (Rev 4). Read §3 (impl spec, build order C2→C1→C3), §6 (byte-identity HARD gate), §8 (tests T-01..T-19 + mutations M1..M15), §2.3 (governance allowlist). If the file is gone, its full spec is in the LEDGER 2026-08-09 entry + below.
>
> WHAT'S FIXED: leg-3 (PR #13) made only the PRICE path honor `trading.exchange`; two named follow-ons remain — (12) aux feeds don't follow the venue (funding silently binance→empty→AuxFeedVenueError once fixed); (13) the campaign path (`run_backtest`/`run_protocol`) never reads/validates the venue (a "kraken" config silently scores binance). One combined branch closes both.
>
> LOCKED DECISIONS: build order **C2 (aux venue) → C1 (campaign param) → C3 (run_protocol)** — C2 first because C1-without-C2 arms a mixed-venue silent hole. **D1 = option (a):** `run_backtest(exchange: str | None = None)` (None→config-read→binance byte-identical; explicit→used+validated via a `_validated_exchange` choke point extracted from launcher.py:136-142), threaded through run_protocol via **Option Y** `exchange = args.exchange or protocol.get("exchange") or "binance"` (campaigns default binance explicitly, decoupled from config.json; protocol `exchange` field + `--exchange` CLI). **D2 = fail-loud C:** `AuxFeedVenueError(RuntimeError)` at data_manager.py:772-778 when the no-data branch fires AND `getattr(feed.fetcher,"exchange_id","binance") != "binance"`; binance/venue-independent feeds keep warn+NaN byte-identical. Venue-qualify `FundingRateFetcher.cache_key` mirroring `CcxtFetcher` decision-(a) (binance UNPREFIXED → `BTCUSDT_funding_8h` unchanged). Correct the "will be NaN" log → "all-NaN for every bar" (P3-measured).
>
> COMMITS:
> • **C2** (aux venue): backtester.py:124 (thread `exchange=self.exchange` into the factory call); feed_registry.py (all 3 factory lambdas gain trailing `exchange="binance"` + R-NIT/R-LIT comments); funding_rate_fetcher.py (cache_key prefix rule + docstring); ccxt_fetcher.py:108-110 (docstring correction); data_manager.py (`AuxFeedVenueError` + E7 predicate + corrected log line); 1-line venue-fixed-binance annotations at feed_registry.py:128, prescreen_signal.py:145, measure_funding_carry.py:38. Tests T-06,07,08,09,10,11,14,15.
> • **C1** (campaign param): launcher.py (extract `_validated_exchange`; run_backtest gains `exchange: str | None = None` + resolution + TradingParams/engine forwards + docstring); test_exchange_selection.py (:237-238 docstring rewrite + module-level AST guard). Tests T-01,02,03,04,05,12,13,16. NOTE: T-13 stays RED until C1 — do NOT chase it green at C2 (T-10 is C2's gate).
> • **C3** (run_protocol): run_protocol.py ONLY (Option Y resolution + `parser.add_argument("--exchange", default=None)`; pass `exchange=` at BOTH :1070 AND :1144). Tests T-17,18,19 (T-19 = both-absent→explicit binance, both modes).
>
> BYTE-IDENTITY GATE (HARD, re-derive INDEPENDENTLY): the default path (no `trading.exchange`) must reproduce **config_sha `5ccbec42` / data_sha `5a75366c` / 24 trades / −23.021% / −5.646**, metrics.json sha256 **`a3172f93a6b03352a8ee7113ead5fdd7d299784eb16e03cdbd1d94b497a9bc1f`**. Suite baselines (Phase A, main repo, XBTUSD_60.csv present): **fast 302/0, slow 16/0**. Commit-gate DELTA baselines on the changed files: **basedpyright 114, ruff 97** (all pre-existing noise; only NEW diagnostics inside changed lines are findings). This fix changes NO default output.
>
> DELIBERATE non-default deltas (declare LOUD + control run in FORK_CHANGES + PR): D-i kraken now honored (was silent binance); D-ii bogus exchange exits 1 in run_backtest (was silent); D-iii venue-mixed aux feed raises AuxFeedVenueError (run_backtest surfaces the typed error; simulate catches→exit 1). Consequence: **every kraken run loading FEED_REGISTRY refuses to start until kraken funding data exists** (P9-confirmed: kraken-spot funding raises ccxt `NotSupported` even ONLINE) — that's the kraken-funding near-term ticket (order 14).
>
> PIPELINE (governance, ALL 1M, transcript-verify EACH): fable plan is DONE. → **sonnet-5 impl** (`model:"sonnet"`), ONE lane, commits C2→C1→C3, tests-first (defect-capturing tests WATCHED FAILING on the pre-fix tree). → **opus-4.8 BLIND red-team** (`redteam-48`, blind to the plan rationale — hunt silent venue fallbacks, cache-filename regressions, lookahead, byte-identity breaks, surviving mutants, over-broad fail-loud, G1 arming). → **opus-4.8 code review** (`reviewer-48`, severity-rated, separate lane; enforce §2.3's 4-site governance allowlist [2 cache_key rules + fail-loud predicate + `_validated_exchange`] via `grep -nE 'exchange_id|== *"binance"|!= *"binance"'` on the diff). → **fable verifier** (independent re-execution of §6 + §8; commit-message audit — quote only measured specifics). → merge `--no-ff` into mac/setup; merged-tip acceptance; FORK_CHANGES (D-i/D-ii/D-iii + G1 note) + LEDGER + TRIALS rows; Notion tickets 12+13 → Done. → **upstream PR** (on Dorian's go): cherry-pick onto Jeremy's tip, blob-identity gate, red-team pre-review; body = both tickets + D-deltas + G1/R5 disclosure + C3 as a severable tail commit.
>
> STRATEGIC CONTEXT: **kraken is the strategic-PRIMARY venue (Binance lacks an EU MiCA license); binance = byte-identity reference only.** Technical default STAYS binance (back-compat of existing *USDT protocols; a kraken default would break them with "No data"); kraken-primary is achieved by NEW protocols opting in explicitly (`exchange: kraken` + *USD symbols). Venue/Exchange OBJECT is a DEFERRED epic (Notion, order 30) — trigger-gated, joint with Jeremy; governance rule = no new venue-conditional branches outside the 4 allowlisted sites without reopening it. **Jeremy should eventually be looped on kraken-primary** (Dorian's call how/when — do NOT announce it on Slack).
>
> HARD RULES: never run live; holdout sealed (never a window past 2025-12-31; never open holdout_sealed/); every market-data experiment → a research/TRIALS.csv row; no secrets; origin only, PRs to Jeremy (don't touch PR branches except on his feedback); no Co-Authored-By trailers. zsh traps: unquoted `$var` doesn't word-split; heredoc + `&&` mangles commit messages (use `git commit -F <file>`); double `cd` fails (absolute paths). Commit gate: basedpyright + ruff on changed .py, DELTA only (pre-existing noise is not a finding). Byte-identity re-derived independently; deliberate breaks declared with a control run.
>
> BUDGET: ~8% token budget until Tuesday 12am. Be economical — lean lanes, NO redundant re-measuring (the Phase A numbers above are trusted). If budget runs low mid-build: commit the completed commits (each is atomic + green), update LEDGER + NEXT_SESSION with exactly what remains, stop cleanly. A clean partial beats a broken whole.
>
> HOW DORIAN WANTS YOU TO WORK: OMC teams; fable gates (plan DONE → fable now verifies), opus-4.8 orchestrates + BLIND red-team/review, sonnet-5 codes, all 1M; transcript-verify every lane; visual todo first; one change per commit, green before the next; verify by execution; keep Notion current (boards/tickets/Decisions log); update LEDGER + commit before session end; rewrite NEXT_SESSION + its Notion mirror at session end; Slack wrap at session end (plain-first, numbers second).
>
> FIRST ACTIONS: (1) orient (git status/log; read the 3 files + plan §3/§6/§8). (2) `git checkout -b fix/exchange-plumbing-campaign-aux`. (3) launch the sonnet-5 impl lane on C2 (build order), tests-first. (4) proceed C2→C1→C3 → blind red-team → code review → fable verifier → merge, per the pipeline. Get Dorian's nod before opening any upstream PR.

---

## 2. State as of 2026-08-09 (afternoon)

| | |
|---|---|
| Branch | `mac/setup` — run `git log` for HEAD (last bookkeeping ~ this handoff commit) |
| Upstream | `d7a3710a` — **PR #18 (E-012) MERGED** + synced back byte-identical (`1b183758`) |
| Exchange-plumbing | Plan Rev 4 LOCKED (`.omc/plans/exchange-plumbing-aux-and-campaign.md`); Phase A DONE + signed off; **NOT implemented** |
| Baseline anchor | `5ccbec42`/`5a75366c`/24/−23.021/−5.646; metrics.json sha `a3172f93`; fast 302/slow 16; bp 114/ruff 97 |
| Decisions | option (a) param + Option Y; fail-loud C; Venue object deferred (epic); **kraken strategic-primary (MiCA), default stays binance** |
| Server | culi.to LIVE; `loloze` (Jeremy) awaits SSH key |
| Blocked on Jeremy | `loloze` SSH key; (later) kraken-primary loop-in; upstream PR review when offered |
| Open tickets | exchange-plumbing 12/13 (In progress); kraken-funding ingest (14, near-term); 3-literals venue-qualify (31); Venue epic (30); ingest-holdout guard (7); Branch-2 holdout gate; risk layer (23) |
| Next task | IMPLEMENT exchange-plumbing (§1) |

## 3. The queue (fork-order top-first)

IMPLEMENT exchange-plumbing (C2→C1→C3) → offer it upstream (Dorian's go) → kraken-funding ingest (order 14, unblocks kraken funding-carry campaigns) → the first kraken breadth campaign (19-pair *USD universe — where the edge probability is) → ingest-holdout guard (7) → Branch 2 (holdout gate + pre-commit, needs the prose-accrual decision) → risk layer (23) → Venue-model epic (30, trigger-gated, joint with Jeremy).

## 4. Files to read

| File | Why |
|---|---|
| `CLAUDE.fork.md` | mission, hard rules, lane protocol, worktree provisioning |
| `research/LEDGER.md` | newest entry (this session) + CARRIED-FORWARD |
| `.omc/plans/exchange-plumbing-aux-and-campaign.md` | **the authoritative Rev-4 plan** — §3 impl, §6 byte-identity, §8 tests/mutations, §2.3 governance |
| `FORK_CHANGES.md` | E-012 Merged-upstream row; the exchange-plumbing deltas go here after the build |
| Notion: Decisions log 2026-08-09; tickets 12/13; Venue epic; kraken-funding ticket | the locked decisions + statuses |
