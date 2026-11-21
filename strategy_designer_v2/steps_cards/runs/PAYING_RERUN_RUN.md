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

## Reading (2026-11-22, about 00:30 Paris; 0 USD; cut twice by the 2-hour limit and a machine restart, resumed each time)
`topics/41_review/rerun_before_after.md` holds the table, book by book.
| Group | Expected | Found |
|---|---|---|
| The 21 books made on 21 November | identical | **21 of 21 identical** (step 5's statistic and step 6's six measures): a rerun reproduces a record |
| The 14 older books | they change; some may stop paying | **14 of 14 changed, 14 still pay.** Step 5's statistic unchanged (it reads the forecast and the prices, not the positions); step 6 slightly better: Sharpe +0.00 to +0.07, Calmar +0.00 to +0.15 |

**Correction to the expected outcome:** the change is the measured costs (lower on most coins), not the holding rule.
The older plans were made before the holding setting existed (2026-11-19) and have none, so they still re-size every bar;
the operator ruled they enter the register as they are (topic 41). `common/engine_changes.md` says which engine change
reaches which record.

**Then:** the 35 books go into the register of `orchestration/ideas_similarities_check/`, and their comparisons are read
against night 3's hand checks (topic 41, plan step 4).
