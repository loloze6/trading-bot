# Data use: which coins and years each research step uses, how they are chosen, when they change

(Shared definition, `../HOW_WE_DESIGN_A_CARD.md`. **Status: agreed design, not built** (the operator, 2026-11-26,
next steps A4; designed in the review of night 8, from the draft in `topics/55_data-use-and-stage-moves.md`). Until
it is built, the research runs as before: 6 coins, folds 2018 to 2025, `explore_and_check.md`, `unseen_dates.md`,
`unseen_coins.md`. It replaces those three cards' data rules when built; topic 53 (which coins, grouped how) is
answered here for the grouping.)

## Business objective, one question
**Which data may each research step use, so that a strategy is found on some data, combined on other data, and
confirmed once on data nobody used, with no person choosing which data serves what?**
Why: a result judged on the data that found it proves nothing (night 7 and 8: every slice of data was looked at in
turn, and the frozen holdout is a future half-year, empty today); a person's choice of coins or dates is a hidden search (the 6 usual
coins were picked for their long history; the new years were looked at when portfolios were chosen).

## The words
| Word | Meaning |
|---|---|
| Strategy | one idea's tested settings |
| Candidate | a strategy confirmed (step 5) and profitable (step 6); also, if next steps A2 is agreed, one confirmed and failing step 6 on Calmar alone |
| Portfolio version | the combination card (`orchestration/combine/card.md`) applied to every candidate |
| Run | one search loop on one subject (`run_brief`, `loop`) |
| Batch | several runs launched in parallel, each on its own branch |
| Category | a coin's kind of use: payments, platforms, privacy, finance, infrastructure, AI, meme |
| Window | a 4-month block of dates: January to April, May to August, September to December |

## 1. The coins

**1.1 The universe:** every coin that trades against USD on Kraken with at least 3 years of daily data and a median
daily traded value of at least 100,000 USD over the last 12 months, listed with its category in `common/coins.md`
(the rules, the categories and the final draw of 2026-11-26; fixed until the next final draw). On 2026-11-26: 32
coins; final group XLM, SOL, DASH, UNI, LINK, FET, SHIB; portfolio group the other 25. The 39 coins with files (19 earlier, 20 fetched on 2026-11-26, `runs/DATA_COINS_RUN.md`) and their
categories are listed there.

**1.2 Three groups, with three roles:**
| Group | Role | How it is chosen | When it changes |
|---|---|---|---|
| **Final** | the one confirmation before live | one coin per category, drawn at random among the category's coins with at least 4 years of data; the seed is written in `common/coins.md` | only after it has been used (rule 6): a new draw, the used coins join the portfolio group |
| **Portfolio** | every candidate's common record; building and adjusting the portfolio | every coin not in the final group | when the final group changes |
| **Research, for one run** | finding and checking strategies | 8 coins drawn at random among the portfolio group, at least one per category (the 8th among all); the seed is the run's name | at the start of every run, written in the run's header |

Why 8 coins per run and not all: 25 coins in every backtest would make each idea about 6 times longer to test; a new
draw at every run makes a strategy work on changing coins (the operator, 2026-11-26: "random in a recurrent way"),
and step 9 then measures every candidate on all the portfolio coins.

## 2. The years
| Use | Years |
|---|---|
| Research, explore half (the analysts, step 8) | 2016-01-01 to 2021-12-31 |
| Research, check half (step 5's direction) | 2022-01-01 to the end of the last complete window |
| Research backtest, steps 5 and 6 | both halves, cut in 4-month windows |
| Portfolio and final | the same 32 windows (`04_backtest/windows/research_2016.json`), each coin from its first window after its 91st day: one kind of record for steps 9, 11 and 12 (decided 2026-11-26 during the build) |

**Refreshed:** the data is extended to the last complete day at the start of every batch (or run alone); a window
that has ended joins the check half at the next run. The explore half never grows.

## 3. Data quality
| Case | Rule | Why |
|---|---|---|
| A hole of one day | ignored | the existing rule (topic 18) |
| A longer hole | the coin is left out of that window only; counted in the run | a window must read whole data |
| A coin's first 90 days | never used | thin, erratic prices no strategy could trade |
| A coin that started or stopped trading during a window | left out of that window | as the engine's warm-up rule today |
| Before 2016 | not used | the files are thin (BTC: one trade a day in 2013; LTC: 187 missing days before 2016) |

**Why this cannot leak:** no rule changes how a bar is read; a day's decision uses data up to that day's close only.

## 4. The steps, in order
| # | Step | Data | What it decides | What starts it |
|---|---|---|---|---|
| 1 | Brief, or a target box (next steps B2) | none | — | a run is launched |
| 2 | Ideas | none | — | the brief |
| 3 | Test plan | none | — | each idea, in `select_next`'s order |
| 4 | Backtest | the run's 8 research coins, both halves | — | the plan |
| 5 | Is the effect real? | the same; a "yes" must point the same way on the check half alone | confirmed or not | step 4 |
| 6 | Does it pay? | the same | profitable or not | step 5 |
| 7 | Similarity check | the same | the nearest held strategy (information) | step 6 |
| 8 | Analysts | the run's 8 coins, **explore half only** | new ideas, back to 2 | step 6 |
| 9 | The candidate's common record | **all portfolio coins**, the 32 windows | — | the strategy becomes a candidate |
| 10 | Portfolio version | the candidates' common records | which candidates, their weights | **the list of candidates changed** |
| 11 | Ready for the final test? | the version on the portfolio coins | it earns more than holding those coins (equal weight, the same days) | each new version |
| 12 | Final test, once | **the final coins**, the 32 windows | **go or no-go for live** | step 11 says ready |
| 13 | After the final test | go: live or paper trading; no-go: back to research | a new final draw | step 12 |

A strategy alone "holds" on data it was not found on when its effect keeps its direction and it earns after costs;
the portfolio, in addition, earns more than holding the same coins (the operator, 2026-11-26: for the portfolio only).
No per-strategy test on new data: new data judges the portfolio (the operator, 2026-11-26).

## 5. Where steps 9 to 11 run
One rule: **when the list of candidates changes, a new portfolio version is built**; it runs where the register of
candidates is complete. A run alone: right after a strategy becomes a candidate. A batch: at the morning merge (before
it, each branch holds only its own candidates). No person builds a version; every version is listed
(`orchestration/combine/portfolios/INDEX.md`).

## 6. What it replaces
| Today | With this card |
|---|---|
| 6 fixed coins (BTC, ETH, LTC, XMR, XRP, ZEC: the 6 with data before 2018) | 8 coins drawn per run from the portfolio group |
| folds A to D, 2018 to 2025 | 2016 to the last complete window; explore 2016-2021, check 2022 onward |
| each strategy tested on 2016-17, 2026 and the other coins (`unseen_dates.md`, `unseen_coins.md`) | removed; step 9 gives every candidate one record on all portfolio coins |
| the frozen holdout (a future half-year, empty today; the one before it was opened on 2026-11-18) | removed; the final coins are the last test (a clean-up list for the operator: the guard code, the policy file, CLAUDE.md's rule) |
| the portfolio built and judged by hand | steps 10 to 12, by rule |

## 7. Build plan (each part proven before the next; shared code only on the operator's go)
1. The 20 coins' daily files (session `data-coins`, 2026-11-26).
2. `common/coins.md`: the categories, their source, the final draw and its seed (written 2026-11-26).
3. Step 4's coins and windows: the run's draw, the 2016-2026 windows, the explore and check halves (`run_brief`,
   `run_backtest`, `explore_and_check.md`), with a rerun proof on a fixed plan.
4. Step 9: a candidate's common record (from `unseen_test --coins`), and its call by `run_idea`.
5. Steps 10 to 12: `combine.py` started by the candidate list's change; step 11's bar; step 12 once.
6. The 120 current candidates rerun for step 9 (engine time only); the next portfolio version.
7. A watched pilot of the whole chain before the next batch (NIGHT_RULES).

## Open (for the operator)
1. The number of research coins per run: 8 (proposed).
2. The category source.
3. Step 11's bar: earns more than holding (proposed), or a fixed target.
4. The 90-day exclusion after a coin's listing.
5. ~~A liquidity rule~~: settled in `common/coins.md` (100,000 USD a day over the last 12 months, for the universe).
6. Kraken rebuilt its archive: the 20 new files come from the new edition, the 19 old ones from the earlier one (BTC:
   8 highs in 2013 and volumes up to 4.5 % apart). Refetch the 19 from the new edition, with a rerun proof?
