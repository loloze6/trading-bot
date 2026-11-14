# Exercise 6: reading

Exercise 5 rerun unchanged: same prompt, same seven ideas, opus. It checks stability. No config was run by the engine.

## Cost

0.43 USD for the seven ideas (0.02 to 0.12 each), against 1.80 in exercise 5. The difference is not real savings. Each request was identical to one sent in exercise 5 less than an hour earlier, so most of its input came from the cache. A request sent cold costs about 0.26, as in exercises 4 and 5. See the proposal below for a way to get this saving on purpose.

## Against the card's criteria

| Idea | Exercise 5 | Exercise 6 |
|---|---|---|
| 001-01, 001-03 RSI | clean | clean; same configs |
| 002-01, 002-05 moving averages | clean, SMA 50/200 | clean; same configs |
| 003-01 low volume | clean | clean; same config shape |
| 004-01 altcoins | untestable | untestable |
| 005-01 divergence | untestable | **forced: two faults** |

**005-01 in detail.** The plan uses a regime, "close at its 20-day high". Inside it, the short is sized by how weak RSI is, using a negated buy-and-hold constant as an offset. That breaks two criteria:
1. **"Never forced."** The deviation says it plainly: "No comparison with RSI at the previous peak is made, because the catalogue has no rolling RSI maximum." That is the very comparison the idea is about.
2. **"No constant inside a regime."** It breaks the letter of the rule. Here it causes no jump of its own: the constant only centres the RSI part, which is capped. The jump at the regime's edge comes from the regime, as in every regime config.

The rest of the plan is careful: one cluster per 10 bars, a permutation test, a minimum of 20 episodes. That is why the model thought it had a valid test.

## Stability

Six of seven plans are stable from exercise 5 to 6: the same configs and the same kind of criteria. The divergence idea is the unstable one. Over the last three exercises it was untestable, untestable, then forced. In exercises 1 and 2 it was forced every time. Whether "close enough" is close enough is a judgement call, and the model makes it differently from run to run.

## Status

Exercise 6 has one plan with two faults, so "two clean exercises in a row" is not met. Exercise 5 stays the only clean one.

## Proposals (not made)

1. **Say what "close" means.** One prompt line: "A config is not close if it drops the comparison the idea is about; then answer untestable." This targets the exact reasoning of this run, where the model kept the "new high" part and dropped the "lower than at the previous high" part. It still leaves the judgement to the model, so it needs two clean runs to show it works.
2. **Cut the cost by about four.** The two references are the same in every call, but they come after the idea in the request, so a new idea cannot reuse them from the cache. Put them first: in the system prompt, or at the start of the request. Every idea after the first would then cost about 0.05 instead of 0.26. This is a change of order, not of content, so the plans should not change. The next exercise would check that.
