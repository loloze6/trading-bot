# Exercise 5: the helper as built, five calls in a row on one index

`../helper/make_brief.py` with `../helper/system_prompt.md`, opus, on a test index that starts empty (`briefs/`). Each call sees the briefs written before it. Log: `run_log.txt`. Cost: 0.398 USD.

| # | request | brief | attempts | cost |
|---|---|---|---|---|
| 1 | RSI theme | 001 RSI extremes: reversal, continuation or nothing? | 2 (first was 210 words) | 0.054 |
| 2 | TradingView page | 002 moving-average cross: trends persist; 9 other theories listed | 2 (203 words) | 0.234 |
| 3 | no theme | 003 thin-volume moves revert, heavy-volume moves persist | 1 | 0.021 |
| 4 | no theme again | 004 bitcoin leads altcoins with a lag | 2 (no header) | 0.039 |
| 5 | RSI theme again | 005 RSI divergence: does it warn of a reversal? | 2 (212 words) | 0.050 |

**The index works.** 3 and 4 are different theories. 5 is close to 001 and says so itself ("this is not the question of whether RSI extremes predict moves"). No brief repeats another. Every saved brief is one theory, gives its reason as the helper's own, says what would prove it wrong, and cites no result.

**Small faults in saved briefs.** 002 adds "a cross the other way marks the end of that trend", close to an exit rule. 004 and 001 slip a test condition into the refutation ("once their own past returns are accounted for", "for all three coins").

**The checks work but cost a retry.** 4 of 5 first answers were refused, 3 for length (203 to 212 words). Opus writes about 210 words when told "at most 200". The retry doubles the cost of those briefs.

Two follow-ups, not made because they are untested:
1. Tell the model "150 to 180 words" and keep the code limit at 200, so the first answer usually passes.
2. Keep each refused answer in the log. Today the reason for call 4's refusal is known ("no header") but the text is not.
