# E-018 — Near-miss scoreboard

**State:** in-progress (unparked 2026-08-23; S1 dispatched same day)
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §3.2, verbatim: "**Near-miss scoreboard (your
ranking idea, adopted for ideation only).** Objective: failed-but-instructive
ideas feed the generator. Deliverable: a ranked, auto-updated table over all
tested ideas (evidence quality, failed-criterion margins, root causes),
readable by the idea-generation stage, firewalled from promotion decisions."

Also Part 1, verbatim, on why the firewall is the point and not an
afterthought: "we build both, firewalled: the **near-miss scoreboard** (new,
step 3.2) — a ranked table of every tested idea ... that the idea-generation
stage reads as raw material, and that promotion is *forbidden* to read. The
scoreboard inspires; only the gates decide."

**The difficult requirement is the firewall, not the table.** A ranked table
is a straightforward read-model over the knowledge base. Firewalling it from
promotion — ensuring the promotion decision path has no read access to it —
is the part that protects the frozen pass/fail gates from becoming, in
effect, a leaderboard. A scoreboard built first with the firewall added later
is a leakage vector: any interim state where promotion *can* read the
scoreboard defeats the reason it exists.

**~~Blocked on:~~ UNPARKED 2026-08-23 (operator).** The park was inherited
from Phase 3's position in the plan, not derived from this epic's own inputs.
Three reasons it does not hold:

1. **This scoreboard needs nothing from Phase 2.** It ranks ideas *already
   tested*. Its input is 38 verdict files and 36 recorded `primary_failure_mode`
   values sitting on disk today (MEASURED 2026-08-23, parsed across
   `runs/run_*/artifacts/verdict_interpretation.yaml`, denominator 59 run dirs).
   The new data axes are not an input.
2. **Its stated consumer is now an epic.** `docs/CAMPAIGN_PROGRAM.md` Part 1
   describes this table as what *"the idea-generation stage reads as raw
   material, and that promotion is forbidden to read."* E-032 is that stage.
   Parking the feedstock while the loop proposed only neighbours for 59 runs
   was self-defeating.
3. **Phase 2's gate is itself largely met, and its one unmet clause has an
   owner.** Breadth is on disk (19 Kraken pairs hourly and daily, verified);
   whale-footprint tooling and two pre-registered protocols exist. The only
   unmet clause — "recorders running" — is now owned by E-007 and is unrelated
   to this epic's inputs.

Original text, kept for the record: *Phase 2 verdict, for the same reason as
E-017 — §3.2 belongs to Phase 3, which is "ongoing once Phase 2 delivers" per
`docs/ROADMAP.md` [retired by E-013; now `docs/CAMPAIGN_PROGRAM.md`]. Phase 2's
gate: "≥2 new data axes on disk with provenance + a first registrable indicator
each; recorders running.*"

## Done when

1. A ranked, auto-updated table exists over all tested ideas, carrying
   evidence quality, failed-criterion margins, and root causes.
2. The table is readable by the idea-generation stage.
3. The table is firewalled from promotion decisions: the promotion decision
   path has no read access to it, verified by inspection of what promotion
   code/process actually consults.

## Stories

- [x] S1 — Build the ranked table over tested
      ideas (evidence quality, failed-criterion margins, root causes). DONE
      2026-08-23 — see Log entry below.
- [ ] S2 — Wire idea-generation read access and verify, by inspection, that
      the promotion path has no read access to the table — build the
      firewall as part of the same story, not a follow-up.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §3.2 and Part 1 (dispatch W35). Parked on Phase 2's gate.

- 2026-08-23 — `parked` → `new`. Unparked by operator ruling. The firewall in
  S2 (promotion must have no read access) is unchanged and non-negotiable: the
  scoreboard inspires, only the frozen gates decide.

- 2026-08-23 — **S1 done.** Built `strategy-research/tools/near_miss_scoreboard.py`
  (generator) + `strategy-research/engineering/roadmap/E-018/artifacts/near_miss_scoreboard.{yaml,md}`
  (generated artifact — regenerate any time via `python tools/near_miss_scoreboard.py`,
  idempotent). Tests: `tests/test_near_miss_scoreboard.py` (20 tests: parsing,
  never-impute, ranking, denominator honesty, a regression lock against the
  real corpus's verdict-field distribution) and
  `tests/test_near_miss_scoreboard_firewall.py` (6 tests — see firewall
  findings below). Fast suites: strategy-research 910 passed (884 baseline +
  26 new, zero drop); trading-bot 383 passed / 2 skipped (untouched, matches
  baseline exactly).

  **Corpus reality (MEASURED, denominator = 59 run dirs unless stated):**
  38 of 59 carry `verdict_interpretation.yaml`; of those, 36 use the "full
  protocol" schema (`protocol_verdict`/`status`/`criteria_summary`/
  `root_cause`) and 2 use a distinct "prescreen/disposition" schema
  (`verdict_label`/`disposition`/structured `prescreen_result_summary` with
  `ic_active_bars`/`edge_to_cost_ratio`) — run_041, run_042. The 21 without a
  verdict file are early/interrupted/quarantined pipeline runs; their
  `pipeline_state.yaml` status/stage is recorded in the table as the "why
  thin" explanation instead of a guess (e.g. `failed`/`backtest_specification`,
  `quarantined_orphan`, `rejected_budget_exceeded`).

  `criteria_summary` itself splits roughly in half: 19 of 38 verdict files use
  structured dicts (`criterion`/`result`/`actual`/`required`), 17 use free-text
  strings needing regex extraction, 2 have no `criteria_summary` at all
  (prescreen schema). Confirmed and reproduced as a locked-in regression test
  (`test_real_corpus_verdict_field_denominators_match_known_good`): of the 38,
  `protocol_verdict` is present in 36 (26 refine / 10 kill / 2 absent-within-
  file) and `status` is present in 33 (14 refine / 10 pivot / 7 escalate / 2
  kill / 5 absent-within-file) — two DIFFERENT fields, reported as separate
  table columns, never collapsed. **"promote" appears in neither field,
  anywhere in the corpus.**

  Numeric near-miss margin (the run's worst-binding FAIL criterion, as a
  fraction of that criterion's own threshold) recovered for 24 of 59 runs.
  IC recovered (structured `prescreen_result_summary` field, or opportunistic
  `ic_all_bars=`/`ic_active_bars=` regex over root-cause prose) for 7 of 59.
  Cost ratio (`edge_to_cost_ratio`) for 5 of 59. Era-behaviour free text
  (root-cause prose citing >=2 distinct years, i.e. an actual cross-period
  comparison, not one incidental date) for 4 of 59. Every one of these is a
  stated denominator in both the Log here and the generated Markdown table's
  own "Denominators" section — nothing is imputed for the rest; those rows
  carry an explicit `not_recorded` marker per field and stay IN the table
  (a thin record is itself information).

  Two real parsing bugs were caught and fixed by a single safety net (a
  derived margin is discarded, not trusted, whenever its sign contradicts the
  criterion's own stated PASS/FAIL — margin_frac > 0 on a FAIL, or < 0 on a
  PASS, is impossible and means the extraction went wrong): (1) a stray
  "2024" from an embedded date range (`"...only 3 windows: 2024-06, 2024-08,
  2024-09"`) getting parsed as a metric value, producing a bogus 403x "pass"
  margin on a FAIL criterion; (2) a percent-vs-fraction unit mismatch between
  a criterion's threshold and its reported actual. A third bug (a rationale's
  own restated threshold, e.g. `"validation_protocol required=1.5"`, being
  picked up as if it were the observed value) is now excluded by name via
  `_REQUIREMENT_LABELS`. All three are regression-tested by name in
  `test_near_miss_scoreboard.py`.

  Ranking key (stated plainly per the dispatch's requirement, since there is
  no single obvious one): tier 0 = FAIL criteria with a recoverable numeric
  margin, ordered by *smallest magnitude miss* (closest to passing first, per
  the scoreboard's actual purpose — near misses, not blowouts, are the
  interesting feedstock); tier 1 = has a verdict but no recoverable margin,
  ordered by status (refine > escalate > pivot > kill > absent); tier 2 = no
  verdict file at all, by run_id. Positive IC is a tie-break only, never the
  primary key — promotion-adjacent metrics stay secondary to the epic's own
  stated purpose (near-miss margins).

  **Firewall (Task 2 of the dispatch, built now — S2 checkbox left unticked,
  see below).** By inspection: the promotion decision path is
  `workflow/run_campaign.py` (writes/routes `promotion_audit.yaml` and the
  `provisional_promote_*` states) + `workflow/run_phase1_research.py` (shares
  its campaign-state/KB machinery) + `tools/deflate_sharpe.py` (the DSR gate).
  Verified two ways, both now mechanically enforced as tests, not convention:
  an AST import-graph scan plus a broad text-reference scan (catches
  `importlib`/hardcoded-path forms an AST-only check would miss) over the
  ENTIRE `workflow/` and `tools/` trees, and a scan of every
  `workflow_artifacts/skills/*/SKILL.md` for the scoreboard's name or output
  filenames. Result today: **zero readers exist anywhere in the codebase**
  besides the generator itself — expected, since E-032 (idea-generation, the
  intended reader) isn't built yet. A self-test proves the scanner isn't
  vacuous (it injects a fake `import near_miss_scoreboard` into a throwaway
  file and asserts the scanner catches it). The output artifact was placed
  under `engineering/roadmap/E-018/artifacts/` specifically because it is
  NOT glob-reachable by any existing decision-path code (`run_campaign.py`
  globs are scoped to `runs/*` only) and is NOT co-located with
  `campaign_record/campaign_knowledge_base.yaml`, which decision-adjacent
  skills (verdict-interpreter, quant-validation) already require as an input
  — colocating there would have been an easy accidental leak vector.

  **S2 is NOT ticked.** Firewall enforcement (the hard half of S2, "verify by
  inspection that promotion has no read access") is done and tested here, but
  the other half of S2 — "wire idea-generation read access" — has no consumer
  to wire yet; E-032 doesn't exist as code. Leaving S2 open until E-032 exists
  and actually reads this table is the honest state, not a gap in this
  story's own scope.

  **Task 3 (standing, not one-shot):** the generator is a plain re-runnable
  script (`python tools/near_miss_scoreboard.py`), proven idempotent by test.
  NOT wired into the campaign loop yet. The natural hook, named but not
  implemented here (out of scope for S1 — it's decision-adjacent code and
  deserves its own review against the firewall): `workflow/run_campaign.py`'s
  end-of-campaign-review step, the same lifecycle point where
  `campaign_review.yaml`/`campaign_knowledge_base.yaml` already refresh.

- 2026-08-23 — **S1 done.** Dispatched agent built
  `tools/near_miss_scoreboard.py` (626 lines) plus
  `E-018/artifacts/near_miss_scoreboard.{md,yaml}`, and 26 new tests across
  `tests/test_near_miss_scoreboard.py` and
  `tests/test_near_miss_scoreboard_firewall.py`. **The agent was killed by an
  API session limit immediately before writing this Log entry**; the
  dispatching session verified its output and completed the record. Nothing
  was left half-written in code — only this entry was missing.

  **Denominators, MEASURED and independently reconciled** against the
  dispatching session's own earlier parse (they agree exactly): 59 run dirs
  scanned; 38 carry a verdict file (36 full_protocol, 2 prescreen_only); 36
  carry `protocol_verdict`; 33 carry `status`. Recovery falls off sharply for
  the fields that matter most to ideation: a numeric worst-fail margin for
  **24 of 59**, IC for **7 of 59**, cost ratio for **5 of 59**, era behaviour
  for **4 of 59**. Unrecoverable fields are emitted as explicit
  `not_recorded` markers — never imputed, and no run is dropped for having a
  thin record.

  **The thinness is itself the finding.** A scoreboard built to tell the
  idea-generation stage *which near-misses were close* can recover a numeric
  margin for well under half the history, and IC for barely a tenth. This is
  direct, independent corroboration of E-029/E-027's premise from a different
  angle: the trade and verdict records describe outcomes, not decisions.
  Ranking is therefore honest but coarse for older runs, and the epic should
  not claim otherwise.

  **Ranking key**, stated because there is no obvious one: tier 0, failed
  criteria with a recoverable margin, ordered by the *smallest* magnitude miss
  on the run's worst-binding criterion; tier 1, verdict but no numeric margin,
  by status; tier 2, no verdict file, by run_id. Positive IC breaks ties
  within a tier and is never the primary key.

  **Firewall (S2's requirement, built inside S1 as the epic demanded).** A
  static import/reference sweep, not a convention or a runtime guard — the
  cheapest control that works. It asserts that named promotion modules, all
  `workflow/` and `tools/` decision-path code, and every skill file are free
  of scoreboard references, and that the generator defines no
  decision-rule-shaped names. It includes
  `test_scanner_actually_detects_an_injected_violation`, which proves the
  scanner is not blind — the check the project's own "falsify your load-bearing
  claim" rule asks for, and the reason this counts as verified rather than
  asserted.

  Suites verified by the dispatching session, not taken on report:
  strategy-research **910 passed** (884 baseline + 26 new, zero regressions);
  trading-bot 383 passed / 2 skipped, untouched.

  **S2 remains open** for the half S1 could not do: wiring idea-generation
  *read* access. There is no consumer to wire yet — E-032 is that consumer and
  is unbuilt. S1 delivered the table and the firewall; S2 connects it when
  E-032 exists.
