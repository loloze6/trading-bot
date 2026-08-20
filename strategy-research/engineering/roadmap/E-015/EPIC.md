# E-015 — Venue/product declared at brief registration

**State:** done
**Owner:** Jeremy
**Updated:** 2026-08-20

## Why

Source: `docs/ROADMAP.md` §1.3, verbatim: "**Registration rule: venue
declared.** Objective: no more testing on an unauthorized system's
assumptions. Deliverable: every new brief states venue + product; anything
using a product not legally tradable for you is auto-flagged **research-only**
at registration. Immediate consequence to settle: whether the funding family
is live-tradable at all (perp access), or research-only."

Of the seven items in the audit, this is the only one actionable today with
nothing in front of it — no dependency on E-010, E-012, or a phase gate.

**VERIFIED (dispatch W38, tree audit) — Done-when #2 and #3 already shipped**
(2026-07-21, before this epic existed): `config/venue_tradability.yaml` is
the single source of truth for (venue, product) legality, consumed by
`workflow/run_campaign.py:265-277`'s `_materialize_run()`, which writes
`research_brief["research_only"] = not tradable` for every run — with 7 tests
(`tests/test_venue_tradability.py`) covering the tradable/unconfirmed/absent/
undeclared cases. The immediate consequence (Done-when #3) is also recorded:
`campaign_knowledge_base.yaml`'s `funding_mr_daily_retest_killed` entry
carries `venue_live_tradability` — Kraken perp is legally tradable but the
family stays `research_only` pending a funding-cash-flow model.

**Done-when #1 — VERIFIED NOT MET, and the design question it turns on is
now settled:** dispatch W38 traced whether `research_only`, once written into
`research_brief.yaml`, is checked anywhere downstream — promotion, walk-forward,
or the sealed holdout. It is not: `research_only` is written exactly once
(`run_campaign.py:274`) and never read again by any code path
(`workflow/run_phase1_research.py`, `tools/run_protocol.py`, and
`workflow/setup_run.py` all have zero references to the key; the only other
occurrence in the whole tree is `tools/record_schema.py`'s `FLAG` field, an
unrelated Notion/KB-record annotation, not an enforcement check). A brief
missing venue/product today gets `research_only: true` silently and nothing
stops it from proceeding through the pipeline like any other run — the soft
default is **decorative** without a downstream consumer. Per the shipped
design, a missing venue/product field does not fail registration (it defaults
to `research_only: true` instead), so Done-when #1 as originally written
("registration of a brief missing either fails") is NOT met by the shipped
code, and — because nothing downstream enforces `research_only` either — the
soft default cannot currently substitute for it. Done-when #1's hard-fail
requirement is KEPT for this reason; a story is added for the enforcement gap
it exposes.

## Done when

1. The brief registration schema requires a venue field and a product field;
   registration of a brief missing either fails rather than proceeding with
   an implicit default. **MET 2026-08-20** (S1b) — `_parse_brief_frontmatter`
   raises on either field missing, at the actual registration choke point.
2. At registration, any brief whose declared product is not legally tradable
   for the operator (French non-professional) is auto-flagged
   `research-only`, without a manual step. **MET** — `run_campaign.py:265-277`,
   `config/venue_tradability.yaml`, 7 tests.
3. The immediate consequence named in the source text is settled as part of
   enacting this rule: whether the funding family is live-tradable (perp
   access) or `research-only` is decided and recorded. **MET** —
   `campaign_knowledge_base.yaml`'s `funding_mr_daily_retest_killed.venue_live_tradability`.
4. NEW: `research_only: true` is actually enforced at at least one downstream
   gate (promotion, walk-forward, or the sealed holdout) — today it is
   written and never read again. **MET 2026-08-18** — `_route_holdout_evaluation`
   gate 2b (below the two terminal rejects, above the human-pause branch). Enforced in the stronger affirmative
   form: the holdout requires `research_only is False`, so an undeclared or
   unpropagated brief refuses rather than passes.

## Stories

- [x] S1a — Add venue + product as required fields to the brief registration
      schema/contract; wire the auto-flag for products not legally tradable
      for the operator. DONE 2026-07-21, `run_campaign.py`/
      `config/venue_tradability.yaml`, 7 tests (shipped before this epic
      existed; not tracked here at the time).
- [x] S2 — Settle and record the funding family's venue status (live-tradable
      perp access vs. research-only) as the rule's first application. DONE
      2026-07-20, `campaign_knowledge_base.yaml`.
- [x] S1b — **DONE 2026-08-20.** Make missing venue/product a hard registration
      failure (Done-when #1, as originally specified) rather than a silent
      `research_only` default. `_parse_brief_frontmatter` (`run_campaign.py`,
      the single choke point both fresh-launch call sites and
      `register_hypothesis` go through) now requires `venue` and `product`
      alongside its 4 existing required fields, raising the same `ValueError`
      it already raises for those. `_materialize_run`'s own fail-closed
      default (`_venue_product_tradable`'s "missing → not tradable") is left
      untouched as a defensive fallback for any caller that constructs a
      brief dict directly instead of going through the parser (e.g.
      `test_venue_tradability.py`'s existing direct-dict tests, which still
      pass unchanged). 4 new tests, 2 confirmed to fail against the pre-fix
      code before being folded in. One pre-existing test fixture
      (`test_k3_protocol_pinning.py::_VALID_BRIEF_FRONTMATTER`) needed
      venue/product added to stay valid under the new requirement — not a
      regression, a fixture catching up to the tightened contract.
- [x] ~~S3a — Make `research_only` propagate.~~ **DROPPED 2026-08-18** as
      over-engineering (Jeremy's call). Made unnecessary by S3's affirmative
      form: requiring `research_only is False` means a child that inherits
      nothing inherits no permission either, so propagation machinery buys
      nothing a one-line predicate does not already give.
- [x] S3 — **Enforce `research_only` at the holdout gate. DONE 2026-08-18**
      (gate 2b of `_route_holdout_evaluation`), below the two terminal rejects
      and ahead of the human-pause branch. Affirmative check, fail-closed,
      returning `human_pause` + a `research_only_unverified` flag with its own
      classifier bucket and RUNBOOK row (see convention #2 — the original
      `completed_rejected` plan was superseded in review). 17 tests, 14
      mutations killed across 8 review rounds. Closes Done-when #4.

## S3 Phase A — characterization (2026-08-18) — resolved, see Log

Run before writing any enforcement, per the two-phase convention. It found
the story as scoped was **not implementable as one change**, for a reason
that was not visible from the epic's own earlier tracing.

**Finding 1 — the flag is written by 1 of 3 writers, so it does not inherit.**
`research_brief.yaml` has three producers:

| Writer | Path | Sets `research_only`? |
|---|---|---|
| `run_campaign.py:277` `_materialize_run()` | fresh campaign launch | **yes** |
| `run_phase1_research.py:1622` `_safe_write_new_research_brief()` | campaign_review reframe | no |
| `run_phase1_research.py:1647` `setup_next_run()` | refine (`shutil.copy` of `proposed_brief.yaml`) | no |

(`_materialize_refinement_run` at `run_campaign.py:423` writes only
`pre_registration.yaml`, never `research_brief.yaml`.)

So a brief correctly flagged `research_only: true` at launch loses the flag
the moment it is refined or reframed — the child's brief is a copy of an
LLM-authored `proposed_brief.yaml`, which carries no such key. **Measured: 0
of 27 `proposed_brief.yaml` files carry it.** A flagged hypothesis's
grandchild reaches the holdout with a clean brief. That is a propagation
defect sitting underneath the enforcement defect, and enforcement alone
would produce a gate with a documented bypass.

**Finding 2 — nothing in the corpus carries the key at all.** Measured
across the live tree: **0 of 57** existing `research_brief.yaml` files
contain `research_only`. The venue wiring shipped 2026-07-21; every run
predates it or came through a non-setting writer. This kills both naive
implementations:

- *"block when `research_only is True`"* → protects nothing today, on any
  existing run, and stays inert until a fresh campaign launch happens.
- *"block when the key is missing"* (fail-closed, matching this project's
  usual doctrine) → **blocks all 57 existing runs from the holdout.** Correct
  in spirit, unusable as a default without a migration decision.

**Finding 3 — lineage cannot substitute.** Resolving the flag by walking a
run's ancestry at gate time was considered instead of propagation, and is
not viable: only **4 of 59** runs carry a `lineage` block in
`pre_registration.yaml`.

**Finding 4 — where the gate belongs, and a subtlety about *which line*.**
`_route_holdout_evaluation` (`run_phase1_research.py:4322`) is the right
place: it is the single choke point, and it already hosts the DSR gate and
the single-use refusal. But the check must sit **before step 3's
`human_pause`**, not merely before step 4's `holdout_consumed_by` write.
Step 3 prints *"Run the holdout backtest on this range"* — a human obeying
that instruction opens the sealed data, and in this project's own doctrine
**looking is spending**. A check placed only ahead of the consumption
bookkeeping would fire after the seal was already spent in practice.

**Pre-registered conventions for S3a/S3b, for the nod:**
1. S3a propagates by *writing the resolved flag at every writer*, not by
   inheriting a parent value — re-resolve `venue`/`product` through
   `_venue_product_tradable()` at each write, so a refine that legitimately
   changes venue is re-evaluated rather than inheriting a stale verdict.
2. ~~S3b blocks with `return "completed_rejected"`~~ — **SUPERSEDED during
   code review, 2026-08-18.** Shipped as `human_pause` plus a
   `research_only_unverified` flag and its own `_classify_human_pause`
   bucket. Two findings forced it: `completed_rejected` writes
   `status="rejected"`, which `resume_pipeline` refuses to resume, so it
   terminally killed legitimately-tradable refine/reframe descendants (which
   land here as a matter of course, since the flag does not propagate); and a
   *bare* `human_pause` was worse still — it classified as
   `provisional_promote_awaiting_holdout`, whose RUNBOOK row instructs the
   operator to run the holdout backtest by hand, i.e. to spend the seal this
   gate protects. The flag is what makes the pause safe, not decoration.
3. Missing key: treated as `research_only: true` (fail-closed, matching
   `venue_tradability.yaml`'s own "silence must never resolve to a green
   light"), **but** gated behind an explicit migration for the 57 existing
   runs — either a one-off backfill or a dated grandfather list. Not chosen
   here; it is an operator call, and the wrong choice either blocks all
   existing work or silently exempts it.
4. Bit-identity: no existing run's artifacts change; the gate only adds a
   refusal branch.

## Log

- 2026-08-05 — `new`. Created from E-013 S1's audit of `docs/ROADMAP.md` §1.3
  (dispatch W35). No dependency; ready to dispatch.
- 2026-08-05 — `new` → `in-progress` (dispatch W38). Tree audit found S1's
  auto-flag half and S2 already shipped 2026-07-21/07-20, before this epic
  existed. Traced `research_only` end-to-end and found it is written once and
  never read again — no downstream enforcement exists. Done-when #1's
  hard-fail requirement is kept (the soft default cannot substitute for it
  while nothing reads the flag); split into S1b (hard-fail on missing fields)
  and new S3 (downstream enforcement), added as Done-when #4.
- 2026-08-05 (dispatch W39) — Stating plainly what W38's finding above means:
  the flag is written once (`run_campaign.py:274`) and read nowhere, so the
  auto-flag currently provides **no protection at all**. Nothing stops a
  `research_only` brief from reaching the sealed, single-use holdout
  undetected. This is a **safety gap, not a completeness gap** — S3 is not a
  nice-to-have follow-on, it is the only thing standing between a
  non-tradable/unconfirmed-venue brief and a live-money decision made on
  research-only evidence. Notion 🐛 Bugs & Tasks card filed
  (https://app.notion.com/p/3b31d1fb05a281ce802bdf7d947224d9), tagged to this
  epic per amendment 6 (Area: Research pipeline, Priority: High) — the card is
  a pointer only, this EPIC.md stays authoritative. No enforcement
  implemented in this dispatch; scoping where the check belongs (promotion,
  walk-forward, holdout entry, or all three) is S3's design work, not a
  bookkeeping fix.
- 2026-08-15 — `in-progress` → `planned` (PROCESS.md amendment 11). No story
  has actually been dispatched under this epic since W39 — 10 days at
  `in-progress` with zero log activity, same pattern as E-014/E-016.
  Corrected to reflect reality. S3 (the load-bearing safety gap) stays the
  next real step whenever this is picked up.
- 2026-08-18 — `planned` → `in-progress`. S3 dispatched, Phase A only (the
  two-phase convention: characterize and STOP). **Result: S3 as scoped is not
  one change.** The epic had established that `research_only` is never READ;
  Phase A found it is also never PROPAGATED — written by 1 of the 3
  `research_brief.yaml` writers, so it does not survive a refine or reframe
  (0 of 27 `proposed_brief.yaml` carry it). Enforcing alone would ship a gate
  with a built-in bypass for every descendant run. Also measured: 0 of 57
  existing briefs carry the key at all, which makes the fail-closed default
  this project would normally reach for block every existing run from the
  holdout — a real operator decision, not a detail. Split into S3a
  (propagate) and S3b (enforce, blocked behind S3a); conventions
  pre-registered in the Phase A section above. **Nothing implemented; stopped
  for the nod.** Note the correct insertion point is ahead of the gate's
  human-pause branch, not merely ahead of its `holdout_consumed_by` write —
  the pause instructs a human to run the holdout backtest, and looking is
  spending.
- 2026-08-18 (later) — **S3 DONE; S3a dropped as over-engineering (Jeremy).**
  Phase A had framed this as two stories (propagate, then enforce) plus a
  migration decision for 57 legacy runs. Two further measurements collapsed
  all of that: **0 of 57 briefs declare `venue` or `product` at all** (so the
  registration mechanism has never been exercised on a real brief), and **0
  runs have ever reached the holdout gate** — `holdout_consumed_by` is empty,
  the seal has never been touched. There is therefore no legacy corpus to
  migrate and no flag anywhere to propagate; both problems were hypothetical.

  Shipped instead as a single affirmative check at
  `_route_holdout_evaluation`'s gate 2b: the holdout requires
  `research_only is False` and refuses anything else. The affirmative form is
  what makes S3a unnecessary — a child run that inherits nothing inherits no
  *permission* either, so the propagation defect stops being exploitable
  without any propagation machinery. It also does S1b's job in the place that
  matters: the first run this ever blocks is fixed by declaring venue/product
  on its brief, which is exactly the registration rule this epic exists to
  enforce. S1b stays open as the belt-and-braces version at registration time,
  no longer load-bearing.

  Fail-closed was adopted outright rather than phased, because the
  measurements above prove it blocks nothing that exists. 9 tests, and the
  three mutations that matter all killed: gate removed → 8 red; the
  *decorative* `is True` variant → 5 red (this is the one that would have
  looked correct and protected nothing); gate relocated after the human-pause
  branch → 8 red. One real bug caught by the tests before shipping: a run dir
  with no `research_brief.yaml` crashed with `FileNotFoundError` instead of
  refusing, since `load_yaml` raises rather than returning None.
  Both suites green.

- 2026-08-18 (later) — **Eight adversarial review rounds on the shipped gate.**
  Round 1 found three real defects in the delivery (a red CI I had pushed
  without re-checking; a terminal `completed_rejected` that killed legitimate
  refine/reframe descendants; a `--check` that always exited 0). Rounds 2-8
  were almost entirely defects in the FIXES rather than in the original work,
  and the two worst were mine: a bare `human_pause` classified as
  `provisional_promote_awaiting_holdout`, whose RUNBOOK row tells the operator
  to run the holdout backtest — routing them into spending the seal this gate
  exists to protect, strictly worse than the bug it replaced; and an
  `update_state` "hardening" that removed a crash loop but silently zeroed
  `audit_log`, handing a run its full weighted token budget again (reverted,
  with the reasoning recorded in-code so it is not retried).

  Also found and fixed: the flag was never cleared, deadlocking the documented
  recovery path; the gate sat above two terminal rejects and halted whole
  campaigns for runs that would be rejected anyway; the RUNBOOK reset list
  omitted three of the flags its own classifiers read (a stale one masks every
  lower-priority reason); and both guard tests passed trivially — one iterated
  a single flag already ranked below the hold, the other scanned the whole
  RUNBOOK where every flag is named in prose.

  **Two root causes worth carrying forward.** (1) I repeatedly asserted
  mechanisms I had not executed — three false claims written into code
  comments, each costing a round; the `update_state` comment now carries an
  explicit instruction not to re-describe that route without re-running it.
  (2) The sticky-flag design chosen in round 2 generated most of the later
  rounds (clearing, reset lists, priority ordering, ordering tests). The
  alternative offered at the time — have `_classify_human_pause` re-derive
  tradability from the brief instead of trusting a stored flag — would have
  made every one of them impossible by construction. **Recorded as the one
  worthwhile follow-up refactor; not done here.**

- 2026-08-20 — **S1b DONE; epic closed `done`.** All four stories complete
  (S1a, S2, S1b, S3; S3a dropped 2026-08-18 as unnecessary), all four
  Done-when items MET. `_parse_brief_frontmatter` now requires `venue` and
  `product` alongside its existing 4 required fields, raising the same
  `ValueError` style on either being missing — this is the actual
  registration choke point (both fresh-launch call sites in
  `run_campaign.py`, plus `register_hypothesis`'s queue registration, parse
  a brief through this function before anything else happens with it).
  `_materialize_run`'s own fail-closed default is left untouched as a
  defensive fallback for direct-dict callers. 4 new tests
  (`tests/test_venue_tradability.py`); 2 independently confirmed to fail
  against the pre-fix code before folding in. One pre-existing fixture
  (`test_k3_protocol_pinning.py::_VALID_BRIEF_FRONTMATTER`) needed
  venue/product added to stay valid — a fixture catching up to the
  tightened contract, not a regression. Both suites green
  (strategy-research 793/17/0 modulo the 4 pre-existing network/cache-
  dependent failures unrelated to this change — no BTCUSDT cache or network
  access in this environment; trading-bot 365/20/0 untouched). Holdout gate
  PASS. No downstream impact: 0 of 57 existing runs carry venue/product on
  their briefs (per S3's Phase A measurement), so nothing already on disk
  is affected — this only gates brand-new registrations from here on.
