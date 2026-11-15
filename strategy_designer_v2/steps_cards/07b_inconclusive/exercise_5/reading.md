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
