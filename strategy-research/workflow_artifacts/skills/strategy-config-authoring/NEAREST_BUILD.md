# NEAREST_BUILD.md: build the nearest version, do not park (E-068)

You are reading this note because `orchestrator.nearest_build.enabled` is on; it is added to
step 1b's inputs only under that flag. Where it differs from your skill's `component_gap` rules,
this note wins.

**Build the nearest version.** When a clause of the idea cannot be built exactly from the
catalogue's components and transforms, build the closest config they allow and answer
`status: spec_ready`. A run that tests a close approximation teaches the campaign something; a
parked run teaches nothing.
- A different yardstick for the same quantity is an approximation (O-21): for example the 1-bar
  move with `zscore` instead of ATR, or the previous close instead of the bar's open. On 24/7
  perpetuals the open is about the previous close.
- Keep the core of the claim: the direction and the quantity the idea is about.

**List every difference** in `decision.yaml`, one item per clause that is not built as written:
```yaml
deviations:
  - clause: <the card clause, verbatim or close>
    built_instead: <the config element that stands in for it, e.g. "PriceEvolutionComponent(period=1) + zscore">
    missing: <the piece that would make it exact, e.g. "the current bar's open, high and low"; null if nothing is missing>
    effect: <one line: how the approximation can change what the test measures>
```
- Keep the `DEVIATION:` entries in `backtest_spec.yaml` `config_rationale` too, as your skill asks.
- Code copies `missing` into `campaign_record/component_requests.yaml` (marked as a deviation; the
  run continues) and shows the deviations first in the run's finding and in the readers' inputs.

**Park only when the core is lost.** Answer `component_gap` only when nothing you can build keeps
the claim's core. Then `decision.yaml` must also carry:
```yaml
core_lost:
  clause: <the claim clause that cannot be approximated>
  why: <why no composition of components and transforms approximates it>
```
- What you tried stays in `tried`, as your skill asks.
- A `component_gap` without `core_lost` is sent back to you once.
