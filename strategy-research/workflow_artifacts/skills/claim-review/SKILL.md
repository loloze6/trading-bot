# claim-review: does each test measure what the claim says? (E-068)

You are reading this because `orchestrator.claim_test_review` is on. You review ONE card's
`claim` block. You do not judge whether the claim is true, you do not rewrite anything,
and you do not decide anything about the run: your answer is recorded as information.

You receive: the card's `hypothesis_id`, `timeframe` and `claim` (statement, kind, tests),
the block manifest step 1b wrote, and CLAIM_TESTS.md (what every slot of a test measures).

## The checklist, for every test

1. **The stated quantity.** Read the claim's `statement`. Name the quantity it conditions on
   (what makes a bar "selected") and the quantity it predicts, in its own words and unit.
   Examples of different quantities: a price LEVEL (where the close sits) is not a price
   MOVE (how much the close changed over the last n bars); a strategy's forecast value is
   not the move it was built from; a volatility is not a return.

2. **The measured quantity.** Read the test's slots exactly as CLAIM_TESTS.md defines them:
   - selector `field: close` reads the price level at bar t; `field: past_return` with
     `bars: n` reads the move close[t] / close[t-n] - 1; `field: forecast` reads the block's
     forecast at bar t; `quantile` compares that field with its own trailing `lookback` bars;
   - the outcome and its `horizons`, which are counted in BARS of the card's `timeframe`:
     a horizon of h bars on `1h` bars is h hours, on `1d` bars h days;
   - the baseline, the statistic and the direction.
   Write this as `quantity`: one sentence, with the horizons converted to time.

3. **`measures_statement`**: true only if the test selects bars by the quantity the statement
   conditions on (or by the block's forecast, when the block is built to measure exactly that
   quantity) AND its outcome is the quantity the statement predicts. A nearby quantity is
   false: a price level for a move, a move over another number of bars, a volatility for a
   return.

4. **`horizon_units_ok`**: convert every horizon to time (bars x timeframe). True only if the
   horizons reach the span the statement names ("within 6 hours", "over the next 3 days",
   "for two weeks"). If the statement names no span, true. Horizons that convert to another
   span than the one stated (bars counted in the wrong unit) is false.

5. **`direction_baseline_ok`**: true only if `direction` points the way the statement claims
   (higher returns: `greater`; lower: `less`) and the baseline is the comparison the statement
   makes ("than other bars": `complement`; no comparison stated: `placebo` or `rank_ic`).

6. **`issues`**: one short sentence per problem found in steps 3-5, naming the stated and the
   measured quantity (for example "selects on the forecast's sign, not on the volume spike the
   statement names"). An empty list when every check is true.

Whether a test reads the block's output at all is checked by code, not by you.

## Output

Exactly ONE fenced YAML block, with exactly one key `tests`, one entry per test of the claim,
keyed by the test's `name`, each with exactly these five keys:

```yaml
# claim_review.yaml
tests:
  <test name>:
    measures_statement: true
    quantity: "<what this test measures, horizons converted to time>"
    horizon_units_ok: true
    direction_baseline_ok: true
    issues: []
```

`measures_statement`, `horizon_units_ok` and `direction_baseline_ok` are true or false
(unquoted). Quote every string. No other keys, no other text outside the block. An answer in
another shape is recorded as a review error and not retried.
