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

## After try 06 (2026-11-05)
1. **Simpler or more complex?** Two prompts, one runner, one adapter, three step files: about 650 lines in all. No flags, no config file, no schema. The models are two names at the top of the runner.
2. **Fooling ourselves?** The first candidate passed on one fold after 21 looks on its brief, by a hair. It is written up as a candidate with its caveats, not as a strategy. The holdout is untouched and stays the operator's. The profit answer is not the engine's; said in the record.
3. **Building what a run asked?** The runs asked for: the engine's event component (open, for the operator), a shelf rule for filters (a filter waits for a book), and nothing else. No piece was built that a run did not ask for.
4. **Operator deciding, pipeline discovering?** The pipeline discovered three filters and one candidate book on fake briefs; the operator now has two decisions and has written no brief yet. This is the shape the objective asks for.
5. **Deviation from v2's rule?** Nothing new copied from v1. The adapter mirrors v1's closed-book options by reading them, not by importing v1.

## After try 07 (2026-11-05)
1. **Simpler or more complex?** One component added to the engine (about 80 lines), one step in v2 (about 80 lines). The lite profit check left the loop. Net: the loop has the same number of steps and the real backtester at the end.
2. **Fooling ourselves?** The engine and the lite check agree on the candidate, which checks the component and the claim code against each other. Still one fold, still 21 looks. Nothing changed about the holdout.
3. **Building what a run asked?** The component was the BTC run's ask and the operator approved it. Nothing else was added.
4. **Operator deciding, pipeline discovering?** Two decisions still pending with the operator: the candidate's holdout, and a real brief.
5. **Deviation from v2's rule?** One more v1 piece pulled by hand, with its reason: the backtester itself (`run_backtest`). The engine grew by one file; no v1 doc, config or test was touched.

## Before try 08, the first real brief (2026-11-05)
1. **Simpler or more complex?** Nothing added. The brief is the operator's own text in v2's four-line head; a run is one command.
2. **Fooling ourselves?** Fold A is the brief's own fold. A claim must pass on BTC and on a coin of another category, as the brief asks. The closed lane is in the tried list so it is not re-proposed. The holdout is untouched.
3. **Building what a run asked?** Nothing built; this is a run.
4. **Operator deciding, pipeline discovering?** The operator wrote the brief and chose the fold and the budget (two rounds). The pipeline does the rest.
5. **Deviation from v2's rule?** None. One choice made for the operator, said plainly: ADA as the other-category coin, from the brief's clean list.
