# E-036 — An adjacency key that reflects what a strategy actually is

**State:** planned (design below is complete; S2 is the build)
**Owner:** Jeremy
**Updated:** 2026-08-27

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
- [ ] S2 — Implement the fingerprint, the three-way outcome, and the fidelity
      rule. Regression tests must include the reproduced parameter-sweep case
      and a same-component-different-regime case.

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
