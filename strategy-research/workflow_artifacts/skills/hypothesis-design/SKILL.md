---
name: hypothesis-design
description: Produces a clear, testable trading strategy hypothesis from a research brief, including thesis, rationale, edge_source declaration, signal concept, assumptions, and expected failure modes.
---

# Hypothesis Design

## Mission
Create one explicit, testable strategy hypothesis with an honest structural reason it should have edge.

## Required input
- `research_brief.yaml`
- `config/available_feeds.yaml`  (A1.2: read before populating evidence_type)
- `feed_wishlist.yaml`           (A1.2: append new feed requests here if needed)

## Required output
- `hypothesis_card.yaml`

## Output requirements
The artifact must include, IN THIS ORDER:
1. hypothesis_id
2. thesis
3. rationale
4. **edge_source** (MUST be fully populated before signal_concept; see IMPROVEMENT 01 section)
5. signal_concept
6. target_market
7. timeframe
8. assumptions
9. expected_failure_modes

---

## IMPROVEMENT 01 — Edge-Source Declaration (A1.1–A1.3)

### Hard constraint: populate `edge_source` BEFORE writing `signal_concept`

If `edge_source` is not fully populated, stop. Do not proceed to `signal_concept`.
A hypothesis without a declared mechanism is a price permutation, not a hypothesis.

### `edge_source` block

```yaml
edge_source:
  category: <one of five values below>
  specific_mechanism: <1-2 sentences — see A1.3>
  why_not_arbitraged: <see per-category bar below>
  evidence_type: <must be in config/available_feeds.yaml>
  measurable_proxy: <A1.3: the observable that distinguishes mechanism-present vs mechanism-absent>
  requires_new_feed: <present only if evidence_type is NOT in available_feeds.yaml>
```

### Category definitions (A1.1)

- **information_asymmetry** — someone knows something before price reflects it; the signal proxies for that knowledge. Bar for `why_not_arbitraged`: must identify a specific speed/capacity/access constraint.

- **structural_forced_flow** — flows that happen for mechanical/contractual reasons, not opinion: funding rate settlement, liquidation cascades, options gamma hedging, index rebalancing. The forcing mechanism must be nameable and verifiable in an available feed.

- **liquidity_provision** — edge from being paid to provide immediacy (spread capture). Not applicable to directional strategies.

- **cross_venue_dislocation** — temporary price divergence between related instruments or venues. Requires cross-exchange or perp/spot data — NOT currently available. Use `requires_new_feed: cross_exchange_data`.

- **persistent_behavioral_bias** — systematic over/under-reaction, herding, anchoring, or disposition effects that recur because they arise from human/algorithmic behavior patterns, not from exploitable-once information. Bar for `why_not_arbitraged`: must argue why the bias persists despite being publicly known (e.g., capacity limits on the arbitrage trade, recurrence from structural incentives, crowding cycles).

### A1.3 — Anti-confabulation check on `specific_mechanism`

`specific_mechanism` must satisfy ALL of the following:
1. It names a **causal chain** (X happens → Y follows because Z).
2. It names at least one **measurable proxy** from an available feed that would look **different** if the mechanism is real vs. absent.
3. The proxy is computable from `config/available_feeds.yaml` entries. If it is not, the mechanism is a story, not a hypothesis — fall back to `persistent_behavioral_bias` (whose bar is behavioral recurrence without requiring a non-price proxy) or add the hypothesis to `feed_wishlist.yaml` with `requires_new_feed`.

**Examples that PASS (checkable mechanisms):**

```
# PASS — structural_forced_flow with funding feed
specific_mechanism: "When 8h funding rate exceeds ±0.10%, longs/shorts pay heavily to
  maintain positions; forced deleveraging creates mean-reversion pressure that is
  measurable in the funding feed as a spike-then-decay pattern."
evidence_type: funding_open_interest
measurable_proxy: "8h funding_rate (absolute value > threshold); mechanism predicts
  negative correlation between extreme funding and subsequent 4-12h returns."

# PASS — persistent_behavioral_bias with OHLCV only
specific_mechanism: "Strong directional candles on above-average volume signal broad
  consensus; observers who missed the move chase price over the next 1-3 bars,
  creating short-lived momentum detectable in OHLCV."
evidence_type: price_volume_only
measurable_proxy: "volume_ratio (current vol / 20-bar MA) and candle body fraction
  (body / range); mechanism predicts continuation on high-ratio directional bars."
why_not_arbitraged: "Effect is capacity-limited at the 1h timeframe — institutional
  arb reversion takes longer than 3 bars at retail sizes."
```

**Examples that FAIL (sent to feed_wishlist or rejected):**

```
# FAIL — untestable proxy
specific_mechanism: "Institutions rebalance monthly, creating end-of-month flows."
→ No institutional flow data in available feeds.
→ Either rephrase to use a price/volume proxy (e.g., "month-end price levels 
  tend to show reversal") OR log to feed_wishlist as requires_new_feed: institutional_flows.

# FAIL — vague, no proxy
specific_mechanism: "Smart money accumulates at key price levels."
→ "Smart money" and "key levels" are not defined observables.
→ Reject; rewrite with explicit price levels (recent highs/lows, round numbers)
  as the measurable proxy.

# FAIL — requires unavailable data
specific_mechanism: "Order-book imbalance predicts short-term direction."
evidence_type: order_book
→ order_book is not in available_feeds.yaml.
→ Add requires_new_feed: order_book; route to feed_wishlist. Do NOT enter queue.
```

### A1.3 Spirit check — two caught confabulations from the campaign's first generation trial

These examples passed schema validation but failed the spirit check. Both are documented here to train against the pattern.

**Caught confabulation 1 — Mechanism-impure proxy (volume impulse, H-041-B)**

A hypothesis claiming `persistent_behavioral_bias` (herding/FOMO) with proxy `volume_ratio × body_fraction` is schema-compliant but mechanism-impure:
- High-volume directional bars are produced by *two competing mechanisms*: (a) FOMO herding → predicts continuation, (b) liquidation cascades → predicts mean-reversion.
- The proxy cannot distinguish (a) from (b) without `liquidation_data` (unavailable).
- Result: the correlation sign tells you which mechanism dominated on average but the `specific_mechanism` claim ("herding") is not what the proxy measures.

**Rule added:** A proxy that equally activates on a competing mechanism with the opposite directional prediction fails A1.3 spirit, even if the proxy is computable. Options: (i) rephrase as a net-effect hypothesis with explicit ambiguity, (ii) route to feed_wishlist pending `liquidation_data`.

Feed wishlist entry generated: "liquidation_data needed to make volume-impulse hypotheses mechanism-pure."

**Caught confabulation 2 — Daily feed forward-filled to 1h without signal timing constraint (fear_and_greed, naive H-041-C)**

A hypothesis using Fear & Greed (daily feed, forward-filled to 1h) that does not specify *when* the signal fires is mechanism-ambiguous at IC computation time:
- All 24 consecutive 1h bars in a calendar day share identical forecast values.
- Spearman IC computed over all bars is dominated by 24-bar autocorrelation artifact — it measures the feature's within-day persistence, not the mechanism's daily predictive content.
- Schema-compliant (fear_and_greed is an available feed, proxy is computable). Fails spirit: the IC test does not test the mechanism.

**Fix:** Any hypothesis using a daily feed (fear_and_greed, or future daily feeds) must specify in `signal_concept` exactly when the signal fires: "signal fires ONLY at the first 1h bar of each calendar day; all subsequent bars in the same day hold position but do not re-evaluate entry." This converts the hypothesis to a sparse-signal (A8.3) test with active-bar IC on the meaningful n.

### A1.2 — Evidence type constraint

**Schema enforcement gap (A1.4 finding):** JSON Schema validation will NOT reject `evidence_type: order_book` (or any other unavailable feed) if `requires_new_feed` is absent. The schema allows all `evidence_type` enum values because it cannot cross-reference `available_feeds.yaml`. The A1.2 rule is therefore a **skill-level hard rule only** — schema validation passing does NOT mean this rule is satisfied. You must check `available_feeds.yaml` explicitly.

Read `config/available_feeds.yaml` BEFORE populating `evidence_type`.

| If evidence_type is in `available_feeds.yaml.available` | proceed normally |
| If evidence_type is in `available_feeds.yaml.unavailable` | set `requires_new_feed: <feed_name>` and append to `feed_wishlist.yaml`; do NOT enter run queue |

The innovation-expansion rule "at least one non-price_volume_only variant per family" is satisfiable TODAY via `funding_open_interest` (the funding rate feed exists). Do not reach for order_book or cross_exchange data that cannot be tested.

---

## POST-A2.3 — No regime-gating (standing policy)

**No hypothesis produced by this skill may be regime-gated.**

The regime detector for BTC/ETH 1h is `unusable_for_this_symbol_timeframe` per A2.3. Any hypothesis whose mechanism inherently requires regime conditioning ("only works in trends", "valid in RANGING mode") is currently untestable and must be routed to `config/detector_wishlist.yaml` instead of the run queue.

**Rule:** If you find yourself writing `target_market` or `signal_concept` with a regime condition ("when TRENDING", "in ranging markets"), stop. Either:
1. Reformulate as an ungated signal (e.g., "high-velocity directional bars" instead of "TRENDING regime"), or
2. Acknowledge the hypothesis belongs to the detector wishlist and produce a feed_wishlist entry instead.

Ungated formulations only enter the queue.

---

## Success-condition framing

**Quality over volume is the explicit goal.**

Under a "produce hypotheses" instruction, the default LLM behavior is to generate many plausible stories. That is wrong here. The acceptance standard is:

> A small number of honest, edge-source-declared hypotheses that pass the A1.3 anti-confabulation check — plus a well-argued `feed_wishlist.yaml` if untestable ideas arose — is a better outcome than a wide queue of price-permutation hypotheses.

It is acceptable to produce ONE hypothesis if one is all that can be honestly justified. An empty queue with two feed_wishlist entries is a valid and useful output. It is not acceptable to fill the queue with hypotheses that fail the A1.3 check.

---

---

## IMPROVEMENT 04 — Indicator Library Lookup (A4)

**Before finalizing `signal_concept`, look up the proposed indicator in `config/indicator_library.yaml`.**

### Lookup protocol (4 steps, required in order):

**Step 1 — Regime affinity check**
Find the indicator's entry in the library (`id` or nearest `category`). Read `known_regime_affinity`.
- If this hypothesis has a stated or implied target regime and the affinity is `unfavorable`:
  - Either: justify explicitly why this run expects an exception (new mechanism, different symbol, materially different edge_source than prior trials).
  - Or: choose a different indicator with `favorable` or `neutral` affinity for the intended regime.
- If the hypothesis is ungated (no regime condition, as required by A2.3), note the affinity as a prior risk factor in `expected_failure_modes`.

**Step 2 — Campaign empirical results check**
Read `campaign_empirical_results` for this indicator category and symbol/timeframe.
- If an entry exists with `outcome: failed` for the same `symbol_timeframe` and similar regime conditions:
  - Must not re-propose the same indicator + mechanism combination.
  - A re-proposal requires a materially different `edge_source.specific_mechanism` — not a parameter change.
  - Cite the `run_id` of the prior failure and state the mechanism difference explicitly.

**Step 3 — Crowding check**
Read `crowding_risk` for the indicator class.
- If `crowding_risk: high` AND `data_requirements: ohlcv_only`:
  - Check whether a compatible indicator with `data_requirements != ohlcv_only` exists in the library with matching `edge_source_compatibility`.
  - If such an alternative exists and is available in `config/available_feeds.yaml`: prefer it, or explicitly justify why the high-crowding OHLCV indicator is preferred despite the crowding risk.

**Step 4 — Mechanism purity check**
Read the `notes` field for any MECHANISM PURITY WARNING.
- If a warning is present (e.g., volume_ratio / body_fraction), the indicator may not be used for a directional hypothesis without the required additional feed.
- Route to `feed_wishlist.yaml` with the mechanism purity note.

### Indicator lookup result in hypothesis_card.yaml

Add a `library_lookup` field to document the result of steps 1–4:

```yaml
library_lookup:
  indicator_id: "<id from indicator_library.yaml>"
  regime_affinity_for_target: "<favorable|unfavorable|neutral>"
  affinity_justification: "<required if unfavorable; else 'n/a'>"
  prior_campaign_failures: []  # or [{run_id, mechanism_tried}]
  crowding_risk: "<low|medium|high>"
  crowding_deviation_justification: "<required if high and no less-crowded alternative used>"
```

---

## IMPROVEMENT 05 — Exclusion-Digest Awareness: Redirect, Don't Repeat (E-032 S2b)

### Optional, off by default

`campaign_record/exclusion_digest.yaml` is unioned into your context files ONLY when
`config/campaign_config.yaml`'s `orchestrator.exclusion_digest_input.enabled` is true.
It will not always be present. **If it is absent from your provided context, this
section does not apply — proceed as before.** Absence of the digest is not evidence
of a fresh search space; it may simply mean the flag is off.

### When it IS present: read it before you commit to a family

The digest is family-scoped, not indicator-scoped (IMPROVEMENT 04's
`campaign_empirical_results` check is per-indicator; this is campaign-wide, across
every run, keyed at `(family, instrument, timeframe)` — the grain that actually
distinguishes a fresh cell from a retested one). Its `families` map lists, per family,
the `(instrument, timeframe)` triples already run and their `run_ids`. Its
`failed_families_passthrough` lists families with either a recorded `root_cause`
(`detail: dict_entry`) or, more weakly, a bare name with no diagnosis
(`detail: bare_string_low_detail`).

**Before finalizing `edge_source` and `signal_concept`:**
1. Classify your candidate's family the same way IMPROVEMENT 04's lookup does
   (structural indicator id first, then mechanism keyword).
2. If the digest's `families` entry for that family already has a triple at the SAME
   `(instrument, timeframe)` you intend to target — **do not propose it as-is.** Target
   a different, untried `(instrument, timeframe)` under that family, or move to a
   different family/category entirely.
3. If `failed_families_passthrough` names your family with a `root_cause`
   (`dict_entry`): your redirect must address that root cause structurally — a
   different `edge_source.category`, a different `evidence_type`, or a materially
   different `specific_mechanism` — never a parameter change alone. A
   `bare_string_low_detail` entry is weaker evidence; note it, but it does not by
   itself forbid a well-argued re-attempt.
4. **You are empowered, not just permitted, to declare a family exhausted.** If every
   angle you can honestly construct on a family collides with step 2 or 3, say so
   directly in `rationale` (name the family, the colliding triples, the root_cause) and
   select a genuinely different family — not the next parameter over. Record the
   redirect in `library_lookup.prior_campaign_failures` (cite the colliding `run_ids`
   from the digest) so the decision is auditable, not just asserted.

**This is raw material, not the gate.** The mechanical refusal is
`tools/anti_adjacency_gate.py`, downstream and deterministic. Nothing here overrides
it, and a hypothesis that ignores this section is not thereby invalid — it is simply
more likely to be refused later, more slowly, after you have already written it.

---

## A8.6 — Power pre-registration: `plausible_ic_upper` anchor table

**Do not free-hand `plausible_ic_upper` in `power_parameters`.** Pick it from this table by
signal class first; deviate only with an explicit, cited reason.

Motivating evidence (2026-07-04, P1a shakedown): the IDENTICAL indicator
(`moving_average_crossover`, same asset/timeframe, same crowding_risk=high entry in
`config/indicator_library.yaml`) was independently pre-registered at `plausible_ic_upper`
= 0.05, 0.08, and 0.15 across three separate authoring passes — a 3× spread with zero new
evidence between them, purely from unconstrained judgment. `min_detectable_ic` (the
deterministic half of the A8.6 check) converged tightly across all three (~0.026–0.027);
`plausible_ic_upper` was the only free variable, and it is the ONLY input to the power
verdict that isn't computed from the config. This table exists to anchor it.

| Signal class | Description | `plausible_ic_upper` | Basis |
|---|---|---|---|
| Dense OHLCV, high crowding | Continuous/near-every-bar activation, price-only, textbook-taught (MA crossover, RSI, MACD, Bollinger, Keltner) | **0.03–0.05** | This campaign's own empirical ceiling: Keltner `ic_active_bars=-0.032`, RSI `corr=-0.022` — established technical signals on liquid BTC/ETH 1h top out here or below. `indicator_library.yaml`'s `crowding_risk: high` entries. |
| Dense OHLCV, lower crowding | Continuous activation, price/volume-only, but not universally taught (volatility filters, volume-flow subject to A1.3 purity caveats) | **0.05–0.08** | Less mechanically arbitraged than MA/RSI-class signals, but still no non-price informational edge. |
| Sparse feed-based, extreme/threshold-gated | Rare, event-driven activation on a non-OHLCV feed (funding rate extremes, F&G contrarian at 25/75) | **0.10–0.20** | `indicator_library.yaml` literature notes: `funding_rate_extreme` "0.05-0.2", `fear_greed_index_contrarian` "0.05-0.15". Lower crowding (non-standard feed) justifies a higher ceiling than dense OHLCV. |
| Sparse feed-based, continuous/non-extreme | Fires on EVERY occurrence of a structural event, not just tail cases (e.g. funding-rate sign at every 8h settlement, not only \|rate\|>threshold) | **0.08–0.12** | Same feed/mechanism family as the row above, but the per-event effect is diluted (mild + extreme events pooled together) — anchor below the extreme-only case, not at it. |
| Cross-sectional | Rank/relative-value signal across the symbol universe (not yet run in this campaign) | **0.10–0.15** | Typical literature range for cross-sectional equity/crypto factors. Aspirational anchor — no in-campaign empirical result yet; revise this row once one exists. |

If a hypothesis doesn't cleanly fit one row, pick the nearest by (a) OHLCV-only vs.
external feed, (b) activation density, (c) crowding — in that priority order — and state
which axis drove the choice in `power_parameters.power_note`. A number outside every
row's range requires a one-sentence justification citing a specific prior result or
literature figure, not "seems reasonable."

---

## Checklist
- Read `config/available_feeds.yaml` before touching `evidence_type`.
- Read `config/indicator_library.yaml` before finalizing `signal_concept`. (Improvement 04)
- Set `power_parameters.plausible_ic_upper` from the A8.6 anchor table above by signal
  class — do not free-hand it.
- Populate `edge_source` fully before writing `signal_concept`.
- Check: does `specific_mechanism` name a measurable proxy in an available feed? If not, revise or route to `feed_wishlist.yaml`.
- Check: is `evidence_type` available? If not, add `requires_new_feed` and route to feed_wishlist.
- Check: is the hypothesis ungated? Any regime condition → reformulate or route to detector_wishlist.
- Check: indicator library lookup steps 1–4 complete; `library_lookup` field populated in card.
- If `campaign_record/exclusion_digest.yaml` is present in context: check your
  candidate's family against it before finalizing `edge_source`. Prefer a
  family/instrument/timeframe combination absent from `families`, or address a named
  `root_cause` structurally. (Improvement 05)
- State the idea in a way that can be tested without unavailable data.
- Include at least 3 failure modes.
- Prefer hypotheses that can be integrated as a minimal change in the current strategy architecture.

## Forbidden
- Do not write `signal_concept` before `edge_source` is complete.
- Do not write `signal_concept` before indicator library lookup is complete. (Improvement 04)
- Do not use vague mechanistic claims ("smart money", "key levels", "institutions") without a named measurable proxy.
- Do not propose a hypothesis with `evidence_type` outside `available_feeds.yaml.available` as a run-queue candidate — route it to feed_wishlist instead.
- Do not produce regime-gated hypotheses for the run queue (post-A2.3).
- Do not write code.
- Do not propose more than 3 run-queue variants unless explicitly requested.
- Do not assume unavailable data.
- Do not propose ideas that require replacing the whole existing bot architecture.
- Do not re-propose an indicator + mechanism combination already marked `outcome: failed` in the library's `campaign_empirical_results` for the same symbol/timeframe without a materially new mechanism. (Improvement 04)
- Do not repropose a family+instrument+timeframe triple already present in the
  exclusion digest under a materially unchanged mechanism, when the digest is present
  in context. (Improvement 05)
- Do not treat digest absence as evidence of a fresh search space — it may simply mean
  `orchestrator.exclusion_digest_input.enabled` is off. (Improvement 05)

## Context rule
Read `research_brief.yaml`, `config/available_feeds.yaml`, `feed_wishlist.yaml`, `config/indicator_library.yaml`, and, when present, `campaign_record/exclusion_digest.yaml` and `campaign_record/campaign_knowledge_base.yaml`. Do not read other files unless the handoff explicitly requires them.
