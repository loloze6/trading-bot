# Topic 30: Why hourly ideas rarely pay: a critical review of the 1h runs

Status: open  
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

## Decisions
None yet.

## Status and next
Open. Waits for the operator's go.

## Links
`runs/NIGHT_1H_RUN.md`; topics 8, 26; `06_profitability/helper/rule.yaml`; `trading-bot/config/cost_model.yaml`.
