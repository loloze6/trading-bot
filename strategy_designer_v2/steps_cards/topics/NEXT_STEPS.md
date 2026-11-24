# Next steps: the one list (the operator, 2026-11-24: "the next step table list is our line")

The plan, by objective. One line per step: what it serves (objective), why (the evidence that asks for it), what is
done, and its status. A step found by a run or an analysis is added with its source. Status: **next** (can go now),
**operator** (waits for the operator's decision), **later** (kept, not now), **done**.

**The aim:** strategies that earn on years the research never used, combined so that together they earn more for
their risk than any one alone.

## A. Combine strategies by a logical rule, not by chance (topic 44)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| P10 | Choose and weight the portfolio's strategies by one written method | P4: the 20 strategies together held on 2016-17 (Sharpe 1.08) and failed on 2026 (-0.73); the portfolio's bet on the market's direction came out by chance (correlation with holding 0.50, then 0.06); the two strategies with no net lean were the only ones to hold on both periods | (1) split each strategy's daily return into its market part (what it earns from the coins' common move) and its idea part (the rest), on the folds; (2) choose strategies by their idea part; (3) set the portfolio's total market part by one rule (for example near zero); (4) weights by P2's out-of-fold rule. Judged on new dates (holdout or paper trading): P4's unseen dates are now seen | next (computing only; the operator's go on the method) |
| P6 | Agree the combination method's rules before any build | The method must be one standard, not a patch per finding | Review `44_review/COMBINATION_STEP_DRAFT.md` (7 rules, each with its evidence; 5 open points), updated with P10 | operator |
| P5 | Run several strategies in one bot | Needed for live trading of a portfolio | The portfolio layer's card and build (shared code) | later: only once a portfolio holds on new dates |

## B. Make the search find strategies the portfolio does not have (topics 47, 44)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| P9 | The search favours ideas unlike what the portfolio holds | Night 6: 8 of 10 families re-found the portfolio's own effects (5 the next-day rebound after a fall, 3 trend continuation) | `select_next`'s similarity term measures an idea's line against the portfolio's strategies, not only the paying ones | operator |
| 1f | Every strategy trades only in the situation its idea names | 26 strategies were built before step 3 kept the idea's situation: they are in a position on 98 % of days (median) though their ideas name an event ("heavy-volume days", "the deepest falls"); 8 are already rebuilt | Rebuild the other 18 with today's step 3, then steps 4 to 7 (list: `47_review/ungated_real_books.csv`) | operator (about 35 USD) |
| 1d | Ideas say in which market state their effect works | Real books lose in market states where their effect does not hold (study 1) | Steps 2 and 7 name the state; step 5 measures the effect by state | later (after P10) |
| 2b | Know how much of a found result is search luck | The n-th variant of an idea holds less on new dates (study 2) | Measure search luck again, now that step 3 builds the idea as stated | next (computing only) |
| 2a | Stop deepening a line that keeps failing | Deep lines hold less (study 2) | `select_next`: a branch failing the same check again is left | later (after 2b) |
| 2c | A fair bar for strategies found after many tries | Search luck grows with the tries | A stricter bar for deep strategies | only if 2b asks for it |
| 2d | Know whether luck differs by kind of idea | Momentum and other ideas may differ | Split the luck measure by kind | when enough strategies have an unseen test |

## C. Better trades inside a strategy (topic 48, parked)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| 13 | Keep winners, cut what costs | Out of fold, moving the stop to the entry after +1 % lifted the daily mean trade (0.97 % to 1.21 %); hourly books lose on their short side | A real backtest of "stop to entry after +1 %" and of long only on hourly books | later |
| 16 | Hold a trade as long as the idea's gain lasts | The idea's gain peaks within days and then fades | The holding time set from the gain curve | later |
| 17 | Fewer trades for the same idea | 19 % of daily trades reopen the same coin and side within 3 bars and earn less | Merge re-entries | later |
| 18 | Know whether hourly is daily done more often | Hourly books lose to turnover | The x24 test: a daily strategy against its hourly version | later |
| 19 | Resume the trade analysis | Two points left to discuss ("most ideas pay their cost"; daily against hourly) | Topic 48 | operator |

## D. Keep the research machinery reliable
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| 3e | Parallel night sessions do not mix their briefs | Night 6: the four sessions all numbered their brief 031 | A rule: numbers given at the merge, or a range per session | operator (before the next night) |
| 3f | Night jobs survive the cloud's container reclaim | Night 6: a detached process died when an idle container was reclaimed | Night sessions run long jobs as tracked background tasks, saving their progress | next (the next night's instructions) |
| 3b | Hourly research has 2026 data on every coin | Only 6 coins have 2026 hourly bars | The other 13 coins (about 10,000 trade calls) | later (if hourly research resumes) |
| 4 | Similarity sees when two strategies are in a position together | Agreed with the operator | Days both in a position, in the similarity check | later |
| 6 | One environment for all steps | Simpler runs | One Python for all steps | later |
| 7 | Faster step 5 | `signal_statistics.py` is slow | Speed it up | later |
| 10 | Complete records | 431 checks lack the informative measures | Backfill them | later |
| 9 | A clean repository | 21 merged branches remain | Delete them (the designer's access is refused) | operator |

## Done (kept until read)
| # | Objective | Result |
|---|---|---|
| P1-P4 | A first portfolio, chosen and judged by fixed rules | 20 strategies, equal capital, side by side; holds on 2016-17, fails on 2026 (`runs/PORTFOLIO_UNSEEN_RUN.md`) |
| P7 | Night 6's strategies as candidates | 2 new candidates (weekday carry; volume swell) |
| P8 | A rule on the market bet | replaced by P10 |
| N1 | Combinations on unseen dates | replaced by P1-P4 |
| N2 | Step 5 measures the idea's gain beyond the drift | built |
| N3 | Step 3 builds the idea's situation as stated | built (it is 1b) |
| N4 | Engine trade statistics without the entry bar | built |
| 1a, 1c | Phase A by hand; a whole run under N3 | done (night 6) |
| 1d-1 to 1d-11 | Why real books do not pay: 11 measurements | done; 1d-11 corrected 2026-11-24 (in-sample strength says little about new dates) |
| 3, 3c, 3d | 2026 hourly data (6 coins); unseen records readable anywhere; unseen test reruns a period without data | done |
| 8 | A check-in after a usage-limit reset | done |
| 11 | The answer on step 7's cost paragraph | "it" was the share of line 7.d's findings blaming the trading cost: 7 of 22 after the change (4 of 20 before); the cost still reaches every line through the analyst's cost input and the shared size-against-cost paragraph |
