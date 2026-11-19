# Topic 30: Why hourly ideas rarely pay: a critical review of the 1h runs

Status: open (reviewed 2026-11-19; changes wait for the operator)  
Where: research: the whole workflow (briefs, steps 2 to 7, select_next, loop)  
Opened: 2026-11-19 (operator)

## Question
Profitability is almost never reached on 1h bars: what is the root cause, seen from the mechanism (select_next not
going deep enough, step 7 not bringing relevant new ideas, the briefs' ideas not logical or clever enough), and if not
the mechanism, the briefs themselves, bad luck, or something else?

## Seen
The 1h runs with a `run_idea` table (2026-11-19; `hourly_run` predates `run_idea` and has no table):

| Run | What it tested | Ideas | Planned | Confirmed | Profitable | Spent |
|---|---|---|---|---|---|---|
| retest_1h_run | ideas proven on daily bars, retested on 1h | 12 | 12 | 7 | 3 (2 also confirmed) | 13.55 USD |
| slow_1h_run | brief 016 and step 7's ideas from it | 19 | 18 | 8 | 0 | 21.68 USD |
| intraday_1h_run | brief 017 and step 7's ideas from it | 22 | 21 | 14 | 0 | 26.35 USD |

- **New hourly ideas: 39 planned, 22 confirmed, 0 profitable.** The only profitable 1h books are daily ideas retested.
- **All 39 fail every step 6 measure**, Sharpe above 0 included: their books lose money after costs, they do not
  just fall short of a bar.
- **First leads, to check, not conclusions:**
  - *The edge per trade against the cost per trade.* The cost model charges about 18.5 bps a round trip by default
    (`trading-bot/config/cost_model.yaml`). 016-02.g1, confirmed at t +7.68, measures about 0.10 % (10 bps) per
    2-hour slot: a real effect smaller than its cost. But 016-03.g1, confirmed at t +5.27, measures about 0.62 % and
    still does not pay: cost is not the whole story.
  - *The horizon.* The 3 profitable 1h books hold for days (trend ideas); the new hourly ideas hold 2 hours to 3 days.
  - *Step 7 leans to one family* (topic 26: 9 of 10 step 7 ideas in slow_1h_run bet on a rise).

## Why it matters
62 USD spent on the 1h runs; if the cause is in the mechanism, more runs repeat it; if it is the bar size or the
costs, the research should change its target, not its steps.

## Options
| Candidate cause | How the review would test it |
|---|---|
| select_next does not go deep enough | the generations reached per run; whether the best scores were followed or abandoned |
| step 7 does not bring relevant new ideas | step 7's ideas against the brief's: confirmed and profitable rates; how far each moves from its parent |
| the briefs' ideas are not logical or clever enough | the brief ideas' rates; a practitioner's reading of briefs 016 and 017 |
| the briefs (their theme) | the same rates per brief; what the theme can earn at best on 1h |
| bad luck | how many profitable books chance alone would give, from the confirmed rate and the daily runs' rates |
| other: edge per trade below cost per trade on short horizons | per idea: gross return per trade, cost per trade, trades per day (step 6's gross and net, the record's trades) |
| other: step 6's bars set on daily bars | whether the rule's values (0.05 % a day, Calmar 0.75) mean the same on 1h |

Recommended: run the review on the 39 new hourly ideas and the 12 retests, code only (no model call), one table per
candidate cause, then a reading that names the cause or causes with their counts.

## The review (written before it runs, 2026-11-19)
**Purpose:** name the cause or causes of 0 profitable books among the 39 new hourly ideas, with counts; not to judge
whether 1h is worth it (operator: profitability reached on 1d can be reached on 1h, so the outcome is what to change).
**Inputs:** the 39 new hourly ideas (slow_1h_run, intraday_1h_run) and the 12 retests (retest_1h_run), their plans,
records (per window: gross P&L, fees, net P&L, trades, mean trade duration), verdicts, checks and lineage; the daily
runs' rates for comparison. Code only, no model call.
**Expected outcomes, one or more:**
| Outcome | What the counts would show | What it points to |
|---|---|---|
| A. Cost-bound | most confirmed ideas earn before costs and lose after | the edge per trade is below the cost per trade: the steps must aim at edge per trade, not only at a real effect |
| B. Edge does not reach the book | confirmed ideas lose even before costs | step 3's config (sizing, timing) does not trade the effect step 5 measured |
| C. Search-bound | step 7's ideas no better than the brief's; few generations; good scores not followed | select_next or step 7 |
| D. Weak briefs | the brief ideas' rates far below the daily briefs' | the briefs (theme or ideas) |
| E. Luck | with the daily runs' confirmed-to-profitable rate, 0 of 22 is not unlikely | nothing to change yet: more ideas |

## Reading (2026-11-19, code only, 0 USD; scripts in `30_review/`)
**Outcomes A and C, not D or E.** 1h can pay: the daily ideas retested on 1h earn after costs (5 of 7 confirmed).

**A. Cost-bound: the effects are real but too small for how often they trade.** The book at the bars' own closes
(no spread, slippage or fees), against the costs, on the confirmed ideas whose bars are committed:
| Run | Confirmed | Book positive at closes | Positive after costs | Edge per unit traded | Cost per unit traded | Units traded (median) |
|---|---|---|---|---|---|---|
| night_013 (daily) | 11 | 10 | 10 | 38 bps | 9.5 bps | 1,570 |
| retest_1h (daily ideas on 1h) | 7 | 7 | 5 | 22.5 bps | 7.5 bps | 6,565 |
| slow_1h (new hourly ideas) | 8 | 7 | 0 | 2 bps | 10 bps | 17,075 |
Spread and slippage cost about as much as the fees. intraday_1h_run's bars are not committed (records stay small), so
its at-close book is not computed; its 14 confirmed ideas trade 10,000 to 360,000 times and all lose after costs.

**intraday_1h_run, rebuilt** (its bars were not committed): its confirmed ideas rerun here, same plans, data and engine
(13 of 14 started; 017-05.g1 uses a component built on the run session's branch). 7 finished before the background
task's 2-hour limit stopped it; the other 6 were not rerun. In all 7: every window's net result equals the committed one
(144 of 144 each); all 7 earn at closes; 0.3 to 4.6 bps per unit traded against 5.7 to 10.6 bps of cost.

**The analyst saw it first.** Line 7.d's first finding names costs in 38 of 39 analyses (17 of 18, 21 of 21), with the
numbers (016-02.g1: "Fees, not the forecast, sink the book: gains before costs 7.77, fees 18.24"; "the slot effect is
real but too small for its cost"). Its ideas aim where the move is larger (the same slot: 0.25 % in the most volatile
weeks, 0.23 % after a sharp fall, against 0.10 % on average). None was tested (C).

**C. Search-bound: select_next follows confirmation, which is cheap on 1h.** select_next counts a line's analysis as a
success when a tested idea is confirmed OR profitable. With 24 times more bars, small effects reach t +8 to +13.8, so
line 7.g (patterns) kept succeeding: 21 of its ideas tested, many confirmed, none profitable. Line 7.d (not
profitable: why, and what would pay) wrote 80 ideas in the two runs (39 and 41); **none was tested**.

**Why confirmation is cheap on 1h:** a short horizon's random move is small (about ±1 % over 2 hours against ±3.5 % over
a day), so a small effect stands out clearly: 0.10 % over 2 hours gives t 9 over 16,256 coin-days. t says the effect is
real, not that it pays. A higher t threshold for 1h was weighed and not recommended: it holds no cost, so a 0.10 % effect
at t 50 would pass and lose, and a 0.5 % one at t 3 would fail and could pay. **Caveat:** 7.g picks the best hour of
the day in the record and step 5 judges it on the same years, which flatters its t (topic 31).

**Not D (the briefs):** brief ideas are confirmed as often on 1h as on daily bars (2 of 13, against 6 of 37).
**Not E (luck):** at the daily rate (10 of 56 confirmed ideas profitable, 18 %), 0 of 22 has a 1.3 % chance.
**Step 6's bars are not the cause:** the 39 books have a Sharpe below 0 after costs; no bar's value would pass them.

**What a practitioner would change (one at a time, each to the operator):**
1. **select_next: a success is a profitable book** (step 6), not a confirmation: the goal is real and pays, and on finer
   bars confirmation stops telling ideas apart. Cheapest proof: rank both runs again under the new rule and see 7.d's
   ideas come first.
2. **Then test 7.d's waiting ideas** (80, already written; no new step 7 call): do ideas aimed at profitability pay?
3. **Only then, if needed:** make the edge per trade against the cost per trade a stated notion (`common/`) that
   steps 3 and 7 read.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | 1h is not closed: the outcome is what to change | operator | profitability reached on 1d can logically be reached on 1h | closing 1h research |
| 2026-11-19 | Change 1: in select_next, a success is a profitable book, not a confirmation | operator's go, on the design session's proposal | the goal is real and pays; on 1h confirmation is cheap and did not tell ideas apart (7.g record 0.80, none profitable); 7.d's 80 ideas were never tested | a t threshold scaled to the bar (holds no cost); fewer folds on 1h (topic 31) |

## Status and next
Change 1 built (`orchestration/select_next/card.md`: the rule, the records and rankings before and after). Next: change 2,
a short run on 7.d's waiting ideas, on the operator's go. Change 3 only if change 2 shows it is needed.

## Links
`runs/NIGHT_1H_RUN.md`; topics 8, 26; `06_profitability/helper/rule.yaml`; `trading-bot/config/cost_model.yaml`.
