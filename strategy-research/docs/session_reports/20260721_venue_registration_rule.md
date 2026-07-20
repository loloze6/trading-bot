# Dispatch — Phase 1.3: venue/product registration-rule mechanism

Date: 2026-07-21
Precondition check: PASSED — HEAD=850bf56, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/20260720_close.md`,
`_materialize_run(` had exactly 3 matches (def at line 202, `fresh_launch`
call site, dry-run-verify call site), the required-field tuple at line 172
matched, no `_venue_product_tradable`/`_load_venue_tradability` name
collision.

## Per-step done/verdict

1. **Precondition manifest: DONE, all matched.** No STOP triggered.
2. **`config/venue_tradability.yaml`: DONE.** Created verbatim as specified
   (Kraken spot/perp tradable, margin unconfirmed; undeclared/unlisted pairs
   default not-tradable).
3. **`_load_venue_tradability()`/`_venue_product_tradable()`: DONE**
   (`workflow/run_campaign.py`, immediately before `_parse_brief_frontmatter`
   at line 159). One deliberate deviation from "a plain global cache is
   fine": cached **per resolved `ROOT`-relative path**, not a single
   unconditional value. Reason: `tests/conftest.py`'s autouse
   `_sandbox_by_default` fixture gives every single test in this suite its
   own `ROOT`; a single-value cache would have let whichever test happened
   to call `_materialize_run` first (almost certainly one with no
   `venue_tradability.yaml` on disk) poison every later test's result,
   including this dispatch's own new fixtures. Path-keyed caching preserves
   "cache it" while staying correct under that existing isolation guard —
   confirmed by the full suite passing (see step 6).
4. **`_materialize_run` wiring: DONE** (lines 207-213) — `research_brief["research_only"]`
   set from `_venue_product_tradable(brief.get("venue"), brief.get("product"))`
   before `orch.save_yaml(...)`, one unconditional `VENUE-CHECK` `_log(...)`
   line, called plain (no `dry_run` kwarg), matching `register_hypothesis`'s
   own calling convention (verified at line 287/294/315 before writing).
   `_parse_brief_frontmatter`'s required-field tuple, `briefs/*`, and
   `campaign_queue.yaml` were not touched.
5. **Tests: DONE.** New file `tests/test_venue_tradability.py` (chose a new
   file over extending `test_k3_protocol_pinning.py`: the K3 file is scoped
   to protocol-selection linting, a different kernel; reusing its imported
   `campaign_root` fixture from `test_k4_routing_registration.py` — same
   reuse precedent `test_k2_verdict_machinery.py`/`test_k3_protocol_pinning.py`
   already established — keeps this concern in its own file without
   diluting K3's). 6 tests, all drive `_materialize_run` end-to-end and
   assert `research_brief.yaml`'s written `research_only` key (not just the
   helper in isolation): no-venue/product default, Kraken spot, Kraken perp,
   Kraken margin (unconfirmed), unlisted product, unlisted venue.
6. **Suite: DONE.** Baseline `python -m pytest` (before any change): **328
   passed**. After: **334 passed** (328 + 6 new), zero failures, zero new
   errors.
7. **Ledger C14: DONE.** Appended immediately after C13, same v7 section,
   `PIPELINE_IMPROVEMENTS_20260712_v4.md`. CLOSED/shipped-feature format
   mirroring B15's precedent (Symptom/Fix/Resolution/Acceptance, file:line
   sites named, this dispatch cited by name).
8. **This report: DONE.**
9. **Commit: pending** (this report is being written before the commit step;
   see chat reply for the resulting hash).
10. **Read-back: pending**, performed immediately after commit.

## Confirmation

No file outside the authorized set was touched: `config/venue_tradability.yaml`
(new), `workflow/run_campaign.py` (two new module-level helpers + one
3-line/one-log-line addition inside `_materialize_run`), `tests/test_venue_tradability.py`
(new), `PIPELINE_IMPROVEMENTS_20260712_v4.md` (C14 appended), this report
(new), plus the pre-existing untracked `docs/session_reports/20260720_close.md`
folded in per instruction. `SESSION_LOG.md`/`NEXT_SESSION.md` not touched —
mid-arc dispatch, not a session close. No `trading-bot/` file touched.
