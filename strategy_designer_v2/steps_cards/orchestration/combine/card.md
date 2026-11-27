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

## Versions by rule, on the common records (`../../common/data_use.md`, steps 10 to 12; built 2026-11-26)
Once `data_use.md` runs (a run whose `orchestration/loop/<run>/data_use.json` says `"version": 2`), no person builds
or judges a version: three rules do.

| Step | Rule | Where | Output |
|---|---|---|---|
| **10, a new version** | **when the list of candidates changes**, the next version (`v<n+1>`) is built by rules 1 to 5 above, each candidate read on its **common record** (all portfolio coins, the windows of `research_2016.json`; step 9) in place of its research record; rule 4's correlation on the common records' daily returns | `helper/update.py`, called by `run_idea` right after a candidate's common record (version 2 runs only) and by `night_merge` at the end, after the register's rebuild | the version's folder and its INDEX line |
| **11, ready for the final test** | the version's daily Sharpe after costs on the portfolio coins **above** holding the same coins (equal weight, the coin-days it trades, the same days) | `update.py`, on every new version | `measures.json` (`portfolio_coins`, `ready`), the INDEX line |
| **12, the final test, once** | a ready version's strategies, unchanged, at its weights, on the **final coins** (`common/coins.py`, `FINAL`), over the windows of `research_2016.json` past each coin's first 90 days (the same windows and rule as step 9's common record: one kind of record for steps 11 and 12; the designer, 2026-11-26); **go** when its Sharpe after costs is above 0 and above holding the same coins; **once per final group** | `helper/final_test.py VERSION`, by hand (the operator's act) | `final_tests/<group>.json`, `measures.json` (`final_test`), the INDEX line |

- **A candidate:** a register book of kind `paying` (`books.json`; steps 5 and 6 answered) with a common record: its
  chart file `04_backtest/<run>/common/backtests/<plan id>/chart_bars.csv.gz` and its result
  `orchestration/common_record/<run>/<plan id>.json` (both, the interface of step 9).
- **The list compared:** the sorted keys of the candidates, against `candidates` in the `portfolio.json` of the last
  version built this way (the INDEX's order). The same list: nothing is written. No candidate: nothing is written (so
  until step 9 has made a record, every call changes nothing).
- **Why holding as the bar** (`data_use.md`, Open 3, proposed): a portfolio that earns less than holding its own coins
  adds nothing an investor could not get by buying them. Same days, same coins: the comparison reads the market the
  version was in, not another one.
- **The final test's record is written before the run** (the group, the version and its commit, this commit, the
  measures expected and the go bar); its existence marks the final group used, so a second test on the same group is
  refused, even when the first stopped half-way (a test that could be rerun until it says go would be a search).
- **Rule 6 above** (judged on the folds, then the unseen coins, then the sealed holdout) **is replaced in this mode**
  by steps 11 and 12. **`judge_unseen.py` is no longer the judge**: it stays only to read the versions built on the
  research records (v1, v2, v2b), and goes with `unseen_coins.md` in the clean-up list of `data_use.md` (section 6,
  for the operator's go).

## Input
The register (`../ideas_similarities_check/register/books.json`, each book's `side`), each book's records (steps 5
and 6; step 4's chart file: positions and value per coin and day), the coins' daily data, the unseen coins' results
(1u).

## Output
`orchestration/combine/portfolios/<version>/`: `boxes.csv` (each strategy's presence and times the market per box, its
boxes, its return there), `portfolio.json` (the strategies, their boxes and weights, the commit), `measures.json`
(in-sample; then the unseen coins; the overlap shown); one line per version in `portfolios/INDEX.md`.
Versions by rule (steps 10 to 12): the same folder, `boxes.csv` read on the common records, `portfolio.json` with
`records: common` and `candidates`, `measures.json` with `portfolio_coins`, `ready` and, after step 12, `final_test`;
their lines in INDEX.md's second table ("Versions by rule"); `final_tests/<final group>.json`, one per final group;
the final records in `04_backtest/<run>/<final group>/backtests/<plan id>/` (per coin, made by step 9's runner
`common_record.backtest` with the final coins, joined 2026-11-27: one runner for steps 9 and 12), with the book's chart
file over the final coins.

## How to call it (when built)
```
python3 orchestration/combine/helper/boxes.py                    # each register book's presence by box
python3 orchestration/combine/helper/combine.py --version NAME    # a version, by the rules above
python3 orchestration/combine/helper/update.py                    # steps 10 and 11: a version if the list changed
python3 orchestration/combine/helper/final_test.py VERSION --python VENV_PYTHON   # step 12, once per final group
```
Why this cannot leak: it reads finished records after the fact; each day's profile uses closes up to that day.

## Done when
The box reader's tests pass (hand-made records whose boxes are known); on night 7's specialists it gives the profile
their idea names; a first version is built and judged on the unseen coins against (a) and (b).

Steps 10 to 12: their tests pass on hand-made records (`helper/test_update.py`: a changed list builds a version, an
unchanged one does not, ready and not ready against holding, the final test's refusals, its record before the run);
status 2026-11-26: met on hand-made records only; no common record exists yet, and no final test has been made
(`../../runs/BUILD_A4_PORTFOLIO.md`).

## What this function does not do
It does not change a strategy, choose ideas (step 7 and `select_next` never read it), read the unseen results to
choose, move money by the day (parked), or trade (the portfolio layer, P5); nor, after the final test, draw the next
final group (step 13).
