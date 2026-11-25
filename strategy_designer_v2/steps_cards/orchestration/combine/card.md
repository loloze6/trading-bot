# combine: one portfolio from the research's strategies, by the boxes they trade in (designed 2026-11-25; not built)

(Function card, `../../HOW_WE_DESIGN_A_CARD.md`; no model call, so no prompt or model sections. It replaces the draft
`../../topics/44_review/COMBINATION_STEP_DRAFT.md`, whose evidence E1 to E10 it keeps. Designed with the operator on
2026-11-25 (next steps P6b): "a logical reading mechanism of profile, to allow the best combination without
overfitting"; then "regimes do not overlap, so why split the money?"; "one side does not mean we should exclude it:
deciding so would be overfitting"; "go, let's try and iterate if necessary".)

## Business objective, one question
**From every strategy the research has proven, which portfolio uses, in each kind of market, the strategies that
trade there, without any choice tuned on results, and does it hold on data nobody used to build it?**
Why: P4's 20 strategies, combined at equal capital without regard to where they trade, held on 2016-17 and lost on
2026 (`runs/PORTFOLIO_UNSEEN_RUN.md`); night 7 made strategies that trade in one market profile (topic 49), and P10b's
map portfolio earned on 2026 (Sharpe 0.29 against -0.73), but its choice saw 2026.

## The words (`../../common/market_profile.md`)
- **A box:** a market profile (six) and a side (long or short): twelve boxes.
- **A strategy's presence in a box:** the share of its coin-days in a position that fall in that box (the coin's own
  profile that day; the position's sign).
- **Its times the market:** that presence divided by the market's own share of the profile (all coin-days of the same
  coins and dates). About 1: the strategy trades there as often as the market is there (it does not choose); 5: it
  chooses that market (night 7's 038-01: 81 % of its days in "falling agitated", against 16 % for the market).

## The rules
| # | Rule | Why | Number, and what it means |
|---|---|---|---|
| 1 | **Place:** a strategy goes in every box holding at least 10 % of its days in a position; its times the market is shown for each | a strategy is used where it really trades, specialist or not (no strategy is put aside for trading in every market or on one side: that would be a choice made from results) | **10 %**: a box where it trades on fewer days is not where it trades |
| 2 | **Admit:** step 5 confirmed, step 6 profitable enough, and its mean daily return on its days in a position inside its boxes above 0 | it must earn where it is placed | 0 |
| 3 | **One per family** (strategies descending from the same first idea of a brief): the fewest generations, then the earliest made | variants of one idea are one bet (E4: 5 of one family combined, Calmar 0.70; 5 families, 0.80); the choice uses no result | none |
| 4 | **Unrelated:** strategies taken in brief order; one enters if its daily returns correlate under 0.5 with every strategy already in that shares a box with it | two related strategies are one bet twice (E5: at 0.64 to 0.71, no gain from combining); the order uses no result | **0.5**: one explains less than a quarter of the other's moves |
| 5 | **Weights:** each strategy runs at 1 ÷ the number of strategies in its most crowded box, of its own size; fixed once | on a day a coin is in one profile only, so strategies of different profiles never hold the same coin at once: their money is not split; strategies sharing a box are, so that a box never holds more than one full strategy | 1 ÷ n |
| 6 | **Judge:** the portfolio's daily return is, coin by coin, the weighted sum of its strategies' returns, then the mean over coins; step 6's measures on the folds; then the unseen coins (next steps 1u), compared once with two portfolios fixed now: (a) every strategy admitted by rules 2 to 4 at equal weight, (b) P10b's map (P10a's rule, without sides); then the sealed holdout, once, for the chosen version; every version tried stays listed | a choice judged on the data it was chosen on proves nothing; the list of versions shows any search | holds: Sharpe after costs above 0 |

**What keeps it from overfitting:** no number is chosen from results (10 %, 0.5 and 1 ÷ n are fixed on this card
before any portfolio is built); no strategy is weighted or dropped by its result beyond step 6's own answer; the
comparison with (a) and (b) is made once and recorded whatever it shows; the holdout is opened once.

**Shown, not ruled** (visibility): how often, coin-day by coin-day, the strategies' positions add up to more than one
full position (strategies in a wider profile, such as "agitated", overlap with a narrower one, such as "falling
agitated").

**Parked** (topic 53, option D): moving the money each day to the strategies that hold a position that day (more
capital used, weights changing every day).

## Input
The register (`../ideas_similarities_check/register/books.json`, each book's `side`), each book's records (steps 5
and 6; step 4's chart file: positions and value per coin and day), the coins' daily data, the unseen coins' results
(1u).

## Output
`orchestration/combine/portfolios/<version>/`: `boxes.csv` (each strategy's presence and times the market per box, its
boxes, its return there), `portfolio.json` (the strategies, their boxes and weights, the commit), `measures.json`
(in-sample; then the unseen coins; the overlap shown); one line per version in `portfolios/INDEX.md`.

## How to call it (when built)
```
python3 orchestration/combine/helper/boxes.py                    # each register book's presence by box
python3 orchestration/combine/helper/combine.py --version NAME    # a version, by the rules above
```
Why this cannot leak: it reads finished records after the fact; each day's profile uses closes up to that day.

## Done when
The box reader's tests pass (hand-made records whose boxes are known); on night 7's specialists it gives the profile
their idea names; a first version is built and judged on the unseen coins against (a) and (b).

## What this function does not do
It does not change a strategy, choose ideas (step 7 and `select_next` never read it), read the unseen results to
choose, move money by the day (parked), or trade (the portfolio layer, P5).
