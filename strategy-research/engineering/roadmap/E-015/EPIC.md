# E-015 — Venue/product declared at brief registration

**State:** in-progress
**Owner:** Jeremy
**Updated:** 2026-08-05

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
- [ ] S3 — Enforce `research_only` at a real downstream gate (promotion,
      walk-forward, or the sealed holdout) so a `research_only` run cannot
      reach a live-money decision undetected. This is the load-bearing gap:
      without it, `research_only` is a label nothing reads.

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
