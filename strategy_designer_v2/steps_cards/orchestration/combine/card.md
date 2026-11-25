# combine: one portfolio from the research's strategies, by where they act (designed 2026-11-25; not built)

(Function card, `../../HOW_WE_DESIGN_A_CARD.md`; no model call, so no prompt or model sections. It replaces the draft
`../../topics/44_review/COMBINATION_STEP_DRAFT.md` (rules R1 to R7 and their evidence E1 to E10, kept there) with the
profile reading the operator asked for: "a logical reading mechanism of profile, maybe by a dedicated helper, to allow
the best combination without overfitting" (2026-11-25; next steps P6b).)

## Business objective, one question
**From every strategy the research has proven, which portfolio earns in every kind of market it can, without betting
on the market's direction, and does it hold on data nobody used to build it?**
Why: P4's 20 strategies, chosen without regard to where they act, held on 2016-17 and lost on 2026: their days follow
the market's in every profile and most lean long (P10a; `runs/PORTFOLIO_UNSEEN_RUN.md`). Night 7 made strategies that
act in one profile (topic 49), and P10b's map portfolio earned on 2026 (Sharpe 0.29 against -0.73), but its choice saw
2026. Of the 109 proven and profitable strategies, 92 are long only (1t).

## The logic, in plain words
A market is in one of six profiles, and a strategy can be long or short in it: twelve cells (`../../common/market_profile.md`).
A good portfolio has, in as many cells as possible, a strategy that earns there, and no strategy that is simply long
everywhere. So: read where each strategy acts (its home), keep the proven ones, put in each cell its unrelated
specialists, give each profile the same share of the risk, and judge the result on data the choice never saw. Every
number in the rule is fixed below, before any result is read: nothing is tuned on results.

## The profile reader (the helper the operator asked for): a strategy's home
**A strategy's home** (`common/market_profile.md`): the cells (profile and side) where it holds its positions. Read by
`helper/home.py` from the strategy's backtest positions (its chart file) and each coin's own daily profile on that day
(the coin's own bars: topic 49's rule), over the folds only:
- per cell, its share of the strategy's coin-days in a position;
- **its home cells:** the cells holding at least 25 % of those days, and always its largest (P10a's rule);
- **its gain at home:** its daily return on the days it is in a position inside its home cells (for: a strategy put in
  a cell must earn there, not only on the whole);
- **its lean:** long, short or both (`books.json`'s `side`, 1t).
For a strategy whose idea names a profile, the home is mostly that profile (night 7: 82 to 99 % of its days after
1l); for one that names none, the reader shows where it really acts.
Why this cannot leak: it reads finished records after the fact, and each day's profile uses closes up to that day.

## The rules (each general; the draft's evidence applies)
| # | Rule | Fixed number | Why |
|---|---|---|---|
| C1 | **Admission:** step 5 confirmed, the idea's size above 0, step 6 profitable enough, and its gain at home above 0 | none beyond those | the draft's R1 (E1-E3); a strategy must earn where it acts |
| C2 | **One per family** (the brief idea it descends from): the admitted strategy closest to the idea | fewest generations, then earliest | R2 (E4) |
| C3 | **Placed by home:** each admitted strategy sits in its home cells | 25 % of its days | P10a; a strategy acting everywhere sits in several cells |
| C4 | **No market bet:** a strategy with home cells on one side in more than 4 of the 6 profiles (a strategy long everywhere) enters only if no specialist fills those cells; such strategies share at most the capital of one profile | 4 of 6; one profile's share | P4 (E10): the long-leaning strategies lost on 2026; the two with no lean held both periods |
| C5 | **Unrelated inside a cell:** a strategy enters a cell if its daily returns correlate under 0.5 with each strategy already in it; strategies taken by brief number | 0.5 | R3 (E5, E6) |
| C6 | **Weights:** each filled profile the same share of the capital, split equally among its strategies (a strategy in several profiles adds its shares); no weight fitted on returns | equal | P10a's rule; R4 (E7: equal capital won out of fold) |
| C7 | **Fixed, then judged:** each version (its strategies, its weights) is committed before it is judged; every version tried stays listed | | R6 (E9): the count of versions is the visibility of any search |
| C8 | **Judged as a strategy:** step 6's measures on the folds; then the development judge, the unseen coins (next steps 1u: the strategies rerun unchanged on the coins they were not tested on); then once, with the operator's go, the sealed holdout | holds: Sharpe after costs above 0 | R7; the unseen dates are already seen (P4, P10b) |

**What keeps it from overfitting:** no number above is chosen from results (25 %, 4 of 6, 0.5, equal shares come from
the draft and P10a, before this card); the method is compared, once, with two others fixed now (P4's equal capital over
all admitted strategies; P10b's map without sides) on the unseen coins, and the comparison is recorded whatever it
shows; the holdout is opened once, for the chosen version.

## Input
The register (`../ideas_similarities_check/register/books.json`, with each book's `side`), each book's records (steps
5, 6; step 4's chart file), the coins' daily data, the unseen coins' results (1u).

## Output
`orchestration/combine/portfolios/<version>/`: `homes.csv` (each strategy's share by cell, home cells, gain at home,
lean), `portfolio.json` (the strategies, their cells and weights, the commit), `measures.json` (in-sample; then the
unseen coins); one line per version in `portfolios/INDEX.md`.

## How to call it (when built)
```
python3 orchestration/combine/helper/home.py                 # the homes of every book of the register
python3 orchestration/combine/helper/combine.py --version NAME  # a version, by the rules above
```

## Done when
The reader's tests pass (hand-made records whose home is known); the reader on night 7's specialists gives their named
profile as home; a first version is built and judged on the unseen coins against the two fixed alternatives.

## What this function does not do
It does not change a strategy, choose ideas (step 7 and `select_next` never read it), read the unseen results to
choose, or trade (the portfolio layer, P5). It does not scale exposure to keep the portfolio's swing stable (topic 53,
option D, parked).
