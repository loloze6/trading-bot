# E-031 S1 — Queue refill sources: characterization and routing policy

**Story:** S1 (characterize and STOP — no production code).
**Scope:** what could legitimately refill `campaign_queue.yaml` when it empties,
what each candidate source can supply TODAY, and the routing policy S3 should
implement.

All counts below are MEASURED by
`strategy-research/engineering/roadmap/E-031/artifacts/s1_measure_refill_sources.py`
(read-only, re-run any time — see that file's docstring). Denominators are
stated with every count. Anything not directly measured is labeled INFERRED
or RECOMMENDATION, not presented as fact.

## Conclusion first

Of the six candidate refill sources examined, exactly **one** has a real,
currently-open, unblocked candidate: the 4h-timeframe branch of the
`funding_rate_continuous_mean_reversion_expanded_auto` KB reactivation clause
— it has never been tested, needs no new data or feed, and its parent
mechanism was already judged structurally sound (not killed) by
`refinement_notes.yaml`'s own routing. Everything else in scope today is
either blocked on infrastructure the loop cannot self-authorize (a feed, a
predicate re-evaluation nobody wires up), already measured and failed (P4
daily reactivation, 2026-08-23), or not mechanically discoverable at all
(refinement-planner's deferred branches, buried in per-run artifacts with no
index).

The queue-entry schema has a real, load-bearing gap: **there is no legal way
for an entry to say "a machine minted this."** `source` is a closed 3-value
enum (`agent`, `operator_ratified`, `user_delivered`) and the schema is
deny-by-default — an unenumerated field or value is a hard validation error,
not a warning. S3 cannot ship without touching `tools/record_schema.py`.

The recommended policy (detailed in Task 3): auto-mint candidate entries into
a **paused, human-ratified** state, never straight to `ready`; treat "zero
admissible candidates" as a legitimate, instrumented terminal state, not a
failure to paper over; and rely on the *existing*, already-correct per-run
trial-recording machinery for Done-when #3, adding only a disjoint run-ID
prefix so a third writer (the loop itself) doesn't collide with E-025's two
human writers.

---

## Task 1 — candidate seed sources, measured today

### How I searched
Read `campaign_state.yaml`, `campaign_record/feed_wishlist.yaml`,
`campaign_record/campaign_knowledge_base.yaml`, `config/detector_wishlist.yaml`,
`config/available_feeds.yaml`, `config/coin_universe.yaml`,
`config/campaign_queue.yaml`, `workflow/stages.yaml` in full. Grepped the
whole `strategy-research/` tree for `refinement_planner`,
`register_hypothesis(`, `evaluate_and_persist_wishlist_predicate(`,
`reactivation_condition`, `trigger_condition`. Read all 4
`refinement_notes.yaml` files that exist on disk. Cross-checked every
wishlist/reactivation candidate against the config file that would actually
gate it (`available_feeds.yaml` for feed asks, KB `exhausted`/`kb_state_hash`
for reactivation clauses).

### `campaign_state.yaml` (1 file, `campaign_record/campaign_state.yaml`)

This file is **exclusion context**, not a generative source — its job is to
stop a refill mechanism from re-treading dead ground, not to propose new
ground.

- `failed_families`: **9** named families (denominator: this list). All 9
  are 1h-timeframe families; a same-signal daily or 4h variant is not
  automatically excluded by this list (family names are timeframe-scoped by
  convention, e.g. `sma_trend` vs `P4_SMA_TREND_LONGONLY_DAILY`).
- `altitude_history`: **39** entries total; **4** carry `outcome: escalate`
  (denominator: the altitude_history list) — these are the only entries in
  this file that read as "the loop already decided to try a new axis":
  `run_020`/`run_047` → timeframe, `run_027`/`run_029` → instrument. Of the
  4: the timeframe escalation was claimed and executed (`last_escalation`
  field: target=timeframe, detail=15m, `claimed_by_run: run_049` — 15m is
  already in `timeframes_tried`). The two instrument escalations were never
  formally closed by this field, but XS_momentum's later, unrelated 19-pair
  panel work (2026-07-22) substantively answered "try more instruments" on a
  different statistic — untracked here.
- `recent_parameter_dimensions_by_family`: **4** families tracked, only
  **1** (`fear_greed_contrarian: [signal_polarity]`) has a non-empty
  dimension list (denominator: this dict). The other 3 are empty lists —
  nothing to exclude on for those families.
- `instruments_tried`: **4** (`BTCUSDT, ETHUSDT, SOLUSDT, AVAXUSDT`). Cross-
  checked against `config/coin_universe.yaml` (22 symbol entries) and
  `campaign_queue.yaml`'s XS_momentum note (ratifies a 19-pair Kraken
  universe, 2026-07-22). **This field is stale** — it was never updated when
  the 19-pair universe was ratified, five weeks before the loop went idle.
  A refill policy that trusts it as-is will under-count what's actually been
  tried.
- `timeframes_tried`: **3** (`1h, 4h, 15m`). Daily bars now exist for
  BTC/ETH (P4 work) but this field doesn't reflect it either — same
  staleness pattern.

### `campaign_record/feed_wishlist.yaml` (1 file)

**1** live entry (denominator: the `wishlist` list — the file's own
"Example entry (template)" block is a `#` comment, excluded by `safe_load`):
`liquidation_data`, blocking `H-041-B`. Cross-checked against
`config/available_feeds.yaml`: `liquidation_data` is still listed under
`unavailable` (`route: feed_wishlist`). **Not actionable today** — this
entry names a missing capability, not a testable hypothesis, and moving it
to available is an infrastructure decision outside the loop's own authority
(nothing in this repo wires a feed into `available_feeds.yaml`
autonomously).

### `campaign_knowledge_base.yaml` (1 file) — reactivation clauses

The file has two distinct record classes: `findings` (**19** entries,
hypothesis-outcome records — the correct denominator for
`reactivation_condition`) and `meta_findings` (**3** entries, process/
methodology records that don't carry `reactivation_condition` by design).
`exhausted_mechanisms` (6 entries) is a cross-reference index into
`findings`, not additional records.

Of the 19 `findings`, **3** carry a non-null `reactivation_condition`:

1. **`volume_impulse_continuation_blocked`** (H-041-B) — reactivation
   requires a liquidation feed. Same feed as the wishlist entry above.
   **NOT satisfied** (feed unavailable).
2. **`funding_rate_continuous_mean_reversion_expanded_auto`**
   (FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED) — reactivation names
   two branches: re-test the same mechanism at 4h *or* daily. The daily
   branch was already registered and run (`FUNDING_MR_DAILY_RETEST`,
   `run_059`, closed `completed_rejected` — a real kill on measured funding
   P&L, per the KB's `funding_mr_daily_retest_killed` entry, which states
   explicitly: *"The 4h branch of the parent reactivation_condition remains
   DEFERRED and is untouched."* **The 4h branch is genuinely open** — no
   data gap, no engine gap, mechanism already judged structurally sound
   (`refinement_notes.yaml` for the precursor run, see below, called it
   "SOUND... Parameter mismatch is the issue, not mechanism failure").
   This is the strongest candidate found anywhere in this search.
3. **`p4_sma_trend_longonly_daily_auto`** (P4_SMA_TREND_LONGONLY_DAILY) —
   already measured 2026-08-23 and **FAILED on power**: daily-panel n_eff
   1.661 (all-19) / 1.694 (primary-17) vs a required ≥3.0
   (`briefs/artifacts/p4_daily_reactivation_20260823/`). Not actionable; a
   worked example of a reactivation clause resolving to "no."

### `config/detector_wishlist.yaml` — found via search, not in the task's named list

**3** candidate regime-detector families
(`daily_timeframe_er_overlay`, `adx_threshold`, `hidden_markov_model`), each
with a structured, machine-checkable `trigger_condition.predicate` — the
same shape as `feed_wishlist.yaml`'s gating idea, one level more mechanical.
All 3 read `status: not_triggered`, `last_evaluated_at: '2026-07-10'`.

This status **cannot be trusted as current**. The file's own header
declares a "SINGLE-AUTHORITY CONTRACT": only
`run_campaign.py::evaluate_and_persist_wishlist_predicate()` may write
`status`/`last_evaluated_at`/`kb_state_hash`. A repo-wide grep (script
output, `s1_measure_refill_sources.py`) finds **zero callers** of that
function anywhere — it is dead code. `campaign_knowledge_base.yaml` has been
modified after `detector_wishlist.yaml` (mtime comparison confirms this,
and substantively: ~15 findings postdate 2026-07-10, including the entire
P4/MACD/XS_momentum/funding-daily record). The pinned `kb_state_hash` is
stale by construction, and nothing in the current codebase can refresh it.
This is a second, independent instance of the same failure shape the EPIC
already found in `register_hypothesis` (a write path that exists, is
correctly designed, and has no caller).

### refinement_planner's deferred/untaken branches

`refinement_notes.yaml` exists for **4 of 59** run directories
(denominator: `runs/run_*` count). Read all 4:

- `run_0001`, `run_002`, `run_003` are pre-implementation blocker lists
  (data-availability audits, lookahead-contamination checks) — not
  alternate hypothesis branches.
- `run_050` (H-041-A) is the one genuine example: `decision.primary_path`
  names one option taken (REFRAME to backward-extension prescreen) and two
  named-but-untaken alternatives (vol-gating on 1h; a 4h-timeframe variant).
  The taken path ran and closed the underlying KB entry
  `exhausted: true` ("no further reactivation of this same formulation is
  defensible", well-powered null, n_episodes=139). The 4h-timeframe
  alternative overlaps with the KB reactivation clause found above
  (`funding_rate_continuous_mean_reversion_expanded_auto`'s 4h branch) — same
  idea, but that KB entry already carries the evidentiary apparatus this
  per-run note doesn't (an `exhausted` flag, a `reactivation_condition`
  someone will actually check).

**Verdict: not a usable mechanical source today.** One real example in 59
runs, no cross-run index, and the one instance found is subsumed by a
KB-level source that's already more rigorous. Building a scanner for this
in S3 would be duplicate machinery for no marginal supply.

---

## Task 2 — mechanics, from source

**`_select_entry`** (`workflow/run_campaign.py:140-152`): an entry with
`status == "in_progress"` always wins (first match, unconditionally — this
single-process wrapper assumes at most one active lineage). Otherwise the
lowest-`priority`-number entry with `status == "ready"`. Anything else —
`done`, `blocked_on_*`, `paused:*`, or any status this schema doesn't even
enumerate — is never selected; there is no suffix whitelist, so a novel
`blocked_on_*` string is inert by construction, not by an explicit check.
Measured today: `campaign_queue.yaml` has 4 entries, 3 `done` + 1
`blocked_on_daily_bar_ingest`, 0 schedulable.

**`QUEUE_ENTRY_SCHEMA`** (`tools/record_schema.py:195-205`) is closed and
deny-by-default (`validate_record_schema`, lines 336-362: any field not
explicitly enumerated is a hard error, listing all violations, not just the
first). Permitted fields: `id, brief_path, notes, status, priority, source,
relation, run_ids, outcome, verdict_status, verdict_status_basis,
verdict_void_reason, pass_rule_evaluation_ref, refinement_brief_path,
refinement_brief_consumed_for`, plus two dated correction-family patterns.
**`source` is a closed 3-value enum: `{agent, operator_ratified,
user_delivered}`** (line 120). None of the three means "a machine minted
this without a human authoring or ratifying it." **A queue entry cannot
legally express "this was auto-generated" today** — not via `source` (no
value fits) and not via a new field (the schema rejects any field it
doesn't already know about). This is a real, load-bearing finding, not an
inference: confirmed by reading the enum and the deny-by-default validator
directly.

**`register_hypothesis`** (`run_campaign.py:354-397`) requires a real brief
file that passes `_parse_brief_frontmatter` — 6 required frontmatter fields
(`strategy_domain, market_universe, timeframe, research_goal, venue,
product`). It hardcodes `source: "operator_ratified"` and
`relation: "new_registration"` unconditionally, regardless of who or what
invoked it. Repo-wide grep: **1 non-test caller** (the CLI argparse dispatch
at line 2119) plus 4 test call sites. Zero in-pipeline callers, confirming
the EPIC's claim exactly.

**No stage authors a brief from nothing.** `stages.yaml`'s `research_brief`
entry (lines 4-8) is the one stage with no `skill:`/`tool:` key at
all — it is not an executable stage, it's the operator-supplied entry point.
`hypothesis_generation` (lines 10-19, `hypothesis-design/SKILL.md`)
*requires* an existing `research_brief.yaml` as input; its mission is to
elaborate an existing research question into a hypothesis, not invent the
question. `campaign_review` (lines 110-118) can write a prose
`next_research_question` recommendation into `campaign_review.yaml`, but
that's unstructured text inside an artifact, not a brief file with the 6
required fields — and it declares `next: []`, so nothing consumes it
automatically today. So: refill needs a brief; nothing in the pipeline
currently authors one; the closest existing artifact
(`campaign_review.next_research_question`) is prose, not parseable brief
frontmatter, and is orphaned by an empty `next:`.

**`_write_loop_health()` call sites** (4 total: lines 1801, 1932, 1944,
1968) are all reached strictly *after* `entry = _select_entry(...)` returns
non-`None` (each sits inside a branch keyed off a real `entry`). The
exhaustion path — `entry is None` at line 1764, one `_log()` call, then
`return False` at line 1766 — has no `_write_loop_health()` call anywhere
between it and the function's end on that branch. **Confirmed, not
refuted**: the loop-health block never runs on the one condition that
actually stopped the loop.

---

## Task 3 — recommended routing policy

### Legitimate sources, ranked by what they can supply today

1. **KB reactivation clauses, re-evaluated against current state.** The
   only source with a built-in evidentiary bar (a mechanism already
   scrutinized once; a disposition that requires explicit re-checking, not
   just re-proposing). Of 3 found, 1 is genuinely open today (funding-MR 4h
   branch), 1 is blocked on an unowned infra decision (liquidation feed),
   1 already resolved to "no" (P4 daily). **Legitimate first-priority
   seed**, but see "what must be true before launch" below — legitimate
   does not mean auto-launchable.
2. **`detector_wishlist.yaml` predicates, once actually re-evaluated.**
   Legitimate in principle (structured, machine-checkable, already gated
   against premature consumption by `_check_wishlist_trigger`'s hard-pause
   behavior). Not usable today because the one function contracted to
   refresh its status has never been called — S3 must wire that call in
   before this source can supply anything real; until then treat it as
   informative-but-stale, not silently trusted.
3. **`feed_wishlist.yaml`** — not a hypothesis source by itself, correctly
   gated behind `available_feeds.yaml`. Leave it as a human-triggered
   infrastructure decision; the loop has no business promoting a feed from
   unavailable to available on its own authority.
4. **`failed_families` / `altitude_history` / `recent_parameter_dimensions_
   by_family` / `instruments_tried` / `timeframes_tried`** — exclusion
   context only, never generative on their own. Any candidate minted from
   sources 1-2 must be checked against `failed_families` and
   `recent_parameter_dimensions_by_family` before minting. Given
   `instruments_tried`/`timeframes_tried` are demonstrably stale (measured
   above), S3 should not trust them uncorrected — either refresh them as
   part of this work or explicitly exclude them from the auto-check and say
   so in the routing record.
5. **refinement_planner's deferred branches** — not a source to build
   machinery for. Too sparse (1 usable example in 59 runs), not indexed,
   and the one real example is already subsumed by source #1.

### The honest terminal state: zero admissible candidates

This is a **legitimate answer**, and it should be the *default* outcome
recorded whenever it's true, not something the routing logic works around.
Concretely: if the ranked scan above (reactivation clauses checked, wishlist
predicates freshly evaluated, exclusion filters applied) yields nothing, the
schedulability block S2 builds should record *why* (e.g. "0
reactivation-eligible, 0 wishlist-triggered, checked at <timestamp>") and
`process_once()` should still return `False` — but now with a documented,
inspectable reason, not a silent one-line log. **This is my recommendation,
not an existing convention** — nothing in the current codebase already does
this for the idle-queue case (that's the gap E-030's instrument left, per
the EPIC). Escalating to a human at that point is correct and sufficient;
E-031 is plumbing, not judgment, and manufacturing a candidate merely to
avoid returning `False` would be worse than the current silence.

### What must be true before an auto-minted entry may be launched

a. **A real brief file exists**, satisfying `_parse_brief_frontmatter`'s 6
   required fields. Nothing in the pipeline authors this today (Task 2).
   Recommend S3 does **not** attempt to synthesize brief content from a
   reactivation clause's prose — those fields are free text, not
   structured enough to parse safely into `research_goal`/`market_universe`
   etc. without risking a silently wrong brief. A human authors or ratifies
   the brief before the entry can move past its minted state.
b. **The schema gap closes first.** `tools/record_schema.py` needs a real
   `source` value for machine-minted entries (e.g. `system_refill`) and a
   new field to record seed provenance (e.g. `seed_ref`, pointing at the KB
   finding or wishlist family id) — added deliberately, per the schema's
   own instruction at its rejection message ("add it there WITH a declared
   shape"). This is production code, out of scope for S1, but S3 cannot
   ship without it.
c. **Exclusion checks pass** against `failed_families` and
   `recent_parameter_dimensions_by_family` (refreshed or explicitly
   bypassed, per the staleness finding above).
d. **Off by default**, per the epic's Done-when #4, with a bit-identity
   test proving the exhaustion path is byte-for-byte unchanged when the
   flag is off.
e. **Never auto-`ready`.** Recommend the minted entry lands in
   `status: paused:pending_operator_ratification` — this fits the existing
   `QUEUE_STATUS` regex (`paused:.+`) **without a schema change** to the
   `status` field itself, only to `source`/`seed_ref`. A human flips it to
   `ready` exactly like resuming any other pause today. This is a
   recommendation, not a discovered constraint — the schema permits either
   choice; I'm arguing for the more conservative one given E-031's own
   scope boundary against E-032 ("the plumbing that lets an idea reach the
   queue" vs "decides whether the idea is worth having" — auto-`ready` would
   quietly make E-031 also decide the idea is worth *running*).

### Trial accounting for auto-minted entries, cross-checked against E-025

Task 2 established the mechanism precisely: `_record_prescreen_trial` /
`_record_backtest_trial` (in `run_phase1_research.py`, per E-025 S1) fire
per-**run**, keyed by `run_id`, at fixed pipeline stages
(`signal_prescreen`, `protocol_execution`) — they do not read the queue
entry's `source` field at all. So **once an auto-minted entry is actually
launched** through the normal `_materialize_run` → `setup_run` →
`run_phase1_research` path, its trial accounting is already correct and
already covered by E-025's S1/S2 machinery (mandatory `forecast_hash`,
`(trial_id, source)`-keyed idempotency, `deflate_sharpe.py`'s
duplicate-`trial_id` refusal). **Done-when #3 is largely already satisfied
by existing infrastructure, provided one condition holds**: the auto-minted
run's `run_id` must not collide with either existing writer's allocation.

E-025 already established two disjoint schemes: `run_NNN` (master/Jeremy)
and `run_d_NNN` (Dorian's fork). E-031's own EPIC.md already names the
consequence — *"A machine writer is a third writer"* — so S3 must allocate
auto-launched runs from **a third disjoint prefix** (e.g. `run_a_NNN`),
mirroring `_next_new_run_id()`'s existing scan-both-sources approach rather
than reusing its bare `run_NNN` output, and this must land in coordination
with (not ahead of) E-025's S4 union-merge work so a third scheme doesn't
need its own bespoke merge logic.

The actual residual risk to "N stays honest" is **not** the trial-recording
mechanism — it's whether S3's own refill logic could evaluate and discard a
candidate *before* any run exists, with no trace left behind. That's
correct behavior for N (no market data touched, no trial owed — mirrors
`_apply_trial_accounting`'s existing `component_gap` case, which
legitimately does nothing because nothing was measured), but the *decision*
itself should still be auditable — S3 should log which candidates were
considered and why they were or weren't minted, in the same schedulability
block S2 introduces, so "the loop looked and found nothing" is a recorded
fact, not a silent absence someone has to re-derive later (same principle
`_run_has_trial_row`'s docstring already states for the quarantine record).

### What S3 should build (dispatch-ready)

1. **Run-ID prefix for machine-launched runs** (e.g. `run_a_NNN`) — extend
   `_next_new_run_id()` with a `prefix` parameter or add a sibling function
   using the same scan-both-sources logic. Coordinate with E-025 on
   disjointness from `run_NNN`/`run_d_NNN`.
2. **Schema change** (`tools/record_schema.py`): add one `SOURCE` enum value
   (e.g. `system_refill`) and one new `TEXT` field on `QUEUE_ENTRY_SCHEMA`
   (e.g. `seed_ref`) to record which KB finding or wishlist family produced
   the candidate.
3. **A refill function**, called from `process_once()`'s exhaustion branch
   (`run_campaign.py:1764-1766`), before the existing `_log`/`return False`:
   a. Call `evaluate_and_persist_wishlist_predicate()` for each
      `detector_wishlist.yaml` candidate — closes the dead-caller gap found
      in this story.
   b. Scan `campaign_knowledge_base.yaml`'s `findings` for
      `reactivation_condition` not null and `exhausted` false; re-verify
      each named condition against its current source (feed availability,
      sibling KB entries, etc.) — do not trust a cached disposition.
   c. Filter survivors against `failed_families` and
      `recent_parameter_dimensions_by_family` (refreshed per the staleness
      note, or explicitly documented as skipped).
   d. If zero candidates survive: write the "0 admissible" reason into S2's
      schedulability block; `process_once()` still returns `False`, now
      with an inspectable reason.
   e. If ≥1 candidate survives: mint one new queue entry —
      `status: "paused:pending_operator_ratification"`,
      `source: "system_refill"`, `seed_ref` populated, `run_ids: []` — and
      stop. No brief-authoring, no auto-`ready`.
4. **Brief-authoring is explicitly out of scope for S3** — either a human
   writes it as part of ratification, or it's E-032's problem. S3's job
   ends at minting a schema-valid, auditable, non-launchable-without-a-human
   candidate.
5. **Flag**: off by default (e.g. `--enable-auto-refill` or a
   `campaign_config.yaml` boolean). Bit-identity test: flag off →
   `process_once()`'s exhaustion path produces the exact same log line,
   same return value, no new files written.
6. **Tests**: schema validation of the new `source` value and `seed_ref`
   field; the refill filter logic against fixture KB/queue data (reactivation
   scan, wishlist evaluator wiring, exclusion checks); the flag-off
   bit-identity test; a test asserting an auto-minted entry's `status` is
   never `"ready"` straight out of the refill function.

---

## Files read / referenced

- `strategy-research/engineering/roadmap/E-031/EPIC.md`
- `strategy-research/campaign_record/campaign_state.yaml`
- `strategy-research/campaign_record/feed_wishlist.yaml`
- `strategy-research/campaign_record/campaign_knowledge_base.yaml`
- `strategy-research/config/available_feeds.yaml`
- `strategy-research/config/detector_wishlist.yaml`
- `strategy-research/config/coin_universe.yaml`
- `strategy-research/config/campaign_queue.yaml`
- `strategy-research/workflow/run_campaign.py`
- `strategy-research/workflow/stages.yaml`
- `strategy-research/workflow_artifacts/skills/hypothesis-design/SKILL.md`
- `strategy-research/workflow/setup_run.py`
- `strategy-research/tools/record_schema.py`
- `strategy-research/runs/run_0001,002,003,050/artifacts/refinement_notes.yaml`
- `strategy-research/engineering/roadmap/E-025/EPIC.md`
- `strategy-research/briefs/artifacts/p4_daily_reactivation_20260823/` (referenced, not re-derived)
