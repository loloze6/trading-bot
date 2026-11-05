# Step back (recurring, before every try)

The objective of this session: a pipeline that finds a profitable strategy by itself, runs on its own, does not fool itself; the operator decides, the pipeline discovers; simple; v2 from scratch; nothing copied by default; no complexity for its own sake.

Five questions, answered in one line each, before each try.

## Before try 05 (2026-11-05)
1. **Simpler or more complex?** One prompt, four code files, about 400 lines, no flags. Still simple. Watch: `profit.py` must not grow into a second backtester; the engine is the backtester, and its first ask is recorded.
2. **Fooling ourselves?** Seal masked, lookahead scan, pass number written before the data, one fold one verdict, trial rows for every measurement. Risk to carry: 30 claims per brief at a 5% noise rate means one or two false passes per brief are expected; the record must count claims tried per brief, so the holdout step knows how many looks there were.
3. **Building what a run asked?** Try 05 is branch 2 and the next idea: the spine's missing step. Yes.
4. **Operator deciding, pipeline discovering?** The operator has written no brief yet; three fake briefs stand in. The holdout is untouched. Nothing waits for an approval that the spine says is the operator's.
5. **Deviation from v2's rule?** Two v1 pieces pulled by hand, each with a reason (fold loader, holdout policy reader). Nothing else copied.

## After try 05, before try 06 (2026-11-05)
1. **Simpler or more complex?** Two prompts, four code files, no flags, no config. Each try added one file. Still simple.
2. **Fooling ourselves?** The analyst reads only the judge's files; its proposal is judged like any claim. Two briefs ended in "no", which is the honest outcome. Open risk unchanged: looks per brief must be counted in the record before any holdout.
3. **Building what a run asked?** Try 06 is the loop runner, so the pipeline runs on its own: the objective's own words. Yes.
4. **Operator deciding, pipeline discovering?** The pipeline discovered: two volatility filters, no return edge on three fake briefs. The operator's decisions pending: a real brief; the engine's first ask (an event component); whether a validated filter goes on a shelf.
5. **Deviation from v2's rule?** No new v1 piece pulled. `profit.py` stayed at fifty lines.
