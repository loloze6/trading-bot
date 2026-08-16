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

- [ ] S1 — Jeremy: `forecast_hash` mandatory emission at both write sites in
      `run_phase1_research.py` (`rpr:2992-3002`, `rpr:3040-3048` per issue
      #28) + the `(trial_id, source)`-keyed idempotency guard on
      `_record_backtest_trial` (`rpr:1134`) that issue #28 warns a naive
      `run_id`-only guard would get wrong. This is issue #28's H3.
- [ ] S2 — Jeremy: mechanical duplicate-`trial_id` refusal in
      `deflate_sharpe.py`, plus resolving `run_054`/`run_059`'s existing
      triplicate rows.
- [ ] S3 — Dorian: adopt the `run_d_NNN` prefix for new fork-originated
      trials.
- [ ] S4 — Joint: write + verify the union-merge procedure for a fork PR
      touching `campaign_state.yaml` (test with two divergent trial lists).

## Log

- 2026-08-16 — `new` → `planned`. Created to give the dual-writer mechanics
  (agreed in direction since 2026-08-04, never implemented) an actual home —
  previously tracked only as a Notion discussion page and a precondition
  bullet in `CLAUDE.fork.md`, with no epic and no stories. Directly
  motivated by issue #28 surfacing that the gap is live, not theoretical
  (`run_054`/`run_059` already triplicated, `forecast_hash` already null
  everywhere sampled). S1 folds in issue #28's H3, which Jeremy already
  claimed in the H2-H4 split (Slack, 2026-08-16).
