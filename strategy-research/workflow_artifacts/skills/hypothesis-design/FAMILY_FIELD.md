# hypothesis_card.yaml — the `family` field (E-046a Slice 5b-ii-B1)

This file is part of the hypothesis-design skill. It is placed in your context only when
`orchestrator.family_at_creation.enabled` is on; when you can read it, everything below
is REQUIRED. (It lives outside `SKILL.md` so that flag-off runs receive a byte-identical
prompt.)

## What to write

Add one top-level field to `hypothesis_card.yaml`:

```yaml
family: funding_rate_mean_reversion
```

- **Format:** lowercase snake_case — words of `a-z`/`0-9` (first character a letter)
  joined by single underscores, at most 48 characters. No spaces, hyphens, capitals,
  quotes-inside, or trailing underscore. A value that breaks this fails the stage; it is
  never auto-corrected.
- **Meaning:** a short name for the *mechanism* — the signal family implied by
  `edge_source.specific_mechanism` / `signal_concept`. Not a parameter value, threshold,
  instrument, timeframe, run id, or hypothesis id. Two cards testing the same mechanism
  with different parameters share one family. Good: `volatility_breakout`,
  `fear_greed_contrarian`, `funding_rate_mean_reversion`. Bad: `keltner_2p5_atr_btc_1h`
  (parameters/instrument/timeframe), `new_idea` (says nothing), `Keltner-Breakout`
  (format).

## Set once — why this matters

The family is the idea's permanent identity. The campaign's circuit breaker counts
refinements and failures per family by **exact string**: a re-worded label for the same
mechanism (`keltner_breakout` one run, `keltner_threshold_regime` the next) silently
defeats it. When your context shows families already used in this campaign (e.g. the
exclusion digest or knowledge base, when present) and your mechanism is one of them,
reuse that exact string rather than coining a synonym.

## Refine children

If the handoff's `injected_context` carries `inherited_hypothesis_family`, this run
refines an earlier idea: write exactly that value as `family`. The orchestrator
overwrites the field with the inherited value after you finish in any case — a refine
never re-derives its family.
