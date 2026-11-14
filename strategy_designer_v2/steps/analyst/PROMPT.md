# Analyst step (branch 2)

You observe the book. You receive: the brief; the claim (its code and its pass number); `judge_verdict.yaml` (branch 1, if present); `engine_verdict.yaml` (branch 3); and `book_summary.yaml` (per window, strictly numeric: what the forecast, the trades and the equity did). Read the book, not only the claim's numbers. You answer two questions and nothing else.

## 1. What did the book do?
Eight to twelve observations, one sentence each, each tied to a number in `book_summary.yaml` (name the window and the field). Cover:
- where the money came from and went: which windows, long or short, which bars (best and worst bars, equity deciles);
- whether the forecast's size tracked the outcome (quantiles, share at the cap, sign agreement, correlation);
- whether the event bars behaved as the claim said (forward return by sign of the strength);
- where the drawdowns happened;
- what the trades cost (count, hold, average net, fees against gross).
Also say what the windows disagree about. No speculation without a number.

## 2. What one claim should run next?
Either one new claim in the exact nested format below (see `CLAIM_FORMAT.md`), or `next_claim: none` with one line why. Rules:
- It follows from your observations and is distinct from every claim already tried (not a threshold change of one).
- `strength` is dense and signed on every bar; `event` only marks where branch 1 measures it. `min_effect` is honest: a rank correlation you would not call luck.
- Only bars of the brief's symbol and bar size; code rules as in `CLAIM_FORMAT.md`; no lookahead.

## Output
A YAML file:
```yaml
run: <the try folder>
observations:
  - <sentence with its number>
next_claim:
  id: <short_snake_case>
  belief: <one sentence>
  claim:
    when: <plain words>
    then: <plain words>
    compared_to: <plain words>
    horizon_bars: <integer>
    min_effect: <number>
    code: |
      <pandas lines defining event and strength>
  why_no_lookahead: <one line>
  how_it_trades: <one line>
why: <one line: why this claim, or why none>
```
`next_claim` may instead be the word `none`.
