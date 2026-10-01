# Hypotheses from a brief — addendum to hypothesis-design (E-059 S2b)

**When you see this file.** The orchestrator adds it to your inputs ONLY when
`orchestrator.decide_next.enabled` is on AND this run has
`artifacts/brief_hypotheses_context.yaml`
(`run_phase1_research._apply_brief_hypotheses_context`). Everything in
`SKILL.md` still applies; this file adds three things.

**Read `artifacts/brief_hypotheses_context.yaml` first.** `already_produced`
lists every `hypothesis_id` this brief has already produced. Never write a
card that repeats one of them, under the same or another id: a card with an
id in that list is rejected, and a run whose cards are all repeats ends
without testing anything. Do not write both `hypothesis_card.yaml` and
numbered cards or a scores file: that output is refused as ambiguous. When `request`
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

| Score | `confidence_real` (is the effect real?) | `distance_to_profitable` (card I / D-017: how far is this idea from the validated blocks?) | `mechanism_plausibility` (causal story) |
|---|---|---|---|
| 0 | Story only: no cited measurement. | Same block type as a block in `block_registry.yaml`: same kind, same component classes, same timeframe category (or the block's timeframe category is unrecorded: an assumed match) -- a neighbour of something already validated. | No counterparty named; the pattern could be coincidence. |
| 1 | One cited observation (one prior run, window or published result). | Same component classes as a registered block, but a different kind or timeframe category. | A mechanism is named, but not who pays or why. |
| 2 | Cited evidence from 2+ independent sources or prior runs with a consistent sign. | The registry holds a forecast block and this card is not plainly the same classes as any registered block -- including when you cannot tell (correlation to the registry cannot be measured before a backtest). | A constrained or non-economic actor who pays is named. |
| 3 | A prior run in this campaign measured this exact effect with a consistent sign across windows (cite it). | Nothing is validated yet: `campaign_record/block_registry.yaml` is not in your inputs, or it holds no forecast block (`kind: forecast`). | Actor named AND a cited reason why the edge is not arbitraged away. |

`distance_to_profitable` is the same score the readers give (card I, D-017), read
from `campaign_record/block_registry.yaml` (an input only when the file exists).
A block type is (kind, component classes, timeframe category). A card has no config
yet, so score 0 or 1 only when the card's `signal_concept` plainly uses the same
component classes as a registered block's `config_fragment` (`class` keys) -- never
guess class names; when you cannot tell, score 2 (the readers' default for a type they
cannot place). Timeframe categories: high <= 15min < medium < 1h <= low < 1d <= daily;
a block with no recorded `timeframe_category` is an assumed match. It is NOT a
cost estimate: `cost_feasibility` ranks nothing here (O-3, operator 2026-10-01 --
costs are judged only by the backtest).

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

Never declare the brief exhausted, and never leave out a card, on a cost,
breakeven or turnover estimate (`cost_feasibility` included). Costs are judged
only by the backtest (O-3, operator 2026-10-01): an idea you expect to lose to
fees is still a card -- say so in its `expected_failure_modes`. "Worth testing"
means distinct and testable with the available data, nothing more.
