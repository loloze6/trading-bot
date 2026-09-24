# Hypotheses from a brief — addendum to hypothesis-design (E-059 S2b)

**When you see this file.** The orchestrator adds it to your inputs ONLY when
`orchestrator.decide_next.enabled` is on AND this run has
`artifacts/brief_hypotheses_context.yaml`
(`run_phase1_research._apply_brief_hypotheses_context`). Everything in
`SKILL.md` still applies; this file adds three things.

**Read `artifacts/brief_hypotheses_context.yaml` first.** `already_produced`
lists every `hypothesis_id` this brief has already produced. Never write a
card that repeats one of them, under the same or another id. When `request`
is `more_hypotheses`, the orchestrator is asking for NEW hypotheses from the
same brief.

## 1. One card, or several

One card: write `artifacts/hypothesis_card.yaml` as usual. Nothing else here
applies.

Several distinct hypotheses: write `artifacts/hypothesis_card_2.yaml`,
`artifacts/hypothesis_card_3.yaml`, ... (no `hypothesis_card.yaml`). The first
file in name order runs now; each other card waits in the queue and, when the
queue picks it, runs from stage 1b with this exact card (it is never
re-authored). So every card must be complete on its own, with its own
`hypothesis_id` and `criteria`.

## 2. Score every card (only when you wrote several)

Write `artifacts/extra_card_scores.yaml`:

```yaml
cards:
  - card: hypothesis_card_2.yaml
    scores:
      confidence_real: 0-3
      distance_to_profitable: 0-3
      mechanism_plausibility: 0-3
    model_id: <your model id>
    rubric_version: brief-card-v1
  - card: hypothesis_card_3.yaml
    ...
```

Every card file needs exactly one item. Missing, extra or out-of-range keys
stop the run. These scores ONLY rank waiting cards against each other and
against reader proposals. They never decide whether an idea is true; only the
backtest grid does that.

Rubric `brief-card-v1` (anchored; a card with no backtest yet usually scores
`confidence_real` 0-1):

| Score | `confidence_real` (is the effect real?) | `distance_to_profitable` (edge vs cost) | `mechanism_plausibility` (causal story) |
|---|---|---|---|
| 0 | Story only: no cited measurement. | The card's `cost_feasibility` puts the expected edge below the round-trip cost. | No counterparty named; the pattern could be coincidence. |
| 1 | One cited observation (one prior run, window or published result). | Expected edge above cost, but less than 2x cost. | A mechanism is named, but not who pays or why. |
| 2 | Cited evidence from 2+ independent sources or prior runs with a consistent sign. | Expected edge 2-4x cost. | A constrained or non-economic actor who pays is named. |
| 3 | A prior run in this campaign measured this exact effect with a consistent sign across windows (cite it). | Expected edge above 4x cost, from a cited measurement. | Actor named AND a cited reason why the edge is not arbitraged away. |

## 3. The brief is exhausted

If the brief has no further hypothesis that is distinct from
`already_produced` and worth testing, write NO card and write
`artifacts/brief_status.yaml`:

```yaml
brief_status: exhausted
reason: <one or two sentences: why nothing new is left in this brief>
```

The run then ends as `completed_brief_exhausted`, and the queue never asks
this brief for more hypotheses again. Writing this file next to any card
stops the run (contradictory output).
