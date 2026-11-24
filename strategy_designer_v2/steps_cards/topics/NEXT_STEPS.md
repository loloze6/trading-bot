# Next steps: the one list (the operator, 2026-11-24: "the next step table list is our line")

The plan, by objective. One line per step: what it serves (objective), why (the evidence that asks for it), what is
done, and its status. A step found by a run or an analysis is added with its source. Status: **next** (can go now),
**operator** (waits for the operator's decision), **later** (kept, not now), **done**.

**The aim:** strategies that earn on years the research never used, combined so that together they earn more for
their risk than any one alone.

## A. Combine strategies by a logical rule, not by chance (topic 44)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| P10 | Choose and weight the portfolio's strategies by one written method | P4: the 20 together held on 2016-17 and failed on 2026; their market bet came out by chance | Pilot P10a (the market-profile map): no rule helps today's strategies, which are one-sided and act in every profile; equal capital kept. To revisit when the search brings profile specialists (1d) | done for today's strategies (2026-11-24) |
| P10a | **Pilot done 2026-11-24.** The market-profile map (the operator's idea) | Strategies exploit a profile and a side: combine across, search the gaps | Six profiles fixed in advance; each candidate's days by profile and side | done: the strategies are not profile specialists (their days follow the market's), their gain by profile does not repeat across halves (50 %), the map's portfolio does worse; the map guides the search (1d), not the combination (topic 44) |
| P12 | **New 2026-11-24.** Judge the next portfolio once, on dates nobody has seen | P4's unseen periods (2016-17, 2026) are now used; a portfolio chosen after seeing them cannot be judged on them | The sealed holdout (2027 H1, opened once on the operator's go), or paper trading from now on | operator (which judge, and when) |
| P11 | **New (night 6).** The two new candidates enter the next portfolio's choice | P7: "a week's gain carries into Saturday" (Sharpe 1.01) and "volume swells after rises" (0.57) are unrelated to the 20 strategies (correlation 0.32 and 0.21) | They join the candidates P10 chooses from, by the same rule | with P10 |
| P6 | Agree the combination method's rules before any build | The method must be one standard, not a patch per finding | Review `44_review/COMBINATION_STEP_DRAFT.md` (7 rules, each with its evidence; 5 open points), updated with P10 | operator |
| P5 | Run several strategies in one bot | Needed for live trading of a portfolio | The portfolio layer's card and build (shared code) | later: only once a portfolio holds on new dates |

## B. Make the search find strategies the portfolio does not have (topics 47, 44)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| 1f | Every strategy trades only in the situation its idea names | 26 strategies were built before step 3 kept the idea's situation: they are in a position on 98 % of days (median) though their ideas name an event ("heavy-volume days", "the deepest falls"); 8 are already rebuilt | Rebuild the other 18 with today's step 3, then steps 4 to 7 (list: `47_review/ungated_real_books.csv`) | operator (about 35 USD) |
| 1j | Follow-ups stay on their brief's theme | The "keep the idea" rule covers line 7.d only; on night 6 the first follow-ups came from lines 7.b and 7.g, which have no such rule, and left every theme (1h) | Lines 7.b and 7.c stay on the theme or answer "not in the data"; lines 7.e and 7.g mark off-theme findings as discoveries, which the loop turns into briefs of their own (`common/theme.md`) | built 2026-11-24 (topic 50); proof running |
| 1l | **New (topic 49's proof).** A book is flat when its idea says so | A position under the rebalance band (0.2 of the capital) is never closed: on the proof's book, 8 % of its days in a position are such leftovers, outside its idea and its profile | Topic 51: measure the leftovers on the paying books (B), then decide whether a move to flat is always allowed (A, engine) | operator |
| 1k | Know whether step 2's first ideas improve with the analyst's tools | First ideas are confirmed 9 % of the time, follow-ups 56 % (1g); step 2 sees no data, step 7 explores it | A test on night 6's 4 briefs: step 2 with step 7's rules, without and with exploring (folds B and C only), through steps 3 to 5 | later (about 35 USD) |
| 1d | Ideas say in which market state their effect works | Real books lose in market states where their effect does not hold (study 1); the P10 pilot: no strategy has a market profile as its home, every profile cell is empty of specialists | Steps 1, 2 and 7 name the profile (its trend, its agitation or both: `common/market_profile.md`); step 3's code builds it; step 5 judges the book where it trades | done 2026-11-24 (topic 49, proof: a falling-market book is flat outside falling markets, 0 exceptions on 17,524 bars). Next: a night with briefs aimed at profiles |
| 2b | Know how much of a found result is search luck | The n-th variant of an idea holds less on new dates (study 2) | Measure search luck again, now that step 3 builds the idea as stated | next (computing only) |
| 2e | **New (night 6).** An idea unblocked by a component build is run | Night 6, session 1: an idea waiting for a component was not picked again after the component was built, before the budget ended | Check `select_next`'s order for an unblocked idea | later |
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
| 3g | **New (night 6).** Night branches merge by one tested procedure | The morning merge first broke `strategy_components.py` (a line-by-line union dropped repeated lines); caught before the push, rebuilt by class | A merge script: the register by key, the components file by class, the index files by git's merge with a check that every line stays once, then both test suites | next |
| 3h | **New (night 6).** The night's components reach master | 4 components built under the standing go (UpCloseStreakLength, VolatilityRatioWeightedScaledFall, RiseTimesRangeMultiple, a new setting of RecentToPriorVolatilityWeightedReturn), on the working branch with their build records | Merge into master | operator |
| 3b | Hourly research has 2026 data on every coin | Only 6 coins have 2026 hourly bars | The other 13 coins (about 10,000 trade calls) | later (if hourly research resumes) |
| 4 | Similarity sees when two strategies are in a position together | Agreed with the operator | Days both in a position, in the similarity check | later |
| 6 | One environment for all steps | Simpler runs | One Python for all steps | later |
| 7 | Faster step 5 | `signal_statistics.py` is slow | Speed it up | later |
| 10 | Complete records | 431 checks lack the informative measures | Backfill them | later |
| 3i | **New (P9).** Keep the register small | Comparing every book with the 20 portfolio books added about 195,000 lines of comparison files | Commit the summaries and keep each book's full comparison local, as its returns are | later |
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
| P9 | The search favours ideas unlike what the portfolio holds | built (ae0c95e349): a parent is weighed against the held books (paying and the portfolio's); 66 ideas of past runs move back a group |
| 1g | Why a brief's first ideas fail | the effect is not in the data (median t 0.32, 41 % the other way); not the build, not too few cases (topic 47, 1d-12) |
| 1h | Why the follow-ups drift | from the first follow-up, what passes step 5 is mostly trend continuation or the next-day rebound; the search keeps what is confirmed (topic 47, 1d-13) |
| 1i | An idea chosen on some years, checked on others | built (795d4409a6): step 7 explores 2018-21; a confirm must point its way on 2022-25; topic 31 decided |
| 1d-1 to 1d-11 | Why real books do not pay: 11 measurements | done; 1d-11 corrected 2026-11-24 (in-sample strength says little about new dates) |
| 3, 3c, 3d | 2026 hourly data (6 coins); unseen records readable anywhere; unseen test reruns a period without data | done |
| 8 | A check-in after a usage-limit reset | done |
| 11 | The answer on step 7's cost paragraph | "it" was the share of line 7.d's findings blaming the trading cost: 7 of 22 after the change (4 of 20 before); the cost still reaches every line through the analyst's cost input and the shared size-against-cost paragraph |
