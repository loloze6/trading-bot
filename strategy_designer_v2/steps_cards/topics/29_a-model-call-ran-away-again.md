# Topic 29: A model call ran away again

Status: open  
Where: research: step 7 (line 7.d), `common/lib.py`  
Opened: 2026-11-19 (the run session, intraday_1h_run)

## Question
Should a single model call be stopped once it costs far more than usual?

## Seen
- 2026-11-16, demo_run: one 7.b call cost 3.77 USD in 14.4 minutes (usually at most 0.37 USD, about a minute). Parked
  "only if it happens again" (topic 27).
- 2026-11-19, intraday_1h_run, idea 017-02.g3, line 7.d: one call wrote 129,173 output tokens in 866 s (just under the
  15-minute timeout) and cost 3.38 USD. The line's other three calls cost about 0.10 USD each; a usual 7.d line costs
  about 0.30 USD. It ended normally and its answer was used (6 findings, 2 ideas, 3 explorations). The cost is in the
  journal and the log (`logs/<backtest>/step7_7.d.txt`).
- What exists today: every call is killed at 15 minutes (`common/lib.py`); each call's tokens, time and USD are logged.

## Why it matters
Two calls cost about 7 USD, the price of 20 to 30 ordinary lines; a budget run can lose a share of its budget to one call.

## Options
| Option | Gain | Risk |
|---|---|---|
| A limit per call on output tokens (the model's maximum answer length) | a runaway stops early | a long but good answer is cut; a limit the operator did not ask for |
| A limit per call in USD (the `claude` command's `--max-budget-usd`) | caps the cost directly | not known to stop a single answer partway (to test) |
| No limit; visibility only (as today) | no answer is ever cut | a rare call costs 3 to 4 USD |

Recommended: none yet. First measure how often it happens: the share of calls above, say, 1 USD over all runs'
journals, then decide.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-16 | Parked: a limit only if it happens again | operator | one call in one run; the logs show every call | a limit at once |
| 2026-11-19 | No limit added by the run session | run session | the operator's rule: no limit not asked for | - |

## Status and next
Open: the condition of 2026-11-16 ("if it happens again") is met. Waits for the operator's decision.

## Links
Topic 27; `common/lib.py`; the run session's journal in `runs/NIGHT_1H_RUN.md`.
