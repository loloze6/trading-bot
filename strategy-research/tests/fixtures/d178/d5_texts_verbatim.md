DIRECTION 2026-10-22, the three analyst texts for item D, verbatim.

D5(a) Method step 3, replacing the selector sentence at SKILL.md:78-80:
Before a query, count what it can select: bars per window minus the lookback minus the
longest horizon, times the share the selector keeps, times the windows. If that is
under the floor, change the selector or the horizon now; a query that cannot reach its
floor is not run.

D5(b) Closing step (new paragraph before the no-claim rule at SKILL.md:107):
Before you end, write the next-steps ledger on your best observation: four lines, one
each for the opposite direction, another horizon, the all-bars version of a selector
that failed its floors, and the mechanism behind it. Each line is the id of a query of
this session that ran it, or "not run: <the floor, the tool limit, or the budget that
stopped it>". The ledger is a record field (`next_steps`, under `claim` or `no_claim`);
the reader checks that the four lines exist and that every cited query id is one of
this session's. It judges nothing else.

D5(c) Method step 5, added after the killed_by sentence:
When a result clears its floors and you name a mechanism for it, run the query that
mechanism predicts before you write the result as an observation. "It may be a fit to
this fold" is not a reason: the child run and the refold are that test. Only a named
tool limit may stand in place of that query.
