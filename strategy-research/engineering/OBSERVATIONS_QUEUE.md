# Observations queue

Surprising behaviour the operator wants investigated together, in one sitting, rather than
one at a time. Each entry records what was seen and where, and why it is surprising. **It
says nothing yet about the cause.** Investigation fills in "Finding" and, if needed, a
decision (DECISION_LOG) or a ticket.

| # | Seen | Observation | Status |
|---|---|---|---|
| O-1 | C4 run_061, 2026-09-30 | "Long-only" trend component | open |
| O-2 | C4 run_061 → run_062, 2026-09-30 | Stage 2 sending the brief back to stage 1 | open |
| O-3 | C4 run_062, 2026-09-30 | Step 1a declaring the brief exhausted on a cost argument | open |
| O-4 | C4 run_063, 2026-09-30 | Step 2 inventing a component class name | open |
| O-5 | C4 run_063, 2026-09-30 | Asset variants evicted instead of re-windowed; the "at least 2 variants" rule | open |
| O-6 | C4 run_063, 2026-09-30 | Park reason says "component" when most failures were data | open |
| O-7 | C4 run_063, 2026-09-30 | A threshold (breakout) idea in a linear-forecast design | open |

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

## O-3. What does step 1a (brief → hypothesis) see, and why did it declare the brief exhausted?

**Seen:** in run_062 (the R2 "more ideas" request for the same brief), step 1a wrote no idea
and declared the brief exhausted. Its argument: on 1h BTC/ETH spot, a multi-week momentum
signal would need an IC above about 0.20 to clear a "34 bps minimum required edge per trade",
while tested momentum families (EMA ic=-0.021, MACD ic=-0.015) show IC near or below zero; it
also cited "the campaign's exhausted_mechanisms list" and asked for a liquidation-data feed
instead. One run earlier (run_061), the same brief produced a concrete idea. Source:
`runs/run_062/artifacts/debug_hypothesis_generation_raw_output.txt`; its inputs are listed in
`runs/run_062/artifacts/brief_hypotheses_context.yaml`, `run_context.yaml` and the stage's
`handoffs/`.

**Why surprising (operator, 2026-09-30):** a stage whose job is to generate ideas vetoed the
brief with its own back-of-envelope cost arithmetic, before any backtest. The operator wants
to see exactly what inputs the brief → hypothesis step receives.

**To check:** the exact input list and bytes given to step 1a on run_061 and run_062 (brief,
knowledge base, cost model, indicator library, available feeds, tried ideas / exclusion
digest, the BRIEF_HYPOTHESES.md addendum, run 1's own card); where "34 bps" and the IC figures
come from and whether they are right; whether the IC-to-cost arithmetic is sound; why the same
brief gave an idea on run_061 and "exhausted" on run_062; and whether a pre-backtest cost veto
by 1a is intended (hypothesis-design SKILL: `plausibility: implausible` → do not queue) or
too strong.

**Finding:** —

## O-4. Step 2 used a component class that does not exist

**Seen:** run_063's `innovation_expansion` proposed a variant `donchian_sentiment_gate` using
`strategies.strategy_components.FearGreedComponent`. No such class exists; the real one is
`FearGreedContrarianComponent`. The variant was dropped at backtest_specification
(`validate_config.py` violations) and its class was filed as a component request. Source:
`runs/run_063/artifacts/variant_patches.yaml`, `runs/run_063/c4_console.log`,
`campaign_record/component_requests.yaml`.

**Why surprising:** step 2 should build variants from the real catalogue, not from a guessed
name.

**To check:** which catalogue step 2 receives (STRATEGY_DESIGN_GUIDE.md, the component
registry, or none), and whether the class name comes from the prompt or is invented.

**Finding:** —

## O-5. Why were the SOL and XRP variants evicted instead of re-windowed? Is "at least 2 variants" right?

**Seen:** run_063 had 4 variants and only `base` (BTC) survived: `donchian_solusdt` was
refused for coverage (54/95 windows, 57%, below the D-042 60% floor) and `donchian_xrpusdt`
was refused by the data gate (XRPUSD 2022-05 missing 6.5% of bars, above the 5% tolerance).
With 1 of 4 left, below the required 2, the run parked before any backtest. Source:
`runs/run_063/c4_console.log`, `runs/run_063/artifacts/variants/`.

**Operator's view (2026-09-30):** variants exist to test the idea independently of the chosen
setup, so **at least two is right**: a confirmation in two separate tests. The surprise is
that SOL and XRP were evicted outright when a better window could perhaps have been chosen
to run those variants.

**To check:** D-042 / D-045 (partial coverage, 60% floor) and the E-054 data gate's 5% rule;
whether a variant can be re-windowed to the coin's covered period instead of refused, and
how that interacts with D-047 (a wider retest is a new trial) and the same-windows rule of
the grid; why step 2 picked coins whose data it could have checked in advance
(`coin_universe.yaml`, per-coin start dates).

**Finding:** —

## O-6. The park reason says "component" when two of three failures were data

**Seen:** run_063 parked as `waiting_for_component` ("missing class(es):
FearGreedComponent"), although the other two refused variants failed on data (coverage and
missing bars). Source: `runs/run_063/c4_console.log`, queue entry status.

**Why surprising:** the recorded reason decides what the operator does next (build a
component vs fix data); a mixed failure reported as one kind points the wrong way.

**To check:** how the park reason is chosen when variants fail for different reasons, and
whether it should list every reason.

**Finding:** —

## O-7. A breakout rule ("long above the 20-day high, short below the 20-day low") in a linear-forecast design

**Seen:** run_063's step 1a wrote the idea as a threshold rule: LONG when the daily close is
above the 20-day high, SHORT when below the 20-day low, fixed notional, no pyramiding.
Source: `runs/run_063/artifacts/hypothesis_card.yaml`.

**Why surprising (operator, 2026-09-30):** the strategy structure was designed so that a
signal is computed linearly and drives the allocation proportionally (forecast in
[-20, +20] -> allocation). An on/off breakout rule does not respect that linearity.

**To check:** what the design documents say about linear forecasts (DOC/STRATEGY_FRAMEWORK.md,
STRATEGY_DESIGN_GUIDE.md, the hypothesis-design SKILL); what step 1b actually built from the
card (`runs/run_063/artifacts/backtest_spec.yaml`: `DonchianBreakoutComponent` outputs the
close's position inside the N-bar range, which is continuous, not a threshold) and so whether
the tested config matches the card; and whether step 1a is told to express ideas as linear
forecasts.

**Finding:** —
