# Claim format (the ideas step's output)

```yaml
brief: <brief file name>
ideas:
  - id: <short_snake_case>
    belief: <one sentence: what is believed about the market>
    claim:
      when: <plain words: which bars>
      then: <plain words: what happens next>
      compared_to: <plain words: the baseline bars>
      horizon_bars: <integer: how many bars ahead the outcome is measured>
      min_effect: <number: floor on the rank correlation, e.g. 0.03>
      code: |
        <pandas code that defines event and strength, see below>
    why_no_lookahead: <one line>
    how_it_trades: <one line>
notes: <optional>
```

## Dense strength (the consequence of linear forecasts, found in try 09)
The engine grades `strength` against its own recent magnitude on every bar. Two shapes fail: a strength that is 0 on most bars saturates at the cap on its few events (an on-off book by another route), and a strength that is raw noise on every bar (a bar's return, for instance) churns and loses. A good strength is dense and meaningful on every bar: a stretch from an anchor in volatility units, a trend slope, a volume ratio times the sign of the move, a distance beyond a range that is 0 inside and grows outside. Think of it as the component's indicator, not as a trigger. `event` is where branch 1 measures it, nothing more.

## The code block
Python with pandas, a few lines. Names already defined:
- `df`: the bars, columns `open high low close volume`, index = bar close time (UTC, naive), one symbol.
- `ret`: close-to-close return of each bar. `hour`, `dow`: UTC hour (0-23) and weekday (0 = Monday).
- `spaced(cond, n)`: keeps a True of `cond` only if no True in the prior n bars.
- `pd`, `np`.

It must define two Series:
- `event`: boolean, the bars where the belief applies. May be True everywhere for a continuous belief.
- `strength`: numeric, signed, continuous. Positive predicts up, negative down; the magnitude is the belief's own size (a stretch in units of recent volatility, a volume ratio times the sign of the move, a trend slope). No direction field, no plus or minus one.

Only data at or before the bar's close: rolling windows over past bars, `.shift(1)` for "the prior bars". Never `shift(-n)`; the code is refused.

`strength` is a continuous series on every bar and the engine trades it graded; `event` only marks where branch 1 measures the claim. Define `strength` wherever possible (no all-NaN outside events); if the belief exists only at events, strength outside events is 0, which is allowed but makes a sparse book.

## The one measure
The rank correlation between the engine's forecast (the strength on every bar, graded by the engine) and the forward return over `horizon_bars`, on event bars. It must be at least `min_effect`.

## The common rule (applied to every claim; do not restate it)
- The correlation has the same sign in at least 5 of the fold's 6 windows, with at least 30 event bars per window group.
- Cost: 0.15% per round trip.
- One symbol at a time; no formula that needs two symbols.

## Example
```yaml
code: |
  sd = ret.rolling(168, min_periods=168).std().shift(1)
  event = spaced(ret.abs() >= 3 * sd, 12)
  strength = ret / sd
```
A continuous belief: `event = pd.Series(True, index=df.index)`; `strength = df.close.pct_change(24) / ret.rolling(168).std().shift(1)`.
