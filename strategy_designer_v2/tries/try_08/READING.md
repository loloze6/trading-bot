# Try 08: the first real brief (2026-11-05)

**What ran.** The operator's own brief, daily breadth on fold A (`strategy-research/briefs/daily_breadth_fold_a.md`), put in v2's four-line head with the operator's research goal and constraints copied verbatim. One command: `run.py`, fold A, two rounds. A claim is measured on BTC and on ADA (a coin of another category, from the brief's clean list) and must pass on both, which is the brief's own ask. Three model calls, about 0.46 USD. The run folder: `runs/real_01_daily_breadth_fold_a/001/`.

**Result: no.** 12 claims (10 from the ideas step, 2 from the analyst), 0 pass on both coins.

| Round | Claims | Pass on both | Closest |
|---|---|---|---|
| ideas | 10 | 0 | turn-of-month inflow: pass on ADA (+0.37%, 5 of 6 windows), BTC +0.15% against 0.2% asked, right sign in 5 of 6 |
| analyst 1 | 1 (range-position reversion) | 0 | no effect on either coin |
| analyst 2 | 1 (monthly return reversal) | 0 | opposite signs on the two coins |

The mechanisms tried: channel breakout, capitulation rebound, down-streak exhaustion, compression release, high-volume continuation, wick rejection, turn of month, volatility-regime drift, drawdown reversion, signed volume flow, range-position reversion, monthly reversal. The closed lane (SMA distance) was not re-proposed. The analyst's observations were tied to the numbers and its two proposals followed from them; both failed honestly.

**What the result says.** On fold A, daily bars, with the brief's rule that an idea must hold on a coin of another category, none of twelve daily mechanisms earned more than cost on both coins. The brief's own text expected this to be hard ("a single block will rarely pass branch 3 by itself"). One near miss is recorded for a later brief: the turn-of-month effect held on ADA and had the right sign on BTC.

**What the pipeline did right.** It took the operator's brief as written, ran alone, never repeated a tried idea, spent under half a dollar, and answered no with the numbers. The one failure of the try was mine: the brief's YAML head had an unquoted colon, fixed in one line; the pipeline refused it loudly rather than running on a broken brief.

**Open for the operator.** Whether to run the same brief on another fold (one command), or write the next brief. The near miss above is a candidate line for it.
