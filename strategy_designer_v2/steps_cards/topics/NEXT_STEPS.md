# Next steps: the one list (the operator, 2026-11-24: "the next step table list is our line")

One line per step, its status and where its detail lives. Done steps stay until the operator has read them; a new step
found by a run or an analysis is added here with its source. Status: **done**, **running**, **next** (can go now),
**operator** (waits for the operator's decision), **later** (kept, not now).

## Portfolio (topic 44)
| # | Step | Status | Detail |
|---|---|---|---|
| P1 | The candidates: real, size above 0, earning on its own (Sharpe above 0), one per family, unrelated (under 0.5) | done 2026-11-23 (20 books) | topic 44; `44_review/p1_candidates.py` |
| P2 | The weights, out of fold | done 2026-11-23: equal capital | `44_review/p2_weights.py` |
| P3 | In parallel or in one strategy | decided 2026-11-22: in parallel | topic 44 |
| P4 | The fixed portfolio on the unseen dates | running: 13 daily books read (holds 2016-17, Sharpe 2.25; not 2026, -0.74); the 7 hourly books after the 2026 hourly bars (about 07:30 Paris) | `runs/PORTFOLIO_UNSEEN_RUN.md` |
| P5 | The portfolio layer's card and build (shared code) | operator, only if P4 holds | topic 44 |
| P6 | The combination function: rules, evidence, open points | operator: draft to review | `44_review/COMBINATION_STEP_DRAFT.md` |
| P7 | Night 6's books as portfolio candidates (the P1 rule on the new books) | next, in the morning | `runs/NIGHT6_RUN.md` |
| P8 | **New 2026-11-24 (P4, daily books).** The portfolio is mostly a bet on the market's direction: its daily returns correlate 0.70 with holding its coins in 2016-17 and 0.49 in 2026; the long-leaning books (long 52-81 % of coin-days) earn in 2016-17 and lose in 2026, the short-leaning ones the reverse; the two books with no net lean (013-03, 013-04) earn in both (Sharpe 1.84 and 1.70; 1.94 and 0.87). A rule on market exposure (a book's correlation with holding its coins as a P1 condition, or a portfolio-level hedge) is the next design question. **Caution:** the portfolio's unseen periods are now seen; such a rule is designed on the folds and can only be judged on new dates (the holdout, or paper trading) | operator | `runs/PORTFOLIO_UNSEEN_RUN.md` (reading) |

## The research workflow (topic 47)
| # | Step | Status | Detail |
|---|---|---|---|
| N2 | Step 5: the gain beyond the drift at the idea's horizon, with its t by day | done 2026-11-23 | topic 47 |
| N3 | Step 3: the book trades the idea's situation | done 2026-11-23 | `runs/STEP3_SITUATION_RUN.md` |
| N4 | The engine's excursions without the entry bar | done 2026-11-23 | topic 48 |
| 1c | A run read problem by problem, under N3 | running: night 6 is the first whole run under N3 | `runs/NIGHT6_RUN.md` |
| 1d | Ideas name the market state their effect works in | later (reconsider after P4) | topic 47 |
| 1e | **New 2026-11-24.** The rule "an idea is about one coin's own bars, never the market or another coin" (`common/idea_definition.md`, step 1's prompt): books fail by market timing (1d-3, 1d-6); an idea about a coin against the market could avoid it, but needs the rule changed (and the engine to read a second series) | operator | `runs/NIGHT6_RUN.md` |
| 1f | **New 2026-11-24.** The 26 real books built before N3 with their situation graded away, rebuilt under N3 (steps 3 to 7): faithful books for the families the portfolio holds (draft's open point 1) | next (needs the list of 26 written down first; model cost about 2 USD an idea) | topic 47 phase A |
| 2a | `select_next`: breadth over depth | later (with 1b/1c reading) | topic 47 |
| 2b | Search luck measured again | after 1c | topic 47 |
| 2c | A stricter bar for books found after many tries | after 2b, only if needed | topic 47 |
| 2d | The luck measure split by kind of idea | when enough books have an unseen test (P4 adds 20) | topic 47 |
| 1d-11u | **Done 2026-11-24.** 1d-11 measured again with P4's 13 daily books: in-sample strength says little about holding (0.40, was 0.18) | done | topic 47 |

## Trades (topic 48, parked)
| # | Step | Status |
|---|---|---|
| 13 | A real backtest of "stop to the entry after +1 %" and of long only on hourly books | later |
| 16 | A horizon set from the gain curve | later |
| 17 | Merging re-entries | later |
| 18 | The x24 test (a daily book against its hourly version) | later |
| 19 | Resume topic 48 with its two points to discuss | operator |

## Data and infrastructure
| # | Step | Status | Detail |
|---|---|---|---|
| 3 | 2026 hourly bars for the unseen test | running: 6 coins (BTC, ETH, LTC, XMR, XRP, ZEC), Kraken's 2026 archive then its public trades checked against it (`trading-bot/tools/extend_kraken_hourly.py`) | `runs/PORTFOLIO_UNSEEN_RUN.md` |
| 3b | **New 2026-11-24.** The other 13 coins' 2026 hourly bars (the archive part is cheap; the trades part about 10,000 calls) | later, if hourly research resumes | - |
| 3c | **New 2026-11-24.** Unseen records keep their bars on the machine that ran them only (028-04 had to be rebuilt): `unseen_test` writes the record's chart files, as `run_idea` does in sample | done 2026-11-24 (870bcef8a3): proof, the 13 daily books' readings identical from the chart files | `orchestration/unseen_test/card.md` |
| 3d | **Done 2026-11-24.** `unseen_test` never reran a period whose record had no window (data not fetched then) | done (072b469688) | `orchestration/unseen_test/card.md` |
| 4 | Similarity: days both in a position | later (agreed) | topic 44 |
| 6 | One Python for all steps | later | - |
| 7 | The slow `signal_statistics.py` | later | - |
| 8 | A check-in after a usage-limit reset | done for night 6 (the designer's scheduled check-ins) | `runs/NIGHT6_RUN.md` |
| 9 | Delete the 21 merged branches | operator (the designer's token is refused) | - |
| 10 | Backfill the informative measures (431 checks) | later | - |
| 11 | The designer's answer on step 7's cost paragraph ("what didn't it reduce?") | answered 2026-11-24: "it" was the share of line 7.d's findings that put a book's failure on the trading cost; removing the cost from 7.d's sentence left it at 7 of 22 findings (4 of 20 before), on 3 books. The cost still reaches every line through the analyst's cost-of-a-trade input and the shared size-against-cost paragraph; changing those is a separate decision with its own test | operator |
