# Topic 44: combining strategies in one bot

Status: open (design direction decided; nothing built)  
Where: engine (shared code: a portfolio layer above the strategies); research: which strategies to combine  
Opened: 2026-11-22, the operator: "the potential of combining two strategies together", then "tomorrow we would like
to combine two intraday books in one live bot".

## Question
How does one bot run several paying strategies together, so that the combination is what the strategies would give side
by side, and which strategies are worth combining?

## Seen (`runs/COMBINE_TEST_RUN.md`, 2026-11-22)
- **Side by side (method A, half the capital each), folds A to D:** two unrelated books (correlation +0.05, a momentum
  and a reversal book on BTC and ETH): Sharpe 1.26 and 1.23 alone, 1.66 together; deepest fall 40.9 % and 20.8 % alone,
  17.1 % together. Two near copies (correlation +0.99): 1.03 and 1.04 alone, 1.04 together; the daily standard deviation
  of the combination (1.634 %) is the average of the two (1.685 %, 1.588 %), no reduction. At correlation +0.90: Sharpe
  1.07, the standard deviation about 3 % below the average. The variation of a half-and-half combination is
  √(¼σ₁² + ¼σ₂² + ½ρσ₁σ₂): it falls only when the correlation ρ is low.
- **One config with weighted components (method B, the config's own mechanism):** the same as A only for the pair with
  no gate and one holding period. Otherwise it changes the books: the forecast is the weighted mean of the components
  present in the active regime, so an idea switched off that day leaves the mean and the other idea takes its weight
  (the weights are dynamic); and a config has one holding period. In the unrelated pair, momentum ran at full weight on
  the calm days (about 80 %): Sharpe 1.73, but daily ups and downs 60 % larger than A's and a deeper fall (24.6 %).
- **Out of sample (the unseen dates, A):** the unrelated pair stays unrelated (correlation −0.15 in 2016-17, −0.11 in
  2026) and together falls less than either alone; but the reversal book loses on both periods, so the combination
  earns less than momentum alone. Unrelated makes a combination smoother; it pays only if each book holds on its own.

- **The long-and-short book 025-03.d2 split into its legs (`runs/NIGHT4_RUN.md`, test 1, 2026-11-22):** its short leg
  is unrelated to every paying book (at most 0.10 explained) but small and not reliable (+0.006 % a day, t 1.25); its long
  leg is momentum (0.58). Not yet the second book.

## Why it matters
Combining unrelated books is the cheapest gain in risk the research can find (a higher Sharpe and a smaller deepest fall
from books already proven); combining near copies only adds the same bet twice.

## Options for the mechanism
| Option | Gain | Risk |
|---|---|---|
| A. **A portfolio layer above the strategies:** each strategy a complete config, unchanged (its gate, holding period, sizing); each a fixed share of the capital; per coin, the positions added up and one order for the difference (opposite trades netted) | exactly method A, as tested; nothing inside a proven strategy changes; the same layer serves several coins in one bot (topic 10) | a new layer in the engine (shared code); the netting and the shared capital need their own proof |
| B. Static weights in one config (an idea switched off counts as 0 and keeps its weight) | closes the first gap of method B | still one holding period per config, so two ideas of different horizons cannot be combined |
| C. A holding period per component inside one config | B equals A | deep change in the most delicate part of the engine (the holding rule needed three corrections); rebuilds "two books" inside the forecast |

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-22 | The direction: a portfolio layer (option A); the config's component weights stay for combining parts of one idea | the operator, on the designer's recommendation | it is the tested method A with no change to a proven strategy | B: one holding period per config remains; C: too complex for the gain ("a holding period per component sounds a complex logic") |
| 2026-11-22 | Which strategies to combine: unrelated by the similarity check (`orchestration/ideas_similarities_check/`) and each holding on the unseen dates | the operator and the designer, from the test | unrelated makes the combination smoother; each must pay on its own | combining by the folds' result alone (the reversal book paid there and not out of sample) |

## Status and next
Waiting: at least two unrelated paying books that each hold on the unseen dates (today one family, momentum: topic 41's
register). Then: the layer's card (by `HOW_WE_DESIGN_A_CARD.md`), the operator's go for the engine change, its proof
(the layer on two books gives method A's daily returns, minus the netted costs).

## Links
`runs/COMBINE_TEST_RUN.md`, `topics/08_review/` (the test's script and configs), topics 08, 10, 41,
`common/forecast.md` (points 7 and 8).
