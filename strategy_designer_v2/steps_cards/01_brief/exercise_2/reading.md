# Exercise 2: reading against the card's quality criteria

The revised prompt has the seven changes from `../exercise_1/reading.md`. It ran on sonnet and opus with the same three requests as exercise 1, two samples per cell: twelve calls. Outputs are in `side_by_side.md`. Nothing was backtested.

## Cost (USD, list price as reported by each call; sample 1 / sample 2)
| | no theme | RSI theme | TradingView | total |
|---|---|---|---|---|
| sonnet | 0.0097 / 0.0095 | 0.0147 / 0.0103 | 0.0538 / 0.0602 | 0.158 |
| opus | 0.0199 / 0.0193 | 0.0264 / 0.0228 | 0.1229 / 0.1233 | 0.335 |
All twelve: 0.49. Opus costs about twice as much as sonnet, and at most 0.12 USD per brief.

## Did the seven changes work?
| change | sonnet (6 outputs) | opus (6 outputs) |
|---|---|---|
| 1 header: only stated keys | ✓ all | ✓ all |
| 2 the source is the whole page | ✓ both read the page; sample 1 packs four scripts into one line | ✓ both list 15 other theories, whole page |
| 3 other-theories only with a source | ✗ 3 of 4 calls without a source write "other-theories: none" | ✓ all |
| 4 no entry, hold or exit | ✓ all | ✓ all (exercise 1's holding rule is gone) |
| 5 no header value from code | ✓ all | ✓ all (exercise 1's `side` is gone) |
| 6 a question stays a question | ✓ both | ✓ both |
| 7 refutation, not test design | ✗ 3 of 6 add test conditions ("in all three coins and in both trending and ranging conditions", "across many coins", "flips between coins and regimes") | ✓ 6 of 6; one mild "beyond chance in these three coins" |

The other criteria (one theory, says why, can be wrong, no results, faithful) are met in all twelve outputs, with two small points. Both opus source briefs fold a second trigger into the theory ("or price itself crosses the long average"). It is the same mechanism, so I count it as one theory. Sonnet's RSI sample 1 narrows your question to "information that recent returns do not already give". That is a sharp research point, but it changes what you asked. Opus puts the same point among the reasons for "no information", which is the right place.

## Stability (two samples per cell)
- **Opus** gives the same theory, structure and list of other theories in both samples, on all three contexts. The differences are in wording only.
- **Sonnet** gives the same theory both times, but its list of other theories goes from 3 lines to 7 between samples. Its rule breaks come and go between samples.

## A finding the prompt did not aim at: "no theme" gives one theory
All four no-theme outputs give the same theory: a sharp drop on heavy volume is forced selling and partly rebounds. In exercise 1, sonnet gave the same one again. Asked for "a theory of your choice", the model gives its most typical theory, every time. A second no-theme request would give the brief already written. Proposed fix, inside this step: with no theme, the request also lists the theories of the briefs already written, and asks for one not among them.

## The models
- **Opus** met every criterion and every change in six of six outputs, and is stable between samples. It is the one to keep.
- **Sonnet** reads meaning well, but it repeats the two faults the prompt forbids in words (the spare line, the test conditions), in half its outputs. Two prompt fixes did not hold on sonnet, so a third is unlikely to.

Recommendation: opus as the helper, with this prompt unchanged, plus the list of written briefs for the no-theme request.

## Done when, per the card
The card asks for two exercises in a row with no error. This is the first clean one with this prompt; two samples in one exercise do not count as two exercises. One more exercise is due: opus only, the three contexts, with the list of written briefs added to the no-theme request. It costs about 0.17 USD.
