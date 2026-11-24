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
- **025-03.d2 combined with momentum (`runs/NIGHT4_RUN.md`, test 2):** correlation 0.64 and 0.71 on the folds; Sharpe 1.21 to
  1.26 combined (half each, or equal risk) against 1.24 alone. At a share explained of 0.4 to 0.5 two books are mostly one
  bet; a real gain needs a correlation near 0.

- **Real books that do not pay, combined (topic 47, measurement 1d-7, in-sample, 2026-11-23):** one real book (step 5
  confirmed) drawn at random from each of night 5's five sessions, equal risk, 500 draws: correlation 0.12; Calmar 0.49
  alone, 0.80 combined (0.87 with weights known in advance only); deepest fall about 35 % alone, 18 % combined; above
  0.75 in 55 % of draws, 44 % with no paying book in the draw; five books of one family: 0.70. This questions the
  decision "each must pay on its own" (below): real books that do not pay alone may pay together. Not yet on unseen dates.

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
| 2026-11-23 | Which books (replaces the row above): real by step 5, size above 0, earning on its own in sample (step 6's Sharpe above 0, no bar on how much), one per family, unrelated (correlation under 0.5); not "each must pay on its own" (step 6's bars) | the operator ("option A", then "what if we only allow ones rejected by step 6 but with a positive Sharpe", then "Go") | real books that do not pay alone may pay together (1d-7); books that lose sink any weighting (P2, first run) | step 6's bars (too few books, one family); no earning condition (7 losing books, every weighting loses); a strength threshold (the strongest hold least, 1d-11) |
| 2026-11-23 | Weights: equal capital (by the rule written before P2: another rule only if chosen on 3 of 4 folds and better on 3 held-out folds) | the operator ("Go") on the designer's P2 | chosen out of fold on 3 of 4 folds | equal risk, shared risk: not better out of fold |
| 2026-11-22 | Keep every paying strategy with its similarity matrix (the register of paying books, `orchestration/ideas_similarities_check/register/MATRIX.md`, current with every run since `run_idea` calls the check); how to combine them automatically is decided later | the operator | the portfolio needs every strategy that pays and how they relate; the rule for choosing and weighting them comes later | a contribution measured now (most of today's books, one family, would add almost nothing; and a repair changes a book's contribution) |

## Status and next
**Portfolio design steps (2026-11-23, the operator: "before, we need to see what are the candidates, what is the weight,
same strategy or in parallel"):**
| # | Step | What it settles |
|---|---|---|
| P1 | The candidates. Decided 2026-11-23 (the operator: option A): real by step 5, not "each must pay on its own"; its size above 0 (topic 47 N2), with no threshold on in-sample strength (topic 47, 1d-11: the strongest in-sample results hold least on unseen dates); unrelated to the others by the similarity register; its book faithful to its idea (topic 47 N3); one per family | which books |
| P2 | The weights, compared out of fold (chosen on three folds, judged on the fourth): equal capital, equal risk (each book's swing over the previous days), and risk shared with the correlations | how much of each |
| P3 | In parallel or in one strategy: decided 2026-11-22 (in parallel, the portfolio layer, option A); P1-P2 measured that way | how they run together |
| P4 | One portfolio fixed by P1-P3 before any unseen result is seen, run on the unseen dates against its books alone | whether it holds |
| P5 | The portfolio layer's card and build (engine, shared code: the operator's go) | only if P4 holds |

**P1 and P2, measured (2026-11-23, `topics/44_review/p1_candidates.py`, `p2_weights.py`, their CSVs):**
- P1 as decided: 280 register books, 213 with a size above 0, 51 families, 25 candidates (13 daily, 12 hourly; the
  others correlated 0.5 or more with one already in). Not applied: fidelity to the idea (every book predates topic 47 N3).
- P2 on them: every weight rule loses (whole chain Calmar -0.21 equal capital, -0.16 the others), though the median book
  alone is at 0.19. Cause, checked against step 6's records: 7 candidates lose on their own after costs, 4 hourly ones
  heavily (017-01: -1.2 % a day in a position, 21 trades a day, Sharpe -13.8). A size above 0 says the idea exists, not
  that its book keeps it after costs; no weight fixes a book that loses every day.
- Variant measured (`--earning`, not yet decided): the same rule, keeping first only the books that earn on their own in
  sample (step 6's Sharpe above 0; no bar on how much). 173 books, 43 families, 20 candidates (13 daily, 7 hourly).

  | Weights | Calmar fold 1 / 2 / 3 / 4 | whole chain: Calmar, yearly, worst fall, Sharpe |
  |---|---|---|
  | equal capital | 2.02 / 2.04 / 2.38 / 2.57 | 1.37, +10.3 %, 7.5 %, 1.64 |
  | equal risk | 1.71 / 3.27 / 1.64 / 1.84 | 1.17, +5.8 %, 5.0 %, 1.75 |
  | shared risk | 1.94 / 2.90 / 1.87 / 1.76 | 1.19, +5.8 %, 4.9 %, 1.80 |
  | the books alone (median) | 0.67 / 0.61 / 0.25 / 0.27 | 0.24, Sharpe 0.50 |

  Out of fold, equal capital is chosen on 3 of 4 folds and the other choice does worse on its held-out fold: by the
  rule written before the run, **equal capital**. In sample only: the candidates were kept for earning on these same
  dates, so these figures are optimistic; P4 judges on the unseen dates.

**P4 read (2026-11-24): outcome B.** The 20 books, equal capital: holds on 2016-17 (Sharpe 1.08, worst fall 11 %), not on 2026 (Sharpe -0.73, -3.1 % a year, worst fall 5 %; holding the coins -14 %, fall 45 %). Falls far smaller than holding, books uncorrelated, but on 2026 the books lose on average; the long-leaning books follow the market, the two with no net lean hold on both. P5 not started. Reading: `runs/PORTFOLIO_UNSEEN_RUN.md`.

**P10 pilot, the market-profile map (2026-11-24, the operator's idea; `44_review/p10_map.py`, `p10_map.csv`,
`p10_results.csv`).** Six profiles fixed before any strategy was read (the six coins' 60-day trend: rising, choppy,
falling; their 30-day swing against its median: calm, agitated; each day labelled at the previous close); each of the 22
candidates placed by its days in a position, by profile and side.
- **The strategies are not profile specialists:** their days in a position follow the market's days (002-03: 32, 13, 24,
  4, 18, 9 % across the six profiles, against 31, 14, 22, 3, 17, 11 % of all days). They differ by side only (11 long,
  11 short).
- **Where they earn by profile does not repeat:** of 132 strategy-profile cells, the gain keeps its sign from 2018-21 to
  2022-25 in 50 %; cells that earned on 2018-21 earn on 2022-25 in 57 %, those that lost in 58 %.
- **The map's portfolio** (one strategy per filled cell, equal risk per profile: 4 strategies, half in 013-04): Sharpe
  1.02 on the folds against 1.64 for the 20; 2.24 on 2016-17 against 1.08; -1.06 on 2026 against -0.73. Half long, half
  short is the same as equal capital here (11 and 11).
- **Reading:** for these strategies the map cannot guide the combination: they are one-sided and always on. It is a guide
  for the search: no strategy has a profile as its home; ideas that act in one profile only are the empty cells.

**P4** (2026-11-23): the portfolio fixed before its unseen test, its reading rule and expected outcomes written:
`runs/PORTFOLIO_UNSEEN_RUN.md`. **The combination function, draft** (rules, each with its evidence, and open
points): `topics/44_review/COMBINATION_STEP_DRAFT.md`.

Kept (2026-11-22): every paying strategy and its similarity matrix (the register, kept current by `run_idea`). Waiting: at least two unrelated paying books that each hold on the unseen dates (today one family, momentum: topic 41's
register). Then: the layer's card (by `HOW_WE_DESIGN_A_CARD.md`), the operator's go for the engine change, its proof
(the layer on two books gives method A's daily returns, minus the netted costs).

## Links
`runs/COMBINE_TEST_RUN.md`, `topics/08_review/` (the test's script and configs), topics 08, 10, 41,
`common/forecast.md` (points 7 and 8).
