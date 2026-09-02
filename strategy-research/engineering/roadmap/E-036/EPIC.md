# E-036 — An adjacency key that reflects what a strategy actually is

**State:** rejected, restart needed — the design below shipped and works as
built, but Jérémy does not trust what it measures. Out of radar until this
epic is deliberately restarted.
**Owner:** Jérémy
**Updated:** 2026-09-02

## Why

E-032's anti-adjacency gate decides "have we tried this already?" using the key
`(family, instrument, timeframe)`. That key ignores everything that
distinguishes one strategy from another in this engine, so it refuses
legitimate research as if it were a repeat.

Found by the operator 2026-08-27. **Not** caught by the high-effort code review
that preceded it — that review checked the gate's logic for correctness and
never asked whether the key was the right key.

### Measured: the key discards most of the real discrimination

Across the **39 runs** carrying both a `hypothesis_card.yaml` and a
`candidate_strategy_config.json`:

```
distinct strategies under the CURRENT triple        : 18
distinct strategies under a composition fingerprint : 34
```

**The current key collapses 21 of 39 runs into "already tried". The fingerprint
collapses 5.** So the gate as built would wrongly refuse over half the corpus.

### Measured: a parameter sweep reads as a repeat

Reproduced against the live gate:
```
candidate: keltner_channel, BTCUSDT, 1h, atr_mult 3.0 (prior run used 2.0)
verdict  : refuse
reason   : family 'keltner_channel' already run at (BTCUSDT, 1h)
```
Real cases the key destroys: `run_009` (`rsi`, `scaling_factor 0.01`),
`run_011`/`run_012` (`rsi`, `0.4`), `run_010`/`run_013` (`rsi_pullback`, a
different component) — all one triple today.

### What a strategy actually is

```
strategies.regimes.<regime>.components[]
     -> id, class, params{...}, weight, transforms
regime_detector
     -> mode, components[], rules[], default_regime
```
N weighted, parameterised components allocated per regime — and the detector is
itself composed. The digest reads none of it: grepping
`build_exclusion_digest.py` for `components|weight|regime|params|transforms`
returns 3 hits, all prose comments or an unrelated passthrough.

### Origin, so the fix does not swing back

The triple was a deliberate coarsening in E-032 S1. The flat lists it replaced
(`instruments_tried`/`timeframes_tried`) were **family-blind** — a `4h` entry
from keltner runs made 4h look tried for the funding family too. The triple
fixed that wrong direction and introduced the opposite one. **A fix must not
re-introduce family-blindness while removing over-refusal.**

## The structural obstacle

`hypothesis_card.yaml` — what the digest scans today — has **no structured
parameters**. "SMA(100)" exists only as prose inside `signal_concept`. The
structured composition lives in `candidate_strategy_config.json`, produced
later by `backtest_specification`, and present for **41 of 59** run dirs
(hypothesis cards: 48).

So the fix must read the config, tolerate runs that never produced one, and
**degrade honestly** — never silently treat "no config" as "no match".

## The design (complete — S2 implements this, it is not a research question)

### 1. Build the digest from the structured config, falling back on the card

Per run, prefer `candidate_strategy_config.json`. Derive a
**composition fingerprint**: the sorted set of
`(regime, component_id, sorted(params), weight)` across
`strategies.regimes.*.components[]`, plus the detector's `mode` and rule count.

Where no config exists, fall back to the current coarse triple and **tag the
entry `fidelity: coarse`**. Fidelity must be carried into the gate's decision,
not dropped.

### 2. Three outcomes, not two

Replace the binary refuse/admit at Layer 2 with:

- **REPEAT -> REFUSE.** Same family, instrument, timeframe **and** an identical
  composition fingerprint. This is a genuine re-run and is the only case that
  blocks.
- **NEIGHBOUR -> ADMIT, with context.** Same `(family, instrument, timeframe)`
  but a *different* fingerprint — a different parameterisation, a different
  component set, or a different regime allocation. **Admit it, and attach the
  near neighbours to the result** (`run_ids` and how they differ). A parameter
  sweep proceeds, and the generator is told what it is near.
- **NOVEL -> ADMIT.** No family/instrument/timeframe match at all.

This is the core of the fix: **the digest becomes informative rather than
purely prohibitive.** Blocking is reserved for exact repeats; everything else
becomes signal the idea-generation stage can use.

### 3. A coarse-fidelity match never hard-refuses

If the only evidence of a prior run is a `fidelity: coarse` entry (no config on
disk), it can produce NEIGHBOUR at most, never REPEAT. We cannot prove an exact
repeat from a record that never captured composition, and refusing on it would
be the flattering-direction error this project keeps finding.

### 4. Regime allocation is part of identity

`(mean_reversion, rsi, period=14)` and `(trending, rsi, period=14)` are
different strategies and must not collide. The fingerprint keys on the regime
each component sits under, so this falls out for free.

## Done when

1. The digest carries a composition fingerprint derived from the structured
   config, with an explicit `fidelity` field per entry.
2. Layer 2 returns REPEAT / NEIGHBOUR / NOVEL; only REPEAT refuses.
3. A parameter sweep on an already-tried family/instrument/timeframe is
   ADMITTED, with its neighbours attached.
4. A coarse-fidelity entry can never produce a REPEAT.
5. Same component under a different regime does not collide.
6. Off by default with a bit-identity proof; both suites green.

## Stories

- [x] S1 — **Design.** Done 2026-08-27 by the dispatching session, from
      measurements already in hand (the 18-vs-34 count, the reproduced
      parameter refusal, the 41/59 coverage, the real config shape). No
      separate design dispatch was warranted.
- [x] S2 — **Build.** Done 2026-08-27. Implemented the fingerprint, the
      three-way outcome, and the fidelity rule. See the Log entry below for
      the corpus re-comparison, the regression-test disposition, and both
      suites' numbers.

## Relationship to other epics

- **E-032** (done) — owns the gate this fixes. Its Layer 1 (KB, mechanism
  grain) is unaffected and stays as-is; this is a Layer 2 change only.
- **E-034** (done) — supplies `variant_selection.yaml`, whose resolved
  instrument/timeframe the second gate call already uses. Unchanged here.
- **E-035** (new) — external ideas will hit this same gate. A gate that
  refuses over half of what it sees would strangle that epic on arrival.

## Success signal (pre-registered)

Re-running the corpus comparison after S2 yields ~34 distinct strategies rather
than 18, and the reproduced keltner `atr_mult 3.0` case returns ADMIT with
`run_016` attached as a neighbour rather than REFUSE.

## Log

- 2026-08-27 — `planned`, design complete. Opened after the operator challenged
  the key during the session summary review: *"the three keys look a bit too
  simplistic ... does it mean that once tried, we cannot retest the same
  indicator with different parameters?"* Both halves of that were confirmed by
  execution. Notion bug:
  https://app.notion.com/p/3c91d1fb05a2815cb309dc1029fe6ab1

- 2026-08-27 — S2 build complete. Implemented exactly the four design points
  in `tools/build_exclusion_digest.py` (`composition_fingerprint()`, the
  structured/coarse split in `scan_run_triples()`) and
  `tools/anti_adjacency_gate.py` (`layer2_digest_check()`'s REPEAT/NEIGHBOUR/
  NOVEL outcomes). Layer 1 (`layer1_kb_check`) untouched.

  **MEASURED — corpus re-comparison (denominator stated per number, all via
  the current `scan_run_triples`/`composition_fingerprint`, not re-derived by
  hand):**
  - Full digest, all 46 run dirs with a parseable `hypothesis_card.yaml`
    (`build_digest()`'s own `runs_scanned`), fanned across every named
    instrument/timeframe: distinct under the OLD `(family, instrument,
    timeframe)` key = **30**; distinct entries under the NEW `(family,
    instrument, timeframe, fingerprint)` key = **73** (2.4x).
  - Restricted to the 39 runs carrying BOTH `hypothesis_card.yaml` AND
    `candidate_strategy_config.json` (the epic's own stated denominator),
    one entry per run using the FIRST-listed instrument/timeframe (matching
    `evaluate_candidate`'s own default resolution): OLD = **13**, NEW =
    **36** (2.8x).
  - Neither reproduces the pre-registered 18/34 exactly — the original count
    was a one-off measurement whose exact fan-out/dedup convention was not
    committed as a re-runnable script, so an identical repro wasn't possible.
    Both re-derivations agree with it in direction and magnitude (roughly
    2.5-3x more distinct strategies visible under the fingerprint), which is
    the actual claim being tested. Labelling this a partial repro, not a
    match, per this project's "measure, don't estimate" rule.
  - Live proof against the REAL `keltner_channel`/`BTCUSDT`/`1h` bucket (was
    ONE triple of 11 run_ids under the old key): now **9** distinct
    structured entries (two genuine internal repeats: `run_025`+`run_032`,
    `run_033`+`run_034` share identical fingerprints; the rest differ). A
    synthetic candidate with a novel `atr_multiplier` correctly ADMITs as
    NEIGHBOUR, with `run_016` present among the attached neighbours —
    the exact shape of the pre-registered success signal, verified against
    the live digest rather than only a synthetic fixture.

  **Regression disposition (test_anti_adjacency_gate.py,
  test_variant_anti_adjacency_gate.py, test_anti_adjacency_retry_policy.py):**
  every failure after the S2 change was a bare `(family, instrument,
  timeframe)` collision that used to REFUSE and now correctly ADMITs as
  NEIGHBOUR (design point 3: a coarse-fidelity or candidate-side-unfingerprinted
  match can never prove REPEAT). Three tests whose actual subject was the
  REFUSE-driven retry/escalation POLICY (not Layer 2 itself) were rebuilt on a
  genuine Layer-1 KB refusal instead, since `_route_post_innovation_expansion`
  runs before `backtest_specification` ever produces a config and can
  therefore never supply a candidate fingerprint — REPEAT is structurally
  unreachable at that call site, by design, not a gap. Two tests whose subject
  WAS the REFUSE contrast itself (`test_pivot_away_from_clean_parent_...`,
  `test_refuse_escalates_immediately_...`, `test_refuse_classifies_via_...`)
  were upgraded to a genuine identical-fingerprint repeat so the REFUSE they
  test for is still reachable and still real. One test
  (`test_multi_symbol_parent_card_checks_every_instrument_not_just_one`) was
  repurposed to prove the per-instrument NEIGHBOUR annotation survives
  multi-instrument selection (see the `_route_post_variant_selection` REFUSE
  > NEIGHBOUR > first-result priority fix below) instead of proving REFUSE.
  No failure was silently reverted to pass; every changed assertion is
  commented in-file with why.

  **Small necessary extension beyond the four literal design points:**
  `_route_post_variant_selection` (`workflow/run_phase1_research.py`) now
  reads `backtest_spec.yaml`'s own `config` field (the exact dict written
  moments later, verbatim, to `candidate_strategy_config.json`) and passes it
  as `candidate_config` — without this, the ONE call site with a composition
  already on disk before file-write would never be able to prove REPEAT
  either, permanently defeating the fix at the only production call site
  currently wired to Layer 2 composition data. Its multi-instrument result
  selection was also changed from "first REFUSE, else first result" to
  "first REFUSE, else first NEIGHBOUR, else first result" — with three
  outcomes, the old priority could silently drop a NEIGHBOUR found on one
  instrument in favour of a NOVEL result on another, exactly the information
  design point 2 says must reach the result.

  **Both suites green:** `strategy-research`: **1072 passed** (1057 baseline
  + 15 new tests: 6 in `test_anti_adjacency_gate.py`, 9 in
  `test_build_exclusion_digest.py` — exact arithmetic match, no unexplained
  drop). `trading-bot`: **383 passed, 2 skipped** — byte-identical to the
  reference baseline (no files under `trading-bot/` were touched).

  Flag-off bit-identity for both existing call sites
  (`anti_adjacency_retry.enabled`, `variant_anti_adjacency_gate.enabled`)
  re-verified unchanged — neither flag-check function was touched, and their
  own byte-identical-output tests (`test_flag_off_*`) still pass.

---

## REJECTED (Jérémy, 2026-09-02) — the shipped design does not measure the right thing

While reviewing whether to switch the two gate flags on (E-041), Jérémy
rejected the design above outright — not "not done yet," but **not
convincing as a way to identify adjacency at all**, even though it is built,
tested, and measured working exactly as designed:

> *"The initial design of the solution is not convincing me and could explain
> the issue. Rejected on my side as we need to see how to identify
> 'adjacency' of two strategies with such strategy structure (regime with
> logic, sub-strategies allocated to regime, sub-strategies composed of
> weighted components)."*

**Why this is a different kind of problem than a bug.** The composition
fingerprint — `(regime, component_id, sorted(params), weight)` — treats a
strategy as a flat bag of parameterised parts. Jérémy's structure is not
flat: a regime carries its own **detection logic**, each regime is mapped to
its own **sub-strategy**, and each sub-strategy is itself a **weighted
composition** of components. The fingerprint has no representation for the
regime-detection logic at all, and no answer for how much a weight or a
parameter has to change before two compositions stop being "the same idea" —
it treats every difference as equally decisive, which is close to the exact
complaint that killed the original triple.

**Restart from the real question, not from the existing fingerprint.**
Whoever restarts this epic should treat S1 (design) as reopened, not as a
tuning pass on S2's fingerprint. The open question is not "which fields go in
the key" — it is **what makes two strategies the same idea, given that a
strategy is a regime-detector plus a per-regime mapping to weighted
sub-strategy compositions.** That may not have a single closed-form answer;
S1's job is to find out, not to assume the fingerprint shape and refine it.

**Status:** both gate flags (`anti_adjacency_retry`,
`variant_anti_adjacency_gate`) stay off. Not "waiting for a fix" — **the
built fix is rejected.** Treat as **incomplete, out of radar** until this
epic is deliberately restarted with a reconsidered design.
