# Run brief: the paying books rerun on today's engine (2026-11-21, written before the run; topic 41, plan step 3)

**Purpose (operator's go):** every paying book found so far (step 5 confirmed, step 6 profitable enough; 35 distinct
ideas: 22 daily, 9 hourly, 4 four-hourly) rerun once on today's engine and costs, so that the register of paying books
compares them on equal terms; and, on the operator's word, a before and after table: what the holding rule and the
measured slippage changed on books already trusted. Steps 4, 5 (each idea's own `measure.py`, no model call) and 6, into
`paying_rerun_run`; script `topics/41_review/rerun_paying.py`; table `topics/41_review/rerun_before_after.md`. 0 USD.

**Expected outcomes:**
| Group | Expected | If not |
|---|---|---|
| The 21 books made on 21 November (today's engine) | identical before and after (step 5's statistic, step 6's six measures): a rerun reproduces a record | a rerun does not reproduce: find why before any comparison |
| The 14 older books (no holding rule, or its earlier version; the guessed slippage) | they change: fewer trades where a bet is held; costs lower on BTC and ETH, higher on XMR; some may stop paying | none change: the engine changes did not reach them, check the configs |

**Then:** every book still paying after the rerun goes into the register (`orchestration/paying_books/`), and their
comparisons are read against night 3's hand checks (plan step 4).
