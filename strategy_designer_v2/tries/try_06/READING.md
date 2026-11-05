# Try 06: the runner, the pipeline on its own (2026-11-05)

**What ran.** `run.py`, one file: ideas, judge, profit, record, analyst, next claim, judge, repeat until the analyst says none or the round budget is spent. One model adapter (`steps/ask.py`), closed book like v1: no tools, no settings, a neutral working directory. Every step writes a file and a step whose file exists is skipped, so a run resumes from where it stopped. The SDK turned out to be installed here, so the three runs below made their own model calls.

**Result.** Three briefs, three runs, six model calls, about 1.02 USD in total, no hand in the loop.

| Brief | Claims (new, none repeating the 30 already tried) | Pass | Analyst's next claim | Its verdict |
|---|---|---|---|---|
| ETH regime and trend, 1d | 9 | 0 | extension from average reverts | fail |
| Time of week, three pairs, 1h | 9 | 1 filter: volume surprise against the clock, 1.6 to 1.9x, all three pairs, 6 of 6 | volume-surprise direction carries | fail |
| BTC overreaction, 1h | 10 | 1 book: a big bar that closes beyond the prior 24h range keeps going 12h, a big bar inside the range does not | inside-range fade net of fees | fail |

**The first candidate.** The BTC book passed both bars on fold A: judge +0.60% mean difference, 191 against 103 events, 6 of 6 windows; profit +55% net, Sharpe 1.04, max drawdown 15%, 13% time in market, 6 of 6 windows positive. The code looks back only. It is on the shelf as `breakout_spike_continues_inside_spike_reverts`, kind book, profit pass.

**What to hold against it, before anyone gets excited.**
1. One fold. The design says one fold, one verdict, and that verdict is "candidate", not "strategy".
2. Twenty-one claims were tried on this brief across two runs. At a 5% noise rate one false pass per twenty is expected; the record counts the looks.
3. The profit answer is in the claim's own terms: close to close, 0.15% per round trip, no gap handling, no sizing. The engine run needs the event component (the engine's first ask, still open).
4. Sharpe 1.04 against a bar of 1.0. It passed by a hair.

**What the operator decides now, and only the operator.** Whether this candidate goes to the holdout, and whether the engine gets its event component so the backtest can be the engine's. The pipeline stops here on purpose. The sealed store was not touched.

**What the runner showed.** The loop runs alone, resumes after a crash or a stopped model call, never repeats a tried claim, keeps a shelf of validated claims and a trial row per measurement. Two defects found and fixed during the try: round 1 overwrote round 0's verdict file, and a leftover temp folder. Both one line.
