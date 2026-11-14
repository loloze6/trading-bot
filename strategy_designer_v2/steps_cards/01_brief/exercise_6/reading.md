# Exercise 6: the step 1 prompt with the test-condition rule

Prompt change since exercise 5 (`system_prompt_used.md`). The line on refutation now reads: "Do not say how to test it: no condition on the check, such as what to control for or account for, or which coins it must hold for". The card's criterion says the same.

Same five requests as exercise 5, in order, on a new test index (`briefs/`). Log: `run_log.txt`. Cost: 0.224 USD.

| # | request | brief | attempts | cost |
|---|---|---|---|---|
| 1 | RSI theme | 001 RSI extremes: reversal, continuation or nothing? | 1 | 0.030 |
| 2 | TradingView page | 002 moving-average cross: trends persist | 1 | 0.119 |
| 3 | no theme | 003 volume separates reversal from continuation | 1 | 0.023 |
| 4 | no theme again | 004 large coins lead small coins | 1 | 0.024 |
| 5 | RSI theme again | 005 RSI divergence: does it predict a turn? | 1 | 0.029 |

Five of five first answers passed (exercise 5: one of five). The 900-word guard, set after exercise 5, explains most of this.

**Test conditions**
- 001: "for all three coins" is gone. Held.
- 002: the exit-like sentence of exercise 5 ("a cross the other way marks the end") is gone. Held.
- 003: none. Held.
- **004: not held.** "Once the smaller coins' own past moves are known" is still there, and a new one too: "if any delay is so short that it never appears beyond the bar in which the leaders moved". The lead-lag theory seems to carry its standard check with it: the model treats the control as part of what the theory means.
- 005: "a new high or low of similar size without one" sets a matched comparison. Borderline.

The other criteria held on all five briefs: one theory each, a reason marked as the helper's own, no result cited, questions kept as questions, the index respected (003 to 005 differ from what came before).

**Reading.** The rule holds on 3 of 5 briefs, fails on 1, and is borderline on 1. Step 2 now enforces the same rule on its own, and in step 2's exercise 2 no idea kept 004's condition. So a condition that slips through step 1 stops at step 2.

**Proposed: no further step 1 change.** A stronger step 1 rule would need examples, which the prompt avoids. A code check would need a list of phrases, which breaks on the next wording. Step 2 is the net.
