# 7.b exercise 3: the shared lessons, three inputs, ideas taken through the workflow (2026-11-15)

**Before the runs**, the lessons of 7.d and 7.e applied to the prompt and card: the cause "the idea measured
elsewhere than where it shows (horizon, comparison, side)" named; a sharper idea is the tested idea amended, in full;
"no ideas" when the effect is not there is a clear answer.

**Inputs** (current steps, sizing included), all inconclusive: 002-01 (t 0.37), 002-03 (t 1.73), 002-04 (t -0.23).
Two runs each (`run_1/`, `run_2/`, 1.89 USD). Every run checks the horizons, finds where the result splits (bear
against bull years, per coin, momentum inside the regime) and writes its ideas as the tested idea amended, in full.
002-04: both runs propose the same idea ("only while the 200-day average itself falls"), the same as 7.d's repair,
already tested (inconclusive, t -0.37); neither says "no ideas", the effect being present in bear years.

**Two ideas through steps 3 to 6:**

| Idea | What 7.b measured | Step 3's horizon | Step 5 |
|---|---|---|---|
| 002-01 run 2 b1: inside the golden cross, the stronger the coin's recent rise, the larger its return "over the following days" | slope t 3.26 at 10 bars (694 cases) | 20 bars | inconclusive (t 1.13) |
| 002-03 run 1 b1: above the average, only while the average itself rises, "over the following bars" | t 1.17 at 20 bars | 20 bars | inconclusive (t 0.58) |

**Not validated on this exercise:** no idea got a clear answer. **The cause is upstream of 7.b:** the time scale of
an idea is written in words, and step 3 turns the words into bars without a rule. Across the last six ideas:
"the next few days" became 5 bars and "the following days to two weeks" 10 bars (both confirmed);
"the following days" and "the following bars" became 20 bars (both inconclusive), where the line had seen the effect
at 10. This is the parked item "Step 2: an idea's time scale" (`../../POTENTIAL_ADJUSTMENTS.md`).


# 7.b exercise 4: with the time rule (2026-11-15)

**Change since exercise 3** (operator, 2026-11-15): every idea states its time in real time (its horizon, the past
period of its situation), and step 3 converts it to bars (`../../common/idea_definition.md`).

**Two runs on the three inputs** (`run_1/`, `run_2/`, 1.89 USD). Every idea states its horizon in days ("over the
next 10 days", "over the next 20 days"). 002-01: the same idea three times out of five (inside the golden cross, the
higher the 20-day return, the more it rises over the next 10 days). 002-04: both runs repeat the idea already tested
(the 200-day average falling; inconclusive at 10 bars), not taken again.

**Two ideas through steps 3 to 6:**

| Idea | Step 3's horizon | Step 5 | Step 6 |
|---|---|---|---|
| 002-01 run 2 b1: inside the golden cross, the higher the 20-day return, the larger the return over the next 10 days | 10 bars (exercise 3's version: 20 bars, t 1.13) | inconclusive, t 1.69 | not profitable: Sharpe 0.85, Calmar 0.72 (original book 0.49, 0.20) |
| 002-03 run 2 b2: above the 200-day average, only while the 20-day return is positive, over the next 20 days | 20 bars | inconclusive, t 1.65 | not profitable: Sharpe 0.87, Calmar 0.74 (original book 0.68, 0.39) |

**Reading.** The time rule works: step 3 takes each idea's own horizon. 7.b's ideas are sharper and their books
better, but no idea reaches a clear answer: 7.b's own numbers came from its best cut (t 3.26 in the data, 1.69 in the
test), and each condition it adds leaves fewer cases. Not validated.


# 7.b exercise 5: the "more data" route (2026-11-15)

**Change** (operator, 2026-11-15): when the effect is the same everywhere but too small for the data, the clear answer
needs more cases, not a narrower idea: the tested idea unchanged, on more data (its `data:` line, from
`../../common/data_available.md`, given to the prompt through the shared-file mechanism of `analyse.py`).

**Two runs on the three inputs** (`run_1/`, `run_2/`, 2.10 USD). 002-03: run 1 answers "no ideas: the trend effect
is not there" (above against below the average gives nothing; the t rests on five outlier blocks); run 2 proposes the
tested idea unchanged on 15 coins. 002-01: the momentum idea again, and a new one in both runs (a fresh golden cross
is followed by a weaker 10 days). 002-04: narrower versions of the idea already tested.

**Through steps 3 to 6:**

| Idea | Data | Step 5 | Step 6 |
|---|---|---|---|
| 002-03 run 2: the further above the 200-day average, the more it rises over the next 20 days (the tested idea, on more data) | 15 coins | **confirmed** (OLS slope t 2.40) | not profitable (Sharpe 0.84, Calmar 0.50) |
| 002-01: inside the golden cross, the higher the 20-day return, the more it rises over the next 10 days (exercise 4's idea; on more data, as the operator asked) | 15 coins | **confirmed** (t 4.61; on the 6 coins t 1.69) | **profitable** (Sharpe 0.90, Calmar 0.88) |
| 002-01 run 2: in the 30 days after a golden cross, the next 10 days fall relative to the coin's usual move | 6 coins | inconclusive (t -1.71) | not profitable |

**Reading.** The route gives clear answers: the effect was real but too small for 6 coins. On 002-03 the two runs
disagreed ("not there" against "more data"), and the test decided; a third run (`run_3/`, after a wording fix that
keeps any label out of the idea's text) chose narrower ideas. The line's route varies from run to run.

## After the route order (run 4, 2026-11-15)

With the routes in order (close to zero, then the same everywhere but small, then in part of the data), run 4 on
002-03 chose the third route (the effect turns negative in bear years, so it is not "the same everywhere"): "above the
200-day average, only while the 60-day return is positive". Through steps 3 to 6: inconclusive (t 0.53). On 002-03,
narrower ideas failed three times (rising average t 0.58; 60-day momentum t 0.53) and the same idea on more data was
confirmed (t 2.40): the order's condition for "more data" is too strict.


# 7.b exercise 6: the route follows step 5's result (2026-11-15)

**Changes** (operator, 2026-11-15): the route follows the test's result (step 5's main measure), not a measure of the
line's own: on the idea's side but short of the bar, the tested idea unchanged on more data; on the other side or
zero, the idea amended to a part of the data where the effect shows clearly, or "no ideas". Added after this exercise:
"more data" only while more data is available than the test used.

**Run 1** (before the wording said "step 5's result"): 002-03 answered "no ideas, close to zero", judging on its own
measures (t 0.3) instead of the test's (t 1.73); 002-01 proposed an idea of its own. **Run 2** (after): both chose
"the tested idea unchanged, on more data".

| Idea | Data | Step 5 |
|---|---|---|
| 002-03: the further above the 200-day average, the larger the next 20 days (the tested idea, on more data) | 15 coins | confirmed (t 2.40; exercise 5) |
| 002-01: inside the golden cross, the wider the 50/200 spread, the larger the next 10 days (the tested idea, on more data) | 19 coins | inconclusive (t 0.74; on 6 coins t 0.37) |

**The record of the routes on 7.b's inputs:** more data, 3 tested, 2 confirmed, 1 still unclear (with three times the
cases, t barely moved: the effect is close to zero); narrower ideas, 5 tested, none confirmed.
