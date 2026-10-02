# Observations queue

Surprising behaviour the operator wants investigated together, in one sitting, rather than
one at a time. Each entry records what was seen and where, and why it is surprising. **It
says nothing yet about the cause.** Investigation fills in "Finding" and, if needed, a
decision (DECISION_LOG) or a ticket.

| # | Seen | Observation | Status |
|---|---|---|---|
| O-1 | C4 run_061, 2026-09-30 | "Long-only" trend component | found: bug -- component check at the wrong level (1b's gap was false); fix |
| O-2 | C4 run_061 → run_062, 2026-09-30 | Stage 2 sending the brief back to stage 1 | found: working as intended (card M); prompt gap |
| O-3 | C4 run_062, 2026-09-30 | Step 1a declaring the brief exhausted on a cost argument | found: exhaustion as intended; cost veto a design gap (decision) |
| O-4 | C4 run_063, 2026-09-30 | Step 2 inventing a component class name | found: bug (missing input), fix |
| O-5 | C4 run_063, 2026-09-30 | Asset variants evicted instead of re-windowed; the "at least 2 variants" rule | found: SOL as intended; XRP a design gap (decision) |
| O-6 | C4 run_063, 2026-09-30 | Park reason says "component" when most failures were data | found: reporting bug, fix |
| O-7 | C4 run_063, 2026-09-30 | A threshold (breakout) idea in a linear-forecast design | found: doc bug + fidelity gap (fix); forecast rule (decision) |
| O-8 | C4 run_061, 2026-10-01 | Data gate blocks every version over small gaps the backtest already handles | found: design gap; target design ticketed (CUL-367); run_061 continued by override |
| O-9 | C4 run_061, 2026-10-02 | Nothing before the backtest says which test windows are used, or how long they are | partly addressed: D-059 window_months + RUNBOOK 1f; automatic check parked (CUL-372); continuous testing open |
| O-10 | C4 run_061, 2026-10-02 | `base` made 0 trades in 95 windows: the forecast was shrunk ~1,000,000x | found: doc bug + missing fail-loud check; trial invalidated, run stopped |
| O-11 | C4 run_064, 2026-10-02 | The first C4 backtests ran, then grading stopped on two engineering faults | found: bugs, ticketed (CUL-369, CUL-370, CUL-368); queued-card pass_rule fixed (#296); CUL-368 partly fixed (#298); CUL-369 fixed (D-058, past results not re-scored) |
| O-12 | C4 run_064, 2026-10-02 | The brief's venue/product never reaches the backtest (data, fees, slippage) | fixed: D-057 (#298) -- the brief's venue reaches the protocol; remaining gaps listed; C4 briefs must say `perp` before relaunch |
| O-13 | PR #295 review, 2026-10-02 | The size check deliberately passes two "zero" cases: a zero rebalance floor, and an all-zero forecast | recorded (by design, #295); no action |
| O-14 | D-057 work, 2026-10-02 | A Binance run takes its fee from the spot schedule but its slippage and market check from the margin entry | parked (operator, 2026-10-02): no Binance research going forward, Kraken is the target venue |
| O-15 | CUL-369 work, 2026-10-02 | The whole-test chain never counts a window's first day (its anchor), so each window's entry-day P&L is left out | parked (operator, 2026-10-02): the entry it leaves out is a monthly-restart artifact, not a real cost; real issue moved to O-9 |

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

**Finding (2026-09-30 investigation, read-only; corrected the same day after the operator's
challenge -- the first version accepted 1b's claim and was wrong):** **bug in where the
component check runs (fix), plus a gap in the design guide.**

- **How a strategy config is built.** Each regime holds a list of component *instances*:
  `{id, class, params, weight, transforms}`.
  - The regime's forecast is the weighted mean of the instances' transformed values,
    clipped to ±20 (`trading-bot/strategies/strategy_engine.py:572-600`).
  - A weight may be negative. Only the regime's total weight must be > 0 (validator V8,
    `tools/validate_config.py:259-278`).
  - So a strategy is designed from a **combination** of instances, not from a single class.
- **A long/short SMA trend can be built today with no new code.** Two equivalent forms:
  - **Form A.** `SmaTrendLongOnlyComponent` (`lookback_L: 50`, `scaling_factor: 40`,
    weight 1) plus `BuyAndHoldStrategy` (a constant +10) with `scale` `factor: -2`
    (= -20), weight 1. That gives ½·{0, 40} + ½·(-20) = {-10, +10}.
  - **Form B.** The same SMA class with `scaling_factor: 10` at weight 2, plus
    `BuyAndHoldStrategy` at weight -1. That also gives {-10, +10}.
  - Checked on synthetic prices (no market data, no backtest, scratch script not
    committed): both forms pass the validator with zero violations. The engine's forecast
    is +10 when the prior close is above the prior SMA(50) and -10 otherwise, on 495 of
    495 bars.
- **So run_061's `component_gap` was false.** 1b said the transform pipeline "cannot enable
  [a] single component instance" to go short. That is true for one instance, but a config
  is not limited to one instance.
- **Where the component-existence check runs:**
  - **Code check, at the right level (the class).** Step 5a runs validator V12 on the
    written config, which requires every class to load, and the engine loads each class at
    start. This is what card J describes: a gap is "caught when the config is checked
    (Step 5a)".
  - **LLM check, at the wrong level (the "indicator").** The 1b SKILL says "If ANY
    required indicator/transform/regime is absent from the reference,
    status=component_gap" (`strategy-config-authoring/SKILL.md:130`).
    - 1b decides this before any config exists, and the code takes its word:
      `component_gap` leads straight to a component request and a park
      (`run_phase1_research.py:14250-14264`).
    - Nothing checks whether a combination of existing classes would do.
    - This is the gate that stopped run_061. It asked the operator to build a component
      that was not needed.
- **Why 1b missed it.**
  - The design guide gives the combination formula, calls `BuyAndHoldStrategy` a
    "constant +10" and says a weight is "normalized by sum". It never says that a weight
    may be negative or that a constant can serve as an offset, and it gives no
    composition example.
  - `WORKFLOW_CAPABILITIES.md` covers "signal direction inverted" (`negate`) but not "turn
    a one-sided signal into a two-sided one".
- **About the class itself.** `SmaTrendLongOnlyComponent` is long-only on purpose: the
  P4 brief says "spot-only, no shorts" (`strategy_components.py:942-998`). No other SMA
  class exists anywhere in `trading-bot/strategies/`. The standard two-sided SMA signal is
  available, but as a combination, not as a class.

**Recommended fix:**
1. **Guide.** Add a short "composing a signal" section:
   - weights may be negative (the regime total must stay > 0);
   - `BuyAndHoldStrategy` plus `scale` is a constant offset;
   - {0, +sf} becomes {-sf, +sf} as 2·x - sf;
   - a signed component becomes long-only with `clip` `min: 0`;
   - include the signed-SMA example above.
2. **1b SKILL.** Return `component_gap` only when no combination of existing classes,
   params, weights and transforms can express the signal. The decision must list the
   combinations it ruled out, and why.
3. **Code (operator decision).** Do not present a 1b gap as a verified one. Recommended,
   and the cheapest option: the park record and the component request label it "claimed
   by step 1b, not checked by code", so the operator reviews it before building anything.
4. A signed `SmaTrendComponent` class would be a convenience only. It is not needed.

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

**Finding (2026-09-30 investigation, read-only):** **working as intended (card M); small
prompt gap.**

- There is no route from stage 2 back to stage 1. run_061 parked at 1b, which left the
  queue empty. Decide-next's rule R2 then asked the still-open brief for another idea.
  That is card M as written: "Before declaring the queue empty, Step 10 re-reads open
  briefs and asks 1a for more" (`engineering_roadmap.html:436`, also `:929`).
- The code is `tools/decide_next.py` `_r2` (`:1499`). It stops after 2 empty R2 calls per
  brief (`BRIEF_MAX_CONSECUTIVE_EMPTY_R2`, `:163`). A parked owner stays eligible for R2.
- The backlog the operator expected is the queue itself. Card M lets 1a write several
  cards: one runs and the rest are queued. On run_061, 1a was offered that path
  (`BRIEF_HYPOTHESES.md` §1, `request: first_launch`), but nothing asks it for more than one:
  - the handoff template says "a single, testable ... hypothesis";
  - the hypothesis-design SKILL says "Create one explicit, testable strategy hypothesis"
    (`SKILL.md:9`) and "acceptable to produce ONE" (`:182`);
  - the addendum is neutral ("One card, or several").
- The C4 brief was itself a single idea (idea A). The result was one card, then an R2 call
  that found there was nothing else (about $0.34 over two attempts).

**Recommended answer:** on `first_launch`, ask 1a for up to 3 distinct cards when the brief
supports them (addendum wording only). Keep R2 as the empty-queue fallback.

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

**Finding (2026-09-30 investigation, read-only):** the exhaustion verdict is **working as
intended**; the pre-backtest cost veto is a **design gap -- decision for the operator**.

- **Inputs.** Both runs got the same inputs except one field.
  - Handoff `research_brief_to_hypothesis.yaml`:
    - `research_brief.yaml` (775 B): BTC/ETH 1h, multi-week momentum with inverse-vol
      sizing. It contains no numbers.
    - `available_feeds.yaml`, `indicator_library.yaml`.
    - Optional: `run_context.yaml` (63 B, only `run_type`), `feed_wishlist.yaml`,
      `campaign_knowledge_base.yaml` (~97 KB: per-mechanism IC results, `coverage_matrix`,
      `exhausted_mechanisms`).
  - Added by code: `exclusion_digest.yaml` (~7 KB), `criterion_menu.yaml` (~10 KB),
    `cost_model.yaml` (~17 KB), and `BRIEF_HYPOTHESES.md` + `brief_hypotheses_context.yaml`.
  - The one difference: on run_062 the context says `request: more_hypotheses` and
    `already_produced: [C4_VOL_MANAGED_TREND_MOMENTUM_V1]`.
  - These are live campaign files, not per-run snapshots, and prompts are not saved. The
    exact bytes 1a saw cannot be proven afterwards; the sizes above are today's.
- **Where the numbers come from.**
  - 34 bps = 2 x 17 bps: the BTCUSDT round trip in `cost_model.yaml` times the safety factor
    of 2 (SKILL `:364`). run_061's own card already wrote 34 bps with
    `plausibility: marginal`.
  - EMA -0.021 and MACD -0.015 are real knowledge-base rows (1h BTC, `ic_all_bars`).
- **The cost argument is wrong on its own terms.**
  - It assumed a 10-bar hold ("required IC = 0.34 / (50 sigma x sqrt(10)) ~ 0.215") for a
    brief about multi-week holds.
  - Its own formula at a 2-week hold (336 bars) gives a required IC of about 34 / (50 x
    sqrt(336)) ~ 0.04. That sits inside the 0.05-0.08 range it called plausible.
  - It also said the knowledge base's `exhausted_mechanisms` list covers EMA/MACD
    trend-following. That list has six ids (Keltner x3, RSI x2, ER detector) and no
    EMA/MACD/SMA entry.
- **Why the same brief gave an idea, then "exhausted".**
  - The cost-veto text is attempt 1, which was never accepted (it failed to parse; fixed in
    PR #277).
  - The accepted retry gives a different reason. The first card already covers the brief's
    mechanism; alternatives repeat price-only technicals with IC at or below zero in the
    knowledge base; gating is forbidden (A2.3).
  - That is what `BRIEF_HYPOTHESES.md` §3 asks for when no distinct idea is left, and the
    brief was one narrow idea. Same verdict, two different arguments: model variance.
  - The first card was not lost. It is parked `waiting_for_component` (O-1).
- **Is the veto intended?**
  - The hard rule (hypothesis-design `SKILL.md:369-372`, `implausible` -> do not queue) was
    moved to 1a from the retired validation stage (quant-validation Improvement 09).
  - Card E says cost survival is measured from a backtest's trade records. Card I puts
    mechanism plausibility into a ranking score.
  - A hard veto from the model's own arithmetic, before any backtest, conflicts with both.
    Here it was wrong.

**Recommended answer:**
1. Keep `cost_feasibility` on the card as information and as an input to card I's
   plausibility score.
2. Remove the hard "do not queue" veto at 1a. Cost survival is judged from the backtest
   (card E, profit bars).
3. Separately, save each stage's input files with their sha256 in the run folder, so a
   question like this one can be answered from the artifacts.

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

**Finding (2026-09-30 investigation, read-only):** **bug (missing input) -- fix.**

- Step 2 (`innovation_expansion`) writes config patches, including component swaps and
  additions. Its SKILL says "Reference the base config's actual shape
  (STRATEGY_DESIGN_GUIDE.md) before writing a path" (`innovation-expansion/SKILL.md:278`).
  But the stage is not given the design guide.
- Its inputs are `research_brief`, `hypothesis_card`, `available_feeds.yaml` and
  `indicator_library.yaml` from the handoff. Code adds `coin_universe.yaml`
  (`run_phase1_research.py:2829-2833`), `backtest_spec.yaml` and the exclusion digest.
  Stages are closed-book (no tools), so it could not open the guide.
- The only Fear & Greed reference it had is `indicator_library.yaml`'s entry
  `fear_greed_index_contrarian`, which gives an id but no class name.
- "FearGreedComponent" appears nowhere in the repo before run_063. The model invented the
  class name, its params (`buy_threshold`, `sell_threshold`, `action: gate`) and its
  behaviour (a pass-through gate). The real `FearGreedContrarianComponent` takes fear/greed
  thresholds and emits a contrarian +/-sf signal; it cannot gate.
- Step 5a caught it correctly (validator V12), so card K's "every component class exists"
  check works. But the invented class was then filed as a component request (card J), which
  asks the operator to build something that should not exist.

**Recommended fix:**
1. Add `docs/STRATEGY_DESIGN_GUIDE.md` to `_CLOSED_BOOK_STAGE_INPUTS["innovation_expansion"]`.
   This is the same catalogue 1b already gets.
2. Optional: when a V12 missing class has a close real name, put that near-match in the
   component request, so it reads as a naming error rather than a build request.

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

**Finding (2026-09-30 investigation, read-only):** **SOL: working as intended (D-042).
XRP: design gap, a decision for the operator. The "at least 2" floor did not cause this
park.**

- **The park was not caused by SOL or XRP.** Coverage skips do not count toward the floor.
  - `_variant_floor` (`run_phase1_research.py:14739-14748`) sets min_needed = min(3,
    variants - skips) = min(3, 4 - 2) = 2.
  - Only `base` was left, because the design variant failed (O-4).
  - With a loadable design variant, the run would have gone on to the backtest with base +
    design, both on BTC.
- **Is "at least 2" right?** Today the floor can be met with no asset variant at all, so the
  "two separate tests" can be two setups on the same coin. The guard sits elsewhere: a
  skipped asset variant caps the idea at INCONCLUSIVE (`tools/variant_coin.py:28-36`). Such
  a run gathers evidence but cannot reach the profit bars.
- **SOL.**
  - Its cache starts 2021-06-17 (`coin_universe.yaml:39`) and the protocol starts 2018-02,
    so it covers 54 of 95 monthly windows (57%, below 60%).
  - It **was** re-windowed: `window_coverage` keeps only the covered windows. It was then
    refused by the D-042 floor, which is correct under D-042.
  - Step 2 had the start date only as free text, and misquoted it in its own rationale as
    "2023-05-03". The skill asks for at least 60% coverage (SKILL `:267-271`), but step 2
    has no computed table.
  - Full-coverage coins in other categories exist, e.g. XRP, ZEC, XMR.
- **XRP.**
  - It covers 95/95 windows at Layer 1. The Layer-2 gate found one bad month (2022-05: 2
    of 31 daily bars missing, 6.5%, above the 5% tolerance) and returned `refine`.
  - The gate module defines `refine` as "a variant can be narrowed around (drop a bad
    window ...)" (`tools/data_availability_gate.py:8-9`). The variant loop never narrows:
    any outcome other than `validate` marks the whole variant not_tested
    (`run_phase1_research.py:1643-1670`).
  - Dropping that one window would leave 94/95 (99%). `variant_protocol(windows_run=)`
    already supports a window subset.
  - D-047(5) only makes a *later, wider* retest a new trial. A first test on 94 windows is
    simply the variant's first trial.

**Recommended answers:**
1. On a Layer-2 `refine` of an asset variant, drop the declined windows and re-apply the
   60% floor (behind a flag, with tests).
2. Give step 2 a code-computed per-coin coverage table for the run's protocol (windows
   covered out of the total).
3. Keep SOL refused unless D-042 is re-decided.
4. Do not make the floor require a tested asset variant. The INCONCLUSIVE cap already stops
   promotion, and blocking would stop BTC runs whenever the second coin lacks data, which
   is the reason D-042 exists.

## O-6. The park reason says "component" when two of three failures were data

**Seen:** run_063 parked as `waiting_for_component` ("missing class(es):
FearGreedComponent"), although the other two refused variants failed on data (coverage and
missing bars). Source: `runs/run_063/c4_console.log`, queue entry status.

**Why surprising:** the recorded reason decides what the operator does next (build a
component vs fix data); a mixed failure reported as one kind points the wrong way.

**To check:** how the park reason is chosen when variants fail for different reasons, and
whether it should list every reason.

**Finding (2026-09-30 investigation, read-only):** **small reporting bug -- fix.**

- The park kind is right. `_variant_park_kind` (`run_phase1_research.py:5100-5133`) ignores
  coverage skips, because SOL and XRP are non-blocking under D-042. That leaves one blocker,
  the missing class, so the entry parks as `waiting_for_component`.
- The message is misleading:
  - "1/4" counts all 4 variants, while "need >= 2" already leaves out the 2 skips.
  - It does not name either skip.
  - Only `artifacts/variants/index.yaml` lists all three reasons. `data_requests.yaml` has
    XRP only, and SOL is in no request file.
- Combined with O-4, the one reason shown sends the operator to build a class that should
  not exist.

**Recommended fix:** the park reason and the decision record list every not-tested variant
as blocking or non-blocking, with its reason. They also say that the idea is capped at
INCONCLUSIVE while asset skips remain.

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

**Finding (2026-09-30 investigation, read-only):** **doc bug + fidelity gap (fix), and a
design rule (decision for the operator).**

- **The framework does not require continuous components.**
  - The forecast is the weighted mean of the components, clipped to [-20, +20], and
    allocation = forecast / 10 (`DOC/STRATEGY_FRAMEWORK.md:29-32`). So allocation is linear
    in the forecast.
  - Several existing components are discrete. `FundingRateMeanReversion`,
    `FearGreedContrarian` and `MacdHistogramCrossover` output {-sf, 0, +sf};
    `SmaTrendLongOnly` outputs {0, +sf}.
  - An on/off breakout therefore maps cleanly to a discrete forecast. What the pipeline
    cannot express is position state: the card's 5-7-day time exit, its ATR x 2 stop, and
    "fixed notional, no pyramiding".
- **No document tells 1a to write the idea as a forecast.** `signal_concept` is free text
  (`hypothesis_card.schema.json:95-98`), and the hypothesis-design SKILL has no such rule.
- **1b did not build the card.**
  - `DonchianBreakoutComponent` (`strategy_components.py:422-434`) outputs where today's
    close sits in the range of the last 20 closes *including today*: (2*pos - 1)*sf.
  - That output is continuous and non-zero on almost every bar. It never "breaks out",
    because the close is always inside its own window. It is a stochastic-style
    oscillator, not a breakout rule.
  - 1b's rationale claims it fires on about 10% of bars. The base config was a different
    strategy from the card, with no exits, and nothing checks the card against the config.
- **The design guide misleads.**
  - It calls the output "breakout position" (`STRATEGY_DESIGN_GUIDE.md:222`).
  - It lists "Lower-band breakdown (short): scaling_factor -20" and "Wider channel (fewer,
    higher-conviction breaks)" (`:310-314`). The first only inverts the oscillator. The
    second is false: the output is never sparse.
  - 1b follows this guide (card K), so the guide's error became a config error.

**Recommended:**
1. Fix: correct the Donchian rows in the guide.
2. Decision: add a hypothesis-design rule: *write `signal_concept` as a forecast in
   [-20, +20], continuous or discrete, and name any exit the forecast cannot express.*
3. Decision: add a 1b rule: *map each clause of `signal_concept` to a config element, or
   list it as a declared deviation, or return `component_gap`.*
4. A true breakout component is a separate build. It would be latched: +sf after a close
   above the previous N-bar high, until a close below the previous N-bar low. The latch
   needs no position state.


## O-8. The data gate blocks every version over small gaps the backtest already handles

**Seen:** run_061 (resumed 2026-10-01 after its component park) paused at the per-variant
data-availability gate with 0 of 4 variants left (`variant_gate_insufficient`), before any
backtest. `base` and `design_sma_21` (BTCUSDT 1h) were refused because 21 of 95 monthly
windows were `refine` (some bars missing, each <= 5%). Source: `c4_run_once.log`,
`runs/run_061/artifacts/variants/*/data_availability_gate.yaml`.

**Operator's view (2026-10-01):** separate two cases.
1. **Data quality:** holes inside a window. Accept them while the overall quality of the
   data set holds (small, or even medium, gaps; a share of the data set, or a better
   formula).
2. **Missing window:** a missing interval at a window boundary, including "one bar, then a
   long gap". That is what `refine` should be for: not evict, but **shrink the window so it
   starts at the end of the missing interval** -- down to a **minimum tested window
   length**; below that minimum the window is dropped (operator, 2026-10-02).

**Finding (2026-10-01, measured):** **design gap. The current logic does neither.**
- The gate rates a window by its missing fraction only (0% validate, <= 5% refine, > 5%
  decline, `tools/data_availability_gate.py:36-40, 462-466`). It does not look at where a
  gap sits or how long it is.
- In the variant loop, any outcome other than `validate` marks the variant not_tested
  (`run_phase1_research.py` ~1659). A `refine` therefore evicts the version; nothing trims.
- Every one of run_061's 21 flagged BTC windows is case 1: all gaps are interior, 1-33 h
  each, 121 h in total, about 0.17% of the data set, worst window 4.9%. None touches a
  window boundary.
- The backtest has handled such gaps since #288 (gap rule on by default: ignore <= 3 bars,
  flatten and re-warm after a large gap). So this gate blocks every 1h BTC/ETH idea over
  the full protocol for gaps the engine already absorbs.
- Same family as O-5 (an XRP variant evicted on one `refine` window instead of
  re-windowed). CUL-367 generalises O-5's recommendation 1 from asset variants to every
  variant.

**Challenge (agreed as the starting point):**
- A data-set-wide percentage alone can hide one bad window, so keep a per-window ceiling
  too.
- "Short" and "long" should be measured against the strategy's warmup, not a fixed
  percentage.
- A long *interior* gap behaves like a boundary gap: the engine already flattens and
  re-warms after it, so the window effectively restarts there.
- A trimmed window must leave room for the warmup after the gap, and keep at least the
  minimum tested window length (to be set: e.g. a share of the window's bars, or a number
  of bars tied to the strategy's horizon); below it the window is dropped.
- Trimming makes per-window metrics noisier. Whole-period metrics (D-034..036) are
  unaffected.
- The rule must be mechanical and pre-registered, never applied after seeing results.

**Actions:**
1. Target design ticketed: **CUL-367** (quality vs missing window; trim instead of
   evict). Not built yet.
2. run_061 was continued by a recorded operator override: `base` and `design_sma_21` were
   marked validated as "interior quality gaps only". `asset_xrpusdt` (one window 6.7%) and
   `asset_solusdt` (57% coverage) stay not_tested, so the idea stays capped at
   INCONCLUSIVE. Record: `runs/run_061/artifacts/human_resolution.yaml`, and the variant
   reasons in `artifacts/variants/index.yaml`.


## O-9. Nothing before the backtest says which test windows are used, or how long they are

**Seen:** run_061's pre-backtest steps (1a, 1b, step 2, 5a, data gate) produced no
statement about the test period. The windows appear only in a generated file,
`protocols/run_061_generated.json`: 1h bars, **95 monthly windows from 2018-02 to 2025-12**,
about 69,000 bars per coin, for every variant.

**Operator's view (2026-10-02):** we should see how the tested window is selected and how
long it is. It should be limited, dynamically or statically, so a backtest does not run on
a too-large data set.

**Facts so far (not yet a finding):**
- The protocol comes from `machine_constraints.protocol` in the run's pre-registration
  (`_ensure_protocol_from_constraints`, `run_phase1_research.py` ~8925-8950), which comes
  from the brief's frontmatter. `briefs/C4_vol_managed_trend.md:27-31` (branch c4/flag-set) sets start
  2018-02-01, end 2025-12-31 and timeframe 1h; its own comment says the protocol block is
  copied from the template.
- So the period is fixed by hand in the brief and cut into monthly windows. No stage
  chooses it, checks it against the idea's horizon, or reports it.

**To check:**
- Who may set or change the period: brief author, 1a, 1b, step 2; and whether any
  skill or handoff tells them about it.
- Window length vs the idea's horizon: monthly windows on 1h bars vs an SMA(50) trend;
  a daily idea on monthly windows.
- A cap or rule: a static maximum number of bars or windows, or a dynamic one derived
  from timeframe, holding period and the required trade count (D-035: >= 100 trades per
  coin). Weigh this against the era-stability bar (2018-20 / 2021-22 / 2023-25), which
  needs the long history.
- How the train (2018-2023) / validate (2024-2025) split is applied inside these 95
  windows.
- Cost: backtest time per variant at 69,000 bars, and how it scales with variants and
  coins.
- Show the period in a pre-backtest artifact or log line, so the operator sees it before
  any trial is spent.
- **Added 2026-10-02 (from O-15, parked): monthly restarts distort slow strategies.**
  - **Entries:** every window starts flat with fresh money, so a slow strategy re-opens
    its position at each window start, about 95 artificial entries over the test.
  - **Exits, confirmed 2026-10-02:** the engine also force-closes any open position on
    each window's last bar (`_close_all_positions_at_end`); run_protocol labels these
    exits `end_of_window` (`_classify_exit_reason`). On run_054 (6-month windows) about
    14% of exits were such forced closes. So monthly windows add an artificial entry
    AND exit per window.
  - **First step, done:** D-059 lets a brief choose fewer, longer windows
    (`window_months`); RUNBOOK 1f.
  - **Possible directions:** carry the position across windows, or test in one continuous
    run and split the results by window afterwards.


## O-10. `base` made 0 trades in 95 windows: the forecast was shrunk about a million-fold

**Seen:** after the O-8 override, run_061's `base` variant backtested 95 windows with **0
trades**. The forecasts were about 1e-5 in size (window 2018-12: |forecast| <= 4.4e-5), so
every allocation change (~4e-6) failed `min_allocation_change` (0.2) on all 768 bars. Source:
`runs/run_061/variants/base/results/20261001T215100Z_d947d333/bars.csv` and `metrics.json`.

**Finding (2026-10-02, measured):** **a units bug the documentation steers into, with
nothing to catch it.**
- 1b's base config is `MovingAverageDistanceComponent` (sma, period 50, scaling_factor 10),
  whose output is a percent, followed by `transforms: [{op: vol_adjusted}]`, which it chose
  to express "vol-managed".
- `vol_adjusted` computes v / (`stddev_24` x close) (`trading-bot/strategies/registry.py:71-76`).
  `stddev_24` is the 24-bar rolling standard deviation of the close in price units
  (`main_strategy.py:82`). The divisor is (dollars x dollars), about 1e5-1e7, so any
  component's output becomes microscopic.
- It only works when followed by a rescale that cancels the factor: the documented
  `history_transforms: vol_normalize` + `ratio_to_mean` pattern. Used alone, the signal
  never trades.
- The design guide recommends it alone for this purpose ("a signal can be divided by
  recent volatility with a data-aware transform such as `vol_adjusted`",
  `STRATEGY_DESIGN_GUIDE.md` ~459). Its transform table gives the formula but not the
  resulting scale (`:298-299`).
- Nothing checks the forecast's size: the validator, step 5a, the data gate and the engine
  all accept a forecast that can never reach the rebalance threshold. The result looked
  like an ordinary "0 trades". Had the run finished, the idea would have been graded on
  a bug.

**Actions (operator, 2026-10-02):**
1. Run stopped during the `design_sma_21` backtest (same transform). No grid, reader or
   idea_status was written. `run_061` is paused at protocol_execution.
2. Trial `run_061:base` marked `invalidated_artifact` with the reason (kept, not deleted;
   run_044 precedent).
3. Next: a small PR with (a) the guide and catalog stating each transform's input units
   and resulting scale, without recommending `vol_adjusted` alone; and (b) a fail-loud
   check that refuses a forecast that cannot reach the rebalance threshold. Then send
   run_061 back to step 1b to re-author the config.


## O-11. The first C4 backtests ran, then grading stopped on two engineering faults

**Seen:** run_064 relaunched run_061's card past step 1a (new run id, so its trials count: the
trial recorder skips a repeated trial_id). Step 1b re-authored the config with the corrected
guide (`vol_normalize` history + `ratio_to_mean` + `scale` 10); the D-056 size probe passed it
(88% of sample bars tradable). Two variants were backtested on 95 monthly BTCUSDT 1h windows,
then protocol_execution halted before grading.

**Measured results (trials, counted in N):**

| variant | trades | pooled gross | pooled net | median Sharpe |
|---|---|---|---|---|
| `base` (scale 10) | 32,648 | -1,354.1 | -12,172.7 | -2.879 |
| `V1_conservative_scale` (scale 5) | 20,513 | -726.6 | -6,098.8 | -2.605 |

Negative before costs; the vol-normalised signal changes size every bar, so it rebalances
several times a day and costs dominate. These figures are not graded: see the faults below,
and the window overlap inflates pooled totals by about 3%.

**Engineering faults found on the way (each its own ticket or PR):**
1. **Windows overlap by one day (CUL-369, Urgent).** Each window's backtest includes the
   whole end day (2018-03 window: 2018-03-01 00:00 to 2018-04-01 23:00, 768 bars). The next
   window starts on that day, so it is counted twice and the grid's time-ordered fit refuses
   the data (`RecordOrderError`). This likely affects every past monthly-window run.
2. **Category report over its size budget (CUL-370).** `profitability.yaml` would be 716,645
   characters (budget 400,000) on 95 windows x 2 variants: a per-window grouping grows
   unbounded. Same root as O-9: nothing caps the protocol length.
3. **No Kraken asset variant can be backtested (CUL-368).** `cost_model.json` has no
   (kraken, margin) entry and run_protocol passes no market_type. The D-056 probe caught it
   on `asset_aaveusdt` before spend; it is now a D-042 coverage skip.
   *Update 2026-10-02:* partly fixed by D-057 (#298). On a run whose brief names Kraken
   futures, asset variants are priced on (kraken, futures), which has a cost entry. Still
   open: on a Binance run, a Kraken-only coin (XRP, AAVE) still resolves to (kraken, margin),
   which has none.
4. **A queued-card launch got no pass_rule** (the first one ever): it skips 1a, so
   `_write_pass_rule_from_card` never ran and the specialist_readers pre-flight refused the
   run before spend. Filled by hand for run_064; fixed and merged (#296).
5. Step 2 once wrote only 1 of its 3 files (16k output tokens, 1 turn). A single retry wrote
   all three. The raw answer is not kept when some files parse, so the cause is unknown.

**State:** run_064 is halted at protocol_execution (status failed). Its two trial rows are
recorded. Nothing runs on its own. Grading needs CUL-369 (and CUL-370) first.

**Dated note (2026-10-02), CUL-369 fixed by D-058:**
- **The convention now:** `test.end` is the last included day everywhere, and windows no
  longer share a day.
- **Past monthly-window results are NOT re-scored** (operator decision). Every run whose
  protocol wrote `end` as the next window's start backtested that day twice. Its pooled
  totals, trade counts and pooled IC double-count about 1 day in 30 (~3%), and must be
  read with that in mind:
  - the 10 hand-made protocols before their migration;
  - every `run_0xx_generated.json`.
- **Runs holding a pre-D-058 generated protocol** (at the time: run_061, run_063, run_064).
  The launch pre-flight now refuses them with the right remedy:
  - **no data spent yet** (run_063): delete `run_063_generated.json`; it regenerates from
    the unchanged pre_registration.yaml;
  - **data already spent** (run_061, run_064): the run cannot resume; relaunch the idea
    under a new run id. Their recorded trials stay counted.


## O-12. The brief's venue/product never reaches the backtest

**Seen:** the C4 brief declares `venue: kraken`, `product: spot`. run_064's backtests nevertheless
ran on **Binance** BTCUSDT data, with the **spot** fee from `config/cost_model.yaml` (7.5 bps
per side) and **Binance margin** slippage from `trading-bot/config/cost_model.json` (1 bps).
The Kraken asset variant (AAVE) crashed on a missing (kraken, margin) cost entry (CUL-368).

**Operator's view (2026-10-02):** the venue is declared in the brief, and C4 should model
**Kraken futures**. The operator remembered a feature that takes the declared venue, checks
its costs and data, and applies them to the backtest.

**Finding (2026-10-02, read in code and Linear):** **that feature was designed but deferred,
never built.**
- **E-015** (Completed): venue + product are required at registration. A non-tradable product
  is flagged `research_only`, and the holdout refuses research-only ideas. It never touches
  data or costs.
- **E-014** (Completed): tradability and the data-availability declaration. Its child
  **CUL-46, "Venue/Exchange model -- deferred design epic (joint design with Jeremy)"**, is
  the wiring itself, and it is still Backlog. CUL-287 (the data fetcher hard-codes `spot`) is
  part of the same gap.
- In code, `run_campaign.py:465-469` says it outright: *"venue has NO protocol-side
  counterpart"*. `venue`/`product` feed only the tradability check (`:768-773`).
- Each piece decides on its own:
  - Data: the protocol's `exchange` field, absent, so Binance (run_protocol "Option Y").
    Non-Binance coins in per-coin variants go to Kraken.
  - Fee: run_protocol's `--cost-product`, never passed, so `spot`.
  - Slippage and the (exchange, market) existence check: the engine's `market_type`, never
    passed, so config.json's `margin`.

**Next (superseded):** Phase A of the wiring. Map every place that decides exchange, market,
fee and slippage, plus which caches exist per venue/market (Kraken futures OHLCV and funding for
BTC/ETH). Then STOP for the operator's nod. No C4 backtest until it is in.

**Resolution (2026-10-02, D-057, PR #298 merged):** the brief's (venue, product) now reaches
the backtest. `tools/venue_resolver.py` turns it into protocol keys at protocol creation:
`exchange`, `market_type`, a `venue` label block, and the coins in the price source's naming
(Kraken spot: `BTCUSD`). run_protocol passes the market to the engine. The fee comes from
`trading-bot/config/cost_model.json` for a venue run, and every result records what was
modelled. Operator decisions:
- **Kraken futures = option A.** Kraken SPOT prices are a declared proxy
  (`venue_data_capability.yaml` `kraken.futures.price_proxy`), with Kraken FUTURES fee
  (5 bps) and slippage.
- **Binance (or no venue): nothing written, byte-identical.**
- **No separate registration gate (CUL-183).** A venue that cannot be resolved fails loud
  at run start, before any LLM call.

The safety review's blocker and majors were fixed before merge:
- the pre-flight rebuild keeps the venue;
- the funding feed is dropped;
- grading uses the recorded fee;
- a protocol that does not match the brief's venue is refused.

**Remaining gaps (known, not fixed here):**
- **Funding is not modelled** for Kraken futures. The result label says so, and the
  `funding_rate` feed is dropped, so a config that needs it is refused.
- **CUL-368** is half fixed (see O-11 item 3).
- **A Kraken brief now refuses any protocol without its venue.** That covers a
  protocol_ref pin, a hypothesis-split child, a refine brief and the fallback. These used to
  run silently on Binance; now they stop with an `[O-12]` error. A split child of a Kraken
  brief therefore cannot run until split children inherit the generated protocol.
- **Both C4 briefs still declare `product: spot`** (`briefs/C4_vol_managed_trend.md`,
  `briefs/C4_donchian_daily_trend.md`). There is no (kraken, spot) cost entry, so their next
  launch will stop at protocol creation. The operator chose Kraken futures; the briefs must
  say `perp` first. Whether to edit them in place or register new briefs is open: past
  trials on these briefs ran on Binance.
- Binance runs: see O-14.


## O-13. The size check deliberately passes two "zero" cases

**Context:** PR #295 (D-056, forecast-size probe), reworked 2026-10-02 to bug-only on invented
data. Recorded at the operator's request so the behaviour is not mistaken for a gap later.

**1. A zero rebalance floor.** A strategy config may set its own
`strategies.min_allocation_change` (the engine uses it instead of config.json's 0.2). At 0,
every nonzero forecast moves the position, so no size can be a bug. The probe's threshold is
then 0 and it never refuses on size, only on an all-NaN forecast. Pinned by
`tests/test_d056_forecast_size_probe.py::test_a_zero_strategy_floor_means_any_nonzero_forecast_trades`
(a 1e-9 forecast passes at floor 0). A negative floor fails loud
(`test_a_negative_strategy_floor_fails_loud`).

**2. An all-zero forecast.** If the forecast is exactly 0 on every bar of the invented series,
the probe passes it with a note ("silent"), never a refusal. A rare-event strategy can be
silent on any sample, and how often a strategy trades is the backtest's question, not the
probe's (operator, 2026-10-02). Pinned by
`test_a_forecast_silent_on_every_bar_passes_with_a_note`; the mutation that refuses it is caught.

**What the probe still refuses:**
- every forecast is NaN;
- a nonzero forecast whose largest magnitude stays below 1/100 of 10 x the floor (a
  units/scale bug; run_061 was 9e-7 vs 2.0);
- a forecast that sits at the +/-20 cap on every one of its nonzero bars, with at least 100
  such bars (`MIN_ACTIVE_BARS_FOR_CAP_CHECK`). This is the same mistake in the other
  direction: the signal is scaled so large it is always clipped, so it carries no size
  information. The operator framed it as persistence above the cap, not frequency.

The probe runs at each coin's own price level (`PRICE_LEVELS`), so a price-unit bug shows up
at the coin's real scale.

**Consequence to keep in mind:** a config whose forecast is silent because of a bug (e.g. a
regime that never activates on any data) passes the probe. The backtest shows it as 0 trades
and the readers must report it as such, not as a market result.


## O-14. A Binance run mixes the spot fee with margin slippage

**Seen (2026-10-02, while building D-057):** a run with no venue (every Binance run so far) is
charged:
- its **fee** from `strategy-research/config/cost_model.yaml`, Binance **spot** schedule,
  7.5 bps per side (run_protocol `--cost-product`, never passed, so `spot`);
- its **slippage** and the engine's (exchange, market) existence check from
  `trading-bot/config/cost_model.json`, Binance **margin** (the engine's default
  `market_type`). That entry's own fee is 10 bps and is not used.

`cost_model.yaml`'s header calls it the "single source of truth" for fees, while E-010 made
`cost_model.json` the single cost source -- and the research path never moved its fee over. So every past Binance result
modelled one market's fee with another market's slippage.

**Why it matters:** it is a cost assumption no-one chose. Moving Binance runs to the json fee
(10 bps) raises the modelled cost of every Binance trade and changes every Binance result, so
it invalidates baselines.

**Next:** its own declared PR (deferred from D-057 on purpose). Decide which market Binance
research models (spot or margin), make that one entry the source of both fee and slippage,
re-pin the tests that assert 7.5 bps, and state the before/after on a reference run. No
re-scoring of past results unless the operator asks.

**Parked (operator, 2026-10-02):** no more time on Binance cost modelling. Research
moves to Kraken, the venue the team will trade on (the operator notes regulation limits
Binance use in France; not verified here). Kraken runs take both fee and slippage from
one `cost_model.json` entry (D-057), so this mix does not affect them. Reopen only if a
Binance run is ever needed again.


## O-15. The whole-test chain never counts a window's first day

**Seen (2026-10-02, while fixing CUL-369):** `portfolio_whole_test.chain_windows` normalises
each window at its close on its first common day (the anchor, the v1 per-window definition).
The window's own return for that day is never counted: the move from its first bar to that
day's close, which includes opening the position and its entry cost.
- **Before CUL-369** windows shared a day, and the previous window's backtest supplied that
  day's return (a "junction").
- **Now** windows are back to back, and each boundary is a flat link with no return. So
  one daily return per window boundary is missing from the whole-test Sharpe, and coverage
  dips about 1 day in 30 (monthly: ~0.97, above the 0.9 floor).

**Why it may matter:** in both layouts, the window's own first-day P&L, including its
entry cost, is not in the chain. For a strategy that re-enters at every window start, that
leaves out one entry cost per window.

**Next (superseded):** open. Possible fix: anchor each window at its starting equity (before
its first bar) instead of its first close, so the first day's return is counted. That
changes the whole-test definition (E-062), so it needs its own decision. Not part of CUL-369.

**Parked (operator, 2026-10-02).** The fix above would add the wrong thing:
- **The entry is a test artifact.** Each monthly window starts flat with fresh money, so
  the strategy opens a position on day 1 of every window: about 95 entries over the test.
  A strategy running live opens once and holds across months; it never pays those
  monthly entries. Counting them would penalise the strategy for how it is tested, not
  for how it trades. That weighs most on slow strategies, such as C4's (~100 trades per
  coin over the whole test).
- **The only real gain is one daily return in ~30 added to the whole-test Sharpe.** That
  makes it slightly more precise; it does not remove a bias.

The underlying issue is testing slow strategies in one-month pieces at all. That is moved
to O-9.

---

## Recommendation: how C4 reaches its first backtest (2026-09-30 investigation; revised after the O-1 correction)

**Cheapest route: fix O-1 and O-4 first, then unpark run_061's idea.** Both fixes are
prompt and doc changes, one small PR each:
- the design guide's "composing a signal" section and the 1b SKILL rule (O-1);
- the design guide given to step 2 (O-4). Without it, step 2 can invent a design variant
  again and park the run, as it did on run_063.

Then `--unpark C4_vol_managed_trend`. Its park resumes at step 1b
(`resume_stage="strategy_config_authoring"`, `run_phase1_research.py:14264`), so one 1b
call re-authors the config with the long/short SMA composition. That reaches the backtest
with no new component, and it tests the O-1 fix directly.

**Be honest about the expected outcome.** A textbook moving-average signal on BTC/ETH 1h
is the lane this project's own kill-map lists as dead, so expect a FAIL. That is still
useful for C4, whose purpose is to show that real runs reach the backtest, the readers
and the profit bars. It costs one trial row. Not checked: whether the card's inverse-ATR
sizing (clipped 50%-200%) can be expressed with the existing `vol_*` transforms. 1b should
report that as a declared deviation if it cannot.

**The Donchian brief comes next.** First correct the Donchian rows in the guide (O-7).
Before building a latched breakout component, check whether a combination of existing
classes can express it (the O-1 lesson); I have not checked this either way.
- Before choosing between a fresh entry and `--unpark C4_donchian_daily_trend`, check
  whether unpark reuses run_063's saved variant set, which still names the invented class.
- Also settle the queued `C4_donchian_daily_trend__more_1`: it asks 1a for a *second*
  Donchian idea, not a re-run.

The O-3 veto change, XRP narrowing (O-5) and the park-reason fix (O-6) can follow C4; none
of them blocks the first backtest.
