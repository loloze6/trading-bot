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
| **11, ready for the final test** | the version's daily Sharpe after costs on the portfolio coins **above** holding the same coins (equal weight, the coin-days it trades, the same days) | `update.py`, on every new version | `measures.json` (`portfolio_coins`, `ready`; the scale and the yearly return at a worst fall of 20 %, informative), the INDEX line |
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
- **Holding is one number** (next steps A10, 2026-11-27). A **coin-day of the portfolio** is one coin on one day for
  which at least one of its strategies has a return. Holding is read from the coins' daily data files
  (`trading-bot/local_data/kraken_<COIN>_1d.csv`): each coin's return from the previous day's close to that day's
  close, on the portfolio's coin-days, then the mean over the coins of that day, on the same days as the portfolio. A
  coin-day whose previous day is missing from the file has no holding return (counted, not filled). Before, each
  coin's closes came from the first strategy's record holding that coin: a record with fewer windows gave the coin
  fewer days, so the bar moved with the order of the strategies (v4: 1.075 or 0.945).
  Why this cannot leak: the closes are read after the fact, for a comparison; no strategy's decision uses them.
- **The return at the risk the operator accepts** (next steps A11; the operator, 2026-11-27: "Fall 20% yes"): one
  informative number on every version, its yearly return when every daily return is multiplied by one scale k, k
  chosen so that the worst fall of the scaled returns is **20 %**. The method: the worst fall grows with k, so k is
  found by halving an interval (from 0, doubling an upper bound until its fall reaches 20 %, then 60 halvings); the
  yearly return is step 6's formula on the scaled returns. A version that never falls has no k. It is before any cost
  of leverage (k above 1 means borrowed money) and **in no rule**: `ready` does not read it.
- **The final test's record is written before the run** (the group, the version and its commit, this commit, the
  measures expected and the go bar); its existence marks the final group used, so a second test on the same group is
  refused, even when the first stopped half-way (a test that could be rerun until it says go would be a search).
- **Rule 6 above** (judged on the folds, then the unseen coins, then the sealed holdout) **is replaced in this mode**
  by steps 11 and 12. **`judge_unseen.py` is no longer the judge**: it stays only to read the versions built on the
  research records (v1, v2, v2b), and goes with `unseen_coins.md` in the clean-up list of `data_use.md` (section 6,
  for the operator's go).

## What a run adds to the portfolio (next steps A8, 2026-11-27; `helper/addition.py`)
**The question:** did this run, or this batch (a list of runs), make the portfolio better? A run is judged by the
final product, not by its count of confirmed and profitable strategies (night 9: 11 candidates, almost nothing added).

**The rule:** the portfolio is built twice by rules 1 to 5 on the common records, as step 10 builds it: **with** every
candidate, and **without** the candidates of the run or batch. Both are then measured on the **same coin-days** (the
coin-days on which both have a return), and the reading reports for both:
- Sharpe, yearly return, worst fall, and the yearly return at a worst fall of 20 % with its scale (A11);
- the same on each calendar year (the year's return at a 20 % fall uses the whole period's scale: one scale per
  portfolio, not one per year);
- which strategies entered the portfolio with the run, and which left it.

It decides nothing and is in no rule: no version is built, nothing is written in `portfolios/`. It writes one small
file, `additions/<name>.md` (the run's name, or the batch's given with `--name`), that the run's reading quotes
(`../../runs/NIGHT_RULES.md`). The file holds no date and no commit: the same candidates give the same file.
Why this cannot leak: it reads finished records after the fact; the two portfolios are built by rules that read no
result beyond step 6's answer.

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
their lines in INDEX.md's second table ("Versions by rule"); `measured_again.json` when a version built before a
change of measure is measured again by the current one (`update.py --measure-again`: its strategies and weights as
stored, its `measures.json` untouched); `additions/<name>.md`, what a run or batch adds (A8);
`final_tests/<final group>.json`, one per final group;
the final records in `04_backtest/<run>/<final group>/backtests/<plan id>/` (per coin, made by step 9's runner
`common_record.backtest` with the final coins, joined 2026-11-27: one runner for steps 9 and 12), with the book's chart
file over the final coins.

## How to call it (when built)
```
python3 orchestration/combine/helper/boxes.py                    # each register book's presence by box
python3 orchestration/combine/helper/combine.py --version NAME    # a version, by the rules above
python3 orchestration/combine/helper/update.py                    # steps 10 and 11: a version if the list changed
python3 orchestration/combine/helper/update.py --measure-again VERSION [VERSION ...]   # a built version, by today's measures
python3 orchestration/combine/helper/addition.py --runs RUN [RUN ...] [--name NAME]    # A8: what a run or batch adds
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

Holding from the data files (A10), the return at a 20 % fall (A11) and what a run adds (A8): their tests pass
(`helper/test_update.py`, `helper/test_addition.py`); v3 and v4 measured again, nights 7 to 9 read; status 2026-11-27:
built (`../../runs/BUILD_A8_A10.md`).

## What this function does not do
It does not change a strategy, choose ideas (step 7 and `select_next` never read it), read the unseen results to
choose, move money by the day (parked), or trade (the portfolio layer, P5); nor, after the final test, draw the next
final group (step 13).
