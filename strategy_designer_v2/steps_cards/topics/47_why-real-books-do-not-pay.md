# Topic 47: why most real effects give a book that does not pay, and why paying books hold less on unseen dates

Status: open (measured 2026-11-23; for the operator's decision on which step to develop)  
Where: research: step 3 (how a book is built), step 6 (the Calmar bar), steps 1-2 (effect size), steps 5-6 and
`select_next` (how many tries of one effect)  
Opened: 2026-11-23, by the operator ("go on 1, 2, 3"), after the night-5 reading (`runs/RETEST_RUN.md`,
`runs/NIGHT5_PATHS.md`).

## Question
The workflow finds real effects (step 5 confirms two in three) but few of them pay (step 6), and paying books hold
less on unseen dates: which step owns each loss?

## Seen
**1. The Calmar gate** (`47_review/calmar_gate.py`, `calmar_gate.csv`; the 81 books step 5 confirmed in the five
night-5 runs, from their committed chart files; Calmar recomputed here equals step 6's to 3e-05).
- 72 of the 81 do not pay; **all 72 fail Calmar** (bar 0.75), 42 on Calmar alone.
- Holding the same coins on the same days: Calmar 0.16 (median), below 0.75 for all 81. The books that do not pay
  reach 0.40 (median); the 9 that pay, 0.85.
- The 72 fall into three groups, by where their deepest fall comes from:

| Group | Books | What it is | Seen in |
|---|---|---|---|
| A. The trade does not pay its cost | 25 | mean return per trade after costs at or below 0 (round trip 0.19 %) | settlement 15, absorption 6 |
| B. The book falls with the market | 41 | earns its cost per trade, but over its deepest fall holding the same coins fell more than 20 % | all runs; the deepest falls mostly in 2022 |
| C. Other | 6 | short or both-sided books caught in a market rise, or small falls | weekend, learned |

- Paying books against the others (medians): in a position on 23 % of the days against 67 %; 1,272 trades against
  5,267; 1.43 % per trade after costs against 0.24 %; deepest fall 12 % against 35 %; the same yearly return (10 %).
  A book that pays trades its effect rarely and strongly; one that does not is in the market most days, with an edge
  per trade close to its cost, and lives through the market's crashes.
- **Correction (operator, 2026-11-23): a crash hurts a book only if it is on the wrong side, or if its effect does not
  work in that market** (`47_review/side_in_fall.py`, `side_in_fall.csv`). Of the 41 books in B, the side they held:

| Books in B | Sides | Side held over the deepest fall | In a position over the fall | Deepest fall | What it is |
|---|---|---|---|---|---|
| 30 | long only | long (median +0.53) | 53 % of coin-days | 40 % | one-sided by design, long through a falling market: the wrong side |
| 11 | both sides | neutral (between -0.16 and +0.03) | 24 % | 15 % | not the market's direction: the effect itself did not work in that period |

  So "falls with the market" holds for the 30 long-only books only. For the 11 two-sided ones the market fell at the
  same time, but they were neutral: their effect failed in that market state (for example the volatility-graded weekend
  reversal: half long, half short, side +0.02 over a fall of 24 % while its coins fell 46 %). Up or down is not the
  only state that matters.
- Step 6 chains the windows in fold order (2022-23, then 2018-21, then 2024-25), not in date order. Chained by date,
  Calmar's verdict changes for 3 of 81 books (1 fail to pass, 2 pass to fail): not the cause.
- 4 of the 81 books are exact copies of another (same Calmar, return and trades): a 7.d repair whose added condition
  changed nothing, a test spent for nothing.

**2. Search luck** (`47_review/search_luck.py`, `search_luck.csv`; the 59 ideas with an unseen test, all runs). The
share of the effect kept on unseen dates is the unseen statistic over what the in-sample effect would give on a period
that long (a statistic grows with the square root of the length).

| Ideas | 2016-17: n, holds, effect kept | 2026: n, holds, effect kept | In-sample t (median) |
|---|---|---|---|
| Generation 0-2 | 36, 92 %, 1.19 | 17, 82 %, 1.19 | 3.38 |
| Generation 3-4 | 21, 71 %, 0.44 | 14, 79 %, 0.63 | 3.77 |
| 0-4 ideas of its branch tested before it | 39, 85 %, 1.00 | 19, 84 %, 0.88 | |
| 5 or more tested before it | 9, 78 %, 0.77 | 6, 67 %, 0.39 | |

- The deeper a book (the more tries before it), the higher its in-sample statistic and the less of it is left on
  unseen dates: the pattern of a selection that keeps luck. Small samples (generation 5+: 2 ideas), and deeper ideas
  are also later nights' non-momentum ideas: the type of idea and the depth are mixed.

## Why it matters
Developing a step without knowing which one owns the loss spends builds where the loss is not.

## Options
| Option | Gain | Risk |
|---|---|---|
| Step 3: a book built for the effect: in a position only when the signal is strong (few, large trades), and not exposed to the market's direction (B: 41 books) | the largest group; what the 9 paying books already do | a new way to build books: a card, a design, a proof |
| Steps 1-2 (and 5): the effect's size per trade against the round trip measured before a book is built (A: 25 books) | stops spending tests on effects too small to trade | none if it is a measure, not a prompt sentence (the operator's caution on cost in prompts) |
| Step 6: the Calmar bar (0.75; holding gives 0.16) | a business choice, not a defect: the 9 paying books reach it | lowering it lets books through that fall with the market |
| Steps 5-6 and `select_next`: a stricter bar for a book found after many tries of its effect, and a branch that keeps failing the same check is left | fewer lucky books; tests spread over more effects | the size of the correction is to be designed |

Recommended: step 3 first (the largest group, and the mechanism the paying books show), with the effect size per trade
measured beside it (A); the search correction next.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-23 | Step 3 first: the book reflects the idea (its situation, its side, its horizon); a hand check on 5 ideas before any build (phase A), then the build (B), then a run (C) | the operator, on the designer's proposal | today's book trades "the score above its usual level" almost every day, not the idea; the check tells the gain before a build | "only when strong enough to pay its cost": a fitted threshold (search luck) and cost in a book's design; building first: a build spent before the gain is known |
| 2026-11-23 | Study 2: no luck correction built yet; breadth over depth in `select_next` (a branch that keeps failing the same check is left); search luck measured again after step 3's change; a stricter bar for books found after many tries designed only if deep books still keep under half their effect | the operator | luck grows with the tries; a book that reflects its idea should need fewer tries | a correction now: sized on small groups, before the larger loss (study 1) is fixed |

## Status and next
**Final next steps after the review (2026-11-23), in order:**
| # | Step | Value | Effort |
|---|---|---|---|
| N1 | Combinations on unseen dates: **replaced (2026-11-23, the operator)** by topic 44's portfolio steps: first the candidates (P1), the weights (P2), in parallel (P3, decided), then one portfolio fixed before any unseen result is seen, on the unseen dates (P4) | decides whether the workflow's aim becomes "find different real effects and combine them" | see topic 44 |
| N2 | Step 5, an informative measure: the idea's gain beyond the coin's drift at its horizon, per trade, with its t by day, against the round trip | shows, per idea, whether the effect is worth trading beyond the market's drift (19 of 81 real books are below 0) | **done 2026-11-23**: the gain was already measured (step 5's size, 2026-11-20, same values as this analysis); added: how sure it is (its t by day) |
| N3 | Step 3: the book trades the idea's situation (1b) | a verdict tests the idea (phase A: 3 of 5 confirmations were of another book) | medium |
| N4 | The engine's MAE and MFE without the entry bar (shared code) | correct trade diagnostics (median daily MFE 6.2 % reported, 3.9 % real) | **done 2026-11-23** (proof in topic 48) |
Kept for later, not sure enough: the stop moved to the entry after +1 %, long only on hourly books, merging re-entries, a horizon set from the edge curve.

| # | Step | Status |
|---|---|---|
| 1a | Phase A: 5 ungated ideas rebuilt to trade only their situation, steps 4-6, measured problem by problem (`runs/BOOK_REFLECTS_IDEA_RUN.md`) | done 2026-11-23: days in a position fell (6-56 %), falls and Calmar did not improve (the situation days fall in the crashes); 3 of 5 no longer confirmed on their own situation |
| 1b | Phase B: step 3's card and build, proved on the same 5 ideas | if 1a gains |
| 1c | Phase C: a run, the problems read one by one against night 5 | after 1b |
| 1d-1 | Crash periods (`47_review/crash_state.py`; a coin in a crash: 30 % below its 90-day high, or 30-day return -20 % or lower, known before the trade): the phase-A books' trades inside crash periods earn as much or more than outside (absorption +0.69 % against +0.41 % a trade; deep 2-hour fall +0.41 % against +0.06 %), with the same swing (about 6 % a trade). Their worst falls are ordinary losing streaks: shuffling a book's days 1,000 times gives a fall at least as deep in 63-95 % of the shuffles. So the falls come from a small edge against a large swing (about +0.5 % against 6 % a trade), not from crashes, not from the book's shape | done 2026-11-23 |
| 1d-2 | Trade odds (`47_review/trade_odds.py`, `trade_odds.csv`; the 81 real books of night 5). Per trade, the swing is 15 to 17 times the mean gain for paying and non-paying books alike: it does not separate them. The margin is thin: a typical real book that does not pay wins 51.5 % of its trades, and 6.5 points fewer winners would bring its mean trade to 0 (paying books: 53 %, 11 points). What separates them is how the trades add up: paying books make 160 trades a year with about 2 of their 6 coins in a position at once, and their daily Sharpe is 0.89 of what independent trades would give; books that do not pay make 660 a year with about 3 to 4 of 6 coins at once, and get 0.34 of it (coins move together: many trades at once act as one bet). Daily Sharpe 0.99 against 0.70; Calmar follows Sharpe (correlation 0.73 over the 81). Rough: per-trade returns are price moves, not weighted by size or holding time | done 2026-11-23 |
| 1d-3 | Losing streaks (`47_review/streaks.py`): coins open trades on the same day twice as often as if independent (2.25 against 1.21: market-wide situations). With each coin's own sequence kept but the timing between coins scrambled, the deepest fall halves (35 % to 17 %) and Calmar triples (0.41 to 1.21; 42 of 72 would pass). A fall is a series of losing bets (operator); the series is deep because the coins lose on the same days | done 2026-11-23 |
| 1d-4 | Other types (`47_review/book_types.py`; 221 register books, all runs): the same in every horizon and bar: swing 7 to 21 times the mean per trade, coins opening together about 2 at a time, the fall halving with the coins decorrelated. Hourly books: the mean trade about 0 (margin -0.4 points). Paying books (23): margin 15 points against 3 | done 2026-11-23 |
| 1d-5 | Levers inside one book (`47_review/levers.py`; stop, target, both, a brake after a loss, a crowded day as one bet, book volatility target): none lifts the typical book (Calmar 0.41 at best unchanged; at most 5 of 72 pass). Targets (limiting a trade's gain) lower Calmar: the edge is in the large winners | done 2026-11-23 |
| 1d-6 | Against the market (`47_review/hedge.py`): each trade less the market's move: Sharpe from 0.71 to -0.94 (not paying) and 0.99 to -0.30 (paying). The edge is the market's move caught at the right times (market timing), not one coin beating the others: hedging removes it, and the coins cannot be decorrelated | done 2026-11-23 |
| 1d-7 | Combining different effects (`47_review/combine.py`): one real book drawn at random from each of the five sessions, equal risk, 500 draws: correlation 0.12; Calmar combined 0.80 against 0.49 alone; deepest fall 18 % against about 35 %; above 0.75 in 55 % of draws (44 % with no paying book). Weights known in advance only: 0.87, 58 %. Control, five books of one family: 0.70, 41 %. In-sample; not yet on unseen dates | done 2026-11-23 |
| 1d-8 | Trade by trade (operator: the trades' file and the forecast profile; `47_review/trade_table.py`, `trade_profile.py`, `clean_excursions.py`, `trade_rules.py`, `breakeven.py`; 1.55 million trades of the 81 real books, every entry feature known before the entry; rules judged out of fold). (1) Losing and winning trades look alike at entry: win rate moves 2 to 5 points across the fifths of any feature, and dropping the worst fifth chosen on three folds makes the fourth worse (daily mean trade 0.97 % to 0.76 %). Exception: the side; shorts lose in the 2018-2025 market (hourly books long only: win rate 46 % to 58 %, mean trade -0.03 % to +0.35 %, better in 67 % of book-folds). (2) Raising the win rate is easy and useless: a take profit at +1 % gives 88 % winners and a mean trade of 0.00 %: the best tenth of trades makes 1.8 times a daily book's total (5.2 times hourly). (3) Stops cut winners: 38 % of daily winners first go 3 % against (after the entry bar); stops at -2 % to -10 % lower the mean trade. (4) Protecting a gain without capping it helps a little: once +1 % is reached the stop moves to the entry price: mean trade 0.97 % to 1.21 %, better in 62 % of book-folds (daily; bar by bar; fills at the entry price assumed). (5) Found on the way: the engine's MAE and MFE include the entry bar, whose range comes before the entry at its close (look-ahead in trading-bot/backtest/run_protocol.py, `_compute_mae_mfe`): engine MFE median 6.2 %, after the entry 3.9 % (daily) | done 2026-11-23 |
| 1d-9 | Trades in depth (`47_review/deep_trades.py`, `event_study.py`; 1.55 million trades; intervals by resampling days, slopes with each book its own base and errors clustered by day). **Forecast size:** daily: no relation to the bet's quality (win rate 50-54 % in every band; slope per forecast point -0.019 %, t -0.56); the money follows the size (48 % of the money from forecasts at the cap of 20); the weakest band (0-2.5) is the worst bet. Hourly: the stronger the forecast, the worse (win rate 46.8 % at 0-2.5 to 40.9 % at 15-20; slope t -18). **When the edge comes:** daily, beyond the coin's drift: +0.09 % at 1 day (t 7.7), +0.12 % at 2-3 days, gone at 5, -0.31 % at 10, -1.36 % at 20 (t -24): the idea's own edge lasts 1 to 3 days and is about one fee; longer holds earn the market's drift, not the idea (losing years 2018 and 2022). Hourly: below the drift from the first hour (-0.03 %, t -30), before costs: the trades are on the wrong side (fades of hourly moves that go on); step 5 confirmed these ideas on a relation (larger forecast, larger move), not on the trades' sign. **Losing streaks:** losses cluster on a coin far beyond chance (runs test: 53 % of daily series, 69 % hourly, against 5 %), but the trade after a loss is not worse (daily +0.52 % against +0.36 % after a win): skipping it is worse on 72 % of daily book-folds: the clusters are market periods, not a signal at entry. **Churn:** 19 % of daily trades reopen the same coin and side within 3 bars, and earn +0.34 % against +1.56 %. **Coins:** daily, a coin that lost on three folds does not lose more on the fourth (54 %); hourly it does (71 %). **Fees:** 2 % of daily gross gains; hourly, the gross is already negative | done 2026-11-23 |
| 1d-10 | **Review (2026-11-23).** Book by book at each plan's horizon (`47_review/edge_at_horizon.py`), the idea's gain beyond the coin's drift: daily median +0.50 % per trade, above a 0.2 % round trip in 29 of 45 books (18 with t > 2 by day), below 0 in 13 (6 with t < -2); hourly median +0.30 %, above the round trip in 23 of 36, below 0 in 6 (3 with t < -2). **Corrections:** 1d-9's "a daily idea's own gain is about one fee" and "hourly ideas are on the wrong side from the first hour" came from all trades pooled, which a few books with hundreds of thousands of trades dominate; per book, most real ideas earn more than their cost beyond the drift. What holds: the books fail Calmar because their gains and losses come at the same moments on all coins (market-timing effects: 1d-3, 1d-6), no rule inside a book helps out of fold (1d-5, 1d-8, 1d-9), different effects combined do (1d-7, in-sample) | done 2026-11-23 |
| 1d | Ideas name the market state their effect works in (steps 2, 7; step 5 measures the effect by state) | after 1a sizes problem 2 |
| 2a | `select_next`: breadth over depth (a branch that keeps failing the same check is left) | design with 1b |
| 2b | Search luck measured again (this card's measurement 2) | after 1c |
| 2c | A stricter bar for books found after many tries, if deep books still keep under half their effect | after 2b, only if needed |
| 2d | Split the luck measure by kind of idea (momentum or not) | when there are enough books with an unseen test |
