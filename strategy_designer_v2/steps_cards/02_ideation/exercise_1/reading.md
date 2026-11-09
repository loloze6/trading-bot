# Exercise 1: reading

`../helper/make_ideas.py` with the prompt in `system_prompt_used.md` (the card's draft 2). Opus and sonnet, the five step 1 briefs in order, each model on its own index starting empty. Outputs: `opus/ideas/`, `sonnet/ideas/`, `side_by_side.md`. Logs: `*/run_log.txt`. Costs: `costs.json`.

## Counts

| Brief | opus: ideas, attempts, cost | sonnet: ideas, attempts, cost |
|---|---|---|
| 001 RSI extremes | 3, 1, 0.034 | 3, 1, 0.018 |
| 002 MA cross | 7, 1, 0.040 | **none saved**, 3, 0.042 |
| 003 volume | 5, 1, 0.043 | 4, 2, 0.024 |
| 004 BTC leads | 5, 1, 0.036 | 6, 3, 0.047 |
| 005 RSI divergence | 4, 1, 0.043 | 5, 1, 0.017 |
| Total | 24 ideas, 5 calls, 0.196 USD | 18 ideas, 10 calls, 0.148 USD |

Sonnet's six refusals were all one fault: a short-name of six words, repeated after the refusal named it.

## Against the criteria (my judgement, idea by idea)

| Criterion | opus (24) | sonnet (18) |
|---|---|---|
| Says something happens | 24 | 18 |
| Faithful to the brief | 24 | 17: `005-05` repeated divergences, not in the brief |
| Leaves open only what the brief leaves open | 22: `002-05`, `002-06` add "or reverse" to a claim brief | 18 |
| No test condition from "wrong if" | 23: `004-01` "beyond what their own earlier returns would predict" | 17: `004-01` "even after accounting for those coins' own past returns" |
| No setting, rule, result, price | 24 | 18 |
| Consequences covered | all, on all five briefs | all, on four briefs; 002 lost |

**What held**
- The header copy works: `instruments` and `source` copied, empty headers left empty, `brief:` on every file.
- No idea claims an absence. Both models turned 004's "small coins lead bitcoin as often" into a comparison on their own (`004-04`).
- Two situations gave two ideas (003 thin and heavy volume). Questions stayed open (001, 005).
- No idea names a setting value.

**What did not**
- The test condition in 004's "wrong if" survived in both models, despite the new prompt line.
- The index was not exercised: no brief produced an idea already written, so `already-indexed` was "none" eleven times. 005 gave different ideas from 001, which is correct; the test simply had no repeat in it.

**Borderline, for you to rule**
1. **Mirror situations.** Both models split every symmetric claim: high and low RSI extremes (001), up and down crosses (002), bearish and bullish divergences (005). By our rule (two situations, either can hold without the other) this is right, and in crypto the two sides often behave differently. It also doubles the count: opus's 002 has 7 ideas, 4 of them two mirror pairs.
2. **"Size" ideas.** Both models add "the move after X differs in size" to 001 and 005. 001's brief mentions size; 005's does not, clearly. A size idea leaves both directions open, so a trader acts on it weakly.
3. **Opus `002-07`** ("from one cross to the opposite cross, price moves the first cross's way") comes from the exit-like sentence in brief 002. It is stated as an observation, not a rule.
4. **Opus `003-03`** (thin against heavy, at equal size) is the comparison of `003-01` and `003-02`. It is the brief's own "wrong if", so another way to see the same consequence, not padding.

**Other observations**
- Index lines with a `source` header carry the whole source reference in brackets: long and noisy (opus 002).
- Sonnet's 001 index lines do not name RSI ("a high extreme reading"); read alone, they are unclear.

## Models
- **Opus**: 5 of 5 first answers passed the shape check. 3 faults in 24 ideas. Writes more ideas per brief.
- **Sonnet**: 2 of 5 first answers passed; one brief lost. 2 faults in 18 ideas, but one is an idea outside the brief, which is the worse kind. Cheaper per call; the retries ate the saving.

## Prompt changes the outputs ask for (not made, untested)
1. Test conditions: name the phrases to drop, with an example: "'once X is accounted for', 'for all three coins' are ways to check, not things we would see".
2. Claim briefs: "If the brief is a claim, the idea states the direction the claim gives."
3. Mirror situations: one line, once you rule on point 1 above.
4. Index line: bracket only the keys that limit the market (instruments, venue, bar, period, side), not `source`. This is a code change.

## Recommendation
Opus. Rule on the mirror and size questions, then exercise 2 with the four changes, and add one brief run twice, so the index is tested on a real repeat.
