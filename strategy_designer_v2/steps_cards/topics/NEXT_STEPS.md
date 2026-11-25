# Next steps: the one list (the operator, 2026-11-24: "the next step table list is our line")

The plan, by objective, and every topic card (`NN_*.md` in this folder; `README.md`: what a topic is): a step names
its topic; a topic not yet a step is in section E; a closed topic has one line in section F (merged with the former
`INDEX.md` on 2026-11-25, the operator: "merging both lists"). One line per step: what it serves (objective), why (the evidence that asks for it), what is
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
| P13 | **New (night 7).** Night 7's candidates enter the portfolio's choice | P1's rule: the falling-agitated rebound (038-01; 035-01 and 051-01 are the same effect), the rising-market late week (045-01), control 032-02.b2 | With P10/P11, by the same rule. Note (2026-11-25): the falling-agitated rebounds hold on 2016-17 and none on 2026 (Sharpe about 0): not yet an answer to the year the portfolio failed | with P10 |
| P10b | **New (night 7).** P10 revisited with profile specialists | P10a's map found no specialist and said to revisit when the search brings some; night 7 (M6): rising and calm specialists earn on 2026 (Sharpe 1.33 and 2.21) where P4 lost (-0.73) | P10a's rule unchanged (each profile equal capital, the strategy most concentrated in each filled cell), on P4's 20 and night 7's specialists, against P4: in-sample and both unseen periods (0 USD) | done 2026-11-25 (`44_review/p10_map.py --night7`, `p10b_print.txt`): Sharpe of the map's portfolio (5 strategies, 2 of night 7) in-sample 1.65, 2016-17 1.73, 2026 0.29; P4 1.64, 1.08, -0.73; the 40 at equal capital 1.84, 2.25, 0.06. On the map's market profile (the six coins' average) the specialists are concentrated about twice the market's share, not 82 %: they are built on each coin's own profile (topic 49), which matches the average on 46 to 63 % of days |
| P12 note | **The judge, recommended 2026-11-25** | Paper trading is too slow (the operator); the unseen dates are used | The sealed holdout stays the single final verdict, opened once with the operator's go; meanwhile the unseen coins (1u) are the development judge of P6's method | operator (the holdout's timing) |
| P6b | **New 2026-11-25.** The combination step's card, with a helper that reads each strategy's profile and side | The portfolio is the final product and no step chooses it; P10b: combining by profile helped on 2026; the operator: "a logical reading mechanism of profile, maybe by a dedicated helper, to allow the best combination without overfitting" | Card from `44_review/COMBINATION_STEP_DRAFT.md` and P10b, rules fixed before any result is read; judged on the unseen coins (1u), then the holdout | next (after 1t) |
| P6 | Agree the combination method's rules before any build | The method must be one standard, not a patch per finding | Review `44_review/COMBINATION_STEP_DRAFT.md` (7 rules, each with its evidence; 5 open points), updated with P10 | operator |
| P5 | Run several strategies in one bot | Needed for live trading of a portfolio | The portfolio layer's card and build (shared code) | later: only once a portfolio holds on new dates |

## B. Make the search find strategies the portfolio does not have (topics 47, 44)
| # | Objective | Why | What | Status |
|---|---|---|---|---|
| 1f | Every strategy trades only in the situation its idea names | 26 strategies were built before step 3 kept the idea's situation: they are in a position on 98 % of days (median) though their ideas name an event ("heavy-volume days", "the deepest falls"); 8 are already rebuilt | Rebuild the other 18 with today's step 3, then steps 4 to 7 (list: `47_review/ungated_real_books.csv`) | operator (about 35 USD) |
| 1n | **Revised again 2026-11-25.** A discovery's ideas come after the theme's own | Night 7: discovery briefs took 107 of 117 ideas tested; their first ideas rank first as any brief's and outside P9 | `select_next`: a discovery brief's ideas are ranked as follow-ups of the idea they were found from (that idea's generation + 1), so the theme's own ideas come first and P9 weighs them against the held books. No manual review (the operator disagreed with recording discoveries for a morning choice) | done 2026-11-25 (`select_next`, `discovery:` field; replay of night 7: the theme's ideas first) |
| 1l | **Un-parked 2026-11-25.** A book is flat when its idea says so | Topic 49's proof: 8 % of a book's days in a position are leftovers; night 7 (M8): a median 16 % of the specialists' days in a position are positions left open outside their profile (size 0.04 to 0.1 of the capital), and they make step 6's measures read days the idea did not ask for | Topic 51, option A: a move to flat is never refused by the band; the band still filters small changes between two non-zero positions. Shared code: design note, rerun proof (the same files apart from the leftovers' closes), then the operator's go to merge (topic 19's decision revisited) | built and proven on the working branch 2026-11-25 (topic 51: 1,408 windows rerun, 0 unexplained differences; the specialists' days inside their profile 81, 80, 64 % → 99, 95, 83 %); merging into master: the operator's go |
| 1m | Briefs aimed at the market profiles the portfolio has no specialist in | P10 pilot; P4 failed in 2026 | Night 7: 4 themes in choppy and falling markets, against a control on the code before 1d and 1j (`runs/NIGHT7_RUN.md`) | done 2026-11-25 (reading corrected): the profile works (29 specialist books, a median 82 % of their days in a position inside their profile, against 39 % for the market; the control's books follow the market's days, as P10 saw); the themes failed (discoveries took the night); no choppy or falling-calm specialist confirmed; the falling-agitated specialists hold on 2016-17, not on 2026 |
| 1o | **New (night 7).** The next night | After night 7's measures (1p) | Not designed yet: too early (the operator, 2026-11-25) | later |
| 1p | Night 7 read by measures M4 to M8 | Night 7's first reading used counts it had said it would not judge | `49_review/night7_measures.py`, `.txt`; summary in `runs/NIGHT7_RUN.md` | done 2026-11-25 (no standard script for every night: not wanted) |
| 1q | **New (night 7).** Discoveries add variety instead of copies | Night 7 (M5): 51 confirmed books, about 6 effects; 31 books one effect (the next-day rebound); 29 of 70 discoveries were that rebound | The operator's two options: (a) no brief from a discovery far from the brief's theme; (b) lines 7.e and 7.g are given one maintained file, the profile map (profile x effect x number of proven and profitable books covering it, `common/market_profile.md`), and look for ideas in the profiles not yet covered. Recommended: (b), with 1n | done 2026-11-25, option b (the operator): `register/PROFILE_MAP.md`, written with the register, given to lines 7.e and 7.g; proof (topic 50): on 3 night 7 backtests, 8 rebound discoveries became 1 new one |
| 1r | **New, parked.** Decide-next as an agent step | The operator's idea (2026-11-25): each idea carries why it exists; an agent reads it to pick the next idea | Topic 52 | parked (to open after a night on 1n and 1q) |
| 1s | **New, parked.** Which coins, grouped how, weighted how | The operator (2026-11-25): coins chosen by data, not by a rationale; equal weight and one verdict; analysts do not differentiate; a portfolio whose risk follows the market (P4: worst fall 11.1 % on 2016-17, 4.8 % on 2026) | Topic 53: A the map shows coins; B coin categories by characteristics; C weights by risk; D the portfolio's exposure by regime for a stable standard deviation | parked |
| 1t | **New 2026-11-25.** The profile map counts each strategy's side | P4: the long-leaning books lost on 2026, the two with no net lean held both periods; the map shows profiles, not sides, so "falling, short: none" is not seen | `register/PROFILE_MAP.md` by profile and side (long, short, both), read by lines 7.e and 7.g | done 2026-11-25: each book's side kept in the register (`books.json`, from its positions; common/market_profile.md); of the 109 paying books, 92 long, 16 both, 1 short; the map's short cells nearly empty |
| 1u | **New 2026-11-25.** The unseen coins: a development judge | The unseen dates are used; 68 of 109 paying books ran on the 6 default coins only; 13 coins have data nobody used for them | The unseen test on the coins a plan did not test, same folds and holds rule; run on P4's 20, P11, night 7's specialists (session `unseen-coins`, 0 USD) | running (session) |
| 1v | **New 2026-11-25.** A watched pilot before a night when a step changed | Night 7 lost most of its turns to a rule nobody ran in a loop | `runs/NIGHT_RULES.md`, before the night, 3; the first: `runs/PILOT_CHAIN_RUN.md` (session `pilot-chain`, 15 USD) | done (rule); pilot running |
| 1w | 1l's effect on our books before its merge | The operator: "observe more in detail the impacts of this change on previous runs" | `runs/TOPIC51_IMPACT_RUN.md`: 42 books and the candidates, steps 4 and 6 on both engines (session `topic51-impact`, 0 USD) | running (session) |
| 1k | Know whether step 2's first ideas improve with the analyst's tools | First ideas are confirmed 9 % of the time, follow-ups 56 % (1g); step 2 sees no data, step 7 explores it | A test on night 6's 4 briefs: step 2 with step 7's rules, without and with exploring (folds B and C only), through steps 3 to 5 | later (about 35 USD) |
| 2e | **New (night 6).** An idea unblocked by a component build is run | Night 6, session 1: an idea waiting for a component was not picked again after the component was built, before the budget ended | Check `select_next`'s order for an unblocked idea | later |
| 2a | Stop deepening a line that keeps failing | Deep lines hold less (study 2) | `select_next`: a branch failing the same check again is left | later (after 2b) |
| 2c | A fair bar for strategies found after many tries | Search luck grows with the tries | A stricter bar for deep strategies | not needed while 2b holds (deep books under N3 keep 0.80 to 0.93 of their effect); to recheck after more nights |
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
| 3e | Parallel night sessions do not mix their briefs | Night 6: the four sessions all numbered their brief 031; since 1j, discoveries also write briefs during the night | A rule: numbers given at the merge, or a range per session (recommended: a range per session, given by `run_brief`) | operator; not needed if 1n is chosen as recommended (one brief per session) |
| 3f | Night jobs survive the cloud's container reclaim | Night 6: a detached process died when an idle container was reclaimed | `runs/NIGHT_RULES.md`: the standing night rules; long jobs run as tracked background tasks, resumed when they end (the loop resumes from its files) | done 2026-11-24 (first used by night 7) |
| 3g | Night branches merge by one tested procedure | Night 6's morning merge broke `strategy_components.py` and left the catalogue stating its class count twice | `orchestration/night_merge` | done 2026-11-25: night 6 replayed, the components file and the register's pages identical to the hand repair, the catalogue right where the hand repair was wrong; first used for night 7's merge |
| 3h | **New (night 6).** The night's components reach master | 4 components built under the standing go (UpCloseStreakLength, VolatilityRatioWeightedScaledFall, RiseTimesRangeMultiple, a new setting of RecentToPriorVolatilityWeightedReturn), on the working branch with their build records | Merge into master | operator |
| 3b | Hourly research has 2026 data on every coin | Only 6 coins have 2026 hourly bars | The other 13 coins (about 10,000 trade calls) | later (if hourly research resumes) |
| 4 | Similarity sees when two strategies are in a position together | Agreed with the operator | Days both in a position, in the similarity check | later |
| 6 | One environment for all steps | Simpler runs | One Python for all steps | later |
| 7 | Faster step 5 | `signal_statistics.py` is slow | Speed it up | later |
| 10 | Complete records | 431 checks lack the informative measures | Backfill them | later |
| 3i | **New (P9).** Keep the register small | Comparing every book with the 20 portfolio books added about 195,000 lines of comparison files | Commit the summaries and keep each book's full comparison local, as its returns are | later |
| 9 | A clean repository | 21 merged branches remain | Delete them (the designer's access is refused) | operator |

## E. Other topics, open or parked (a topic card each; not yet a step above)
| # | Topic | Where | Status |
|---|---|---|---|
| T01 | [Step 3: the noise from writing a test freely](01_step3-noise-from-writing-a-test-freely.md) | research: step 3 | open |
| T02 | [Duplicate ideas: a rule on the plan](02_duplicate-ideas-a-rule-on-the-plan.md) | research: select_next | open |
| T03 | [Ideas tested on data step 7 did not see](03_ideas-tested-on-data-step-7-did-not-see.md) | research: orchestration | open (in part done) |
| T04 | [Record the regime detector's values in the backtest](04_backtest-record-regime-values.md) | research: engine | open |
| T05 | [Coins without data on the reachable venue](05_coins-without-data-on-the-venue.md) | research: data | open |
| T06 | [Brief management](06_brief-management.md) | research: briefs | open (larger topic) |
| T07 | [Two loops calling the components step at the same time](07_two-loops-on-the-components-step.md) | research: components | open |
| T08 | [An idea proven and profitable: what next](08_proven-and-profitable-what-next.md) | research and live | open (larger topic) |
| T09 | [Futures candles for a pre-live check, and the short side](09_futures-candles-and-the-short-side.md) | research and live | open |
| T10 | [Several coins in one bot](10_several-coins-in-one-bot.md) | live session | open |
| T11 | [Hosting the bot](11_hosting-the-bot.md) | hosting research session | open |
| T12 | [Live operations](12_live-operations.md) | live session | open |
| T13 | [Research viewer, round 2](13_research-viewer-round-2.md) | visualizer session | open |
| T14 | [A viewer of the live bot](14_a-viewer-of-the-live-bot.md) | live and visualizer sessions | open |
| T15 | [The GitHub security warning](15_github-security-warning.md) | operator | open |
| T29 | [A model call ran away again](29_a-model-call-ran-away-again.md) | research: step 7, `common/lib.py` | open |
| T30 | [Why hourly ideas rarely pay: a critical review of the 1h runs](30_why-hourly-ideas-rarely-pay.md) | research: the whole workflow | the story so far: [30_review/STORYLINE.md](30_review/STORYLINE.md); change 1 built; the holding period and the diagnosis built on the working branch |
| T31 | [Choosing and judging an idea on different data (folds)](31_choosing-and-judging-on-different-data.md) | research: step 7, step 5, folds | open |
| T32 | [How select_next weighs a step 7 line](32_how-select-next-weighs-a-line.md) | research: select_next | open (parked) |
| T35 | [A horizon in price, not only in time](35_price-horizon.md) | research: common, steps 2, 3; engine | open (after topic 34 step 3) |
| T36 | [Settings counted in bars, carried from daily to finer timeframes](36_fixed-bar-counts-across-timeframes.md) | research: step 3 guide; engine defaults | open |
| T37 | [Long runs without the two-hour limit](37_long-runs-without-the-two-hour-limit.md) | research: how runs are launched | open (parked) |
| T39 | [The idea's size against the cost, coin by coin](39_size-against-cost-per-coin.md) | research: steps 5, 7 | open (parked: about 2 points of accuracy gained; reopen with topic 31) |
| T45 | [Why the research finds almost only long momentum](45_why-the-research-finds-only-long-momentum.md) | research: step 6's rule, books judged alone, one coin at a time | open: investigated; changes for the operator's go |

## Done (kept until read)
| # | Objective | Result |
|---|---|---|
| 1d | Ideas name the market profile their effect lives in | built 2026-11-24 (topic 49): steps 1, 2, 7 name it (trend, agitation or both); step 3's code builds it; proof: a falling-market book flat outside falling markets (0 exceptions, 17,524 bars) |
| 1j | Follow-ups stay on their brief's theme | built 2026-11-24 (topic 50): line 7.b 6 of 6 ideas on the theme (before 4 of 6); line 7.g 5 discoveries, 0 follow-ups (before 6 off the theme); discoveries become briefs in the loop; step 1 names an already-indexed theory instead of inventing one (a defect the proof found) |
| 2b | How much of a found result is search luck, now that step 3 builds the idea as stated | under N3 (night 6, 29 ideas) deep books keep 0.93 and 0.80 of their effect on the unseen periods, against 0.61 and 0.63 before; no stricter bar needed (topic 47, `47_review/search_luck_n3.py`) |
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

## F. Closed topics (decided, built, solved or dropped; the card keeps the reasons)
| # | Topic | Status |
|---|---|---|
| 16 | [Data gathering separate from the backtest](16_data-gathering-separate-from-the-backtest.md) | closed (2026-11-18) |
| 17 | [The data's bar deduced from the trading bar](17_data-bar-from-the-trading-bar.md) | closed (2026-11-18) |
| 18 | [Holes of up to one day ignored](18_holes-up-to-one-day-ignored.md) | closed (2026-11-19) |
| 19 | [The 0.2 rule kept](19_the-0-2-rule-kept.md) | closed (2026-11-18) |
| 20 | [The unseen-dates test made standard](20_unseen-dates-test-made-standard.md) | closed (2026-11-18) |
| 21 | [Speed fixes of the engine](21_engine-speed-fixes.md) | closed (2026-11-18) |
| 22 | [Run briefs in one folder](22_run-briefs-in-one-folder.md) | closed (2026-11-19) |
| 23 | [Built components not merged afterwards](23_built-components-not-merged-afterwards.md) | closed (2026-11-19) |
| 24 | [Components step: a cut build undone; the proof backtest removed](24_components-step-cut-build-and-proof.md) | closed (2026-11-19) |
| 25 | [Loop: when an idea is finished](25_loop-when-an-idea-is-finished.md) | closed (2026-11-19) |
| 26 | [Ideas stay free: no forced long and short](26_ideas-stay-free-long-and-short.md) | closed (2026-11-19) |
| 27 | [Dropped or solved in the review of 2026-11-19](27_dropped-or-solved-in-the-review.md) | closed (2026-11-19) |
| 28 | [Topics kept as cards](28_topics-as-cards.md) | closed (2026-11-19) |
| 33 | [A second round of engine speed work](33_engine-speed-second-round.md) | built 2026-11-20 (A to D); in master since 2026-11-22 (PR 577) |
| 34 | [Why a real idea does not pay, and an idea that pays for its trip](34_an-idea-must-move-more-than-a-trip.md) | built into the steps (size in step 5, size against cost in step 7); the diagnosis kept as a tool in `34_review/` |
| 38 | [The backtest's cost of a trade against real Kraken futures](38_cost-of-a-trade-against-kraken-futures.md) | built 2026-11-20 (an estimate at a 10k USD order); refinement and maker parked |
| 40 | [Repository clean-up, night 3](40_repository-clean-up-night-3.md) | closed 2026-11-21 (all done) |
| 41 | [Is a paying book a new source of profit, or one we already have?](41_does-the-idea-add-beyond-its-filter.md) | built and proven (`ideas_similarities_check`); its reader and its call by run_idea to decide |
| 42 | [Two more measures for step 6: standard deviation and total profit](42_two-more-measures-for-step-6.md) | built 2026-11-22 (two informative measures) |
| 43 | [The findings register](43_the-findings-register.md) | closed 2026-11-21: switched off and deleted |
| 46 | [An idea's id grows past the file name limit](46_idea-ids-grow-past-the-file-name-limit.md) | built 2026-11-23 (option A) |
| 49 | [Ideas name the market profile they act in](49_ideas-name-their-market-profile.md) | built 2026-11-24 (option A) |
| 50 | [Follow-ups stay on their brief's theme](50_follow-ups-stay-on-the-theme.md) | built 2026-11-24 (option A) |
| 51 | [A position smaller than the rebalance band is never closed](51_small-positions-are-never-closed.md) | built on the working branch 2026-11-25 (option A, proven); merge into master: the operator's go |
