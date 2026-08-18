# E-015 — Venue/product declared at brief registration

**State:** in-progress
**Owner:** Jeremy
**Updated:** 2026-08-18

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
   an implicit default. (Not met: shipped code defaults silently to
   `research_only: true` instead of failing — see Why.)
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
   written and never read again.

## Stories

- [x] S1a — Add venue + product as required fields to the brief registration
      schema/contract; wire the auto-flag for products not legally tradable
      for the operator. DONE 2026-07-21, `run_campaign.py`/
      `config/venue_tradability.yaml`, 7 tests (shipped before this epic
      existed; not tracked here at the time).
- [x] S2 — Settle and record the funding family's venue status (live-tradable
      perp access vs. research-only) as the rule's first application. DONE
      2026-07-20, `campaign_knowledge_base.yaml`.
- [ ] S1b — Make missing venue/product a hard registration failure (Done-when
      #1, as originally specified) rather than a silent `research_only`
      default.
- [ ] S3a — **Make `research_only` propagate.** Prerequisite for S3b, found
      by S3's Phase A (see below): the flag is written by one of three
      `research_brief.yaml` writers, so it does not survive a refine or a
      reframe. Enforcing without this yields a gate every descendant walks
      around.
- [ ] S3b — Enforce `research_only` at the holdout gate
      (`_route_holdout_evaluation`), **before** its human-pause branch, so a
      `research_only` run cannot reach a live-money decision undetected.
      Blocked behind S3a.

## S3 Phase A — characterization (2026-08-18, STOPPED for review)

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
2. S3b blocks with `return "completed_rejected"`, matching the two existing
   refusals in that function; it does not raise.
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
