# Dispatch model — roles, process, and which model for which job

Extracted from `docs/ROADMAP.md` Part 3 (dispatch W25), which now points here.

## Relationship to `engineering/roadmap/PROCESS.md`

This file governs how a unit of work is **executed**: who dispatches, who
audits, which model tier, cost discipline, context economy.
`engineering/roadmap/PROCESS.md` governs how work is **organised**: epics,
stories, states, evidence. They meet at exactly one point: **a story is a
dispatch** — `PROCESS.md`'s epics produce the story queue that this file's
loop consumes one at a time. See `PROCESS.md` § "Relationship to the dispatch
model" for the reciprocal statement.

## The dispatch loop

The loop that produced this campaign's results — and caught five defects
before they could lie to us — is kept as the standing process. One unit of
work always looks like: **director drafts a dispatch → operator relays it →
one agent executes under stop-rules → report → director cross-checks the
report against the raw artifacts (recomputing, never trusting narrative) →
ruling → next dispatch.** Disagreements between any two parties are settled
only by recomputation from files and git — never by whoever sounds more
confident.

## The roles and their models

**Current lineup: Opus 5 / Sonnet 5 / Haiku 4.5.** (Correction, this
dispatch: the prior text named "Claude Sonnet 4.6" / "Claude Opus 4.8" —
those model names are stale. Mapped straight across by tier: Sonnet 4.6 →
Sonnet 5, Opus 4.8 → Opus 5, Haiku 4.5 → Haiku 4.5 unchanged, Fable 5 →
Fable 5 unchanged.)

- **Operator (you).** Final authority: ratifies rulings, relays dispatches,
  gives LAUNCH, decides venue and money. Deliberately minimal time cost.
- **Research director (the chat session) — Fable 5.** Plans, writes every
  dispatch (fixed skeleton: precondition manifest, numbered steps, explicit
  STOPs), reviews every report against the artifacts, arbitrates by
  recomputation, maintains roadmap/ledger/KPI. This is the one seat where
  judgment errors are most expensive — it has had to overturn its own
  recon's wrong "exoneration" and catch an impossible-by-construction pass
  criterion — so it stays on the top-tier model.
- **Execution agents — one per dispatch, four classes with locked write
  rights:**
  - *Recon/audit (read-only)* — verify, quote, measure. Default **Sonnet
    5**; drop to **Haiku 4.5** for purely mechanical checks (precondition
    manifests, freshness audits, file inventories).
  - *Diagnosis (read-only, in-process reproduction)* — **Opus 5**.
    Root-cause confirmation is real investigation (e.g. a timezone bug found
    by driving the actual engine code in-process); too cheap here buys wrong
    exonerations.
  - *Implementation (sole writer: code + tests + commits)* — **Opus 5** for
    engine/orchestrator internals; **Sonnet 5** when the dispatch already
    names the exact site and mandates the tests (minimal, well-specified
    changes).
  - *Operations (writes only through orchestrator commands:
    launch/resume/monitor)* — **Sonnet 5 minimum.** A stale-cache echo was
    once caught by operations-level judgment; a cheaper model here risks
    false resumes on untrustworthy halt messages.
- **Independent auditor (third party, read-only) — Sonnet 5.** Mandatory for
  any commit touching the orchestrator, the engine, or shared state:
  re-derives every claim from git and artifacts. So: **three-party process**
  (director + implementor + auditor) for code and state; **two-party**
  (director + agent) suffices for recon and routine operations.

**A "Model:" line in a dispatch header is NOT honored.** (New this
dispatch, evidence-based: sub-agents inherit the parent/session model
regardless of what a dispatch header names. Naming a model in a dispatch is
documentation of *intent* for a human relaying it into a separate session —
it is not a mechanism that pins the executing agent's actual model. Do not
rely on a header line to enforce a tier; the tier is whatever session or
subagent configuration the dispatch is actually run under.)

## Cost discipline

Start at each class's default tier; escalate one tier only after a stop
caused by agent *capability* (not by a wrong premise in the dispatch); try
one tier cheaper after three consecutive clean dispatches of the same type.
Separately, the factory's *internal* stage calls (validation, verdict
interpretation, review) are their own cost lever — judgment stages on
Sonnet-class, mechanical stages on Haiku 4.5 — tuned only when the
cost-per-verdict KPI says so, never speculatively.

## Context economy

Four rules, added to control token burn:

1. **Short director sessions**: the director closes and hands off after each
   arc (roughly 10–15 dispatches); the repo's documents — roadmap, session
   log, next-session file, knowledge base — are the memory, never the chat
   scroll. Every close-out produces the next director's opening prompt.
2. **Bounded agent reports**: agents write their full detail to a file in
   the repo (`docs/session_reports/<date>_<dispatch>.md`) and reply in chat
   with a bounded summary — per-step verdicts plus only the verbatim quotes
   the director must recompute from.
3. **No re-pasting**: a dispatch is relayed once; if deferred, it is
   referenced by name, and any dispatch expected to wait is saved to a repo
   file instead of repeated in chat.
4. **Director model stays top-tier (Fable 5)** — the burn problem is session
   *length*, not the director's tier; downgrading the arbitration seat to
   save tokens is how wrong exonerations get accepted. Agent tiers and the
   escalation ladder above already handle the rest of the cost curve, all
   counted into cost-per-verdict.

## Anti-corner rule

Carried across from `docs/ROADMAP.md` Part 4, which otherwise stays intact:
every session ends with at least one hypothesis-level advance — a verdict, a
registration, or a data-axis milestone — never process alone.
Pipeline/autonomy work happens only where it raises verdicts-per-week.

## Standard verification command

**Run from `strategy-research/`:**

```
python -m pytest
```

**Do not scope this to `tests/` alone.** `recorder/tests/` is a separate,
sibling test directory (`strategy-research/recorder/tests/`), and a
`pytest tests/`-scoped run silently excludes it. Verified this dispatch by
direct count, two ways:

- **Function count** (`grep -rE "^\s*def test_"`, counts each `def`, not
  each parametrized case): `tests/` = 411, `recorder/tests/` = 231,
  **total = 642**. Recorder tests are **231 of 642 (36%)** of the suite —
  a `tests/`-scoped report silently drops more than a third of it.
- **Pytest collected-item count** (differs from the function count above
  because parametrization expands one `def` into several collected items):
  `tests/` alone = 473, `recorder/tests/` alone = 248, bare
  `python -m pytest` from `strategy-research/` = **721** (473 + 248,
  confirmed additive).

**Current expected result** (bare `python -m pytest` from
`strategy-research/`): **721 collected — 719 passed, 1 skipped, 1 failed.**
The one failure, `tests/test_c7ext_verdict_gates.py::test_d3_every_committed_generic_protocol_is_marked_unratified`,
is a known pre-existing failure — not introduced by, or diagnosed as part
of, this dispatch. No repo record of its root cause was found; treat it as
still open, not as explained by anything written here.

`trading-bot/` suite (run from `trading-bot/`): `python -m pytest` — 227
collected, 213 selected / 14 deselected, **211 passed, 2 skipped**.
