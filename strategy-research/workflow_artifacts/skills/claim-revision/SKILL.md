# claim-revision: re-emit the card's `claim` block, once (E-068)

You are reading this because `orchestrator.claim_tests` is on and code found a problem with
the tests of a card's `claim` block AFTER step 1b built the block (its kind is in
block_manifest.yaml). The request in your handoff (`claim_revision_request`) says what is
wrong. You get exactly one chance; nothing you write stops or changes the run, but a claim
whose tests cannot see the block teaches the campaign nothing.

You receive the card (hypothesis_card.yaml), the block manifest, and CLAIM_TESTS.md, the only
blocks a test may be composed from.

## Rules

- **Re-emit ONLY the `claim` block.** No other field of the card.
- **`statement` and `kind` are locked.** Leave them out (code keeps them exactly as they
  are) or copy them unchanged. A changed statement or kind refuses your whole answer.
- **At least one test must read the block's own output.** For a `forecast` block: a selector
  on `field: forecast`, or `statistic: rank_ic` (prefer these two: a forecast has no fixed
  scale, so a quantile or a rank IC is safer than a fixed forecast threshold). For a `regime`
  block: a `regime` or `regime_change` selector. A test that selects on price alone measures
  the same thing for every variant of the block.
- **Never approximate.** A test measures exactly the quantity the statement names, in its
  unit. Horizons are bars of the card's `timeframe` (on `1h` bars, 24 = one day). If no slot
  measures the stated quantity, write `tests: none` with `missing_block`, never a nearby
  quantity (a price level for a move, bars for days).
- Write `pass_if`, `fail_if` and `rationale` for the new tests. Do not write `alpha` or
  `significance`. Every other rule of CLAIM_TESTS.md applies (1 to 3 tests, unique names,
  a reachable floor). `floor_facts` in your handoff gives the bars in the test windows and
  the coins: a `min_events` floor must be at most (bars // the longest horizon) x coins.

## Output

Exactly ONE fenced YAML block with one top-level key, `claim`:

```yaml
# claim.yaml
claim:
  tests:
    - name: ...
  pass_if: "..."
  fail_if: "..."
  rationale: "..."
```

Code checks the block (CLAIM_TESTS.md's rules and the floor). If it passes, it replaces the
card's claim; if not, the original claim is kept. Either way the run continues.
