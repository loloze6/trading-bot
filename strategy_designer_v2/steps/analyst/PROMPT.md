# Analyst step (branch 2)

You read one finished run: the brief, its claims, the judge's verdicts with the numbers per window, and the profit answer for any validated claim. You answer two questions and nothing else.

## 1. What did we see?
Five to ten observations, each one sentence, each tied to a number in the files. Say what held, what did not, what nearly held (the belief looked right but the number asked was wrong), and what the windows disagree about. No speculation without a number.

## 2. What one claim should run next?
Either one new claim in the exact format of `CLAIM_FORMAT.md` (measure, horizon_bars, direction, min_effect, code), or `next_claim: none` with one line why. Rules:
- It must be distinct from every claim already tried on this brief (not a threshold or window change of one of them), and it must follow from your observations.
- Its `min_effect` is chosen now, informed by what the numbers showed, and honest: an effect you would not call luck, and one that pays the 0.15% round-trip cost if the claim is about profit.
- Only bars of the brief's symbol and bar size. Same code rules as the ideas step.

## Output
A YAML file:
```yaml
run: <the try folder>
observations:
  - <sentence with its number>
next_claim: <one idea in CLAIM_FORMAT, or none>
why: <one line: why this claim, or why none>
```
