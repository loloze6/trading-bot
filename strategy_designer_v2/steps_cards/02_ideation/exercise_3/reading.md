# Exercise 3: reading

The prompt is the same as in exercise 2. One code change: code refuses only a major deviation (a block without its idea or consequence, a field over 300 words). It fixes minor ones: the short-name is made file-safe, at most eight words; markup is stripped.

Same inputs and order as exercise 2. Cost: opus 0.211 USD, sonnet 0.101 USD.

## Counts

| Call | opus: ideas, attempts, cost | sonnet: ideas, attempts, cost |
|---|---|---|
| 001 RSI extremes | 4, 1, 0.018 | 5, 1, 0.011 |
| 002 MA cross | 6, 1, 0.033 | 7, 1, 0.015 |
| 003 volume | 6, 1, 0.035 | 5, 1, 0.015 |
| 004 BTC leads | 7, 1, 0.047 | 7, 1, 0.020 |
| 005 RSI divergence | 6, 1, 0.047 | 7, 1, 0.020 |
| 001 again | **0**, all four named as already indexed, 0.031 | **5 new**, plus all five named as already indexed, 0.021 |

No refusal in twelve calls (exercise 2: 7 refusals and one lost brief, all for six-word names). No brief lost.

## Against the criteria (my judgement, idea by idea)

| Criterion | opus (29) | sonnet (36) |
|---|---|---|
| One direction, no "either" | 29 | 35: `001-05` "in whichever direction they go" |
| No test condition | 29 | 35: `004-03` "beyond what the altcoin's own past returns would suggest" |
| Says something happens | 29 | 36 |
| Faithful, no outside reason | 29 | 36 |
| Distinct, index respected | 29 | 29: `002-05`, `002-06` repeat `002-02`, `002-01` (as in exercise 2); `001-06` to `001-10`, written on the repeat, restate `001-01` to `001-05` |
| Answers and consequences covered | all | all |

**Opus is stable.** Its 29 ideas match exercise 2's almost one for one: the same splits, the same consequences, the same counts per brief. It wrote nothing on the repeat and named every idea already written.

**Sonnet repeats its faults.** It writes duplicates on the repeat while naming the originals as already written (exercise 2: 4, here 5). It turns the exit-like sentence into duplicate ideas (both exercises). One test condition came back.

**Still borderline, for you to rule** (the same two as in exercise 2):
1. **A baseline in the idea.** "More often and further than after random points" (002) and "more than after neutral readings" (001-03, 001-04). I read it as what "persists" means, not a test condition.
2. **The span idea.** Opus `002-05`, `002-06`: from one cross to the opposite cross, price moves the way of the first. It is stated as an observation and comes from the brief.

## Against "done when"
For opus, exercises 2 and 3 in a row: every idea meets every criterion, with the same prompt; between them, only the code changed, and only to refuse less. It is met if you rule both borderline points acceptable and would keep the set.

## Recommendation
Opus, as the only model. Sonnet costs half as much but fails the index on every repeat. No prompt change.
