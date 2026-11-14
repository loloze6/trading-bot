# The night against the objective (2026-11-06, written at 03:55 UTC by the delegate, numbers refreshed at the end of the night)

The objective: a pipeline that finds a profitable strategy by itself, runs on its own, and does not fool itself. The operator decides; the pipeline discovers. The numbers are in `README.md`; this file says what they mean for the objective, and nothing about what to trade.

## Runs on its own: yes
From midnight to 03:55 the pipeline ran 55 runs on 40 briefs with no hand in the loop: ideas, verdicts, engine backtests, analyst rounds, replications. It stopped only on defects, nine of them, each fixed in the pipeline with the run that revealed it named in `STEPBACK.md`. One container restart killed the queued jobs; the chain was relaunched and every run resumed from its last file. The cost was 20.65 USD of model calls, about 0.38 USD per run, plus engine time.

## Does not fool itself: mostly, and it says where it cannot
- The judge's pass rate is 4.2% (23 of 548 claims), which is the noise floor of its own rule. This is the single most important number of the night: a judge pass alone means little. The t-statistic now sits next to every effect so the operator can rule on a floor.
- The engine's bar separates: 9 passes in 29 engine runs. Every pass is one fold. The replication step, built tonight, asked whether a passing book travels: of the five early engine passes, none passed the engine on another coin; one later claim (a volume-burst continuation on hourly bars) passed the engine on XRP, ETH and BTC, all on fold C, and failed on LTC. One claim text, three coins, one fold: evidence that it is more than one coin, not evidence that it is more than one fold.
- The operator's own brief answered no on all three research folds (BTC with ADA on A, BTC with LTC on B and C): 32 claims, 0 passes on both coins.
- The two judges disagree often: 12 judge passes failed the engine. The judge measures an event mean; the engine trades the book. The lite book check, 50 lines that matched the engine to the decimal, is now run on every judge-passed book as information. It would let the pipeline skip the engine's six minutes where the lite check already says no, if the operator wants that.
- The holdout was not touched. No second fold was run for any passing claim. Looks per brief are counted and are mostly 10 to 22.

## Finds a profitable strategy: not shown
Nine books passed the profit bar on one fold each. None has been seen on a second fold or on the holdout. The record presents them as candidates with their caveats, not as strategies. Whether any goes to the holdout is the operator's decision, and the pipeline will not take it.

## What the pipeline asked for tonight, and got
A coverage check before any model call; a per-symbol engine refusal instead of a crash; the two-size engine run (full size and a fixed 20% volatility target), which turned one drawdown fail into a pass; a t-statistic as information; the replication step; a lite-book sweep; a query over the records; a generated morning file; a YAML re-ask with the parser's words; the analyst prompt's exact next-claim skeleton. About 350 lines in all, no flag, no config file, no schema.

## What it asked for and did not get (for the operator)
- A significance floor for the judge, or a rule that the lite check gates the engine.
- The holdout path.
- A rule for filters: twelve validated volatility filters sit on the shelf and no book has used one.
- Daily claims with year-long windows cannot reach the engine on folds whose first window sits near the start of a coin's cache; they are refused, not scored. A rule for which folds a coin may run on would avoid the refusals.

## Two things I did as delegate that the operator should know
- I chose the coins and folds for 37 briefs, and twice chose a fold the coins did not cover; the check caught both for free.
- I did not commit during the night, as asked, so everything since the last push lives only on this machine until the morning commit.
