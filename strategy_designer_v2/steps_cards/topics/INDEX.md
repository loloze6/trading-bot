# Topics: the one list

One line per topic (`README.md`: what a topic is, its shape and its life). Open topics wait for the operator's go;
closed ones keep their decisions and reasons. Numbers are fixed: a new topic takes the next one.

| # | Topic | Where | Status |
|---|---|---|---|
| 01 | [Step 3: the noise from writing a test freely](01_step3-noise-from-writing-a-test-freely.md) | research: step 3 | open |
| 02 | [Duplicate ideas: a rule on the plan](02_duplicate-ideas-a-rule-on-the-plan.md) | research: select_next | open |
| 03 | [Ideas tested on data step 7 did not see](03_ideas-tested-on-data-step-7-did-not-see.md) | research: orchestration | open (in part done) |
| 04 | [Record the regime detector's values in the backtest](04_backtest-record-regime-values.md) | research: engine | open |
| 05 | [Coins without data on the reachable venue](05_coins-without-data-on-the-venue.md) | research: data | open |
| 06 | [Brief management](06_brief-management.md) | research: briefs | open (larger topic) |
| 07 | [Two loops calling the components step at the same time](07_two-loops-on-the-components-step.md) | research: components | open |
| 08 | [An idea proven and profitable: what next](08_proven-and-profitable-what-next.md) | research and live | open (larger topic) |
| 09 | [Futures candles for a pre-live check, and the short side](09_futures-candles-and-the-short-side.md) | research and live | open |
| 10 | [Several coins in one bot](10_several-coins-in-one-bot.md) | live session | open |
| 11 | [Hosting the bot](11_hosting-the-bot.md) | hosting research session | open |
| 12 | [Live operations](12_live-operations.md) | live session | open |
| 13 | [Research viewer, round 2](13_research-viewer-round-2.md) | visualizer session | open |
| 14 | [A viewer of the live bot](14_a-viewer-of-the-live-bot.md) | live and visualizer sessions | open |
| 15 | [The GitHub security warning](15_github-security-warning.md) | operator | open |
| 16 | [Data gathering separate from the backtest](16_data-gathering-separate-from-the-backtest.md) | research: data and engine | closed (2026-11-18) |
| 17 | [The data's bar deduced from the trading bar](17_data-bar-from-the-trading-bar.md) | research: step 4 | closed (2026-11-18) |
| 18 | [Holes of up to one day ignored](18_holes-up-to-one-day-ignored.md) | research: engine | closed (2026-11-19) |
| 19 | [The 0.2 rule kept](19_the-0-2-rule-kept.md) | engine and live | closed (2026-11-18) |
| 20 | [The unseen-dates test made standard](20_unseen-dates-test-made-standard.md) | research: orchestration | closed (2026-11-18) |
| 21 | [Speed fixes of the engine](21_engine-speed-fixes.md) | engine | closed (2026-11-18) |
| 22 | [Run briefs in one folder](22_run-briefs-in-one-folder.md) | research: repository | closed (2026-11-19) |
| 23 | [Built components not merged afterwards](23_built-components-not-merged-afterwards.md) | research: components | closed (2026-11-19) |
| 24 | [Components step: a cut build undone; the proof backtest removed](24_components-step-cut-build-and-proof.md) | research: components | closed (2026-11-19) |
| 25 | [Loop: when an idea is finished](25_loop-when-an-idea-is-finished.md) | research: loop | closed (2026-11-19) |
| 26 | [Ideas stay free: no forced long and short](26_ideas-stay-free-long-and-short.md) | research: steps 2, 7 | closed (2026-11-19) |
| 27 | [Dropped or solved in the review of 2026-11-19](27_dropped-or-solved-in-the-review.md) | research | closed (2026-11-19) |
| 28 | [Topics kept as cards](28_topics-as-cards.md) | research: repository | closed (2026-11-19) |
| 29 | [A model call ran away again](29_a-model-call-ran-away-again.md) | research: step 7, `common/lib.py` | open |
| 30 | [Why hourly ideas rarely pay: a critical review of the 1h runs](30_why-hourly-ideas-rarely-pay.md) | research: the whole workflow | the story so far: [30_review/STORYLINE.md](30_review/STORYLINE.md); change 1 built; the holding period and the diagnosis built on the working branch |
| 31 | [Choosing and judging an idea on different data (folds)](31_choosing-and-judging-on-different-data.md) | research: step 7, step 5, folds | open |
| 32 | [How select_next weighs a step 7 line](32_how-select-next-weighs-a-line.md) | research: select_next | open (parked) |
| 33 | [A second round of engine speed work](33_engine-speed-second-round.md) | engine (shared code) | built 2026-11-20 (A to D); in master since 2026-11-22 (PR 577) |
| 34 | [Why a real idea does not pay, and an idea that pays for its trip](34_an-idea-must-move-more-than-a-trip.md) | research: common, observe-and-advise (08), steps 2, 7 | built into the steps (size in step 5, size against cost in step 7); the diagnosis kept as a tool in `34_review/` |
| 35 | [A horizon in price, not only in time](35_price-horizon.md) | research: common, steps 2, 3; engine | open (after topic 34 step 3) |
| 36 | [Settings counted in bars, carried from daily to finer timeframes](36_fixed-bar-counts-across-timeframes.md) | research: step 3 guide; engine defaults | open |
| 37 | [Long runs without the two-hour limit](37_long-runs-without-the-two-hour-limit.md) | research: how runs are launched | open (parked) |
| 38 | [The backtest's cost of a trade against real Kraken futures](38_cost-of-a-trade-against-kraken-futures.md) | engine settings (shared config) | built 2026-11-20 (an estimate at a 10k USD order); refinement and maker parked |
| 39 | [The idea's size against the cost, coin by coin](39_size-against-cost-per-coin.md) | research: steps 5, 7 | open (parked: about 2 points of accuracy gained; reopen with topic 31) |
| 40 | [Repository clean-up, night 3](40_repository-clean-up-night-3.md) | the repository | closed 2026-11-21 (all done) |
| 41 | [Is a paying book a new source of profit, or one we already have?](41_does-the-idea-add-beyond-its-filter.md) | research: a function next to the unseen test; common | built and proven (`ideas_similarities_check`); its reader and its call by run_idea to decide |
| 42 | [Two more measures for step 6: standard deviation and total profit](42_two-more-measures-for-step-6.md) | research: step 6 | built 2026-11-22 (two informative measures) |
| 43 | [The findings register](43_the-findings-register.md) | research: common, step 7 | closed 2026-11-21: switched off and deleted |
| 44 | [Combining strategies in one bot](44_combining-strategies-in-one-bot.md) | engine (a portfolio layer); research: which strategies | open: direction decided (a portfolio layer); waits for two unrelated books that hold |
| 45 | [Why the research finds almost only long momentum](45_why-the-research-finds-only-long-momentum.md) | research: step 6's rule, books judged alone, one coin at a time | open: investigated; changes for the operator's go |
| 46 | [An idea's id grows past the file name limit](46_idea-ids-grow-past-the-file-name-limit.md) | research: the id convention | open: found on night 5; for the operator |
| 47 | [Why most real effects give a book that does not pay](47_why-real-books-do-not-pay.md) | research: steps 3, 6, 1-2, 5 and select_next | open: measured 2026-11-23; for the operator |
