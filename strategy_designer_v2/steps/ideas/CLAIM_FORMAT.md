# Claim format (the ideas step's output)

```yaml
brief: <brief file name>
ideas:
  - id: <short_snake_case>
    belief: <one sentence: what is believed about the market>
    claim:
      when: <the selector: which bars, as a computable condition at the bar's close>
      then: <what happens next, with the horizon, e.g. "the next 24h close-to-close return">
      compared_to: <the baseline bars>
      measure: <how it is measured, e.g. "mean difference of forward returns", "hit rate", "rank correlation", "net return after fees">
      pass_if: <numeric condition, e.g. "difference > 0.15% per 24h, same sign in at least 4 of 5 windows">
    why_no_lookahead: <one line>
    how_it_trades: <one line: how this becomes a long/short/flat decision>
notes: <optional: what the brief implies, what was struck and why>
```

Rules of the format:
- Every field present, every value a plain sentence or number. No prose outside this structure.
- `when`, `then`, `measure` must be computable from bars alone unless the brief names more data.
- `pass_if` is the judge. It names a number and a consistency rule across windows.
