# 7.d exercise 3: final rules, refreshed inputs, ideas taken through the workflow (2026-11-14)

**Inputs.** The card's fixed inputs, 002-01 (golden cross) and 002-03 (close above the 200-day average), backtested
again with the current steps (the sizing rule added by step 3's code; steps 4, 5 and 6 rerun). With the sizing alone:
002-01 Sharpe 0.38 to 0.49, Calmar 0.001 to 0.20; 002-03 Sharpe 0.51 to 0.68, now ahead of holding, Calmar 0.14 to 0.39.
Both still not profitable (002-01: gain against holding and Calmar; 002-03: Calmar only).

**7.d, twice on each** (`run_1/`, `run_2/`, 1.48 USD). Every analysis starts from what failed, measures as the workflow
measures, writes its repairs as the tested idea amended in full, marks new ideas. The same main repair in both runs:
002-01, "only while the coin's recent-weeks return is positive"; 002-03, near the recent high and with a recent rise.

**Three repairs taken through steps 3 to 6** (step 3 read 7.d's idea files directly, keeping only the idea's fields):

| Repair | Step 3 | Step 5 | Book, 6 coins | Book, 9 unseen coins (diagnostic) |
|---|---|---|---|---|
| 002-01 run 2 d1: golden cross, only while the recent-weeks return is positive | plan (exact) | inconclusive (t 0.97) | Sharpe 0.85, +0.30 over holding, Calmar 0.72 (was 0.49, -0.08, 0.20) | profitable: Sharpe 1.22, +0.85, Calmar 1.54 (original book: 0.57, +0.16, 0.34) |
| 002-03 run 2 d1: above the average, the more the closer to the recent high | plan (adapted) | inconclusive (t 0.61) | **profitable**: Sharpe 0.95, +0.40, Calmar 0.92 (was 0.68, +0.11, 0.39) | profitable: Sharpe 1.18, +0.82, Calmar 1.42 (original book: 0.91, +0.49, 0.70) |
| 002-03 run 1 d1: only while the distance above the average widens | missing-components (the change of the distance) | | | |

**Reading.** 7.d's repairs are relevant: each moves the measures that failed, on the 6 coins and on 9 coins the
analysis never saw. Their ideas are not confirmed by step 5: the repairs earn by staying out where the falls are, while
step 5 measures a rise in the mean return (the same as N7-01 in the overnight run).

**What the exercise revealed.** The sizing's longer warm-up costs a few windows (XMR 23/24, XRP 22/24): the parked
warm-up defect of the engine now bites. Both fixed inputs fail on their falls; no input exercises 7.d's other branches
(a gain too weak; too few trades).

## Third input: 002-04, a gain that fails (added on the operator's instruction)

002-04 (short below the 200-day average, refreshed with the sizing): it loses (Sharpe -0.43, -1.00 against holding,
Calmar -0.16). 7.d twice (0.63 USD): both runs start from the gain (the short loses on its own trades, not on fees:
the coin keeps rising while the book is short) and both find that shorts deep below the average rebound.

| Repair | Step 3 | Step 5 | Book, 6 coins | Book, 9 unseen coins (diagnostic) |
|---|---|---|---|---|
| run 1 d1: below the average, the coin keeps falling only while the average itself declines | plan (exact) | inconclusive (t -0.37) | Sharpe -0.16, -0.72 against holding, Calmar -0.09 (was -0.43, -1.00, -0.16) | Sharpe -0.43, -0.83, Calmar -0.21 (original book: -0.38, -0.78, -0.19) |
| run 2 d1: ..., except when the close has already fallen sharply and far below its recent high | missing-components (the distance below the recent high, and the speed of that fall) | | | |

**Reading.** On the falls branch (002-01, 002-03) 7.d's repairs hold on coins it never saw. On the gain branch they
move the measures only on the coins it read, and not on unseen coins: the short side fights the coins' upward drift,
and the conditional cut 7.d found there (t 1.93 in one quartile) does not carry over. Two of the five repairs needed a
component the catalogue does not have (the change of the distance to an average; the distance below the recent high).

## Final review and confirming run (`run_3/`, 1.03 USD)

The review against the business objective found four things, all fixed in the line's prompt and card:
- the card's objective still said "angle by angle"; it now says "starting from the measures that failed", and "or say
  that none would";
- the measures are named by what they mean (falls, one period carrying the result, the gain, how often it trades), and
  "one period carrying the result" has its own angle instead of sitting with the falls;
- "a new idea, marked as such" put the label inside the idea's text, which step 3 reads; an idea of its own is now
  written like any idea;
- nothing said what to answer when no idea removes the cause; "no ideas, with that cause" is now said.

One run on the three inputs with the fixed prompt: no label in any idea's text (0 of 9); repairs written in full; the
same main repairs as runs 1 and 2 on 002-01 and 002-03; on 002-04 the line reads the short's bet as reversed (the
deeper below the average, the larger the rebound) and proposes it as an idea of its own.

## 2026-11-22: confirmed and not profitable only; repairs that keep the idea (the operator's go; topic 45)
**Change:** the entry condition (step 5 confirmed and step 6 not profitable enough), the prompt (repairs only; the
self-check; "no ideas" only on the size against the cost), the card, `common/idea_created_from.md` ("A repair of a
confirmed idea"). **Fixed inputs:** 9 confirmed books that do not pay, 7 of them among the least explained by the paying
books (0.01 to 0.33): 012-02, 016-03.g1, 012-01, 011-01.g1, 011-01.g2, 013-02.g1, 022-04.b1, 022-04.b2, 026-04.b2. The
three without bars on this machine were rerun through step 4 first (254, 274 and 288 summary files identical to their
records). **Old:** the analyses each run wrote. **New:** the line rerun with the new prompt (15 analyses in all, the
first pass included; 7.48 USD).

**First pass (the self-check as a sentence: "a condition you add must not be an effect of its own"), 6 books:** 14
ideas, all repairs, but 3 added a trend condition ("only while the close is above its 50-day average", "while the
coin's 30-day return is positive") and no finding measured the condition alone: the sentence was not applied. **Fix:**
the self-check made a measurement in the exploration (the bars where the condition holds without the idea's signal,
against those where both hold), given in the finding.

**Final prompt, 9 books:**
| | Old line | New line |
|---|---|---|
| Ideas | 20 | 24 |
| Replacing the confirmed idea (keeping under half of its words) | 4 (3 of them momentum: "near-high momentum keeps rising", "nearness to 90-day high", "four-week momentum continues") | 0 (the least kept: 65 %) |
| Repairs adding a trend or momentum condition | 5 | 2, each measured alone and found not to be the effect (016-03: a rising 30-day trend alone +0.017 % over 24 hours, t 0.3; 026-04.b2: the same condition on light weekends +0.28 %, t 0.62) |
| "No ideas" | 0 | 0 |

Example, 022-04.b2 (unrelated to every paying book, 0.01 explained): old, "volatility reversal with trend", "nearness
to 90-day high", "four-week momentum continues"; new, two repairs of the idea itself, "... only while the coin's 30-day
volatility is calm". The repairs now draw on the idea's own material: the size of the move, volatility, volume, repeated
cases, a longer horizon.

**Not yet shown:** whether the new repairs pay (steps 3 to 6 on them): the next run reads it, with each repair's book
against its parent's in the similarity check.

**"No ideas" without the cost (operator, 2026-11-22):** the sentence now says an idea is closed only when the effect itself
cannot be traded in any version of it (situation, strength, horizon, side); the cost is no longer named. Rerun on 3 of
the 9 books (013-02.g1, 022-04.b2, 012-01; 1.3 USD): no closure (0, as before), 7 ideas, all repairs (73 to 100 % of the
parent's words). Findings naming cost or fees: 7 of 22, against 4 of 20 with the previous sentence: the cost focus
does not come from this sentence; the analyst still receives the cost of a trade, and step 7's shared rules
(`07_common/helper/common_rules.md`) keep the paragraph on the size against the cost, decided after the step 7 A/B test
(2026-11-21). Three books, one run each: a small sample.
