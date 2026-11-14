# Exercise 2: reading

Prompt changes since exercise 1 (`system_prompt_used.md`):
- one direction per idea, never "either";
- a question brief gives one idea per answer that has a reason;
- mirror situations are two situations;
- what we would see, not how to check it;
- the "wrong if" hint removed.

Code change: the index line brackets only the market keys, not `source`.

Inputs: the five step 1 briefs (exercise 5), then 001 again. Each model on its own index. Cost: opus 0.332 USD, sonnet 0.156 USD.

## Counts

| Call | opus: ideas, attempts, cost | sonnet: ideas, attempts, cost |
|---|---|---|
| 001 RSI extremes | 4, 1, 0.030 | 4, 1, 0.015 |
| 002 MA cross | 6, 2, 0.079 | 6, 1, 0.014 |
| 003 volume | 6, 1, 0.037 | 6, 1, 0.016 |
| 004 BTC leads | 7, 2, 0.110 | **none saved**, 3, 0.054 |
| 005 RSI divergence | 6, 1, 0.046 | 6, 2, 0.036 |
| 001 again | **0**, all four named as already indexed, 0.029 | **4 new**, plus the four named as already indexed, 0.022 |

Every refusal (opus 2, sonnet 5) was a short-name of six words. Mirror splits make longer names ("up-cross-to-down-cross-gain").

## Against the criteria (my judgement, idea by idea)

| Criterion | opus (29) | sonnet (26) |
|---|---|---|
| One direction, no "either" | 29 | 24: `003-03`, `003-04` "holds the gain or keeps rising" |
| No test condition | 29; 004's "once accounted for" did not come through | 26 (004 not saved) |
| Says something happens | 29 | 26 |
| Faithful, no outside reason | 29 | 26 |
| Distinct | 29 | 22: `002-05`, `002-06` repeat `002-02`, `002-01` (after a downward cross, price falls); `001-05` to `001-08`, written on the repeat, restate 001-01 to 001-04 against neutral readings |
| Question answers covered | 001: reversal and continuation, both sides; 005: reversal and continuation, both sides | the same |
| Consequences covered | all | all except 004, lost |

**What the changes fixed**
- **"Either"**: from 2 opus ideas and 6 "differs" ideas in exercise 1 to none in opus.
- **Test conditions**: 004's old brief still says "once their own past returns are accounted for"; no idea from either model kept it. Step 2 now holds the rule on its own, whatever the brief says.
- **"Size differs" ideas**: gone.
- **Index**: opus wrote nothing on the repeat and named all four ideas. Sonnet named the four and still wrote four close variants. That is allowed by the rule ("a close idea is allowed"), but they are padding: the first call should have written them if they were worth writing.

**Borderline, for you to rule**
1. **"More often than after random points"** (002) and **"more than after neutral readings"** (001-03): a baseline inside the idea. I read it as the meaning of "persists" or "continues", not a test condition, but it is close.
2. **Opus `002-05`, `002-06`** ("from an up cross to the next down cross, price rises"): built on the brief's exit-like sentence. Stated as an observation, not a rule, and it is a different situation from `002-01` (a whole span, not the bars after the cross).
3. **Count**: opus 4 to 7 per brief, 29 in all. Mirror splits double most briefs. No padding by setting or outside reason.

## Models
- **Opus**: no fault in 29 ideas; correct on the repeat; 2 short-name refusals.
- **Sonnet**: 6 faults in 26 ideas (2 "either", 4 duplicates); padding on the repeat; one brief lost again on short-names, as in exercise 1.

## Changes the outputs ask for (not made, untested)
1. **Short-name check**: 7 of 7 refusals across both models, and 2 lost briefs over two exercises, are six-word names. Proposed: the prompt keeps "three to five words"; the code accepts up to eight, as a runaway guard only. This is the step 1 lesson (instruction in the prompt, code against runaway answers).
2. None to the prompt from opus's output.

## Recommendation
Opus. With change 1, run exercise 3 unchanged otherwise. If it is clean, the "two exercises in a row" rule is met by exercises 2 and 3 only if you accept that change 1 is a code change, not a prompt change.
