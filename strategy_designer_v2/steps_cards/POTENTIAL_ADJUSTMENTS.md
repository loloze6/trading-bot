# Improvements: one list (parked)

Every improvement noted while designing, running and trading, in one list: research (this file's steps and the bot's
engine), live, hosting and viewer topics alike. Each waits for the operator's go. What is done is removed (git keeps it;
each fix is in its card and its commit). Reviewed with the operator 2026-11-19 (20 items to 11, then one list with the
operator's topics). Where = the session or part of the workflow it belongs to.

| # | Improvement | Where | Status |
|---|---|---|---|
| 1 | [Step 3: the noise from writing a test freely](#1-step-3-the-noise-from-writing-a-test-freely) | research: step 3 | parked |
| 2 | [Duplicate ideas: a rule on the plan](#2-duplicate-ideas-a-rule-on-the-plan) | research: select_next | parked |
| 3 | [Ideas tested on data step 7 did not see](#3-ideas-tested-on-data-step-7-did-not-see) | research: orchestration | unseen dates done; unseen coins and a limit per data set parked |
| 4 | [Record the regime detector's values in the backtest](#4-record-the-regime-detectors-values-in-the-backtest) | research: engine | parked |
| 5 | [Coins without data on the reachable venue](#5-coins-without-data-on-the-reachable-venue) | research: data | parked |
| 6 | [Brief management](#6-brief-management) | research: briefs | larger topic, parked |
| 7 | [Two loops calling the components step at the same time](#7-two-loops-calling-the-components-step-at-the-same-time) | research: components | parked (loops run one at a time) |
| 8 | [An idea proven and profitable: what next](#8-an-idea-proven-and-profitable-what-next) | research and live | larger topic: observe and advise (market-direction split measured), paper trading |
| 9 | [Futures candles for a pre-live check](#9-futures-candles-for-a-pre-live-check) | research and live | parked until a topic opens |
| 10 | [Several coins in one bot](#10-several-coins-in-one-bot) | live session | not started |
| 11 | [Hosting the bot](#11-hosting-the-bot) | hosting research session | research report ready; waits for the operator |
| 12 | [Live operations](#12-live-operations) | live session | not started |
| 13 | [Research viewer, round 2](#13-research-viewer-round-2) | visualizer session | in progress (hourly runs shown); a brief-link fix waits for the operator |
| 14 | [A viewer of the live bot](#14-a-viewer-of-the-live-bot) | live and visualizer sessions | not started |
| 15 | [The GitHub security warning](#15-the-github-security-warning) | operator | not examined |

## 1. Step 3: the noise from writing a test freely
- **Details only a plan can settle:** how its non-overlapping samples are drawn, which test it uses, and what each case
  is ("sharp-move bars": up moves only, or every labelled bar?). Step 5's conventions cover the common cases.
- **One idea, different tests:** the same idea gets different verdicts from two plans written separately (second night:
  013-04 t +1.99 in one run and +2.46 in another; 012-01 +2.11 and +3.26), and one judgement differs by bar size or
  between mirror ideas (a volume split "adapted" on daily bars, "replaced" on hourly ones; 003-05 against 003-06).
- **True mismatches remain:** plans whose config does not trade the stated situation (night_013_run d2: averaging an
  always-negative and an always-positive block; second night: two more, one at 82 %).

## 2. Duplicate ideas: a rule on the plan
`select_next` finds a duplicate only when two ideas have the same text and data. Seen: two ideas from different parents
(`...d1_weekend-moves-reverse-both-ways` and `...b1_weekend-fall-reverses-monday.d1_weekend-moves-reverse-both-ways`,
night_run) gave the same t (+2.75) and the same failures, about 1 USD each; step 2's 002-01 (after the cross) and 002-05
(from cross to cross) became the same config in step 3. A rule on the plan (same config, same data) rather than on the
text would catch both. Not built.

## 3. Ideas tested on data step 7 did not see
From the overnight run (2026-11-13): of 8 ideas confirmed on the 6 default coins, 4 did not hold on 9 other coins, and
step 7's own numbers are inflated by its search; 6 coins count as about 2 independent coins (books' correlation 0.40 to
0.46), so years, not coins, set what an idea can show. Unseen dates are standard since 2026-11-18
(`orchestration/unseen_test/`). Left to discuss: test the same plan unchanged on coins step 7 never saw (the overnight
tool `oos.py`, removed, in git history); and count the ideas tried on one data set, with a limit past which a result
there counts only with an unseen test.

## 4. Record the regime detector's values in the backtest
From the overnight run (2026-11-13; step 5's false "mismatch" on N1-01), parked by the operator.
- **What was seen:** the engine records the strategies' components, but not the regime detector's components: only its decision (the `regime` column). Step 5 and step 7 must recompute the detector's measures from prices.
- **To do:** record the detector's value and each of its components' values in the backtest record, for analysis.

- **Also in the backtest record** (2026-11-19): `forecast_distribution.csv` puts a forecast of exactly 0 in the bin
  "-5_0" (bins closed on the right), so its "negative" bins count the flat bars. Read the bars for the sign.
## 5. Coins without data on the reachable venue
BNB: no data on Kraken. Parked with the quality of the backtest output.

## 6. Brief management
The operator's grouping: **result loop back** (a file next to the brief, not inside it, saying what its run found: its
ideas' results, its blocked ideas, where the lines went), **brief archiving**, **brief reopening**. Seen tonight: the
answer to "which of the theory's ideas are real and pay" was written by hand in runs/NIGHT_RUN.md; no file holds it.

## 7. Two loops calling the components step at the same time
Two loops on the same working tree would build into the same shared files (`strategy_components.py`, the catalogue,
the specs) at the same time. Tonight the briefs ran one after the other. (A build cut by a restart is undone at the
step's next start since 2026-11-19: `components/card.md`.)

## 8. An idea proven and profitable: what next
Operator, 2026-11-15. Line 7.f ("what could break a confirmed idea and its profitable book") is on hold: being real and
profitable is not a result to diagnose but the end of the research, where a decision starts. To design as one topic:
the final test on the sealed holdout, what could break the idea and its book, how several such books combine, paper
trading, a small live test, and watching it once live. First inputs: 7.e's two confirmed and profitable ideas
(002-03's e1, N2-04's e1, 2026-11-14).
- **2026-11-18:** the unseen test is done (`runs/UNSEEN_RUN.md`, outcome 1); next is paper trading of momentum in uptrends
  (night_013) and high-RSI trend continuation (validation), via the live session.
- **The regime line, folded in here (operator, 2026-11-15):** most of its problem is now covered by validated lines
  (7.d asks when a book should not be in the market; 7.b and 7.c propose an effect limited by a condition; the sizing
  cuts exposure in violent periods). What is left belongs with combining books: a regime shared by several strategies
  (one condition that switches books on and off), and pure regime findings (a condition with nothing graded inside,
  not an idea under the shared definition), as building blocks for that switch.

- **A stage of its own: observe and advise** (operator, 2026-11-19). After the verdict (step 5) and the profitability
  check (step 6, pass or fail only), informational measures and an advice, gating nothing. First measure, from the
  one-sided ideas' investigation (153 backtests with a verdict, 12 runs): each book's return in the windows where the
  market rose and where it fell, next to the market's. The 13 profitable books, per coin and window:
  | Profitable books | Windows where the market | Market | Book | Windows the book gained |
  |---|---|---|---|---|
  | long only | rose | +92 % | +24.7 % | 73 % |
  | long only | fell | -30 % | -3.4 % | 19 % |
  | both sides | rose | +63 % | +19.7 % | 79 % |
  | both sides | fell | -26 % | +4.0 % | 44 % |
  They earn in rises and stand aside in falls: they need rises somewhere, not a bull market (2026, a falling year:
  Sharpe 0.4 to 1.8, holding 0.1). Of the 13 profitable books, 11 trade long only; short-only ideas lose even when the
  market falls (-0.5 % against -30 %), so ideas are kept free (no forced long and short). Also to observe: most
  profitable books are one family ("in when the trend is up"), one bet counted many times. Advice to consider when
  books are combined: not only long-trend books; at least one that earns in falling windows.
## 9. Futures candles for a pre-live check
Live trades Kraken futures; the research backtests spot. Prices differ by 0.002% to 0.05%: 5 decisions in 321 days
differ (the 0.2 rule on a knife edge), at most 8.67 per 1,000. Futures candles start 2022-03-23 (ZEC 2022-08-24), so
they cannot replace spot for the folds (B and C are 2018 to 2021). Proposed when a topic opens: the data source as a
backtest setting (spot by default) and a pre-live check of an idea going live on futures candles from 2022-03, with
funding once modelled (funding is the larger spot vs futures difference).

- **The short side** (2026-11-19): live trades perpetual futures, where longs usually pay shorts funding in rising
  markets; the backtest ignores it, so it understates what a short earns. A brief that tests the short side on purpose
  (side "short" or "long and short") is worth it once funding is modelled.
## 10. Several coins in one bot
One bot trading a few coins at once, each with its share of the account (the research tests one book per coin). The operator's topic (2026-11-18).

## 11. Hosting the bot
The live bot runs on the operator's PC today. The hosting session compared providers (1blu, OVH VPS-1, netcup): `trading-bot/live/hosting/research.md` on its branch. The operator's topic (2026-11-18).

## 12. Live operations
Failure, stop, restart, crash, notification. The operator's topic (2026-11-18).

## 13. Research viewer, round 2
Improvements, hosting, access from the phone. The operator's topic (2026-11-18).

## 14. A viewer of the live bot
The live runs' books and decisions, day by day. The operator's topic (2026-11-18).

## 15. The GitHub security warning
GitHub reports 1 critical vulnerability on the default branch (Dependabot alert 1). Not examined. The operator: park.
