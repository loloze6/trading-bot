# E-025 S4 — Union-merge procedure for fork trials (design)

**Status:** DRAFT for the joint S4 discussion. **S4 is joint** — Jeremy owns the authoritative ledger; this is the fork's opening proposal, not a landed decision.
**Satisfies:** EPIC.md Done-when #4 — *"A documented, tested procedure for merging a fork PR that adds trials to `campaign_state.yaml` (union, not overwrite) — verified by a test that simulates two divergent trial lists and asserts the merged result contains both, with no duplicate IDs."*
**Depends on:** the [WRITER_CONTRACT](./WRITER_CONTRACT.md) (row shape + `(trial_id, source)` key) and S3 (`run_d_NNN` disjoint IDs, merged fork-side `635afa36`).

## What S3 already bought us

With `run_NNN` (master) and `run_d_NNN` (fork) **disjoint by construction**, a `trial_id` collision between the two writers is structurally impossible. So the union of two trial lists is **loss-less and unambiguous** — there is never a "which copy wins" decision on the trial rows. That is what makes S4 small: the hard part isn't the trial union, it's what to do with the *rest* of the file (below).

## Core: union of `trial_sharpes`

Append-only union, keyed on `(trial_id, source)`:

1. Start from master's `trial_sharpes`.
2. Add each fork row whose `(trial_id, source)` is not already present.
3. A `(trial_id, source)` present on **both** sides with **differing** content → **REFUSE** (never silently take one). Disjoint prefixes guarantee this can't arise from honest writers, so its appearance means a bug or a hand-edit — exactly what the tripwire is for.
4. Post-merge, run `check_no_duplicate_trial_ids` (ds:105) — the merged list must pass.

In the honest path, step 3 never fires; the union is just "master rows + fork's `run_d` rows."

> **Key wording — heads-up vs the EPIC.** The EPIC's merge rule (EPIC.md:52) and Done-when #1 (:68) say "union by **`trial_id`**". The operative key in the code (`check_no_duplicate_trial_ids`, ds:121) and in this design is the 2-tuple **`(trial_id, source)`** — because a single `trial_id` legitimately carries a `prescreen` row plus a `backtest`/`backtest_failed` row. This is not a disagreement with the EPIC, it's the precise form of the same invariant; flagging so the loose EPIC phrasing doesn't read as a contradiction when this lands.

## The real work: the rest of `campaign_state.yaml`

`trial_sharpes` is one of ~16 top-level keys. The others (verified in the live file):
`runs`, `altitude_history`, `recent_parameter_dimensions_by_family`, `failed_families`, `instruments_tried`, `components_built`, `timeframes_tried`, `diagnostics_log`, `notes`, `last_escalation`, plus scalars (`campaign_id`, `research_question`, `review_every_n_runs`, `status`, `updated_at`). A running campaign writes many of these, not just `trial_sharpes` — so a naive git merge of the YAML is genuinely conflict-prone. Three ways to handle it, increasing invasiveness:

**Option A (recommended) — restrict what a fork PR may touch.**
A fork PR to master's `campaign_state.yaml` is **append-only to `trial_sharpes` and `runs`**, disjoint `run_d` ids, and does **not** modify master's campaign-narrative fields (`diagnostics_log`, `altitude_history`, `notes`, counters — the running campaign's own state, master-owned). Union becomes trivial and largely git-mergeable; the fork stays out of master's narrative. Presumes the fork's trials are contributions to master's campaign, **or** the fork's own campaign narrative lives in a separate `campaign_state.yaml` (Open Question 1).

**Option B — a semantic merge tool.**
`union_merge_campaign_ledger(master, fork) -> merged` that unions the list-valued keys (`trial_sharpes` on `(trial_id, source)`, `runs` on `run_id`, the `*_tried` lists as sets) and applies a declared rule per scalar (`updated_at` = max; `campaign_id`/`research_question`/`status` = master-wins). Registered as a git merge driver for `campaign_state.yaml`, or run as a PR-prep step. More robust if the fork legitimately touches more fields; more code to own and test.

**Option C — per-writer shards.**
Split `trial_sharpes` into master + an included fork shard, union at load. Zero git conflict by disjoint files, but most invasive to Jeremy's schema + `load_campaign_state`. Not recommended unless A/B prove insufficient. (Mirrors workflow-mitigation #4 for `research/LEDGER.md` — but the ledger is Jeremy's format to change, so this stays a last resort.)

## Recommended shape

- A **tested pure function** `union_merge_trial_ledgers(a, b) -> merged` (the core of A/B), in `deflate_sharpe.py` or a small sibling — satisfies Done-when #4's "tested procedure" directly and is cheap + ours to draft.
- The **PR-flow convention** (Option A): fork PRs append-only `run_d` trials; master reviews + merges; post-merge `check_no_duplicate_trial_ids` gates.
- **Git integration** (merge driver vs manual PR-prep) is a follow-on decision **Jeremy owns** as the authoritative-ledger holder.

## Pre-registered tests (Done-when #4)

- `test_union_merge_two_divergent_ledgers`: master `[run_045/prescreen, run_045/backtest]`, fork `[run_d_007/prescreen, run_d_007/backtest_failed]` → merged has all 4 rows; `check_no_duplicate_trial_ids` passes; the `statistic_valid=="sharpe"` subset feeding N equals the concatenation's.
- `test_union_merge_refuses_true_collision`: inject `(run_045, backtest)` on both sides with differing `sharpe` → refuse (never silently pick a side).
- `test_union_merge_is_append_only`: no master row dropped or mutated; fork rows appended.
- **Mutation:** weaken the key to `trial_id`-only → the collision test stops refusing / a legitimate second-source row is dropped → RED. (Mutation-test the guard at its public entry, per fork discipline.)

## Open questions for the joint S4 discussion

1. **Same campaign, or separate?** `campaign_state.yaml` is scoped to ONE `campaign_id`/`research_question`. Do fork trials contribute to master's *current* campaign (append to its `trial_sharpes`), or does the fork run its **own** campaign (own `campaign_state.yaml`, own `campaign_id`) with a separate N? This decides whether S4 is "union into master's campaign" (Option A) or "across two campaign files." **The EPIC's authoritative-ledger decision — "fork trials land via PR" into master's single `campaign_state.yaml` — already tilts toward Option A / same-campaign.** What stays genuinely open is the deeper half: the **holdout-spend budget is global** across all campaigns/attempts, so flag whether global-N (across campaigns, for holdout honesty) is a distinct concern from per-campaign DSR-N. **This is the one genuinely unresolved design question; everything else is mechanics.**
2. **Merge driver vs manual PR-prep tool** — Jeremy's call as ledger owner.

## Fork's recommended answer to Open Question 1 (proposal for the joint discussion)

Selection-bias correction here is **two layers**, and the confusion is from collapsing them. Making both explicit resolves the question and closes a loophole the one-layer view leaves open.

### Layer 1 — within-campaign selection → per-campaign DSR-N (correct as-is)

`deflate_sharpe.compute_dsr` (ds:227) deflates a candidate's Sharpe by the expected max of **N** trial Sharpes (Bailey & López de Prado): larger N ⇒ larger expected-max benchmark ⇒ more deflation. That N is pulled from one `campaign_state.yaml`'s `trial_sharpes` (ds:315→382), i.e. one `campaign_id` / one `research_question`. **The correct question isn't "same or different research topic" — it's "what set did the promoted candidate get selected from?"** DSR's expected-max model presumes the N trials all competed for the *same* selection slot. So:

- Pooling trials that did **not** compete for the same slot makes N *wrong* — and wrong in **either** direction, so "pool everything, over-deflation is the safe side" does not hold. (Pooling also shifts `mu_sr`/`sigma_sr`, not just N, so the magnitude isn't even monotone — it is not a "conservative therefore safe" move, it is a mis-specified one.)
- Two writers researching **different** questions have **disjoint selection sets** → per-campaign N is right for each, no union needed, and their `campaign_state.yaml` files are disjoint → **trivially git-mergeable**. This is the fork's expected case (Jeremy: RSI mean-reversion; fork: Kraken breadth).
- Two writers **co-running one campaign** across two machines (splitting trial *generation* on the same `research_question`) is a deliberate opt-in mode — **there** the selection set genuinely spans both, and S4's union-merge is the normal path (`run_d_NNN` makes it loss-less). This is precisely E-025's "either side's DSR sees only half the attempts."

### Layer 2 — cross-campaign / promotion-to-holdout selection → a family-wise correction (the real gap)

Per-campaign DSR gives **zero** protection against picking the best *across* campaigns. That is not a corner case — it is the exploit that makes Layer 1 alone unsafe: **slice one research program into many small "campaigns," and each per-campaign DSR is nearly undeflated while the N-way selection among campaign winners is counted nowhere.** Under the "separate campaigns is the default" recommendation, Layer 2 is therefore not optional polish — it is the *only* thing standing between cross-campaign cherry-picking and a spent holdout. Two requirements:

1. **Campaign boundaries are pre-registered** — a campaign = a pre-registered `research_question` (same discipline as `HYPOTHESIS.md`), so boundaries can't be drawn post-hoc to launder N.
2. **The shared terminal resource gets a family-wise correction, not just a spend-guard.** A global holdout-spend record **already exists** — `holdout_consumed_by` in `strategy-research/config/campaign_data_policy.yaml:530`, a global list of hypothesis_ids that spent the single holdout evaluation, enforced by `_route_holdout_evaluation` (rpr:4277 refuses a second look; rpr:4298 appends). But it is a **single-use refusal guard, not a correction input**: `len(holdout_consumed_by)` already *is* the global holdout-look count, yet nothing feeds it into a deflation across promotions. **Counting-for-refusal ≠ counting-for-correction.** The gap is a family-wise correction layered *on top of* the existing counter — ideally enriching each holdout-spend record with the selection context it took (`campaign_id`, that campaign's N, how many campaign-level candidates competed for the promotion slot) so the correction is *computable*, not just a count nobody deflates against.

### Reconciliation with the fork's committed bars

This is not a new demand — it reconciles two things already in `CLAUDE.fork.md`:
- The standing "**report best of N tried, N from TRIALS.csv**" bar is a *global* count — that is the Layer-2 / reporting-layer number, distinct from the per-campaign DSR-N of Layer 1. The two-layer frame is what makes both true at once instead of contradictory.
- The fork's committed dual-writer gate (backlog #5) — "**no DSR computation and no holdout touch until both ledgers are merged**" — the Layer-2 correction *extends* that agreed gate to the holdout-promotion layer; it invents nothing new.

### Net (fork's opening position — all Jeremy-joint calls)

- **Default = distinct campaigns per writer** (own `campaign_state.yaml`/`campaign_id`, disjoint files, no union). Note the code seam: `CAMPAIGN_STATE_PATH` (rpr:59) is one hardcoded path today, so "each writer its own file" is a small code change (per-`campaign_id` filenames in master's tree, still landed via PR) — smaller than Option B's merge tool, and it dissolves the union problem for the common case.
- **This refines, not reverses, the EPIC.** "Authoritative ledger" = the *collection* of campaign files in master's tree, every one landed via PR — one *authority*, not one *file*. Nothing in the EPIC decision requires a single file.
- **S4 (union-merge of `trial_sharpes`)** is correctly scoped for the co-run case and worth landing now.
- **Layer 2 is named here, not built here.** Naming it is S4's job (it *is* the answer to "is global-N distinct from per-campaign N"); delivering it would be scope creep. Propose it become its own small epic/issue — *"family-wise correction on top of `holdout_consumed_by`," due before the first holdout touch* — so it can't evaporate.

## Already closed (confirm, don't re-scope)

- The pre-existing `run_054`/`run_059` triplicates (EPIC Done-when #3) were **resolved by Jeremy's S2** (EPIC Log, 2026-08-16: `run_054` byte-identical dedup; `run_059` kept the real-numbers row and dropped the degenerate all-null one, `dedup_note` stamped). S4 should **confirm** #3 is closed, not reopen it.

## Ownership & guardrails

S4 is **joint**. The pure union function + tests are cheap and ours to draft (this doc → a PR when Jeremy's ready). The authoritative-ledger integration (branch, merge driver, PR flow) is Jeremy's. **Nothing here runs a campaign or touches the holdout** — S4 is verified with synthetic two-list fixtures only.
