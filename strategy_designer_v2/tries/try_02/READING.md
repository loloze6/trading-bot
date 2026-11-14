# Try 02: the claim judge, on real bars (2026-11-05)

**What ran.** `steps/judge/judge_claims.py`, code only. Three claims from try 01's BTC brief, measured on Kraken BTC hourly bars on fold A (six windows). Cost 0.15% per round trip, from the engine's cost model. Pass rule: the claim's own threshold on the whole fold, the same sign in at least 5 of 6 windows, the claim's own minimum events. The sealed range is masked through the policy reader and never printed. One trial row per claim in `records/trials.yaml`.

**Result.** All three fail, honestly.

| Claim | Events | Effect on the fold | Verdict |
|---|---|---|---|
| large bar fades within 24h | 138 | event mean -0.00%, no better than other bars | fail |
| low-volume shocks revert more | 18 vs 87 | the opposite sign, and too few events | fail |
| volume-climax shocks revert within 12h | 42 vs 96 | +0.09%, below the 0.30% asked and not consistent | fail |

On this fold, a large hourly BTC bar does not revert. The belief behind all ten ideas of that brief is not there, at least on fold A. That is the verdict a run should give, in one line, before any strategy config is written.

**What this shows about the spine.** Idea in, number out, pass or fail, and the why is the number. No menu, no grid, no confirmation step. About 150 lines of code, of which the measure is the only part that is claim-specific.

**What is still hand-made.** The three claims were turned into code by hand. The next piece is the step that does that from the claim text: either an AI writes the measurement code against a small library of five measure types (mean difference, ratio of absolute returns, rank correlation, hit rate, net return after cost), or the ideas step writes claims directly in that library's terms. The second is simpler.

**Proposed try 03.** Make the ideas step emit claims in the measure library's terms, so the judge is generic code and no hand translation remains. Then run the full chain, brief to verdict, on the three fake briefs.
