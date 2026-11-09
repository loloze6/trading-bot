# Exercise 1: reading against the card's quality criteria

Nine closed-book calls: three models (haiku, sonnet, opus) by three contexts (no theme; the RSI theme; the TradingView page). One prompt, reviewed in `prompt_review.md`. Outputs in `side_by_side.md`. One call per cell, so a difference between two models may be chance. Nothing was backtested.

## Cost (USD, list price as reported by each call)
| | no theme | RSI theme | TradingView | total |
|---|---|---|---|---|
| haiku | 0.0006 | 0.0015 | 0.0047 | 0.0068 |
| sonnet | 0.0092 | 0.0105 | 0.0531 | 0.0728 |
| opus | 0.0197 | 0.0231 | 0.1144 | 0.1571 |
All nine: 0.237. The source dominates the cost (12,000 tokens in against 1,600). The calls pay a cache-write premium on input that a one-off call does not need; called directly, input would cost about half. At most 0.11 USD per brief: cost does not decide the model.

## Against the criteria (✓ met, ✗ broken)
| criterion | haiku | sonnet | opus |
|---|---|---|---|
| one theory | ✓ ✓ ✗ (c3 adds a variant) | ✓ ✓ ✓ | ✓ ✓ ✓ |
| a mechanism, not a rule or formula | ✓ ✓ ✗ (c3 names 10 and 50 bars) | ✓ ✓ ✓ | ✓ ✓ ✗ (c3: "stays on that side until the opposite cross") |
| says why, or says it does not know | ✓ ✓ ✓ | ✓ ✓ ✓ | ✓ ✓ ✓ |
| can be wrong | ✓ ✓ ✓ | ✓ ✓ ✓ | ✓ ✓ ✓ |
| header: only stated keys | ✗ (c1 "bar: (not stated)") ✓ ✓ | ✓ ✓ ✓ | ✓ ✓ ✗ (c3 side taken from a code setting) |
| no results | ✓ ✓ ✓ | ✓ ✓ ✓ | ✓ ✓ ✓ |
| faithful to the request or source | ✓ ✗ (c2 turns your question into an answer) ✗ (c3 lists no other theories) | ✓ ✓ ~ (c3 read one script, not the page) | ✓ ✓ ✓ |

What held everywhere: no model cited a result, from the source ("optimized for better total profit", "tested on BTCUSDT") or from memory. All nine give a refutation in market terms. With a source, all three say the reason is theirs, not the source's, which is true: the page gives none. All three picked the moving-average cross as the theory most of the page supports.

## The models
- **Haiku.** 20 times cheaper than opus. It broke four rules across three calls: a placeholder header line, parameter values, no list of the other theories, and it answered your RSI question ("RSI extremes revert") instead of keeping it a question. A code check catches the first. The last two are errors of meaning that only you would catch. Not fit for this step.
- **Sonnet.** No format error. Honest about what it does not know ("I do not know which effect dominates"). Its best line: the cross fires late, so the theory works only if the trend outlasts the lag. Two weaknesses. In c3 it read the source as one script and missed the rest of the page. In c2 its refutation sets test conditions ("once volatility and trend are accounted for", "shared by all three coins"), which is the helper setting a bar.
- **Opus.** The best reading of meaning. In c2 it keeps three answers open, including "RSI predicts nothing because everyone watches it", the answer a researcher must keep. In c3 it lists five other theories from the page, each a possible next brief. In c1 it names its own rival explanation. Two rule breaks, both from the source's code: a holding rule inside the theory, and `side` copied from a script setting. Twice the cost of sonnet.

Recommendation: opus, with the prompt changes below. Its faults are the ones a sentence of prompt fixes; haiku's are not. Sonnet is the fallback if opus's two faults survive the fix and sonnet's do not.

## Prompt changes the outputs ask for
1. Header: "Write no line for a key that is not stated. If none is stated, write the two `---` lines with nothing between." (haiku c1)
2. "The source is everything pasted, lists included." (sonnet c3)
3. "With a source, always write `other-theories:`; write `none` if the source holds one theory. Without a source, leave that line out." (haiku c1 and c3)
4. "Do not say when to enter, hold or exit." (opus c3)
5. "A setting in code is not a statement of the source. Take header values only from the source's text." (opus c3)
6. "If the request is a question, keep it a question." The prompt said "may". Yours was a question, and one model answered it. (haiku c2)
7. "Say what market behaviour would show it wrong. Do not say how to test it." (sonnet c2)

## What this exercise does not show
Whether the briefs are good for step 2. That is learned when step 2 is iterated. Whether one call per cell is stable: a second sample of opus and sonnet on the revised prompt would show whether the differences above are the models or chance.
