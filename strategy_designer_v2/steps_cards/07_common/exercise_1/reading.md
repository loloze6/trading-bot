# Step 7, exercise 1: every line, one call against analyst then deducer

**What ran.** The shared mechanism (`helper/analyse.py`) with each line's prompt, on real backtests where the line's entry condition holds, in both modes. 17 analyses, 5.38 USD, about 1 to 2 minutes each. No answer had to be dropped; two were refused once and passed on retry (the date check). Logs: each line's `exercise_1/run_log.txt`.

| Line | Backtests | One call | Analyst, then deducer |
|---|---|---|---|
| 7.a not observable | 001-01, 002-05 cut to one window | 6 and 5 findings; 2 and 2 ideas | 7 and 6 findings; 3 and 2 ideas |
| 7.b inconclusive | full-data 002-01, 002-03 | 7 and 8; 2 and 3 | 8 and 9; 3 and 3 |
| 7.c rejected | planted 002-05 (a planted fall) | 8 findings; 3 ideas | 10; 2 |
| 7.d not profitable | full-data 002-01, 002-03 | 9 and 7; 3 and 4 | 14 and 10; 5 and 4 |
| 7.e, 7.f | full-data 002-01, 002-03 | not run: entry condition not met (right) | |
| 7.g patterns | full-data 002-03, hourly 001-01 | 7 and 6; 3 and 2 | 11 and 10; 10 and 5 |

## What works
- **Findings rest on numbers.** For lines b, d and g, 95 to 99 % of the numbers in the findings are in the explorations' results; the rest are taken from the plan or verdict, computed from results (shares, the cases needed for t = 2), or written as percentages. For 7.a, about 80 %, for the same reasons. No invented number was found.
- **Ideas rest on named findings,** and each line kept to its objective:
  - 7.a proposes the same idea where it can be observed (more windows, 4-hour or hourly bars);
  - 7.b and 7.d locate where the effect is, or what removes the loss;
  - 7.g finds patterns the idea does not explain.
- **The analyses read like a practitioner's.** On 002-03 (7.d): fees are small; the losses come from entries that reverse within days; the edge sits in the largest forecasts; the last 20 days' direction separates winners from losers.
- **Findings converge across lines and modes.** "Above the long average *and* rising over the last weeks, the coin keeps rising" comes out of 7.b, 7.d and 7.g, in both modes.
- **Judgement under a planted effect (7.c).** From the data alone, the model saw that the rejection was a uniform −1 % offset, the same in every window, forecast size, trend age and weekday, and of an implausible size. In one run it declined to propose counter-ideas. It even found that the planted loss sits entirely in the gap from one close to the next open (t = −680): that is how the prices were shifted. 7.c can only be truly tested on a real rejected idea; this tests its mechanism.

## Defects found and fixed during the exercise
1. **The runner failed on a record without a trades file** (the planted records): it now gives an empty table.
2. **Error messages showed file paths** to the model ("planted_test", "minus1pct"): paths are now stripped. The plan and check text given to the model no longer carry their path lines either. The planted record's name still reaches the model through the plan id in the verdict's header; for real backtests the id is the idea's name, so this affects only the planted test.
3. **A period was named by its months and year** ("January to April 2022", from one window grouped by year and month). The instructions now ask for windows or years only, and code refuses a month name next to a year, a "Q1 2022" or a "2022-03". The 7.a analyses were rerun; no date remains.
4. **Step 5's verdict wrote the situation check as "1 of the active bars"** (meaning 100 %), which the model read as one bar. It now writes a percentage; 111 verdicts were re-rendered.

## To decide
- **Setting values in ideas.** Almost every idea names values: inherited from the tested plan ("the 200-day average", "RSI(14)"), but also new ones found in the data ("over the past 30 days", "stayed above for 60 bars", "two to four months"). The inherited ones only say where a finding is. The new ones are fitted to this data: that is the fishing risk the guard was meant for. Step 2's definition already says "no setting value". Only one analysis (7.d split, 002-01) wrote value-free ideas.
- **One call or analyst then deducer.** Both work and agree on the main findings. The split finds more (7 to 14 findings against 5 to 9) and proposes more (up to 10 ideas, against at most 4), at about 20 % more cost. One call is tighter; the split is broader. Its deducer, who does not see the data, is the one that wrote value-free ideas. No information visibly lost at the hand-over.
- **Chance in pattern-hunting (7.g).** Weekday findings came with their statistics (t = -2.75 and +3.66, the same sign in all six coins), but seven weekdays were tested. Only unseen data can settle such an idea: the parked point "on which data step 7's ideas are tested".

## Not tested
- **7.e and 7.f** have no real input: no backtest is profitable enough. Their entry condition was tested (they did not run).
- **7.c** only on a planted record (above).
