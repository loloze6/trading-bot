# E-025 — Trial-ledger dual-writer merge protocol (mechanics)

**State:** planned
**Owner:** Jeremy (joint with Dorian)
**Updated:** 2026-08-16

## Why

Two people now run campaigns against one single-use holdout and one
deflated-Sharpe N, on two machines, with no defined way to combine their
trial ledgers — so either side's promotion gate (`DSR > 0.95`) can be
cleared by a count that only saw half the actual attempts. Full mechanism
and the failure shape: Notion "🔢 Trial-Ledger Merge Protocol" page.

**Direction already agreed, mechanics were not.** Dual-writer (both people
run campaigns) was confirmed as the interim by both Jeremy and Dorian
(2026-08-04) — `CLAUDE.fork.md` already states this and lists the six
required pieces of machinery as a precondition ("before ANY campaign runs
on this Mac"). None of the six are implemented yet:

1. Which repo/branch hosts the authoritative ledger.
2. Disjoint trial-ID allocation (collision is possible today — both sides
   mint sequential `run_NNN`).
3. Append-only, union-on-conflict merge (a naive git merge can silently
   drop one side's trials).
4. The binding rule: no DSR computation, no promotion claim, no holdout
   touch until both ledgers are merged.
5. `forecast_hash` mandatory on every new trial from either side.
6. A mechanical check — `deflate_sharpe.py` refuses to run on a ledger with
   duplicate `trial_id`s.

**Directly evidenced by GitHub issue #28** (trial-accounting characterization,
Dorian, 2026-08-16): the live `campaign_state.yaml` already shows `run_054`
and `run_059` each appearing 3 times (H3 — no idempotency guard on backtest
re-entry), and `forecast_hash` is `null` on every sampled row, so cross-fork
dedup already cannot function even single-author. This is not a hypothetical
gap — it is actively producing wrong numbers today. Issue #28's H3 (backtest
re-entry overcount + dead `forecast_hash` dedup) is item 5+6 above; fixing it
is in scope for this epic, not a separate thing.

## Decisions (2026-08-16, resolves the Notion page's §6 open items)

- **Authoritative ledger:** `loloze6/trading-bot` master,
  `strategy-research/campaign_record/campaign_state.yaml`. The fork's copy
  is a working copy; new fork trials land via PR, same flow as every other
  change in this collaboration. No new infrastructure needed.
- **ID scheme:** keep sequential `run_NNN` for master-originated trials
  (already minted through the 060s). Fork-originated trials get an
  author-prefixed range, `run_d_NNN`, starting fresh — cheap, no history
  rewrite, collision-proof by construction, and human-readable provenance
  (useful independent of this epic, e.g. for auditing who ran what).
- **Merge rule:** union by `trial_id`, append-only, never "take mine." A
  real `trial_id` collision after the ID scheme above should be structurally
  impossible — the mechanical check (S4) is a tripwire for that invariant,
  not a normal-path gate.
- **`forecast_hash` mandatory:** on every new trial, both writers, effective
  now. This is issue #28's H3 fix.
- **No-DSR-until-merged:** `deflate_sharpe.py` is only ever run against
  master's ledger state, after any pending fork PR touching
  `campaign_state.yaml` has merged — never against a local/unmerged copy.
- **Where this is written down:** `CLAUDE.fork.md` is canonical (already
  states the six-item precondition); this EPIC.md is the implementation
  record. Not the Notion page — per this project's own convention, git is
  authoritative, Notion is a notification surface.

## Done when

1. `deflate_sharpe.py` raises if the ledger contains duplicate `trial_id`s.
2. Every new trial written by either side carries a non-null `forecast_hash`
   (verified: a run that omits it fails loud, not silently).
3. `run_054`/`run_059`'s existing triplicate rows are resolved (deduplicated
   or explained) as part of landing the idempotency guard — not left as
   inherited noise.
4. A documented, tested procedure exists for merging a fork PR that adds
   trials to `campaign_state.yaml` (union, not overwrite) — verified by a
   test that simulates two divergent trial lists and asserts the merged
   result contains both, with no duplicate IDs.
5. `CLAUDE.fork.md` (both copies) and this EPIC.md agree; Notion page
   updated to point here rather than carrying the decision itself.

## Stories

- [x] S1 — Jeremy: `forecast_hash` mandatory emission at both write sites in
      `run_phase1_research.py` (`rpr:2992-3002`, `rpr:3040-3048` per issue
      #28) + the `(trial_id, source)`-keyed idempotency guard on
      `_record_backtest_trial` (`rpr:1134`) that issue #28 warns a naive
      `run_id`-only guard would get wrong. This is issue #28's H3. Done
      2026-08-16, see Log.
- [x] S2 — Jeremy: mechanical duplicate-`trial_id` refusal in
      `deflate_sharpe.py`, plus resolving `run_054`/`run_059`'s existing
      triplicate rows. Done 2026-08-16, see Log — also landed the
      no-DSR-until-merged git check (Done-when #4's other half), not
      originally scoped as a separate story.
- [x] S3 — Dorian: adopt the `run_d_NNN` prefix for new fork-originated
      trials. Done (`635afa36`, held from upstream pending S4).
- [~] S4 — Joint: write + verify the union-merge procedure for a fork PR
      touching `campaign_state.yaml` (test with two divergent trial lists).
      **Mechanics verified 2026-08-16 (Jeremy) against a real hermetic git
      repo — see Log.** Still open: land a real two-sided PR (Dorian) to
      prove the documented procedure end to end, not just in a test fixture.

## Log

- 2026-08-16 — `new` → `planned`. Created to give the dual-writer mechanics
  (agreed in direction since 2026-08-04, never implemented) an actual home —
  previously tracked only as a Notion discussion page and a precondition
  bullet in `CLAUDE.fork.md`, with no epic and no stories. Directly
  motivated by issue #28 surfacing that the gap is live, not theoretical
  (`run_054`/`run_059` already triplicated, `forecast_hash` already null
  everywhere sampled). S1 folds in issue #28's H3, which Jeremy already
  claimed in the H2-H4 split (Slack, 2026-08-16).
- 2026-08-16 — S1 and S2 (Jeremy's stories) landed same day:
  - `_compute_forecast_hash()` (canonical-JSON sha256 of
    `candidate_strategy_config.json`) wired into both `_record_prescreen_trial`
    and `_record_backtest_trial`, all 4 call sites in
    `run_phase1_research.py`. Fails loud on a missing config rather than
    writing null.
  - `_record_backtest_trial` gained the `(trial_id, source)`-keyed
    idempotency guard issue #28 specified (not a naive `trial_id`-only
    guard, which would wrongly suppress a legitimate backtest row when a
    prescreen row for the same `run_id` already exists).
  - `deflate_sharpe.py` gained `check_no_duplicate_trial_ids` (the read-side
    backstop for the same invariant) and `check_ledger_is_merged` (the
    no-DSR-until-merged binding rule — compares the local ledger against
    `origin/master`, hard-fails on divergence, `--allow-unmerged` is the
    explicit named opt-out), both wired into `main()`.
  - `campaign_state.yaml`'s real triplicate rows resolved: `run_054`'s two
    duplicate backtest rows were byte-identical (mechanical dedup, no
    judgment call); `run_059`'s two backtest rows were NOT identical — kept
    the one with real numbers (n=699, matches the trade count confirmed by
    the same-day `d7f42c6` timestamp-format fix) and removed the degenerate
    one (all-null fields, the exact fingerprint of that same pre-fix lookup
    failure). Flagged explicitly in a `dedup_note` on each surviving row for
    override if this call is wrong.
  - 12 new tests (`tests/test_dual_writer_guards.py`), full suite 740/0 fast
    (strategy-research), combined `run_tests.py` both suites PASS.
  - **Not yet done:** S3 (Dorian — `run_d_NNN` prefix adoption) and S4
    (joint — verify the actual union-merge procedure end to end with a real
    two-sided PR) are still open. Done-when #4 (tested merge procedure) is
    not satisfied by this entry.
- 2026-08-16 (later) — Dorian's H2/H4 (issue #28's other two defects, not
  part of E-025's own S1-S4 but coordinated through it) landed same day:
  PR #31 (H4 — a crashed backtest now records one `backtest_failed` row
  before re-raising, so N counts the spent look) and PR #32 (H2 — a
  re-entered prescreen now upserts the fresh outcome on `(trial_id,
  "prescreen")` instead of a stale first result surviving under the old
  `run_id`-only skip-guard). Both additive, both keyed consistently with
  S1/S2's `(trial_id, source)` invariant, both verified locally before
  merge (34 accounting-related tests green, full suite 759/0 fast,
  combined `run_tests.py` PASS). Also: S3 (`run_d_NNN`) confirmed done on
  Dorian's side (`635afa36`, held from upstream pending S4).
  **Campaign-gate status at this point: H2, H3, H4 code-complete. H1 (the
  methodology decision — kills count toward N) decided but not yet wired
  in.** Two adjacent, still-unowned findings from #30's characterization
  pass remain open and untouched by any of H1-H4: `n_trades` reads the
  wrong per-symbol key (always 0 on backtest rows), and three different
  code paths compute "how many trials were tested" on three different
  bases (COUNT-DIV).
- 2026-08-16 (later still) — **H1 wired in.** `compute_dsr` gained an
  explicit `n_trials` param, splitting N (every real attempt — the
  multiple-testing count) from the sample used to estimate `mu_sr`/
  `sigma_sr` (still needs real Sharpe values; a large N does not
  manufacture an estimable variance). `compute_promotion_audit` now
  passes `total_hypotheses_tested` — which already existed and already
  counted honestly, just was never fed into the DSR itself. Mirrored in
  `run_phase1_research.py::_write_promotion_audit`, deliberately using
  `len(deduped_trials)` and deliberately not touching that file's own
  COUNT-DIV mismatch (out of scope, already tracked separately). 5 new
  tests, including proof the fix moves the actual DSR number under a
  larger honest N, and the byte-identical-when-omitted default path.
  Full suite 762/0 fast. **All four of issue #28's H1-H4 are now
  code-complete. Only S4 (joint, union-merge verification) remains before
  E-025 itself is done.**
- 2026-08-16 (later still) — **S4 mechanics verified against a real
  hermetic git repo** (`tests/test_s4_union_merge.py`, two real clones,
  real `git merge`, nothing mocked). Three findings, contradicting the
  "just merges" assumption implicit in the epic's own wording:
  1. Plain `git merge` on concurrent `campaign_state.yaml` edits (both
     sides appending to `trial_sharpes`/`runs`) **conflicts loudly** — it
     does not silently drop either side's trials, but it is not zero-touch
     either. Every concurrent dual-writer sync on this file will conflict.
  2. The correct resolution: **keep every list entry from both sides,
     always** — never `git checkout --ours`/`--theirs` on this file.
     Verified this produces the full union with no duplicate `trial_id`s
     against `check_no_duplicate_trial_ids`.
  3. **Tried and rejected: `merge=union` .gitattributes driver.** It
     auto-resolves without a conflict (looks successful, exit 0) but
     interleaves the unrelated `updated_at` scalar with the adjacent
     `runs` list's lines, producing a `campaign_state.yaml` that **does
     not parse as YAML at all** — silent structural corruption, exit 0,
     no error. This is the exact "naive merge silently drops data" failure
     the epic named, just one layer down (corrupts the file structure
     instead of dropping a trial). Do not adopt `merge=union` for this
     file. Regression-pinned so nobody rediscovers this the hard way.

  Procedure landed on: plain git merge (conflict is the expected, correct
  outcome), manual resolution keeps every list entry from both sides,
  `check_no_duplicate_trial_ids` is the mechanical backstop on the
  resolved result before any DSR computation. Flagged to Dorian directly —
  his next fork PR touching `campaign_state.yaml` will conflict by design,
  and must not be "resolved" with `--theirs`/`--ours` or a union driver.

  **What's left for S4:** a real two-sided PR proving this procedure
  end-to-end (a test fixture is not the same as Dorian's actual fork PR
  workflow) — the one piece that is genuinely joint and can't be verified
  solo.
