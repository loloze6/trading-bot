# Claim format (the ideas step's output, read by the judge as is)

```yaml
brief: <brief file name>
ideas:
  - id: <short_snake_case>
    belief: <one sentence: what is believed about the market>
    claim:
      when: <plain words: which bars>
      then: <plain words: what happens next>
      compared_to: <plain words: the baseline bars>
      measure: <one of: mean_diff | abs_ratio | rank_corr | hit_rate | net_return>
      horizon_bars: <integer: how many bars ahead the outcome is measured>
      direction: <positive | negative for mean_diff, rank_corr, hit_rate, net_return; above | below for abs_ratio>
      min_effect: <number: the threshold on the measure's value, e.g. 0.003 for 0.3% of return, 0.10 for a correlation, 1.20 for a ratio>
      code: |
        <pandas code that defines a, b and signal (or feature), see below>
    why_no_lookahead: <one line>
    how_it_trades: <one line>
notes: <optional>
```

## The code block
Python with pandas, a few lines. It runs with these names already defined:
- `df`: the bars, columns `open high low close volume`, index = bar close time (UTC, naive), one symbol, the brief's bar size.
- `ret`: close-to-close return of each bar (`df.close.pct_change()`).
- `hour`, `dow`: the bar's UTC hour (0-23) and weekday (0 = Monday).
- `spaced(cond, n)`: keeps a True of `cond` only if no True in the prior n bars (one event per n bars).
- `pd`, `np`.

It must define:
- `a`: boolean Series, the bars of the claim (the "when").
- `b`: boolean Series, the comparison bars. For "all other bars" write `b = ~a`. Not used by `rank_corr`.
- `signal`: Series of +1 or -1, the direction the claim predicts for the forward return at each bar (required by mean_diff, hit_rate, net_return; for a pure "it reverts" claim: `signal = -np.sign(ret)`).
- `feature`: numeric Series (required by rank_corr only).

Only data at or before the bar's close: rolling windows over past bars, `.shift(1)` for "the prior bars". Never `shift(-n)` in a selector; the judge refuses it.

## The five measures (what the judge computes from your code)
- `mean_diff`: mean of `signal * forward return` on `a` minus the same on `b`.
- `abs_ratio`: mean of `|forward return|` on `a` divided by the same on `b`.
- `rank_corr`: Spearman correlation between `feature` and the forward return, on `a`.
- `hit_rate`: share of `a` bars where `signal * forward return > 0`, minus the same on `b`.
- `net_return`: mean of `signal * forward return` on `a`, minus the round-trip cost.

Forward return = close `horizon_bars` later over close now, minus one.

## The common rule (the judge applies it to every claim; do not restate it)
- The claim passes if its measure meets `min_effect` in its `direction` on the whole fold, and the sign of the effect is the same in at least 5 of the fold's 6 windows, and `a` and `b` each hold at least 30 bars.
- Cost: 0.15% per round trip (the engine's Kraken cost). Use it when you think about `min_effect` for `net_return`.
- One symbol at a time: a claim is measured on each symbol the brief names and passes only if it passes on each. Claims that need two symbols in one formula are not computable in this version; do not write them.
