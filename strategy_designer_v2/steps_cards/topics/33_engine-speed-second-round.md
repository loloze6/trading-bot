# Topic 33: A second round of engine speed work

Status: built 2026-11-20 (A to D, files identical, `topics/33_review/duration/14_round2_proof.md`); merged into the working branch on 2026-11-20 (7826ad81) and into master on 2026-11-22 (PR 577)  
Where: engine (`trading-bot/`), shared code  
Opened: 2026-11-19 (operator, during d_line_1h_run)

## Question
Can an hourly backtest run faster without changing any result?

## Seen
- 2026-11-20: the holding reruns took 15 to 65 minutes per hourly book (volatile evening-fall in the pilot: over
  53 minutes), and a two-sided hourly book trading often over 35 minutes.
- d_line_1h_run, 2026-11-19: an idea takes 13 to 14 minutes, of which step 4 (the backtest) 606 to 688 s; step 3 about
  30 s, step 5 about 30 s, step 6 7 to 19 s, step 7's lines about 1.5 min (in parallel).
- An hourly backtest: 6 coins x 24 windows x about 2,900 hourly bars, about 420,000 bars, on 4 cores.
- After the first round (topic 21): 135 s for one coin on one fold (6 windows), so about 13.5 min expected for 6 coins
  and 4 folds on 4 cores; measured 10 to 11 min. One intraday book that traded very often took 2,613 s (topic 30's
  rebuild).

## Why it matters
If hourly research becomes the main track, the backtest is about 80 % of an idea's time: 17 ideas take about 4 hours.

## Options
| Option | Gain | Risk |
|---|---|---|
| Profile an hourly backtest again and fix the largest costs, each proven by identical files (as topic 21) | faster, results unchanged | shared code: proof and the operator's go |
| Fewer coins or folds on 1h | faster | less reliable (topic 31) |
| More cores | faster | the environment's choice |

Recommended: the profiling round, when hourly research is the main track.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Parked | operator | the run's speed is as measured; not needed for this run | - |
| 2026-11-20 | Unparked: find time for it, maybe in another session | operator | "one backtest per hour is really slowing us down while we are continuously enhancing" | - |
| 2026-11-20 | A session of its own (`session_012maTgTnbCc9ZEaRY48QDd1`, "Engine speed, round 2"), with the brief `topics/33_review/duration/10_round2_brief.md`; research-changing options only proposed | operator ("yes; ensure knowledge transfer, especially on the options that would impact our research process (folds etc.)") | the backtest is about 80 % of an idea's time | – |

## Status and next
2026-11-20: proposed, a session of its own (its own container, so the running queue is not slowed), on its own branch:
measure (profile one hourly backtest: one coin, one fold), findings, plan with gain, effort and risk, the operator's go,
then each change proven by identical files on fixed inputs (as in round 1, `topics/33_review/duration/`). Nothing is merged
into the working branch while a run is going, and nothing into master without the operator's go. Meanwhile, without the
engine: the replay of topic 36 (`36_review/book_sim.py`, 10 s a book, where a component is computed on every bar) and
rerunning only the books whose step 6 could change.

2026-11-20, round 2 session (branch `engine-speed-round2`): measurement `topics/33_review/duration/11_round2_measure.md`,
plan `12_round2_plan.md` (A: bootstrap only where read; B: volatility components reuse the previous bar's stds; C: one
call per coin and fold; D: per-bar glue). Waiting for the operator's go; no engine change made.

## Links
Topic 21; `topics/33_review/duration/`; `runs/D_LINE_1H_RUN.md`.
