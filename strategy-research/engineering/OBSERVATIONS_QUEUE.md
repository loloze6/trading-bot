# Observations queue

Surprising behaviour the operator wants investigated together, in one sitting, rather than
one at a time. Each entry records what was seen and where, and why it is surprising. **It
says nothing yet about the cause.** Investigation fills in "Finding" and, if needed, a
decision (DECISION_LOG) or a ticket.

| # | Seen | Observation | Status |
|---|---|---|---|
| O-1 | C4 run_061, 2026-09-30 | "Long-only" trend component | open |
| O-2 | C4 run_061 → run_062, 2026-09-30 | Stage 2 sending the brief back to stage 1 | open |

---

## O-1. Why would an indicator component be long-only?

**Seen:** run_061's `strategy_config_authoring` (step 1b) parked the idea with
`component_gap`. Its reason: "Bidirectional SMA(50) trend component required by hypothesis is
not in STRATEGY_DESIGN_GUIDE.md catalog; SmaTrendLongOnlyComponent is long-only and cannot be
configured to produce short signals", and the transform pipeline "cannot enable single
component instance to detect opposite SMA condition". Source:
`runs/run_061/artifacts/decision.yaml`. The class is
`trading-bot/strategies/strategy_components.py` (`SmaTrendLongOnlyComponent`, and
`GatedSmaTrendLongOnlyComponent`).

**Why surprising (operator, 2026-09-30):** the pipeline should look up the indicators that
are available, and every indicator should produce a forecast that can be positive (long) or
negative (short). A long-only indicator contradicts that model.

**To check:** why this component clips to long-only, and whether that is design or legacy;
whether a sign-symmetric SMA trend component exists under another name; whether the 1b claim
about the transform pipeline is true (`strategies/registry.py`, e.g. negate/scale); and how
1b builds its catalogue (STRATEGY_DESIGN_GUIDE.md vs the component registry).

**Finding:** —

## O-2. Is "stage 2 sends the brief back to stage 1 for another idea" part of the design?

**Seen:** after run_061 parked, decide-next minted a queue entry
`C4_vol_managed_trend__more_1` (R2: "ask step 1a for more hypotheses from an open brief"),
which became run_062. Source: `runs/run_061/artifacts/parked/park_1/decision_record.yaml`,
`config/campaign_queue.yaml`, `tools/decide_next.py` (step 4, R2).

**Why surprising (operator, 2026-09-30):** the expected flow was that a brief is ingested
once, several ideas are generated from it and stored in an idea backlog, and runs take ideas
from that backlog. A path back from stage 2 to stage 1 was not expected.

**To check:** what the target design says (roadmap v27 card M, multi-hypothesis briefs; E-059
S2b; delivery plan slice 6b); whether step 1a on run_061 was offered the multi-card path
(`hypothesis_card_<n>.yaml` + `extra_card_scores.yaml` → `queued_hypotheses.yaml`) and why it
wrote one card; and whether R2 is the intended top-up when the backlog is empty or a leftover.

**Finding:** —
