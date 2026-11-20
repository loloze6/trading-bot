# Topic 34: an idea must move more than a round trip costs

Status: open  
Where: research: shared definitions (`common/idea_definition.md`), steps 2 and 7  
Opened: 2026-11-20, a session, from the holding night (`runs/HOLDING_NIGHT_RUN.md`, sets 1 and 2)

## Question
How do we make the workflow look for hourly ideas whose predicted move pays for the trade that captures it?

## Seen
- 2026-11-20, holding night: every confirmed hourly idea was rerun with each bet held for its own horizon (option 2).
  - **Short horizons (1 to 4 bars): 14 distinct books.** They earn 0.8 to 7 bps per unit traded before costs, and a
    unit costs about 10 bps. 0 have a Sharpe after costs above 0, held or not.
  - **Long horizons (24 to 72 bars): 8 distinct books.** They earn 20 to 60 bps per unit before costs. Sharpe after
    costs is above 0 for 7 with the hold, against 0 without it. 2 beat holding the coin, and 0 pass step 6 (2 fail
    only Calmar, at 0.64 and 0.65).
- 16 of the 21 hourly ideas confirmed by step 5 have a horizon of 1 to 4 bars (slow_1h_run, intraday_1h_run).
- `common/idea_definition.md` says nothing about the cost of trading. Step 2 and step 7 therefore propose ideas with
  no reference to how large the move must be. Step 5 then confirms them, because it judges whether the effect is
  real, not whether it pays.

## Why it matters
Most hourly ideas the workflow finds are real but smaller than one round trip. No holding rule and no sizing can make
them pay, so the loop spends its runs on ideas that cannot reach step 6.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Define in `common/idea_definition.md` that an idea is worth testing when its expected move over its horizon is well above the cost of a round trip (the venue's cost, read from the config); steps 2 and 7 read that definition | one rule for every timeframe; the ideas proposed change, not the checks | the models may still misjudge the size of a move; it is seen at step 5 and step 6, not guarded |
| B. Show step 7 the earned per unit traded before costs, next to the cost of a unit, as an observation | step 7 can propose a longer horizon or a stronger condition from a real number | changes only the next ideas, not the first ones from a brief |
| C. Require a minimum horizon on hourly bars | simple | a limit written for one timeframe, against "one rule for every case"; a short idea with a large move would be refused |

Recommended: A, then B if a run shows step 7 needs the number. A puts the business definition where steps 2 and 7
already read it: an idea is a move that can pay for its trade. It holds for daily and hourly bars alike.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|

## Status and next
Waits for the operator. On a go: a definition line in `common/idea_definition.md`, the cost read from the venue config,
steps 2 and 7's prompts pointing to it, then a run of one hourly brief to see whether the horizons and per-unit
earnings of the ideas change.

## Links
`runs/HOLDING_NIGHT_RUN.md` (readings of sets 1 and 2), topic 30, `common/forecast.md` point 7 (the holding period),
`topics/30_review/hold_rerun.py`.
