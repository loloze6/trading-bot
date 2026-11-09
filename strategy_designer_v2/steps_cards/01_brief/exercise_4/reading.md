# Exercise 4: the index rule "same is refused, close is allowed", on opus

Change from exercise 3 (`helper_system_prompt.md`): the helper no longer stops on a theory already in the index. It writes another one that still answers the request. Only a theory that is the same (same claim, same reason, same market) is refused; a close one is allowed. Same index of three lines, three calls, 0.182 USD.

| request | got | close to | words (limit 120) | cost |
|---|---|---|---|---|
| no theme | weekend moves partly reverse when weekday liquidity returns | none | 120 | 0.026 |
| RSI theme | does a divergence between price and RSI extremes predict a turn? | 002 (same indicator, different claim) | 139 ✗ | 0.031 |
| TradingView page | price crossing back over its long average keeps going | 003 (same mechanism, different trigger and reason) | 120 | 0.125 |

The rule works: no stop, no repeat, each answer still answers its request. Two faults, both in the RSI brief: 19 words over the limit, and bold headings in place of prose. Fix: "plain prose, no headings" in the prompt, and a word count in code that sends an over-long brief back.

Seen, not judged: the TradingView brief is the source's second entry mode of the same script. Close briefs will often be the same mechanism with another trigger. One call per request.

Note: "plain prose with no headings or bold" was added to `helper_system_prompt.md` after these three calls ran. It is untested.

Changed after this reading, on the operator's word: the limit is 200 words, not 120 (`helper_system_prompt.md`).
