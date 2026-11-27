# Topic 56: choppy markets, why no strategy pays

Status: open (parked: to revisit later, the operator, 2026-11-27)  
Where: the search (steps 5 to 7), the market profiles (`../common/market_profile.md`)  
Opened: 2026-11-27, by the operator, from night 9's review ("I would expect here that we challenge the timing,
entry, exit of the trade")

## Question
**Can a strategy earn in choppy markets (no lasting rise or fall), and if not, why not, so that the search stops
spending there or spends there differently?**

A choppy market is one profile of `common/market_profile.md`: a coin neither up nor down by the profile's rule over
the last 60 days; calm or agitated by its daily swing against its own year.

## Seen
**1. The search (nights 7 to 9, `47_review/why_by_profile.txt`):**
| | Choppy calm | Choppy agitated | Choppy (no agitation named) | All choppy |
|---|---|---|---|---|
| Ideas tested | 40 | 49 | 55 | 144 |
| Confirmed (step 5) | 7 | 14 | 6 | 27 |
| Confirmed and profitable (step 6) | 0 | 0 | 0 | **0** |
| Sharpe of the confirmed (median) | 0.47 | 0.51 | 0.07 | |
| Sharpe minus holding's | -0.09 | -0.05 | -0.53 | |
| Calmar (bar 0.75) | 0.18 | 0.42 | 0.01 | |
| Costs / gross profit | 5 % | 8 % | 85 % | |
| Days in a position | 24 % | 5 % | 22 % | |

Every confirmed choppy strategy fails Calmar (27 of 27); most also fail Sharpe against holding. Costs explain the 6
"choppy" ideas only (night 9's first reading said the costs explained all of them: corrected 2026-11-27).

**2. The repairs (`47_review/night9_review.py`, part 4):** 47 repairs of choppy strategies (line 7.d): the median Sharpe
change -0.03, 18 of 47 improved, best Sharpe 0.81, best Calmar 0.71, 0 profitable (falling markets: 52 repairs, 5
profitable). All 144 choppy ideas were on daily bars; the repairs changed the entry in about 39 of 45, the holding or
the exit in about 6.

**3. The trades (`47_review/choppy_giveback/`, 2026-11-27):** the 27 confirmed choppy strategies against the 41
confirmed and profitable ones of nights 7 to 9; 134,888 trades read from each record and the daily bars, 0 skipped;
119,097 of them also in the engine's own trade file, all equal within 0.01 points on best gain, worst loss and return.
Median per strategy:
| | Choppy calm (7) | Choppy agitated (14) | Choppy (6) | All choppy (27) | Profitable (41) |
|---|---|---|---|---|---|
| Days held | 7 | 5 | 8 | 5 | 1 |
| Result per trade after costs | +1.51 % | -0.27 % | -2.04 % | -0.27 % | +0.61 % |
| Best gain reached during the trade | 9.97 % | 6.99 % | 9.22 % | 7.59 % | 4.71 % |
| Worst loss reached during the trade | 7.06 % | 6.13 % | 10.56 % | 6.52 % | 5.66 % |
| Share of the best gain given back (above 1: the trade ends below its entry) | 0.84 | 1.03 | 1.21 | 1.03 | 0.87 |
| Strategies whose mean trade earns | 6 of 7 | 2 of 14 | 0 of 6 | 8 of 27 | 31 of 41 |

Profitable strategies held as long (5 days, 11 of them) reach a best gain of 15.5 % and keep 28 % of it.

Result per trade had every trade exited after N days instead (same entries, same costs; median across strategies;
strategies where it beats the plan's exit in brackets):
| | Plan's exit | 1 day | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| Choppy calm | +1.51 % | +0.01 (1/7) | +0.13 (1/7) | +0.22 (1/7) | +0.87 (1/7) | +0.88 (0/7) |
| Choppy agitated | -0.27 % | -0.02 (10/14) | -0.11 (6/14) | -0.13 (8/14) | +0.04 (13/14) | -0.28 (6/14) |
| Choppy | -2.04 % | -0.91 (6/6) | -1.31 (5/6) | -1.62 (5/6) | -1.51 (6/6) | -1.71 (6/6) |
| All choppy | -0.27 % | -0.12 (17/27) | -0.40 (12/27) | -0.31 (14/27) | -0.09 (20/27) | -0.28 (12/27) |

## What it shows
1. **The exit is not the lever.** No holding time makes the median choppy trade pay; the best (5 days) leaves it at
   -0.09 %.
2. **The entry has no edge in direction on daily bars.** After entry, a choppy trade goes about as far against the
   position (6.5 %) as with it (7.6 %), and ends where it started: the "effect" step 5 confirms is real on average but
   too small against the market's back-and-forth.
3. **Choppy calm is the exception:** its trades earn (+1.51 %) and keep their gain like profitable strategies (0.84).
   It fails on the portfolio-level measures (Calmar 0.18, Sharpe below holding), with a position on 24 % of days: a
   candidate for the combination (next steps A2) rather than for a repair.
4. **Untested:** finer bars. Every choppy idea ran on daily bars; a choppy market's swings last a few days, so an
   entry and an exit inside the day might catch them. That would be a new idea to test, not a repair, and I do not
   know whether it helps (hourly ideas have mostly failed to pay elsewhere: topic 30).

## Why it matters
144 ideas in choppy markets, 0 profitable strategies (night 9 alone: 4 sessions aimed there, 171 USD, whose only
profitable strategies were found in falling markets); the next batches need to know whether to aim there.

## Options
| Option | Gain | Risk |
|---|---|---|
| a. Park choppy: no batch aims at it; choppy calm strategies go to the combination by A2 | no spend where nothing paid | a box stays empty in the portfolio |
| b. One run in choppy markets on 4-hour bars, the repairs allowed to change the holding and the exit | answers point 4 | a run's budget; hourly and 4-hour effects often too small for their costs (topic 30) |
| c. Keep searching on daily bars | none shown | the same 0 of 144 |

Recommended: **a**, revisited after A2 (whether choppy calm strategies add to the portfolio) and after the next batch;
b only if the portfolio still lacks a choppy strategy then.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-27 | Topic noted and parked, to revisit later; a line in `NEXT_STEPS.md` | the operator | "create a card for choppy with your detailed observations and outcomes ... we would revisit it later" | - |

## Status and next
Parked. Reopened by the operator, with A2's result (choppy calm in the combination) and the next batch's reading.

## Links
`47_review/why_by_profile.py` and `.txt`; `47_review/night9_review.py` and `.txt`; `47_review/choppy_giveback/`
(`giveback.py`, `table.py`, `results.md`, `per_book.csv`, the books in `choppy_books.json`); `../runs/NIGHT9_RUN.md`
(reading, corrected); next steps C3.
